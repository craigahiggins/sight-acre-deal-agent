# Sight Acre Deal Agent

AI-assisted deal sourcing, triage, research and pipeline management for Sight Acre.

## What is included
- Executive dashboard
- Multi-sector mandates: Leisure, Development, Modular, Renewables, Senior Living, Corporate, Special Situations
- 0-100 Sight Acre Deal Score
- Scout / Research / Investment / Red Flag / Ranking agent design
- SQLite deal database
- Approval-only outbound action queue
- Seed data so the dashboard works immediately

## Run locally
1. Install Python 3.10+
2. `python -m venv .venv`
3. Activate the environment
4. `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and add your OpenAI API key
6. `python seed.py`
7. `streamlit run app/dashboard.py`

## Live sourcing
Run `python run_agent.py` after setting `OPENAI_API_KEY`.
The MVP intentionally keeps outbound contact in an approval queue rather than sending autonomously.

## Next integrations
- Companies House
- UK planning portals / Planning Data
- Insolvency Gazette and administrator feeds
- Commercial property portals and leisure brokers
- Crunchbase
- Apify web actors
- Clay enrichment
- CRM / email once approved
