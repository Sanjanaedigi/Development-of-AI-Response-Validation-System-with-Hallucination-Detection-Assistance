from app.agents.common import overlap


def evaluate(question, response, evidence):

    if not evidence:
        return {
            "score": 0.50,
            "explanation": (
                "No evidence was available for accuracy verification."
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
                "for accuracy verification."
            ),
            "details": {
                "mode": "uncertain"
            }
        }

    # Compare the AI response with the best evidence
    overlap_score = overlap(reference, response)

    # Combine evidence relevance and response support
    score = (
        (overlap_score * 0.60) +
        (similarity * 0.40)
    )

    score = min(1.0, max(0.0, score))

    if score >= 0.70:
        explanation = (
            "The AI response is strongly supported "
            "by the most relevant retrieved evidence."
        )

    elif score >= 0.40:
        explanation = (
            "The AI response is partially supported "
            "by the retrieved evidence."
        )

    else:
        explanation = (
            "The AI response has weak support "
            "from the retrieved evidence."
        )

    return {
        "score": round(score, 4),
        "explanation": explanation,
        "details": {
            "retrieval_similarity": round(similarity, 4),
            "overlap_score": round(overlap_score, 4)
        }
    }