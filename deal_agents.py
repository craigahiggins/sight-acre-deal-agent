from pydantic import BaseModel, Field
try:
    from agents import Agent
except Exception:
    Agent = None

class DealAssessment(BaseModel):
    name: str
    sector: str
    location: str = ""
    source: str = "AI research"
    asking_price: float | None = None
    potential_value: float | None = None
    strategic_fit: int = Field(ge=0, le=10)
    return_potential: int = Field(ge=0, le=10)
    entry_price_score: int = Field(ge=0, le=10)
    financeability: int = Field(ge=0, le=10)
    asset_backing: int = Field(ge=0, le=10)
    synergies: int = Field(ge=0, le=10)
    deal_probability: int = Field(ge=0, le=10)
    seller_motivation: int = Field(ge=0, le=10)
    execution_complexity: int = Field(ge=0, le=10, description="10 means easy to execute")
    summary: str
    red_flags: str
    recommended_action: str

BASE_CONTEXT = """Sight Acre is screening asset-backed and strategically synergistic opportunities across leisure, modular construction, renewables, senior living, development and selected corporate acquisitions. Prefer transactions with identifiable value creation, development upside, financing routes, asset backing and cross-group synergies. Be sceptical; never invent facts. Clearly distinguish verified facts from inference."""

def build_agents():
    if Agent is None:
        raise RuntimeError("Install openai-agents first")
    scout = Agent(name="Scout", instructions=BASE_CONTEXT + "\nFind candidate deals and motivated-seller signals. Return only opportunities worth researching.")
    researcher = Agent(name="Researcher", instructions=BASE_CONTEXT + "\nResearch ownership, accounts, debt/charges, planning, market context and counterparties. Flag missing evidence.")
    investment = Agent(name="Investment Analyst", instructions=BASE_CONTEXT + "\nAssess entry valuation, value creation, financeability, returns and downside. Use conservative assumptions.")
    redflag = Agent(name="Red Flag Analyst", instructions=BASE_CONTEXT + "\nTry to kill the deal: identify legal, financial, planning, environmental, operational and counterparty risks.")
    ranker = Agent(name="Deal Ranker", instructions=BASE_CONTEXT + "\nSynthesize research into a structured 0-10 assessment for each scoring dimension.", output_type=DealAssessment)
    return scout, researcher, investment, redflag, ranker
