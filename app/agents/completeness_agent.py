from app.agents.common import overlap


def evaluate(question, response, evidence):

    if not evidence:
        return {
            "score": 0.50,
            "explanation": (
                "Completeness is uncertain because "
                "no evidence was available."
            ),
            "details": {
                "mode": "uncertain"
            }
        }

    # Select the most relevant evidence
    best_evidence = max(
        evidence,
        key=lambda item: item.get("similarity", 0)
    )

    reference = best_evidence.get("text", "").strip()
    similarity = best_evidence.get("similarity", 0)

    if not reference:
        return {
            "score": 0.50,
            "explanation": (
                "No usable evidence was available "
                "to check completeness."
            ),
            "details": {
                "mode": "uncertain"
            }
        }

    # Check how much of the important information is covered
    coverage = overlap(reference, response)

    score = (
        (coverage * 0.70) +
        (similarity * 0.30)
    )

    score = min(1.0, max(0.0, score))

    if score >= 0.70:
        explanation = (
            "The response covers most of the important "
            "information in the retrieved evidence."
        )

    elif score >= 0.40:
        explanation = (
            "The response covers some of the important "
            "information in the retrieved evidence."
        )

    else:
        explanation = (
            "The response may omit important information "
            "from the retrieved evidence."
        )

    return {
        "score": round(score, 4),
        "explanation": explanation,
        "details": {
            "retrieval_similarity": round(similarity, 4),
            "coverage": round(coverage, 4)
        }
    }