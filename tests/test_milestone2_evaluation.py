import json

from app.agents import (
    relevance_agent,
    accuracy_agent,
    hallucination_agent,
)


def load_evaluation_cases():
    with open(
        "data/milestone2_evaluation_set.json",
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def test_milestone2_agents_on_evaluation_set():
    cases = load_evaluation_cases()

    assert len(cases) >= 7

    for case in cases:
        question = case["question"]
        response = case["ai_response"]
        reference_answer = case["reference_answer"]
        evidence = [
            {
                "text": case["evidence"],
                "similarity": 1.0,
            }
        ]

        relevance = relevance_agent.evaluate(
            question,
            response,
            evidence,
        )

        accuracy = accuracy_agent.evaluate(
            question,
            response,
            evidence,
            reference_answer,
        )

        hallucination = hallucination_agent.evaluate(
            question,
            response,
            evidence,
        )

        assert 0 <= relevance["score"] <= 1
        assert 0 <= accuracy["score"] <= 1
        assert 0 <= hallucination["score"] <= 1

        assert relevance["explanation"]
        assert accuracy["explanation"]
        assert hallucination["explanation"]

        assert "evidence" in accuracy

        assert "unsupported_claims" in (
            hallucination["details"]
        )

        assert "claim_evaluations" in (
            hallucination["details"]
        )


def test_milestone2_expected_behaviors():
    cases = load_evaluation_cases()

    for case in cases:
        evidence = [
            {
                "text": case["evidence"],
                "similarity": 1.0,
            }
        ]

        relevance = relevance_agent.evaluate(
            case["question"],
            case["ai_response"],
            evidence,
        )

        accuracy = accuracy_agent.evaluate(
            case["question"],
            case["ai_response"],
            evidence,
            case["reference_answer"],
        )

        hallucination = hallucination_agent.evaluate(
            case["question"],
            case["ai_response"],
            evidence,
        )

        category = case["category"]

        if category == "correct":
            assert accuracy["score"] >= 0.80
            assert hallucination["score"] >= 0.70

        elif category == "incorrect":
            assert accuracy["category"] == "Incorrect"
            assert hallucination["score"] == 0.0

        elif category == "irrelevant":
            assert relevance["score"] < 0.40

        elif category == "unsupported":
            assert len(
                hallucination["details"]["unsupported_claims"]
            ) >= 1

        elif category == "contradictory":
            assert accuracy["category"] == "Incorrect"
            assert hallucination["details"][
                "contradiction_detected"
            ] is True