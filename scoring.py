WEIGHTS = {
    "strategic_fit": 20,
    "return_potential": 20,
    "entry_price_score": 15,
    "financeability": 10,
    "asset_backing": 10,
    "synergies": 10,
    "deal_probability": 5,
    "seller_motivation": 5,
    "execution_complexity": 5,
}

def calculate_score(values: dict) -> int:
    """Each input is 0-10. Execution complexity is scored 10 = easy to execute."""
    total = 0.0
    for key, weight in WEIGHTS.items():
        v = max(0, min(10, float(values.get(key, 0))))
        total += (v / 10.0) * weight
    return round(total)

def grade(score: int) -> str:
    if score >= 85: return "A"
    if score >= 70: return "B"
    if score >= 55: return "C"
    return "D"
