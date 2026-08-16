from db import init_db, connect
from scoring import calculate_score, grade

DEALS = [
    dict(name="Somerset Country Park", sector="Leisure", location="Somerset, UK", source="Broker / off-market signal", asking_price=11000000, potential_value=26000000, strategic_fit=10, return_potential=9, entry_price_score=8, financeability=8, asset_backing=10, synergies=10, deal_probability=7, seller_motivation=8, execution_complexity=8, status="Contact owner", summary="Established leisure asset with expansion land and potential EcoHabs deployment.", red_flags="Confirm planning position, occupancy quality and existing debt security.", recommended_action="Owner approach and request management accounts + title/planning pack."),
    dict(name="Grid-Ready Solar Project", sector="Renewables", location="Midlands, UK", source="Developer network", asking_price=7000000, potential_value=18000000, strategic_fit=9, return_potential=9, entry_price_score=8, financeability=8, asset_backing=8, synergies=9, deal_probability=7, seller_motivation=7, execution_complexity=7, status="Due diligence", summary="Solar/storage project with apparent grid progress and scope for AGGL participation.", red_flags="Grid queue status and land option must be independently verified.", recommended_action="Verify grid offer, planning, land control and capex assumptions."),
    dict(name="Modular Manufacturer C", sector="Modular", location="North West, UK", source="Corporate signal", asking_price=4200000, potential_value=10000000, strategic_fit=10, return_potential=8, entry_price_score=9, financeability=7, asset_backing=7, synergies=10, deal_probability=8, seller_motivation=9, execution_complexity=7, status="Approach", summary="Potential bolt-on manufacturing capacity with owner succession signals.", red_flags="Customer concentration and plant condition unknown.", recommended_action="Confidential owner approach; request order book, machinery register and margins."),
    dict(name="Retirement Village Site D", sector="Senior Living", location="South West, UK", source="Planning search", asking_price=6000000, potential_value=21000000, strategic_fit=9, return_potential=9, entry_price_score=8, financeability=7, asset_backing=9, synergies=9, deal_probability=6, seller_motivation=6, execution_complexity=6, status="Investigate", summary="Consented/part-consented senior living opportunity with modular delivery potential.", red_flags="Planning conditions and absorption assumptions need testing.", recommended_action="Planning/title diligence and preliminary development appraisal."),
]

init_db()
with connect() as conn:
    conn.execute("DELETE FROM deals")
    for d in DEALS:
        s = calculate_score(d)
        d["score"], d["grade"] = s, grade(s)
        cols = ",".join(d.keys()); qs = ",".join(["?"]*len(d))
        conn.execute(f"INSERT INTO deals ({cols}) VALUES ({qs})", tuple(d.values()))
    conn.commit()
print("Seeded deal database.")
