import os
import asyncio
from dotenv import load_dotenv

from agents import Runner, WebSearchTool, ModelSettings

from db import init_db, connect
from scoring import calculate_score, grade
from deal_agents import build_agents


load_dotenv()


def compact(text, limit=6000):
    """Keep agent hand-offs small enough to avoid excessive token use."""
    if text is None:
        return ""
    text = str(text)
    return text[:limit]


async def main(query=None):

    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Add OPENAI_API_KEY first.")

    init_db()

    scout, researcher, investment, redflag, ranker = build_agents()

    # Keep every agent response concise.
    concise_settings = ModelSettings(
        max_tokens=1800
    )

    for agent in [scout, researcher, investment, redflag, ranker]:
        agent.model_settings = concise_settings

    mandate = query or (
        "Find one genuine high-potential UK acquisition or development "
        "opportunity across leisure, modular construction, renewables, "
        "senior living or development land. Use current public web information. "
        "Do not invent facts. Prefer opportunities with identifiable price, "
        "owner/seller, location and value-creation potential."
    )

    # -------------------------------------------------
    # 1. SCOUT
    # -------------------------------------------------

    scout.tools = [WebSearchTool()]

    scout_prompt = f"""
    SEARCH MANDATE:
    {mandate}

    Find ONE best candidate only.

    Return no more than 700 words.

    Include:
    - opportunity name
    - sector
    - location
    - asking price if available
    - seller/owner if available
    - why it may fit Sight Acre
    - 3-5 key factual findings
    - source names / URLs where available

    Do not provide general market commentary.
    """

    found = await Runner.run(
        scout,
        scout_prompt,
        max_turns=4
    )

    scout_result = compact(found.final_output, 5000)

    # -------------------------------------------------
    # 2. RESEARCH
    # -------------------------------------------------

    researcher.tools = [WebSearchTool()]

    research_prompt = f"""
    Research this specific candidate only:

    {scout_result}

    Verify the important facts using current public web information.

    Return no more than 800 words.

    Focus only on:
    - asset/business
    - seller/owner
    - asking price / transaction evidence
    - financial information available
    - planning/development potential
    - debt/charges/distress indicators if publicly visible
    - key risks
    - evidence/source references

    Clearly state when information cannot be verified.
    """

    research = await Runner.run(
        researcher,
        research_prompt,
        max_turns=4
    )

    research_result = compact(research.final_output, 6000)

    # -------------------------------------------------
    # 3. INVESTMENT ANALYSIS
    # -------------------------------------------------

    investment_prompt = f"""
    Analyse the following opportunity for Sight Acre.

    RESEARCH:
    {research_result}

    Return no more than 500 words.

    Assess:
    - strategic fit
    - likely value creation
    - entry-price attractiveness
    - financeability
    - asset backing
    - synergies
    - key assumptions

    Do not invent missing financial figures.
    """

    inv = await Runner.run(
        investment,
        investment_prompt,
        max_turns=2
    )

    investment_result = compact(inv.final_output, 4000)

    # -------------------------------------------------
    # 4. RED FLAG REVIEW
    # -------------------------------------------------

    redflag_prompt = f"""
    Act as a sceptical investment committee reviewer.

    RESEARCH:
    {research_result}

    Return no more than 400 words.

    Identify:
    - factual red flags
    - diligence gaps
    - planning/legal/financial/counterparty concerns
    - reasons Sight Acre should NOT proceed

    Do not repeat the whole research.
    """

    risks = await Runner.run(
        redflag,
        redflag_prompt,
        max_turns=2
    )

    risk_result = compact(risks.final_output, 3500)

    # -------------------------------------------------
    # 5. FINAL STRUCTURED ASSESSMENT
    # -------------------------------------------------

    synthesis = f"""
    CANDIDATE:
    {scout_result}

    VERIFIED RESEARCH:
    {research_result}

    INVESTMENT VIEW:
    {investment_result}

    RED FLAGS:
    {risk_result}

    Produce the required structured Deal assessment.

    Be conservative.
    Do not invent facts or financial figures.
    If information is unknown, mark it unknown.
    """

    assessed = await Runner.run(
        ranker,
        synthesis,
        max_turns=2
    )

    d = assessed.final_output.model_dump()

    d["score"] = calculate_score(d)
    d["grade"] = grade(d["score"])
    d["status"] = "New"

    with connect() as conn:
        cols = ",".join(d.keys())
        qs = ",".join(["?"] * len(d))

        conn.execute(
            f"INSERT INTO deals ({cols}) VALUES ({qs})",
            tuple(d.values())
        )

        conn.commit()

    print(
        f"Added: {d['name']} | "
        f"score {d['score']}/100 | "
        f"grade {d['grade']}"
    )


if __name__ == "__main__":
    asyncio.run(main())
