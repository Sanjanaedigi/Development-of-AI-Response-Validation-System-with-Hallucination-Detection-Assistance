WEIGHTS = {"relevance": 0.25, "accuracy": 0.25, "hallucination": 0.25, "completeness": 0.25}
PASS_THRESHOLD = 0.70


def overall_score(results: dict) -> float:
    return round(sum(float(results[name]["score"]) * weight for name, weight in WEIGHTS.items()), 4)


def verdict(score: float):
    if score >= PASS_THRESHOLD:
        return "VALID", "All four Milestone 1 evaluation dimensions meet the overall validation threshold."
    return "FILTER BLOCKED", "The response did not reach the Milestone 1 overall validation threshold."
