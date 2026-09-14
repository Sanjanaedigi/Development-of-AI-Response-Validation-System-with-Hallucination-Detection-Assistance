from app.agents.common import overlap, evidence_text
from app.knowledge_base.embeddings import (
    generate_embeddings,
    cosine_similarity,
)


def _relevance_category(score):
    """Convert numerical relevance score into a category."""

    if score >= 0.80:
        return "Fully Relevant"
    elif score >= 0.60:
        return "Mostly Relevant"
    elif score >= 0.40:
        return "Partially Relevant"
    elif score >= 0.20:
        return "Mostly Unrelated"
    else:
        return "Off-Topic"


def _semantic_similarity(question, response):
    """Calculate semantic similarity between question and response."""

    vectors = generate_embeddings([question, response])

    similarities = cosine_similarity(
        vectors[0],
        vectors
    )

    return float(similarities[1])


def evaluate(question, response, evidence=None):
    """
    Evaluate how relevant an AI response is to the question.

    Relevance is primarily determined using semantic similarity.
    Keyword overlap is retained as an additional signal.
    """

    if evidence is None:
        evidence = []

    # -------------------------------------------------
    # STEP 1: Semantic similarity
    # -------------------------------------------------

    semantic_score = _semantic_similarity(
        question,
        response
    )

    # -------------------------------------------------
    # STEP 2: Keyword overlap
    # -------------------------------------------------

    question_response_overlap = overlap(
        question,
        response
    )

    # -------------------------------------------------
    # STEP 3: Evidence support
    # -------------------------------------------------

    ev = evidence_text(evidence)

    if ev:
        evidence_support = overlap(
            response,
            ev
        )
    else:
        evidence_support = 0.0

    # -------------------------------------------------
    # STEP 4: Final relevance score
    # -------------------------------------------------

    if evidence_support > 0:

        score = (
            0.60 * semantic_score
            + 0.30 * question_response_overlap
            + 0.10 * evidence_support
        )

    else:

        score = (
            0.60 * semantic_score
            + 0.40 * question_response_overlap
        )

    score = round(
        min(1.0, max(0.0, score)),
        4
    )

    # -------------------------------------------------
    # STEP 5: Category
    # -------------------------------------------------

    category = _relevance_category(score)

    # -------------------------------------------------
    # STEP 6: Explanation
    # -------------------------------------------------

    if category == "Fully Relevant":

        explanation = (
            "The response is strongly related to the submitted "
            "question and directly addresses the requested topic."
        )

    elif category == "Mostly Relevant":

        explanation = (
            "The response is relevant to the submitted question "
            "but may not fully address all requested details."
        )

    elif category == "Partially Relevant":

        explanation = (
            "The response is related to the submitted question "
            "but only addresses part of the requested information."
        )

    elif category == "Mostly Unrelated":

        explanation = (
            "The response has limited semantic connection to "
            "the submitted question."
        )

    else:

        explanation = (
            "The response does not meaningfully address the "
            "submitted question and appears to be off-topic."
        )

    # -------------------------------------------------
    # STEP 7: Structured result
    # -------------------------------------------------

    return {
        "score": score,
        "category": category,
        "explanation": explanation,
        "details": {
            "semantic_similarity": round(
                semantic_score,
                4
            ),
            "question_response_overlap": round(
                question_response_overlap,
                4
            ),
            "evidence_support": round(
                evidence_support,
                4
            )
        }
    }