import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import streamlit as st
import pandas as pd
from db import init_db, connect

from run_agent import main as run_live_agent
import asyncio
st.set_page_config(page_title="Sight Acre Deal Centre", layout="wide")
init_db()



st.title("Sight Acre Deal Centre")
st.caption("AI deal sourcing • research • scoring • red flags • human-approved outreach")
st.subheader("Live AI Deal Scout")

search_mandate = st.text_input(
    "Deal sourcing mandate",
    value="Find one high-potential UK deal across leisure, modular construction, renewables, senior living or development land that appears worthy of deeper investigation. Use current public web information and do not invent facts."
)

if st.button("🔎 Run Live AI Scout", type="primary"):
    with st.spinner("AI agents are searching, researching and analysing the market..."):
        try:
            asyncio.run(run_live_agent(search_mandate))
            st.success("Live deal found and analysed. Refreshing Deal Centre...")
            st.rerun()
        except Exception as e:
            st.error(f"Live scout error: {e}")
with connect() as conn:
    df = pd.read_sql_query("SELECT * FROM deals ORDER BY score DESC", conn)

if df.empty:
    st.info("No deals yet. Run seed.py or run_agent.py.")
    st.stop()

c1,c2,c3,c4 = st.columns(4)
c1.metric("Live opportunities", len(df))
c2.metric("A-rated", int((df.grade == 'A').sum()))
c3.metric("Potential value", f"£{df.potential_value.fillna(0).sum()/1e6:,.1f}m")
c4.metric("Avg. deal score", f"{df.score.mean():.0f}/100")

sector = st.multiselect("Sector", sorted(df.sector.unique()), default=sorted(df.sector.unique()))
show = df[df.sector.isin(sector)]
st.dataframe(show[["score","grade","name","sector","location","asking_price","potential_value","status"]], use_container_width=True, hide_index=True,
    column_config={"asking_price": st.column_config.NumberColumn("Asking price", format="£%.0f"), "potential_value": st.column_config.NumberColumn("Potential value", format="£%.0f")})

st.subheader("Deal Brief")
selected = st.selectbox("Open deal", show.name.tolist())
r = show[show.name == selected].iloc[0]
left,right = st.columns([2,1])
with left:
    st.markdown(f"### {r['name']} — {int(r['score'])}/100 ({r['grade']})")
    st.write(r['summary'])
    st.markdown("**Recommended action**")
    st.write(r['recommended_action'])
    st.markdown("**Red flags / diligence**")
    st.write(r['red_flags'])
with right:
    st.markdown("**Score components**")
    labels = ["Strategic fit","Return potential","Entry price","Financeability","Asset backing","Synergies","Deal probability","Seller motivation","Execution ease"]
    keys = ["strategic_fit","return_potential","entry_price_score","financeability","asset_backing","synergies","deal_probability","seller_motivation","execution_complexity"]
    for label,key in zip(labels,keys): st.progress(int(r[key])*10, text=f"{label}: {int(r[key])}/10")

st.divider()
st.subheader("Approval Gate")
st.write("Outbound contact is deliberately not autonomous. Queue an approach for approval first.")
if st.button("Queue owner/broker approach"):
    with connect() as conn:
        conn.execute("INSERT INTO approvals (deal_id, action_type, proposed_action) VALUES (?, ?, ?)", (int(r['id']), "Outreach", str(r['recommended_action'])))
        conn.commit()
    st.success("Approach queued for approval.")

with connect() as conn:
    approvals = pd.read_sql_query("SELECT a.id,d.name,a.action_type,a.proposed_action,a.status,a.created_at FROM approvals a JOIN deals d ON d.id=a.deal_id ORDER BY a.id DESC", conn)
if not approvals.empty:
    st.dataframe(approvals, use_container_width=True, hide_index=True)

