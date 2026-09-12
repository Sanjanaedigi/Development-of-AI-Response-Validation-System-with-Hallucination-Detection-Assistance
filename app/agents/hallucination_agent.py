from app.agents.common import overlap


def evaluate(question, response, evidence):

    if not evidence:

        return {
            "score": 0.50,
            "explanation": (
                "Hallucination safety is uncertain "
                "because no evidence was supplied or retrieved."
            ),
            "details": {
                "mode": "uncertain"
            }
        }

    # Use strongest retrieved evidence
    best_evidence = max(
        evidence,
        key=lambda item: item.get("similarity", 0)
    )

    reference = best_evidence.get(
        "text",
        ""
    )

    if not reference.strip():

        return {
            "score": 0.50,
            "explanation": (
                "No usable evidence was available "
                "for hallucination verification."
            ),
            "details": {
                "mode": "uncertain"
            }
        }

    support = overlap(
        response,
        reference
    )

    safety = min(
        1.0,
        support + 0.10
    )

    if safety >= 0.70:

        explanation = (
            "Most important response terms are "
            "supported by the available evidence."
        )

    else:

        explanation = (
            "Several response terms are not sufficiently "
            "supported by the available evidence; "
            "possible hallucination."
        )

    return {

        "score": round(
            safety,
            4
        ),

        "explanation": explanation,

        "details": {
            "support_ratio":
                round(
                    support,
                    4
                )
        }
    }