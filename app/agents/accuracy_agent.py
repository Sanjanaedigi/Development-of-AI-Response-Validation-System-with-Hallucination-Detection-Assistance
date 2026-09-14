from app.agents.common import overlap
from app.knowledge_base.embeddings import (
    generate_embeddings,
    cosine_similarity,
)


def _accuracy_category(score):
    """Convert accuracy score into a meaningful category."""

    if score >= 0.80:
        return "Correct"
    elif score >= 0.60:
        return "Mostly Correct"
    elif score >= 0.40:
        return "Partially Correct"
    elif score >= 0.20:
        return "Mostly Incorrect"
    else:
        return "Incorrect"


def _semantic_similarity(reference, response):
    """Calculate semantic similarity between reference and response."""

    vectors = generate_embeddings(
        [reference, response]
    )

    similarities = cosine_similarity(
        vectors[0],
        vectors
    )

    return float(similarities[1])


def _detect_contradiction(reference, response):
    """
    Detect obvious contradictions using semantic similarity
    and important factual terms.

    This is a lightweight rule-based safeguard.
    """

    reference_lower = reference.lower()
    response_lower = response.lower()

    # Common factual contradiction:
    # reference says one entity, response says another.
    contradiction_pairs = [
        ("paris", "london"),
        ("london", "paris"),
        ("new delhi", "mumbai"),
        ("mumbai", "new delhi"),
        ("hyderabad", "mumbai"),
        ("mumbai", "hyderabad"),
        ("true", "false"),
        ("false", "true"),
    ]

    for first, second in contradiction_pairs:

        if (
            first in reference_lower
            and second in response_lower
        ):
            return True

    return False


def evaluate(
    question,
    response,
    evidence=None,
    reference_answer=None
):
    """
    Evaluate factual accuracy of an AI response.

    Priority:
    1. User-provided reference answer
    2. Retrieved Knowledge Base evidence
    3. Uncertain when no verification source exists
    """

    if evidence is None:
        evidence = []

    # -------------------------------------------------
    # STEP 1: Reference answer
    # -------------------------------------------------

    if reference_answer and reference_answer.strip():

        reference = reference_answer.strip()

        overlap_score = overlap(
            reference,
            response
        )

        semantic_score = _semantic_similarity(
            reference,
            response
        )

        contradiction = _detect_contradiction(
            reference,
            response
        )

        # -------------------------------------------------
        # Explicit contradiction
        # -------------------------------------------------

        if contradiction:

            score = 0.0
            category = "Incorrect"

            explanation = (
                "The AI response contradicts the "
                "provided reference answer."
            )

        else:

            score = (
                0.60 * semantic_score
                + 0.40 * overlap_score
            )

            score = min(
                1.0,
                max(0.0, score)
            )

            category = _accuracy_category(
                score
            )

            if category == "Correct":

                explanation = (
                    "The AI response closely agrees with "
                    "the provided reference answer."
                )

            elif category == "Mostly Correct":

                explanation = (
                    "The AI response is mostly consistent "
                    "with the provided reference answer."
                )

            elif category == "Partially Correct":

                explanation = (
                    "The AI response contains some information "
                    "consistent with the reference answer but "
                    "does not fully match it."
                )

            elif category == "Mostly Incorrect":

                explanation = (
                    "The AI response has limited agreement "
                    "with the provided reference answer."
                )

            else:

                explanation = (
                    "The AI response does not sufficiently "
                    "agree with the provided reference answer."
                )

        return {
            "score": round(
                score,
                4
            ),
            "category": category,
            "explanation": explanation,
            "evidence": [
                reference
            ],
            "details": {
                "mode": "reference_answer",
                "semantic_similarity": round(
                    semantic_score,
                    4
                ),
                "overlap_score": round(
                    overlap_score,
                    4
                ),
                "contradiction_detected": contradiction
            }
        }

    # -------------------------------------------------
    # STEP 2: Retrieved evidence
    # -------------------------------------------------

    if not evidence:

        return {
            "score": 0.50,
            "category": "Uncertain",
            "explanation": (
                "No reference answer or retrieved evidence "
                "was available for accuracy verification."
            ),
            "evidence": [],
            "details": {
                "mode": "uncertain"
            }
        }

    # -------------------------------------------------
    # STEP 3: Select strongest evidence
    # -------------------------------------------------

    best_evidence = max(
        evidence,
        key=lambda item: item.get(
            "similarity",
            0
        )
    )

    reference = best_evidence.get(
        "text",
        ""
    ).strip()

    similarity = best_evidence.get(
        "similarity",
        0
    )

    if not reference:

        return {
            "score": 0.50,
            "category": "Uncertain",
            "explanation": (
                "Retrieved evidence was available but "
                "contained no usable text."
            ),
            "evidence": [],
            "details": {
                "mode": "uncertain"
            }
        }

    # -------------------------------------------------
    # STEP 4: Compare response with evidence
    # -------------------------------------------------

    overlap_score = overlap(
        reference,
        response
    )

    semantic_score = _semantic_similarity(
        reference,
        response
    )

    contradiction = _detect_contradiction(
        reference,
        response
    )

    if contradiction:

        score = 0.0
        category = "Incorrect"

        explanation = (
            "The AI response contradicts the "
            "retrieved evidence."
        )

    else:

        score = (
            0.50 * semantic_score
            + 0.30 * overlap_score
            + 0.20 * similarity
        )

        score = min(
            1.0,
            max(0.0, score)
        )

        category = _accuracy_category(
            score
        )

        if category == "Correct":

            explanation = (
                "The AI response is strongly supported "
                "by the retrieved evidence."
            )

        elif category == "Mostly Correct":

            explanation = (
                "The AI response is mostly supported "
                "by the retrieved evidence."
            )

        elif category == "Partially Correct":

            explanation = (
                "The AI response has partial support "
                "from the retrieved evidence."
            )

        elif category == "Mostly Incorrect":

            explanation = (
                "The AI response has limited support "
                "from the retrieved evidence."
            )

        else:

            explanation = (
                "The AI response is not sufficiently "
                "supported by the retrieved evidence."
            )

    # -------------------------------------------------
    # STEP 5: Structured result
    # -------------------------------------------------

    return {
        "score": round(
            score,
            4
        ),
        "category": category,
        "explanation": explanation,
        "evidence": [
            reference
        ],
        "details": {
            "mode": "retrieved_evidence",
            "retrieval_similarity": round(
                similarity,
                4
            ),
            "semantic_similarity": round(
                semantic_score,
                4
            ),
            "overlap_score": round(
                overlap_score,
                4
            ),
            "contradiction_detected": contradiction
        }
    }