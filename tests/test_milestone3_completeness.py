from app.agents.completeness_agent import evaluate


def test_fully_complete_reference_answer():
    response = (
        "Exercise improves physical health, mental health, "
        "sleep quality, and helps manage weight."
    )

    reference = (
        "Exercise improves physical health, mental health, "
        "sleep quality, and helps manage weight."
    )

    result = evaluate(
        "What are the benefits of exercise?",
        response,
        [],
        reference,
    )

    assert result["score"] >= 0.70
    assert result["details"]["mode"] == "reference_answer"
    assert result["details"]["missing_aspects"] == []
    assert len(result["details"]["addressed_aspects"]) > 0
    assert result["details"]["reasoning"]


def test_partially_complete_reference_answer():
    response = (
        "Exercise improves physical health and mental health."
    )

    reference = (
        "Exercise improves physical health, mental health, "
        "sleep quality, and helps manage weight."
    )

    result = evaluate(
        "What are the benefits of exercise?",
        response,
        [],
        reference,
    )

    assert 0.40 <= result["score"] < 0.70
    assert result["details"]["mode"] == "reference_answer"
    assert len(result["details"]["missing_aspects"]) > 0
    assert result["details"]["reasoning"]


def test_substantially_incomplete_reference_answer():
    response = (
        "Exercise is an activity that people do regularly."
    )

    reference = (
        "Exercise improves physical health, mental health, "
        "sleep quality, and helps manage weight."
    )

    result = evaluate(
        "What are the benefits of exercise?",
        response,
        [],
        reference,
    )

    assert result["score"] < 0.40
    assert result["details"]["mode"] == "reference_answer"
    assert len(result["details"]["missing_aspects"]) > 0
    assert result["details"]["reasoning"]


def test_completeness_with_rag_evidence():
    evidence = [
        {
            "text": (
                "Exercise improves physical health, mental health, "
                "sleep quality, and helps manage weight."
            ),
            "similarity": 0.92,
        }
    ]

    response = (
        "Exercise improves physical health and mental health."
    )

    result = evaluate(
        "What are the benefits of exercise?",
        response,
        evidence,
    )

    assert result["details"]["mode"] == "retrieved_evidence"
    assert result["score"] < 0.70
    assert len(result["details"]["missing_aspects"]) > 0
    assert result["details"]["reasoning"]


def test_completeness_without_reference_or_evidence():
    result = evaluate(
        "What are the benefits of exercise?",
        "Exercise is useful.",
        [],
    )

    assert result["score"] == 0.50
    assert result["details"]["mode"] == "uncertain"
    assert result["details"]["missing_aspects"] == []
    assert result["details"]["reasoning"]