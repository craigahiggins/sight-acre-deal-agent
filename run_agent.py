import os, asyncio
from dotenv import load_dotenv
from agents import Runner
from agents import WebSearchTool
from agents import Agent
from db import init_db, connect
from scoring import calculate_score, grade
from deal_agents import build_agents

load_dotenv()

async def main(query=None):
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Add OPENAI_API_KEY to .env first.")
    init_db()
    scout, researcher, investment, redflag, ranker = build_agents()
    mandate = query or "Find one high-potential UK deal across leisure, modular construction, renewables or senior living that appears worthy of deeper investigation. Use current public web information and do not invent facts."
    scout.tools = [WebSearchTool()]
    found = await Runner.run(scout, mandate)
    research_prompt = f"Research this candidate in depth and cite/describe the evidence used:\n{found.final_output}"
    researcher.tools = [WebSearchTool()]
    research = await Runner.run(researcher, research_prompt)
    inv = await Runner.run(investment, research.final_output)
    risks = await Runner.run(redflag, research.final_output)
    synthesis = f"CANDIDATE:\n{found.final_output}\n\nRESEARCH:\n{research.final_output}\n\nINVESTMENT:\n{inv.final_output}\n\nRISKS:\n{risks.final_output}"
    assessed = await Runner.run(ranker, synthesis)
    d = assessed.final_output.model_dump()
    d["score"] = calculate_score(d); d["grade"] = grade(d["score"]); d["status"] = "New"
    with connect() as conn:
        cols = ",".join(d.keys()); qs = ",".join(["?"]*len(d))
        conn.execute(f"INSERT INTO deals ({cols}) VALUES ({qs})", tuple(d.values()))
        conn.commit()
    print(f"Added: {d['name']} | score {d['score']}/100 | grade {d['grade']}")

if __name__ == "__main__":
    asyncio.run(main())
