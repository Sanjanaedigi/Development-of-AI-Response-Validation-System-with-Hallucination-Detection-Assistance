import csv

from app.batch_evaluator import evaluate_csv


def create_csv(tmp_path, rows):
    file_path = tmp_path / "batch_test.csv"

    with file_path.open(
        "w",
        encoding="utf-8",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "question",
                "ai_response",
                "reference_answer",
                "source_document"
            ]
        )

        writer.writeheader()
        writer.writerows(rows)

    return str(file_path)


def test_valid_batch_evaluation(tmp_path):

    rows = [
        {
            "question": "What is the capital of France?",
            "ai_response": "The capital of France is Paris.",
            "reference_answer": "Paris is the capital city of France.",
            "source_document": ""
        },
        {
            "question": "What is 2 plus 2?",
            "ai_response": "2 plus 2 equals 4.",
            "reference_answer": "2 plus 2 equals 4.",
            "source_document": ""
        }
    ]

    file_path = create_csv(
        tmp_path,
        rows
    )

    result = evaluate_csv(file_path)

    assert len(result["results"]) == 2
    assert len(result["invalid_rows"]) == 0


def test_invalid_row_does_not_stop_batch(tmp_path):

    rows = [
        {
            "question": "What is the capital of France?",
            "ai_response": "The capital of France is Paris.",
            "reference_answer": "Paris is the capital city of France.",
            "source_document": ""
        },
        {
            "question": "",
            "ai_response": "This row is invalid.",
            "reference_answer": "",
            "source_document": ""
        },
        {
            "question": "What is 2 plus 2?",
            "ai_response": "2 plus 2 equals 4.",
            "reference_answer": "2 plus 2 equals 4.",
            "source_document": ""
        }
    ]

    file_path = create_csv(
        tmp_path,
        rows
    )

    result = evaluate_csv(file_path)

    assert len(result["results"]) == 2
    assert len(result["invalid_rows"]) == 1
    assert result["invalid_rows"][0]["row"] == 3


def test_missing_required_column(tmp_path):

    file_path = tmp_path / "missing_column.csv"

    with file_path.open(
        "w",
        encoding="utf-8",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["question"]
        )

        writer.writeheader()

        writer.writerow(
            {
                "question": "What is the capital of France?"
            }
        )

    try:

        evaluate_csv(str(file_path))

        assert False, (
            "Expected ValueError for missing "
            "required column."
        )

    except ValueError as exc:

        assert "ai_response" in str(exc)


def test_optional_reference_and_source_fields(
    tmp_path
):

    rows = [
        {
            "question": "What is the capital of France?",
            "ai_response": "The capital of France is Paris.",
            "reference_answer": "",
            "source_document": (
                "Paris is the capital city of France."
            )
        }
    ]

    file_path = create_csv(
        tmp_path,
        rows
    )

    result = evaluate_csv(file_path)

    assert len(result["results"]) == 1
    assert len(result["invalid_rows"]) == 0