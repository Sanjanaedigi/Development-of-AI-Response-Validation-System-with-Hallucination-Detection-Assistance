from app.agents import (
    relevance_agent,
    accuracy_agent,
    hallucination_agent,
    completeness_agent,
)


def test_relevance_high_for_matching_response():

    result = relevance_agent.evaluate(
        "What is RAG?",
        "RAG retrieves relevant information.",
        [
            {
                "text": "RAG retrieves relevant information."
            }
        ],
    )

    assert result["score"] >= 0.60


def test_relevance_low_for_unrelated_response():

    result = relevance_agent.evaluate(
        "What is the capital of India?",
        "Python is a programming language.",
        [],
    )

    assert result["score"] < 0.40


def test_accuracy_correct_response():

    result = accuracy_agent.evaluate(
        "What is the capital of France?",
        "The capital of France is Paris.",
        [],
        "Paris is the capital city of France.",
    )

    assert result["score"] >= 0.80
    assert result["category"] == "Correct"


def test_accuracy_incorrect_response():

    result = accuracy_agent.evaluate(
        "What is the capital of France?",
        "The capital of France is London.",
        [],
        "Paris is the capital city of France.",
    )

    assert result["score"] == 0.0
    assert result["category"] == "Incorrect"


def test_accuracy_partially_correct_response():

    result = accuracy_agent.evaluate(
        "What are the benefits of regular exercise?",
        "Regular exercise helps improve physical health.",
        [],
        (
            "Regular exercise improves physical health, "
            "strengthens muscles, supports mental health, "
            "and reduces the risk of chronic diseases."
        ),
    )

    assert 0.40 <= result["score"] < 0.80


def test_hallucination_detected_for_contradiction():

    result = hallucination_agent.evaluate(
        "What is the capital of France?",
        "The capital of France is London.",
        [
            {
                "text": "Paris is the capital city of France.",
                "similarity": 1.0,
            }
        ],
    )

    assert result["score"] == 0.0
    assert result["details"]["contradiction_detected"] is True


def test_hallucination_low_risk_for_supported_response():

    result = hallucination_agent.evaluate(
        "What is the capital of France?",
        "The capital of France is Paris.",
        [
            {
                "text": "Paris is the capital city of France.",
                "similarity": 1.0,
            }
        ],
    )

    assert result["score"] >= 0.70
    assert result["details"]["contradiction_detected"] is False


def test_scores_are_bounded():

    relevance = relevance_agent.evaluate(
        "What is RAG?",
        "RAG retrieves relevant information.",
        [],
    )

    accuracy = accuracy_agent.evaluate(
        "Q",
        "correct answer",
        [],
        "correct answer",
    )

    hallucination = hallucination_agent.evaluate(
        "Q",
        "claim",
        [
            {
                "text": "claim",
                "similarity": 1.0,
            }
        ],
    )

    completeness = completeness_agent.evaluate(
        "Q",
        "answer",
        [
            {
                "answer": "answer",
                "text": "answer",
            }
        ],
    )

    assert 0 <= relevance["score"] <= 1
    assert 0 <= accuracy["score"] <= 1
    assert 0 <= hallucination["score"] <= 1
    assert 0 <= completeness["score"] <= 1