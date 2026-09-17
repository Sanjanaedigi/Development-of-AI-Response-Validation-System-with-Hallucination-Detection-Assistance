WEIGHTS = {
    "relevance": 0.25,
    "accuracy": 0.25,
    "hallucination": 0.25,
    "completeness": 0.25,
}

PASS_THRESHOLD = 0.70
NEEDS_IMPROVEMENT_THRESHOLD = 0.40


def overall_score(results: dict) -> float:
    """
    Calculate the weighted overall evaluation score.
    """

    score = sum(
        float(results[name]["score"]) * weight
        for name, weight in WEIGHTS.items()
    )

    return round(score, 4)


def _has_critical_hallucination(results: dict) -> bool:
    """
    Check whether the hallucination agent detected
    a direct contradiction.
    """

    hallucination = results.get("hallucination", {})
    details = hallucination.get("details", {})

    return bool(
        details.get("contradiction_detected", False)
    )


def verdict(results: dict):
    """
    Determine the final M3.2 verdict.

    Pass:
        Overall score >= 0.70

    Needs Improvement:
        Overall score >= 0.40 and < 0.70

    Fail:
        Overall score < 0.40

    Critical override:
        A direct contradiction detected by the
        hallucination agent results in Fail.
    """

    score = overall_score(results)

    # Critical hallucination/contradiction override
    if _has_critical_hallucination(results):
        return (
            "Fail",
            "A critical contradiction was detected "
            "between the AI response and the available evidence."
        )

    if score >= PASS_THRESHOLD:
        return (
            "Pass",
            "The response achieved the required "
            "weighted evaluation threshold."
        )

    if score >= NEEDS_IMPROVEMENT_THRESHOLD:
        return (
            "Needs Improvement",
            "The response passed the minimum evaluation "
            "level but one or more dimensions require improvement."
        )

    return (
        "Fail",
        "The response did not reach the minimum "
        "weighted evaluation level."
    )