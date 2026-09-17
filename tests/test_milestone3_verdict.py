from app.core.scoring import overall_score, verdict


def _results(
    relevance,
    accuracy,
    hallucination,
    completeness,
    contradiction=False,
):
    return {
        "relevance": {
            "score": relevance,
        },
        "accuracy": {
            "score": accuracy,
        },
        "hallucination": {
            "score": hallucination,
            "details": {
                "contradiction_detected": contradiction,
            },
        },
        "completeness": {
            "score": completeness,
        },
    }


def test_weighted_overall_score():
    results = _results(
        0.80,
        0.60,
        1.00,
        0.40,
    )

    score = overall_score(results)

    assert score == 0.70


def test_pass_verdict():
    results = _results(
        0.90,
        0.90,
        0.90,
        0.90,
    )

    result, reason = verdict(results)

    assert result == "Pass"
    assert reason


def test_needs_improvement_verdict():
    results = _results(
        0.50,
        0.50,
        0.50,
        0.50,
    )

    result, reason = verdict(results)

    assert result == "Needs Improvement"
    assert reason


def test_fail_verdict():
    results = _results(
        0.20,
        0.20,
        0.20,
        0.20,
    )

    result, reason = verdict(results)

    assert result == "Fail"
    assert reason


def test_contradiction_causes_fail():
    results = _results(
        0.90,
        0.90,
        0.90,
        0.90,
        contradiction=True,
    )

    result, reason = verdict(results)

    assert result == "Fail"
    assert "contradiction" in reason.lower()


def test_weighted_score_uses_all_dimensions():
    results = _results(
        1.00,
        0.00,
        1.00,
        0.00,
    )

    score = overall_score(results)

    assert score == 0.50