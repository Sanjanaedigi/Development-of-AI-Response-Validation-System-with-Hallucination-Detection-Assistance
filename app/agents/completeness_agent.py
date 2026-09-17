import re

from app.agents.common import overlap
from app.knowledge_base.embeddings import (
    generate_embeddings,
    cosine_similarity,
)


def _semantic_similarity(reference, response):
    vectors = generate_embeddings([reference, response])
    similarities = cosine_similarity(vectors[0], vectors)
    return float(similarities[1])


def _split_aspects(text):
    """
    Split reference/question content into meaningful aspects.
    Uses sentences first, then simple clause separation.
    """
    text = text.strip()

    if not text:
        return []

    sentences = re.split(r"(?<=[.!?])\s+", text)

    aspects = []

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        parts = re.split(
            r"\s+(?:and|also|as well as|but)\s+",
            sentence,
            flags=re.IGNORECASE,
        )

        for part in parts:
            part = part.strip(" ,;:")

            if len(part.split()) >= 2:
                aspects.append(part)

    return aspects


def _evaluate_aspect(aspect, response):
    """
    Determine whether an expected aspect is addressed,
    partially addressed, or missing.
    """
    overlap_score = overlap(aspect, response)
    semantic_score = _semantic_similarity(aspect, response)

    combined_score = (
        0.40 * overlap_score
        + 0.60 * semantic_score
    )

    combined_score = min(1.0, max(0.0, combined_score))

    if combined_score >= 0.70:
        status = "addressed"
    elif combined_score >= 0.40:
        status = "partially_addressed"
    else:
        status = "missing"

    return {
        "aspect": aspect,
        "status": status,
        "score": round(combined_score, 4),
    }


def _build_explanation(addressed, partial, missing):
    if not missing and not partial:
        return (
            "The AI response addresses all identified "
            "expected aspects of the question/reference."
        )

    if missing and partial:
        return (
            f"The AI response addresses {len(addressed)} aspect(s), "
            f"partially addresses {len(partial)} aspect(s), and "
            f"omits {len(missing)} aspect(s)."
        )

    if missing:
        return (
            f"The AI response addresses {len(addressed)} aspect(s) "
            f"but omits {len(missing)} expected aspect(s)."
        )

    return (
        f"The AI response addresses {len(addressed)} aspect(s) "
        f"but only partially covers {len(partial)} aspect(s)."
    )


def evaluate(
    question,
    response,
    evidence=None,
    reference_answer=None,
):
    """
    Evaluate whether the AI response sufficiently covers
    the expected information.

    Priority:
    1. Provided reference answer
    2. Retrieved RAG evidence
    3. Uncertain if neither is available
    """

    if evidence is None:
        evidence = []

    response = response.strip()

    # ---------------------------------------------------------
    # 1. Select the source used for completeness evaluation
    # ---------------------------------------------------------

    if reference_answer and reference_answer.strip():
        reference = reference_answer.strip()
        mode = "reference_answer"

    elif evidence:
        best_evidence = max(
            evidence,
            key=lambda item: item.get("similarity", 0),
        )

        reference = best_evidence.get("text", "").strip()
        mode = "retrieved_evidence"

    else:
        return {
            "score": 0.50,
            "explanation": (
                "Completeness is uncertain because no "
                "reference answer or retrieved evidence "
                "was available."
            ),
            "details": {
                "mode": "uncertain",
                "addressed_aspects": [],
                "partially_addressed_aspects": [],
                "missing_aspects": [],
                "reasoning": (
                    "There was no reference or evidence "
                    "available to determine the expected "
                    "information."
                ),
            },
        }

    # ---------------------------------------------------------
    # 2. Validate source text
    # ---------------------------------------------------------

    if not reference:
        return {
            "score": 0.50,
            "explanation": (
                "Completeness is uncertain because the "
                "available reference/evidence contained "
                "no usable text."
            ),
            "details": {
                "mode": "uncertain",
                "addressed_aspects": [],
                "partially_addressed_aspects": [],
                "missing_aspects": [],
                "reasoning": (
                    "The selected source did not contain "
                    "usable information for completeness checking."
                ),
            },
        }

    # ---------------------------------------------------------
    # 3. Identify expected aspects
    # ---------------------------------------------------------

    aspects = _split_aspects(reference)

    # If the source is a short factual answer, treat the
    # complete reference as one expected aspect.
    if not aspects:
        aspects = [reference]

    # ---------------------------------------------------------
    # 4. Evaluate every expected aspect
    # ---------------------------------------------------------

    evaluations = []

    for aspect in aspects:
        result = _evaluate_aspect(aspect, response)
        evaluations.append(result)

    addressed = [
        item["aspect"]
        for item in evaluations
        if item["status"] == "addressed"
    ]

    partial = [
        item["aspect"]
        for item in evaluations
        if item["status"] == "partially_addressed"
    ]

    missing = [
        item["aspect"]
        for item in evaluations
        if item["status"] == "missing"
    ]

    # ---------------------------------------------------------
    # 5. Calculate completeness score
    # ---------------------------------------------------------

    if evaluations:
        score = sum(
            item["score"]
            for item in evaluations
        ) / len(evaluations)
    else:
        score = 0.50

    score = min(1.0, max(0.0, score))

    # ---------------------------------------------------------
    # 6. Build reasoning
    # ---------------------------------------------------------

    explanation = _build_explanation(
        addressed,
        partial,
        missing,
    )

    reasoning = (
        f"Completeness was evaluated using {mode.replace('_', ' ')}. "
        f"{explanation}"
    )

    return {
        "score": round(score, 4),
        "explanation": explanation,
        "details": {
            "mode": mode,
            "expected_aspects": aspects,
            "addressed_aspects": addressed,
            "partially_addressed_aspects": partial,
            "missing_aspects": missing,
            "aspect_evaluations": evaluations,
            "reasoning": reasoning,
        },
    }