import re

from app.agents.common import overlap
from app.knowledge_base.embeddings import (
    generate_embeddings,
    cosine_similarity,
)


def _detect_contradiction(reference, response):
    """Detect obvious factual contradictions."""

    reference_lower = reference.lower()
    response_lower = response.lower()

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


def _semantic_support(reference, response):
    """Calculate semantic support between evidence and response."""

    vectors = generate_embeddings(
        [reference, response]
    )

    similarities = cosine_similarity(
        vectors[0],
        vectors
    )

    return float(similarities[1])


def _split_claims(response):
    """
    Split the AI response into individual sentence-level claims.
    """

    claims = re.split(
        r"(?<=[.!?])\s+",
        response.strip()
    )

    return [
        claim.strip()
        for claim in claims
        if claim.strip()
    ]


def _evaluate_claim(claim, reference):
    """
    Evaluate one claim against the available evidence.
    """

    support = overlap(
        claim,
        reference
    )

    semantic_support = _semantic_support(
        reference,
        claim
    )

    contradiction = _detect_contradiction(
        reference,
        claim
    )

    if contradiction:

        return {
            "supported": False,
            "contradicted": True,
            "support_score": 0.0,
            "semantic_support": round(
                semantic_support,
                4
            ),
            "reason": (
                "The claim contradicts the available "
                "reference evidence."
            )
        }

    score = (
        0.60 * semantic_support
        + 0.40 * support
    )

    score = min(
        1.0,
        max(0.0, score)
    )

    if score >= 0.70:

        return {
            "supported": True,
            "contradicted": False,
            "support_score": round(
                score,
                4
            ),
            "semantic_support": round(
                semantic_support,
                4
            ),
            "reason": (
                "The claim is supported by the "
                "available reference evidence."
            )
        }

    return {
        "supported": False,
        "contradicted": False,
        "support_score": round(
            score,
            4
        ),
        "semantic_support": round(
            semantic_support,
            4
        ),
        "reason": (
            "The claim is not sufficiently supported "
            "by the available reference evidence."
        )
    }


def evaluate(question, response, evidence):

    if not evidence:

        return {
            "score": 0.50,
            "explanation": (
                "Hallucination safety is uncertain "
                "because no evidence was supplied or retrieved."
            ),
            "details": {
                "mode": "uncertain",
                "unsupported_claims": [],
                "claim_evaluations": []
            }
        }

    best_evidence = max(
        evidence,
        key=lambda item: item.get("similarity", 0)
    )

    reference = best_evidence.get(
        "text",
        ""
    ).strip()

    if not reference:

        return {
            "score": 0.50,
            "explanation": (
                "No usable evidence was available "
                "for hallucination verification."
            ),
            "details": {
                "mode": "uncertain",
                "unsupported_claims": [],
                "claim_evaluations": []
            }
        }

    claims = _split_claims(response)

    claim_evaluations = []
    unsupported_claims = []

    for claim in claims:

        result = _evaluate_claim(
            claim,
            reference
        )

        claim_evaluations.append({
            "claim": claim,
            **result
        })

        if not result["supported"]:
            unsupported_claims.append({
                "claim": claim,
                "reason": result["reason"],
                "evidence": reference
            })

    if not claim_evaluations:

        return {
            "score": 0.50,
            "explanation": (
                "No factual claims were available "
                "for hallucination verification."
            ),
            "details": {
                "mode": "uncertain",
                "unsupported_claims": [],
                "claim_evaluations": []
            }
        }

    supported_scores = [
        item["support_score"]
        for item in claim_evaluations
    ]

    safety = sum(supported_scores) / len(
        supported_scores
    )

    safety = min(
        1.0,
        max(0.0, safety)
    )

    contradiction_detected = any(
        item["contradicted"]
        for item in claim_evaluations
    )

    if contradiction_detected:

        safety = 0.0

        explanation = (
            "One or more claims in the AI response "
            "contradict the available evidence."
        )

    elif unsupported_claims:

        explanation = (
            "One or more claims in the AI response "
            "are not sufficiently supported by the "
            "available evidence."
        )

    else:

        explanation = (
            "All evaluated claims are supported by "
            "the available evidence and show low "
            "hallucination risk."
        )

    return {
        "score": round(
            safety,
            4
        ),
        "explanation": explanation,
        "details": {
            "mode": "claim_level_verification",
            "claim_count": len(claim_evaluations),
            "support_ratio": round(
                sum(
                    item["support_score"]
                    for item in claim_evaluations
                ) / len(claim_evaluations),
                4
            ),
            "contradiction_detected":
                contradiction_detected,
            "unsupported_claims":
                unsupported_claims,
            "claim_evaluations":
                claim_evaluations
        }
    }