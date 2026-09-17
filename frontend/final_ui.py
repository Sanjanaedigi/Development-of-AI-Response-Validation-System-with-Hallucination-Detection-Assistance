import os
import sys
import requests
import pandas as pd
import streamlit as st

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def evaluate_csv_row(
    question,
    ai_response,
    reference_answer=None,
    source_document=None
):
    """
    Evaluate one CSV row using the existing
    batch evaluation pipeline.
    """

    from app.evaluation.orchestrator import evaluate_submission

    return evaluate_submission(
        question=question,
        ai_response=ai_response,
        reference_answer=reference_answer or None,
        reference_evidence=source_document or None
    )
    
st.set_page_config(
    page_title="AI Response Validation System",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AI Response Validation System")
st.caption("Validate • Verify • Detect Hallucinations • Explain AI Responses")

API_URL = st.sidebar.text_input(
    "Backend API URL",
    "http://127.0.0.1:8000/api/v1/evaluate"
)

st.subheader("📝 Evaluation Input")

question = st.text_area(
    "📝 User Question *",
    height=120,
    placeholder="Enter the user's question..."
)

ai_response = st.text_area(
    "🤖 AI Generated Response *",
    height=180,
    placeholder="Enter the AI-generated response..."
)

reference_evidence = st.text_area(
    "📚 Reference / Evidence (Optional)",
    height=160,
    placeholder="Optional: provide evidence to verify the AI response..."
)

source_document = st.text_area(
    "📄 Source Document / Reference Material (Optional)",
    height=120,
    placeholder="Optional: provide source material..."
)


if st.button(
    "🔍 VALIDATE AI RESPONSE",
    type="primary",
    use_container_width=True
):

    # Required fields
    if not question.strip():
        st.error("Question is required.")

    elif not ai_response.strip():
        st.error("AI Generated Response is required.")

    else:

        payload = {
            "question": question.strip(),
            "ai_response": ai_response.strip(),
            "reference_evidence": reference_evidence.strip() or None,
            "source_document": source_document.strip() or None,
        }

        try:

            with st.spinner("Running evaluation pipeline..."):

                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=120
                )

            if response.status_code != 201:

                st.error(
                    f"Backend returned {response.status_code}: "
                    f"{response.text}"
                )

            else:

                data = response.json()

                st.success("Evaluation Completed Successfully!")

                st.subheader("📊 Validation Results")

                verdict = data["verdict"]

                overall = data["overall_score"] * 100

                if verdict == "Pass":

                    st.success(
                        f"🟢 PASS | Overall Score: "
                        f"{overall:.1f}%"
                    )

                elif verdict == "Needs Improvement":

                    st.warning(
                        f"🟡 NEEDS IMPROVEMENT | Overall Score: "
                        f"{overall:.1f}%"
                    )

                else:

                    st.error(
                        f"🔴 FAIL | Overall Score: "
                        f"{overall:.1f}%"
                    )

                    st.info(
                        f"**Verdict Reason:** "
                        f"{data['verdict_reason']}"
                    )

                # Scores
                cols = st.columns(4)

                metrics = [
                    ("🎯 RELEVANCE", data["relevance"]["score"]),
                    ("✅ ACCURACY", data["accuracy"]["score"]),
                    ("🛡️ HALLUCINATION SAFETY", data["hallucination"]["score"]),
                    ("📋 COMPLETENESS", data["completeness"]["score"]),
                ]

                for col, (label, score) in zip(cols, metrics):

                    col.metric(
                        label,
                        f"{score * 100:.1f}%"
                    )

                # Explanations
                st.subheader("🔎 Evaluation Explanations")

                for name in [
                    "relevance",
                    "accuracy",
                    "hallucination",
                    "completeness"
                ]:

                    item = data[name]

                    st.markdown(
                        f"**{name.title()} — "
                        f"{item['score'] * 100:.1f}%**"
                    )

                    st.write(item["explanation"])
                    
                    if name == "accuracy":

                        evidence = item.get("evidence", [])

                        if evidence:

                            with st.expander("📚 Accuracy Supporting Evidence"):

                                for evidence_item in evidence:

                                    st.info(evidence_item)
                                    
                    if name == "hallucination":

                        details = item.get("details", {})

                        unsupported_claims = details.get(
                            "unsupported_claims",
                            []
                        )

                        if unsupported_claims:

                            with st.expander("⚠️ Unsupported / Hallucinated Claims"):

                                for claim in unsupported_claims:

                                    st.error(
                                        claim.get(
                                            "claim",
                                            "Unknown claim"
                                        )
                                    )

                                    st.write(
                                        claim.get(
                                            "reason",
                                            ""
                                        )
                                    )

                                    if claim.get("evidence"):

                                        st.info(
                                            "Evidence: "
                                            + claim["evidence"]
                                        )

                        elif details.get(
                            "contradiction_detected",
                            False
                        ):

                            st.error(
                                "⚠️ A contradiction was detected "
                                "between the AI response and evidence."
                            ) 
                    if name == "completeness":

                        details = item.get("details", {})

                        addressed = details.get(
                            "addressed_aspects",
                            []
                        )

                        partial = details.get(
                            "partially_addressed_aspects",
                            []
                        )

                        missing = details.get(
                            "missing_aspects",
                            []
                        )

                        if addressed:

                            with st.expander("✅ Addressed Aspects"):

                                for aspect in addressed:

                                    st.write("• " + aspect)

                        if partial:

                            with st.expander("🟡 Partially Addressed Aspects"):

                                for aspect in partial:

                                    st.write("• " + aspect)

                        if missing:

                            with st.expander("❌ Missing Aspects"):

                                for aspect in missing:

                                    st.write("• " + aspect)                      

                # Retrieved evidence
                st.subheader("📚 Retrieved Evidence")

                if data["retrieved_evidence"]:

                    for item in data["retrieved_evidence"]:

                        st.info(
                            f"**Dataset:** "
                            f"{item.get('dataset', 'Unknown')} | "
                            f"**Similarity:** "
                            f"{item.get('similarity', 0) * 100:.1f}%\n\n"
                            f"{item.get('text', '')}"
                        )

                else:

                    st.warning(
                        "No matching evidence was retrieved."
                    )

                st.caption(
                    f"Validation Record ID: "
                    f"{data['submission_id']}"
                )

        except requests.exceptions.RequestException:

            st.error(
                "Cannot connect to FastAPI backend. "
                "Start it with: "
                "python -m uvicorn app.main:app --reload"
            )
# =========================================================
# M3.4 - BATCH CSV EVALUATION
# =========================================================

st.divider()

st.header("📦 Batch CSV Evaluation")

st.write(
    "Upload a CSV file containing multiple question-answer pairs "
    "to evaluate them using the same validation pipeline."
)

uploaded_file = st.file_uploader(
    "📂 Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    try:

        batch_data = pd.read_csv(
            uploaded_file
        )

    except pd.errors.ParserError:

        st.error(
            "❌ Invalid CSV format. "
            "Please check that the CSV contains "
            "properly formatted columns and rows."
        )

        st.stop()

    st.subheader("📄 Uploaded CSV")

    st.dataframe(
        batch_data,
        use_container_width=True
    )

    required_columns = {
        "question",
        "ai_response"
    }

    missing_columns = (
        required_columns
        - set(batch_data.columns)
    )

    if missing_columns:

        st.error(
            "Missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

    else:

        st.success(
            f"CSV loaded successfully: "
            f"{len(batch_data)} records found."
        )

        if st.button(
            "🚀 START BATCH EVALUATION",
            type="primary",
            use_container_width=True
        ):

            progress_bar = st.progress(0)

            status_text = st.empty()

            batch_results = []

            invalid_rows = []

            total_rows = len(batch_data)

            for index, row in batch_data.iterrows():

                row_number = index + 2

                question_value = (
                    str(row["question"])
                    if pd.notna(row["question"])
                    else ""
                ).strip()

                response_value = (
                    str(row["ai_response"])
                    if pd.notna(row["ai_response"])
                    else ""
                ).strip()

                reference_value = (
                    str(row.get("reference_answer", ""))
                    if pd.notna(
                        row.get("reference_answer")
                    )
                    else ""
                ).strip()

                source_value = (
                    str(row.get("source_document", ""))
                    if pd.notna(
                        row.get("source_document")
                    )
                    else ""
                ).strip()

                status_text.write(
                    f"Evaluating row "
                    f"{index + 1} of {total_rows}..."
                )

                if not question_value or not response_value:

                    invalid_rows.append(
                        {
                            "row": row_number,
                            "reason": (
                                "Question or AI response "
                                "is missing."
                            )
                        }
                    )

                else:

                    try:

                        result = evaluate_csv_row(
                            question_value,
                            response_value,
                            reference_value,
                            source_value
                        )

                        result["row_number"] = row_number
                        result["question"] = question_value

                        batch_results.append(result)

                    except Exception as exc:

                        invalid_rows.append(
                            {
                                "row": row_number,
                                "reason": str(exc)
                            }
                        )

                progress_bar.progress(
                    (index + 1) / total_rows
                )

            st.session_state["batch_results"] = (
                batch_results
            )

            st.session_state["batch_invalid_rows"] = (
                invalid_rows
            )

            st.success(
                "Batch evaluation completed."
            )


# =========================================================
# BATCH RESULTS
# =========================================================

if "batch_results" in st.session_state:

    st.divider()

    st.header("📊 Batch Evaluation Results")

    batch_results = st.session_state["batch_results"]

    if batch_results:

        results_table = []

        for result in batch_results:

            results_table.append(
                {
                    "Row": result.get(
                        "row_number",
                        "N/A"
                    ),
                    "Question": result.get(
                        "question",
                        "N/A"
                    ),
                    "Response ID": result.get(
                        "submission_id",
                        "N/A"
                    ),
                    "Relevance": round(
                        result["relevance"]["score"] * 100,
                        1
                    ),
                    "Accuracy": round(
                        result["accuracy"]["score"] * 100,
                        1
                    ),
                    "Hallucination Safety": round(
                        result["hallucination"]["score"] * 100,
                        1
                    ),
                    "Completeness": round(
                        result["completeness"]["score"] * 100,
                        1
                    ),
                    "Overall Score": round(
                        result["overall_score"] * 100,
                        1
                    ),
                    "Verdict": result.get(
                        "verdict",
                        "N/A"
                    )
                }
            )

        results_df = pd.DataFrame(
            results_table
        )

        st.dataframe(
            results_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No valid records were available for evaluation."
        )


# =========================================================
# INVALID ROWS
# =========================================================

if "batch_invalid_rows" in st.session_state:

    invalid_rows = st.session_state[
        "batch_invalid_rows"
    ]

    if invalid_rows:

        st.subheader("⚠️ Invalid Rows")

        invalid_df = pd.DataFrame(
            invalid_rows
        )

        st.dataframe(
            invalid_df,
            use_container_width=True,
            hide_index=True
        )
# =========================================================
# BATCH RESULT DETAIL INSPECTION
# =========================================================

if "batch_results" in st.session_state:

    st.divider()

    st.header("🔎 Batch Result Detail Inspection")

    batch_results = st.session_state["batch_results"]

    if batch_results:

        selected_row = st.selectbox(
            "Select a result to inspect",
            range(len(batch_results)),
            format_func=lambda i: (
                f"Row {batch_results[i].get('row_number', 'N/A')} "
                f"— {batch_results[i].get('submission_id', 'N/A')} "
                f"— {batch_results[i].get('verdict', 'N/A')}"
            )
        )

        selected_result = batch_results[selected_row]

        st.subheader("📌 Evaluation Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Overall Score",
                f"{selected_result['overall_score'] * 100:.1f}%"
            )

        with col2:
            st.metric(
                "Verdict",
                selected_result.get("verdict", "N/A")
            )

        with col3:
            st.metric(
                "Response ID",
                selected_result.get(
                    "submission_id",
                    "N/A"
                )
            )

        st.subheader("🎯 Relevance")

        st.write(
            selected_result["relevance"].get(
                "explanation",
                "No explanation available."
            )
        )

        st.subheader("🎯 Accuracy")

        st.write(
            selected_result["accuracy"].get(
                "explanation",
                "No explanation available."
            )
        )

        accuracy_details = selected_result[
            "accuracy"
        ].get("details", {})

        if accuracy_details.get("evidence"):

            st.write("**Supporting Evidence:**")

            for evidence in accuracy_details["evidence"]:

                st.info(str(evidence))

        st.subheader("🛡️ Hallucination Detection")

        st.write(
            selected_result["hallucination"].get(
                "explanation",
                "No explanation available."
            )
        )

        hallucination_details = selected_result[
            "hallucination"
        ].get("details", {})

        if hallucination_details.get(
            "unsupported_claims"
        ):

            st.write("**Unsupported / Hallucinated Claims:**")

            for claim in hallucination_details[
                "unsupported_claims"
            ]:

                st.warning(str(claim))

        if hallucination_details.get(
            "contradiction_detected"
        ):

            st.error(
                "⚠️ Critical contradiction detected."
            )

        st.subheader("📋 Completeness")

        st.write(
            selected_result["completeness"].get(
                "explanation",
                "No explanation available."
            )
        )

        completeness_details = selected_result[
            "completeness"
        ].get("details", {})

        if completeness_details.get(
            "addressed_aspects"
        ):

            st.write("**Addressed Aspects:**")

            for item in completeness_details[
                "addressed_aspects"
            ]:

                st.success(str(item))

        if completeness_details.get(
            "partially_addressed_aspects"
        ):

            st.write("**Partially Addressed:**")

            for item in completeness_details[
                "partially_addressed_aspects"
            ]:

                st.warning(str(item))

        if completeness_details.get(
            "missing_aspects"
        ):

            st.write("**Missing Aspects:**")

            for item in completeness_details[
                "missing_aspects"
            ]:

                st.error(str(item))        
# =========================================================
# BATCH AGGREGATED STATISTICS
# =========================================================

if "batch_results" in st.session_state:

    batch_results = st.session_state["batch_results"]

    if batch_results:

        st.divider()

        st.header("📈 Batch Evaluation Statistics")

        total_evaluated = len(batch_results)

        average_relevance = sum(
            result["relevance"]["score"]
            for result in batch_results
        ) / total_evaluated

        average_accuracy = sum(
            result["accuracy"]["score"]
            for result in batch_results
        ) / total_evaluated

        average_hallucination = sum(
            result["hallucination"]["score"]
            for result in batch_results
        ) / total_evaluated

        average_completeness = sum(
            result["completeness"]["score"]
            for result in batch_results
        ) / total_evaluated

        average_overall = sum(
            result["overall_score"]
            for result in batch_results
        ) / total_evaluated

        pass_count = sum(
            1
            for result in batch_results
            if result.get("verdict") == "Pass"
        )

        needs_improvement_count = sum(
            1
            for result in batch_results
            if result.get("verdict") == "Needs Improvement"
        )

        fail_count = sum(
            1
            for result in batch_results
            if result.get("verdict") == "Fail"
        )

        hallucination_count = sum(
            1
            for result in batch_results
            if result["hallucination"]["score"] < 0.70
        )

        st.subheader("📊 Average Scores")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric(
                "Relevance",
                f"{average_relevance * 100:.1f}%"
            )

        with col2:
            st.metric(
                "Accuracy",
                f"{average_accuracy * 100:.1f}%"
            )

        with col3:
            st.metric(
                "Hallucination Safety",
                f"{average_hallucination * 100:.1f}%"
            )

        with col4:
            st.metric(
                "Completeness",
                f"{average_completeness * 100:.1f}%"
            )

        with col5:
            st.metric(
                "Overall",
                f"{average_overall * 100:.1f}%"
            )

        st.subheader("📋 Verdict Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "✅ Pass",
                pass_count
            )

        with col2:
            st.metric(
                "⚠️ Needs Improvement",
                needs_improvement_count
            )

        with col3:
            st.metric(
                "❌ Fail",
                fail_count
            )

        st.subheader("🛡️ Hallucination Frequency")

        st.metric(
            "Records with Hallucination Risk",
            hallucination_count
        )

        st.caption(
            "Hallucination risk is counted when "
            "the hallucination safety score is below 70%."
        )                