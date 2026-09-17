import csv

from app.evaluation.orchestrator import evaluate_submission


def evaluate_csv(file_path: str):
    """
    Evaluate multiple question-answer records from a CSV file.

    Required columns:
        question
        ai_response

    Optional columns:
        reference_answer
        source_document
    """

    results = []
    invalid_rows = []

    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:

        reader = csv.DictReader(file)

        required_columns = {"question", "ai_response"}

        if not reader.fieldnames:
            raise ValueError("CSV file has no header row.")

        missing_columns = required_columns - set(reader.fieldnames)

        if missing_columns:
            raise ValueError(
                "Missing required CSV columns: "
                + ", ".join(sorted(missing_columns))
            )

        for row_number, row in enumerate(reader, start=2):

            question = (row.get("question") or "").strip()
            ai_response = (row.get("ai_response") or "").strip()

            reference_answer = (
                row.get("reference_answer") or ""
            ).strip()

            source_document = (
                row.get("source_document") or ""
            ).strip()

            # -----------------------------------------
            # Validate required fields
            # -----------------------------------------

            if not question or not ai_response:

                invalid_rows.append(
                    {
                        "row": row_number,
                        "reason": "Question or AI response is missing."
                    }
                )

                continue

            # -----------------------------------------
            # Evaluate valid row
            # -----------------------------------------

            try:

                result = evaluate_submission(
                    question=question,
                    ai_response=ai_response,
                    reference_answer=reference_answer or None,
                    reference_evidence=source_document or None
                )

                result["row_number"] = row_number

                results.append(result)

            except Exception as exc:

                invalid_rows.append(
                    {
                        "row": row_number,
                        "reason": str(exc)
                    }
                )

    return {
        "results": results,
        "invalid_rows": invalid_rows
    }