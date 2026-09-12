WEIGHTS = {
    "relevance": 0.25,
    "accuracy": 0.25,
    "hallucination": 0.25,
    "completeness": 0.25,
}

def overall_score(results):
    return round(sum(results[k]["score"] * w for k, w in WEIGHTS.items()), 4)

def verdict(score):
    if score >= 0.70:
        return "VALID", "The response passed the initial Milestone 1 validation threshold."
    return "FILTER BLOCKED", "The response did not reach the initial validation threshold."
