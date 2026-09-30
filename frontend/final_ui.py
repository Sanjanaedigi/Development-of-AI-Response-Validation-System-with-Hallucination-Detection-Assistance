import os
import sys
import requests
import pandas as pd
import streamlit as st


# =========================================================
# PROJECT PATH
# =========================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Response Validation System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# PROFESSIONAL UI STYLING
# =========================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: #0b1120;
        color: #e5e7eb;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    h1, h2, h3 {
        color: #f8fafc !important;
    }

    p, label {
        color: #cbd5e1 !important;
    }


    /* ---------- HEADER ---------- */

    .main-header {
        padding: 10px 0 25px 0;
    }

    .main-title {
        font-size: 34px;
        font-weight: 750;
        color: #f8fafc;
        margin-bottom: 4px;
    }

    .main-subtitle {
        font-size: 15px;
        color: #94a3b8;
    }


    /* ---------- MODE PANEL ---------- */

    .mode-panel {
        background: #111827;
        border: 1px solid #263244;
        border-radius: 16px;
        padding: 20px;
        min-height: 520px;
    }

    .mode-title {
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1px;
        color: #94a3b8;
        margin-bottom: 15px;
    }

    .mode-description {
        color: #64748b;
        font-size: 13px;
        line-height: 1.5;
        margin-bottom: 20px;
    }


    /* ---------- WORKSPACE ---------- */

    .workspace {
        background: #111827;
        border: 1px solid #263244;
        border-radius: 16px;
        padding: 28px;
    }

    .section-title {
        font-size: 23px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 4px;
    }

    .section-subtitle {
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 24px;
    }


    /* ---------- INPUT CARDS ---------- */

    .input-card {
        background: #0f172a;
        border: 1px solid #263244;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 15px;
    }


    /* ---------- RESULT CARDS ---------- */

    .result-card {
        background: #0f172a;
        border: 1px solid #263244;
        border-radius: 14px;
        padding: 20px;
        margin-top: 18px;
    }

    .score-number {
        font-size: 27px;
        font-weight: 750;
        color: #f8fafc;
    }

    .score-label {
        font-size: 12px;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: .6px;
    }


    /* ---------- API STATUS ---------- */

    .api-status {
        display: inline-block;
        padding: 7px 13px;
        border-radius: 20px;
        background: #0f2d24;
        border: 1px solid #176b50;
        color: #6ee7b7;
        font-size: 12px;
        font-weight: 650;
    }


    /* ---------- BATCH UPLOAD ---------- */

    .upload-info {
        background: #0f172a;
        border: 1px dashed #475569;
        border-radius: 14px;
        padding: 25px;
        text-align: center;
        margin-bottom: 20px;
    }


    /* ---------- TABLE ---------- */

    [data-testid="stDataFrame"] {
        border: 1px solid #263244;
        border-radius: 10px;
    }


    /* ---------- BUTTONS ---------- */

    .stButton > button {
        border-radius: 9px;
        min-height: 45px;
        font-weight: 650;
    }


    /* ---------- DIVIDER ---------- */

    hr {
        border-color: #263244 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

header_left, header_right = st.columns([5, 1])

with header_left:

    st.markdown(
        """
        <div class="main-header">
            <div class="main-title">
                🛡️ AI Response Validation System
            </div>
            <div class="main-subtitle">
                Validate • Verify • Detect Hallucinations • Explain AI Responses
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with header_right:

    st.markdown(
        """
        <div style="text-align:right; padding-top:12px;">
            <span class="api-status">● API Connected</span>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# API CONFIG
# =========================================================

API_URL = "http://127.0.0.1:8000/api/v1/evaluate"


# =========================================================
# BATCH EVALUATION FUNCTION
# =========================================================

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


# =========================================================
# EVALUATION MODE
# =========================================================

if "evaluation_mode" not in st.session_state:
    st.session_state["evaluation_mode"] = "single"


# =========================================================
# LEFT NAVIGATION + RIGHT WORKSPACE
# =========================================================

mode_col, workspace_col = st.columns(
    [1.15, 4.85],
    gap="large"
)


# =========================================================
# LEFT SIDE
# =========================================================

with mode_col:

    st.markdown(
        """
        <div class="mode-title">
            EVALUATION MODE
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "Choose how you want to validate AI responses."
    )

    st.write("")

    if st.button(
        "📝  Single Evaluation",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state["evaluation_mode"] == "single"
            else "secondary"
        )
    ):

        st.session_state["evaluation_mode"] = "single"

    st.write("")

    if st.button(
        "📊  Batch CSV Evaluation",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state["evaluation_mode"] == "batch"
            else "secondary"
        )
    ):

        st.session_state["evaluation_mode"] = "batch"

    st.write("")
    st.write("")

    st.markdown(
        """
        <div class="mode-description">
            <b>Single Evaluation</b><br>
            Validate one AI response using question,
            reference evidence and source material.
            <br><br>
            <b>Batch Evaluation</b><br>
            Evaluate multiple question-answer pairs
            from a CSV file.
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# RIGHT WORKSPACE
# =========================================================

with workspace_col:

    # =====================================================
    # SINGLE EVALUATION
    # =====================================================

    if st.session_state["evaluation_mode"] == "single":

        st.markdown(
            """
            <div class="section-title">
                📝 Single Evaluation
            </div>

            <div class="section-subtitle">
                Evaluate one AI-generated response against available evidence.
            </div>
            """,
            unsafe_allow_html=True
        )

        # -------------------------------------------------
        # INPUT SECTION
        # -------------------------------------------------

        st.markdown(
            '<div class="input-card">',
            unsafe_allow_html=True
        )

        question = st.text_area(
            "📝 User Question *",
            height=110,
            placeholder="Enter the user's question..."
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


        st.markdown(
            '<div class="input-card">',
            unsafe_allow_html=True
        )

        ai_response = st.text_area(
            "🤖 AI Generated Response *",
            height=160,
            placeholder="Enter the AI-generated response..."
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


        input_col1, input_col2 = st.columns(2)

        with input_col1:

            reference_evidence = st.text_area(
                "📚 Reference / Evidence",
                height=140,
                placeholder=(
                    "Optional evidence used to verify "
                    "the AI response..."
                )
            )

        with input_col2:

            source_document = st.text_area(
                "📄 Source Document / Reference Material",
                height=140,
                placeholder=(
                    "Optional source material..."
                )
            )


        st.write("")

        validate_clicked = st.button(
            "🔍  VALIDATE AI RESPONSE",
            type="primary",
            use_container_width=True
        )


        # =================================================
        # SINGLE EVALUATION
        # =================================================

        if validate_clicked:

            if not question.strip():

                st.error(
                    "Question is required."
                )

            elif not ai_response.strip():

                st.error(
                    "AI Generated Response is required."
                )

            else:

                payload = {
                    "question": question.strip(),
                    "ai_response": ai_response.strip(),
                    "reference_evidence":
                        reference_evidence.strip()
                        or None,
                    "source_document":
                        source_document.strip()
                        or None,
                }

                try:

                    with st.spinner(
                        "Running evaluation pipeline..."
                    ):

                        response = requests.post(
                            API_URL,
                            json=payload,
                            timeout=120
                        )

                    if response.status_code != 201:

                        st.error(
                            f"Backend returned "
                            f"{response.status_code}: "
                            f"{response.text}"
                        )

                    else:

                        data = response.json()

                        st.success(
                            "Evaluation completed successfully."
                        )

                        st.divider()

                        # =================================
                        # RESULT HEADER
                        # =================================

                        st.markdown(
                            "### 📊 Validation Results"
                        )

                        verdict = data["verdict"]

                        overall = (
                            data["overall_score"] * 100
                        )


                        if verdict == "Pass":

                            st.success(
                                f"🟢 PASS  •  "
                                f"Overall Score: "
                                f"{overall:.1f}%"
                            )

                        elif verdict == "Needs Improvement":

                            st.warning(
                                f"🟡 NEEDS IMPROVEMENT  •  "
                                f"Overall Score: "
                                f"{overall:.1f}%"
                            )

                        else:

                            st.error(
                                f"🔴 FAIL  •  "
                                f"Overall Score: "
                                f"{overall:.1f}%"
                            )

                            st.info(
                                f"**Verdict Reason:** "
                                f"{data.get('verdict_reason', '')}"
                            )


                        # =================================
                        # SCORE CARDS
                        # =================================

                        cols = st.columns(4)

                        metrics = [
                            (
                                "🎯 Relevance",
                                data["relevance"]["score"]
                            ),
                            (
                                "✅ Accuracy",
                                data["accuracy"]["score"]
                            ),
                            (
                                "🛡️ Hallucination Safety",
                                data["hallucination"]["score"]
                            ),
                            (
                                "📋 Completeness",
                                data["completeness"]["score"]
                            ),
                        ]

                        for col, (label, score) in zip(
                            cols,
                            metrics
                        ):

                            with col:

                                st.metric(
                                    label,
                                    f"{score * 100:.1f}%"
                                )


                        # =================================
                        # EXPLANATIONS
                        # =================================

                        st.markdown(
                            "### 🔎 Evaluation Explanations"
                        )

                        for name in [
                            "relevance",
                            "accuracy",
                            "hallucination",
                            "completeness"
                        ]:

                            item = data[name]

                            with st.expander(
                                f"{name.title()} — "
                                f"{item['score'] * 100:.1f}%"
                            ):

                                st.write(
                                    item.get(
                                        "explanation",
                                        "No explanation available."
                                    )
                                )


                                if name == "accuracy":

                                    evidence = item.get(
                                        "evidence",
                                        []
                                    )

                                    if evidence:

                                        st.markdown(
                                            "**📚 Supporting Evidence**"
                                        )

                                        for evidence_item in evidence:

                                            st.info(
                                                str(evidence_item)
                                            )


                                    accuracy_details = item.get(
                                        "details",
                                        {}
                                    )

                                    if accuracy_details.get(
                                        "evidence"
                                    ):

                                        for evidence_item in (
                                            accuracy_details["evidence"]
                                        ):

                                            st.info(
                                                str(evidence_item)
                                            )


                                if name == "hallucination":

                                    details = item.get(
                                        "details",
                                        {}
                                    )

                                    unsupported_claims = (
                                        details.get(
                                            "unsupported_claims",
                                            []
                                        )
                                    )

                                    if unsupported_claims:

                                        st.markdown(
                                            "**⚠️ Unsupported / "
                                            "Hallucinated Claims**"
                                        )

                                        for claim in (
                                            unsupported_claims
                                        ):

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

                                            if claim.get(
                                                "evidence"
                                            ):

                                                st.info(
                                                    "Evidence: "
                                                    + claim["evidence"]
                                                )


                                    elif details.get(
                                        "contradiction_detected",
                                        False
                                    ):

                                        st.error(
                                            "⚠️ A contradiction was "
                                            "detected between the "
                                            "AI response and evidence."
                                        )


                                if name == "completeness":

                                    details = item.get(
                                        "details",
                                        {}
                                    )

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

                                        st.markdown(
                                            "**✅ Addressed Aspects**"
                                        )

                                        for aspect in addressed:

                                            st.success(
                                                str(aspect)
                                            )


                                    if partial:

                                        st.markdown(
                                            "**🟡 Partially Addressed**"
                                        )

                                        for aspect in partial:

                                            st.warning(
                                                str(aspect)
                                            )


                                    if missing:

                                        st.markdown(
                                            "**❌ Missing Aspects**"
                                        )

                                        for aspect in missing:

                                            st.error(
                                                str(aspect)
                                            )


                        # =================================
                        # RETRIEVED EVIDENCE
                        # =================================

                        st.markdown(
                            "### 📚 Retrieved Evidence"
                        )

                        if data.get(
                            "retrieved_evidence"
                        ):

                            for item in data[
                                "retrieved_evidence"
                            ]:

                                st.info(
                                    f"**Dataset:** "
                                    f"{item.get('dataset', 'Unknown')} "
                                    f"| **Similarity:** "
                                    f"{item.get('similarity', 0) * 100:.1f}%"
                                    f"\n\n"
                                    f"{item.get('text', '')}"
                                )

                        else:

                            st.warning(
                                "No matching evidence was retrieved."
                            )


                        st.caption(
                            "Validation Record ID: "
                            + str(
                                data.get(
                                    "submission_id",
                                    "N/A"
                                )
                            )
                        )


                except requests.exceptions.RequestException:

                    st.error(
                        "Cannot connect to FastAPI backend."
                    )

                    st.info(
                        "Start the backend with:\n\n"
                        "`python -m uvicorn app.main:app --reload`"
                    )


    # =====================================================
    # BATCH CSV EVALUATION
    # =====================================================

    else:

        st.markdown(
            """
            <div class="section-title">
                📊 Batch CSV Evaluation
            </div>

            <div class="section-subtitle">
                Evaluate multiple AI responses using the same validation pipeline.
            </div>
            """,
            unsafe_allow_html=True
        )


        # -------------------------------------------------
        # CSV UPLOAD
        # -------------------------------------------------

        st.markdown(
            """
            <div class="upload-info">
                <h3>📂 Upload Evaluation CSV</h3>
                <p>
                    Upload a CSV containing question and AI response pairs.
                </p>
                <p>
                    Required: <b>question</b>, <b>ai_response</b>
                </p>
                <p>
                    Optional: <b>reference_answer</b>,
                    <b>source_document</b>
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


        uploaded_file = st.file_uploader(
            "Choose CSV file",
            type=["csv"],
            label_visibility="collapsed"
        )


        if uploaded_file is not None:

            try:

                batch_data = pd.read_csv(
                    uploaded_file
                )

            except pd.errors.ParserError:

                st.error(
                    "❌ Invalid CSV format. "
                    "Please check the file."
                )

                st.stop()


            st.markdown(
                "### 📄 Uploaded CSV Preview"
            )

            st.dataframe(
                batch_data,
                use_container_width=True,
                hide_index=True
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
                    + ", ".join(
                        sorted(missing_columns)
                    )
                )

            else:

                st.success(
                    f"CSV loaded successfully — "
                    f"{len(batch_data)} records found."
                )


                if st.button(
                    "🚀  START BATCH EVALUATION",
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
                            if pd.notna(
                                row["question"]
                            )
                            else ""
                        ).strip()


                        response_value = (
                            str(row["ai_response"])
                            if pd.notna(
                                row["ai_response"]
                            )
                            else ""
                        ).strip()


                        reference_value = (
                            str(
                                row.get(
                                    "reference_answer",
                                    ""
                                )
                            )
                            if pd.notna(
                                row.get(
                                    "reference_answer"
                                )
                            )
                            else ""
                        ).strip()


                        source_value = (
                            str(
                                row.get(
                                    "source_document",
                                    ""
                                )
                            )
                            if pd.notna(
                                row.get(
                                    "source_document"
                                )
                            )
                            else ""
                        ).strip()


                        status_text.write(
                            f"Evaluating row "
                            f"{index + 1} of "
                            f"{total_rows}..."
                        )


                        if (
                            not question_value
                            or not response_value
                        ):

                            invalid_rows.append(
                                {
                                    "row": row_number,
                                    "reason":
                                        "Question or AI response "
                                        "is missing."
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

                                result["row_number"] = (
                                    row_number
                                )

                                result["question"] = (
                                    question_value
                                )

                                batch_results.append(
                                    result
                                )

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


                    st.session_state[
                        "batch_results"
                    ] = batch_results


                    st.session_state[
                        "batch_invalid_rows"
                    ] = invalid_rows


                    st.success(
                        "Batch evaluation completed successfully."
                    )


        # =================================================
        # BATCH RESULTS
        # =================================================

        if "batch_results" in st.session_state:

            st.divider()

            st.markdown(
                "### 📊 Batch Evaluation Results"
            )

            batch_results = st.session_state[
                "batch_results"
            ]


            if batch_results:

                results_table = []


                for result in batch_results:

                    results_table.append(
                        {
                            "Row":
                                result.get(
                                    "row_number",
                                    "N/A"
                                ),

                            "Question":
                                result.get(
                                    "question",
                                    "N/A"
                                ),

                            "Response ID":
                                result.get(
                                    "submission_id",
                                    "N/A"
                                ),

                            "Relevance":
                                round(
                                    result[
                                        "relevance"
                                    ][
                                        "score"
                                    ] * 100,
                                    1
                                ),

                            "Accuracy":
                                round(
                                    result[
                                        "accuracy"
                                    ][
                                        "score"
                                    ] * 100,
                                    1
                                ),

                            "Hallucination Safety":
                                round(
                                    result[
                                        "hallucination"
                                    ][
                                        "score"
                                    ] * 100,
                                    1
                                ),

                            "Completeness":
                                round(
                                    result[
                                        "completeness"
                                    ][
                                        "score"
                                    ] * 100,
                                    1
                                ),

                            "Overall Score":
                                round(
                                    result[
                                        "overall_score"
                                    ] * 100,
                                    1
                                ),

                            "Verdict":
                                result.get(
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


                # Download results

                csv_data = results_df.to_csv(
                    index=False
                ).encode("utf-8")


                st.download_button(
                    "⬇️  DOWNLOAD RESULTS CSV",
                    data=csv_data,
                    file_name="batch_evaluation_results.csv",
                    mime="text/csv",
                    use_container_width=True
                )


            else:

                st.info(
                    "No valid records were available for evaluation."
                )


        # =================================================
        # INVALID ROWS
        # =================================================

        if "batch_invalid_rows" in st.session_state:

            invalid_rows = st.session_state[
                "batch_invalid_rows"
            ]


            if invalid_rows:

                st.divider()

                st.markdown(
                    "### ⚠️ Invalid Rows"
                )


                invalid_df = pd.DataFrame(
                    invalid_rows
                )


                st.dataframe(
                    invalid_df,
                    use_container_width=True,
                    hide_index=True
                )


        # =================================================
        # DETAIL INSPECTION
        # =================================================

        if "batch_results" in st.session_state:

            batch_results = st.session_state[
                "batch_results"
            ]


            if batch_results:

                st.divider()

                st.markdown(
                    "### 🔎 Batch Result Detail Inspection"
                )


                selected_row = st.selectbox(
                    "Select a result to inspect",
                    range(len(batch_results)),
                    format_func=lambda i: (
                        f"Row "
                        f"{batch_results[i].get('row_number', 'N/A')}"
                        f" — "
                        f"{batch_results[i].get('verdict', 'N/A')}"
                    )
                )


                selected_result = batch_results[
                    selected_row
                ]


                st.markdown(
                    "#### 📌 Evaluation Summary"
                )


                col1, col2, col3 = st.columns(3)


                with col1:

                    st.metric(
                        "Overall Score",
                        f"{selected_result['overall_score'] * 100:.1f}%"
                    )


                with col2:

                    st.metric(
                        "Verdict",
                        selected_result.get(
                            "verdict",
                            "N/A"
                        )
                    )


                with col3:

                    st.metric(
                        "Response ID",
                        selected_result.get(
                            "submission_id",
                            "N/A"
                        )
                    )


                with st.expander("🎯 Relevance"):

                    st.write(
                        selected_result[
                            "relevance"
                        ].get(
                            "explanation",
                            "No explanation available."
                        )
                    )


                with st.expander("🎯 Accuracy"):

                    st.write(
                        selected_result[
                            "accuracy"
                        ].get(
                            "explanation",
                            "No explanation available."
                        )
                    )


                    accuracy_details = (
                        selected_result[
                            "accuracy"
                        ].get(
                            "details",
                            {}
                        )
                    )


                    if accuracy_details.get(
                        "evidence"
                    ):

                        st.write(
                            "**Supporting Evidence:**"
                        )

                        for evidence in (
                            accuracy_details[
                                "evidence"
                            ]
                        ):

                            st.info(
                                str(evidence)
                            )


                with st.expander(
                    "🛡️ Hallucination Detection"
                ):

                    st.write(
                        selected_result[
                            "hallucination"
                        ].get(
                            "explanation",
                            "No explanation available."
                        )
                    )


                    hallucination_details = (
                        selected_result[
                            "hallucination"
                        ].get(
                            "details",
                            {}
                        )
                    )


                    if hallucination_details.get(
                        "unsupported_claims"
                    ):

                        st.write(
                            "**Unsupported / "
                            "Hallucinated Claims:**"
                        )

                        for claim in (
                            hallucination_details[
                                "unsupported_claims"
                            ]
                        ):

                            if isinstance(
                                claim,
                                dict
                            ):

                                st.warning(
                                    claim.get(
                                        "claim",
                                        str(claim)
                                    )
                                )

                            else:

                                st.warning(
                                    str(claim)
                                )


                    if hallucination_details.get(
                        "contradiction_detected"
                    ):

                        st.error(
                            "⚠️ Critical contradiction detected."
                        )


                with st.expander(
                    "📋 Completeness"
                ):

                    st.write(
                        selected_result[
                            "completeness"
                        ].get(
                            "explanation",
                            "No explanation available."
                        )
                    )


                    completeness_details = (
                        selected_result[
                            "completeness"
                        ].get(
                            "details",
                            {}
                        )
                    )


                    if completeness_details.get(
                        "addressed_aspects"
                    ):

                        st.write(
                            "**Addressed Aspects:**"
                        )

                        for item in (
                            completeness_details[
                                "addressed_aspects"
                            ]
                        ):

                            st.success(
                                str(item)
                            )


                    if completeness_details.get(
                        "partially_addressed_aspects"
                    ):

                        st.write(
                            "**Partially Addressed:**"
                        )

                        for item in (
                            completeness_details[
                                "partially_addressed_aspects"
                            ]
                        ):

                            st.warning(
                                str(item)
                            )


                    if completeness_details.get(
                        "missing_aspects"
                    ):

                        st.write(
                            "**Missing Aspects:**"
                        )

                        for item in (
                            completeness_details[
                                "missing_aspects"
                            ]
                        ):

                            st.error(
                                str(item)
                            )


        # =================================================
        # BATCH STATISTICS
        # =================================================

        if "batch_results" in st.session_state:

            batch_results = st.session_state[
                "batch_results"
            ]


            if batch_results:

                st.divider()

                st.markdown(
                    "### 📈 Batch Evaluation Statistics"
                )


                total_evaluated = len(
                    batch_results
                )


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
                    if result.get(
                        "verdict"
                    ) == "Pass"
                )


                needs_improvement_count = sum(
                    1
                    for result in batch_results
                    if result.get(
                        "verdict"
                    ) == "Needs Improvement"
                )


                fail_count = sum(
                    1
                    for result in batch_results
                    if result.get(
                        "verdict"
                    ) == "Fail"
                )


                hallucination_count = sum(
                    1
                    for result in batch_results
                    if result[
                        "hallucination"
                    ][
                        "score"
                    ] < 0.70
                )


                st.markdown(
                    "#### 📊 Average Scores"
                )


                col1, col2, col3, col4, col5 = (
                    st.columns(5)
                )


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


                st.markdown(
                    "#### 📋 Verdict Summary"
                )


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


                st.markdown(
                    "#### 🛡️ Hallucination Frequency"
                )


                st.metric(
                    "Records with Hallucination Risk",
                    hallucination_count
                )


                st.caption(
                    "Hallucination risk is counted when "
                    "the hallucination safety score is below 70%."
                )