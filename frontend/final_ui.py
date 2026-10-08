import os
import sys
import json
from io import BytesIO

import requests
import pandas as pd
import streamlit as st
def percentage(value):
    try:
        number = float(value)

        # Backend stores scores as 0–1
        if number <= 1:
            number = number * 100

        return f"{number:.1f}%"

    except (TypeError, ValueError):
        return "0.0%"
# =========================================================
# PDF EXPORT
# =========================================================

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle,
)
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


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
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Response Validation System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #263244;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    .sidebar-title {
        font-size: 18px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 5px;
    }

    .sidebar-subtitle {
        font-size: 12px;
        color: #94a3b8;
        line-height: 1.5;
        margin-bottom: 25px;
    }

    .sidebar-section {
        font-size: 11px;
        font-weight: 700;
        color: #64748b;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }

    .project-title {
        font-size: 32px;
        font-weight: 750;
        color: #f8fafc;
        margin-bottom: 4px;
    }

    .project-subtitle {
        font-size: 15px;
        color: #94a3b8;
        margin-bottom: 14px;
    }

    .api-status {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background-color: #132e25;
        color: #86efac;
        border: 1px solid #1f513d;
        border-radius: 20px;
        padding: 5px 12px;
        font-size: 13px;
        margin-bottom: 25px;
    }

    .api-dot {
        width: 7px;
        height: 7px;
        background-color: #22c55e;
        border-radius: 50%;
        display: inline-block;
    }

    .page-title {
        font-size: 27px;
        font-weight: 700;
        color: #f8fafc;
        margin-top: 8px;
        margin-bottom: 5px;
    }

    .page-description {
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 25px;
    }

    .section-label {
        font-size: 11px;
        font-weight: 700;
        color: #64748b;
        letter-spacing: 1.3px;
        margin-bottom: 12px;
    }

    .info-card {
        background-color: #111827;
        border: 1px solid #263244;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 16px;
    }

    .metric-card {
        background-color: #111827;
        border: 1px solid #263244;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
    }

    .metric-label {
        color: #94a3b8;
        font-size: 13px;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #f8fafc;
        font-size: 30px;
        font-weight: 700;
    }

    .result-card {
        background-color: #111827;
        border: 1px solid #263244;
        border-radius: 14px;
        padding: 20px;
        margin-top: 18px;
    }

    .result-title {
        color: #f8fafc;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .score-box {
        background-color: #172033;
        border: 1px solid #2b3950;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
    }

    .score-name {
        color: #94a3b8;
        font-size: 12px;
        margin-bottom: 5px;
    }

    .score-value {
        color: #f8fafc;
        font-size: 24px;
        font-weight: 700;
    }

    .verdict-pass {
        display: inline-block;
        background-color: #123524;
        border: 1px solid #1f6b42;
        color: #86efac;
        padding: 7px 15px;
        border-radius: 20px;
        font-weight: 700;
    }

    .verdict-improve {
        display: inline-block;
        background-color: #3a2d0b;
        border: 1px solid #80621a;
        color: #fde68a;
        padding: 7px 15px;
        border-radius: 20px;
        font-weight: 700;
    }

    .verdict-fail {
        display: inline-block;
        background-color: #3b1515;
        border: 1px solid #7f1d1d;
        color: #fca5a5;
        padding: 7px 15px;
        border-radius: 20px;
        font-weight: 700;
    }

    .detail-title {
        color: #e2e8f0;
        font-size: 15px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 5px;
    }

    .detail-text {
        color: #94a3b8;
        font-size: 14px;
        line-height: 1.6;
    }

    .stButton > button {
        width: 100%;
        border-radius: 9px;
        min-height: 44px;
        font-weight: 600;
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {
        background-color: #111827;
        color: #f8fafc;
        border: 1px solid #334155;
        border-radius: 9px;
    }

    div[data-testid="stTextArea"] textarea {
        min-height: 120px;
    }

    label {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #263244;
        border-radius: 10px;
        overflow: hidden;
    }

    hr {
        border-color: #263244;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = "Single Evaluation"

if "single_result" not in st.session_state:
    st.session_state.single_result = None

if "batch_results" not in st.session_state:
    st.session_state.batch_results = None


# =========================================================
# API CONFIGURATION
# =========================================================

DEFAULT_API_URL = (
    "http://127.0.0.1:8000/api/v1/evaluate"
)

API_URL = st.sidebar.text_input(
    "Backend API URL",
    value=DEFAULT_API_URL,
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    """
    <div class="sidebar-title">
        🛡️ AI Response Validation
    </div>

    <div class="sidebar-subtitle">
        Validate, verify and detect hallucinations
        in AI-generated responses.
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    '<div class="sidebar-section">EVALUATION MODE</div>',
    unsafe_allow_html=True,
)

if st.sidebar.button(
    "📝  Single Evaluation",
    use_container_width=True,
):
    st.session_state.selected_mode = "Single Evaluation"
    st.rerun()

if st.sidebar.button(
    "📊  Batch Evaluation",
    use_container_width=True,
):
    st.session_state.selected_mode = "Batch Evaluation"
    st.rerun()

if st.sidebar.button(
    "📈  Dashboard",
    use_container_width=True,
):
    st.session_state.selected_mode = "Dashboard"
    st.rerun()

st.sidebar.markdown("---")

st.sidebar.markdown(
    f"""
    <div style="
        font-size:12px;
        color:#64748b;
        margin-bottom:5px;
    ">
        CURRENT MODE
    </div>

    <div style="
        font-size:14px;
        color:#e2e8f0;
        font-weight:600;
    ">
        {st.session_state.selected_mode}
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# MAIN HEADER
# =========================================================

st.markdown(
    """
    <div class="project-title">
        🛡️ AI Response Validation System
    </div>

    <div class="project-subtitle">
        Validate • Verify • Detect Hallucinations • Explain AI Responses
    </div>

    <div class="api-status">
        <span class="api-dot"></span>
        API Connected
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def safe_score(value):
    try:
        if value is None:
            return 0.0

        if isinstance(value, str):
            value = value.replace("%", "").strip()

        number = float(value)

        if number > 1:
            number = number / 100

        return max(0.0, min(1.0, number))

    except Exception:
        return 0.0


def get_nested(data, *keys, default=None):

    current = data

    for key in keys:

        if not isinstance(current, dict):
            return default

        current = current.get(key)

        if current is None:
            return default

    return current


def display_verdict(verdict):

    if not verdict:
        verdict = "UNKNOWN"

    verdict_text = str(verdict).upper()

    if (
        "PASS" in verdict_text
        and "BLOCK" not in verdict_text
    ):
        css_class = "verdict-pass"
        icon = "✅"

    elif (
        "IMPROVE" in verdict_text
        or "NEEDS IMPROVEMENT" in verdict_text
    ):
        css_class = "verdict-improve"
        icon = "⚠️"

    elif (
        "FAIL" in verdict_text
        or "BLOCK" in verdict_text
        or "REJECT" in verdict_text
    ):
        css_class = "verdict-fail"
        icon = "❌"

    else:
        css_class = "verdict-improve"
        icon = "ℹ️"

    st.markdown(
        f"""
        <span class="{css_class}">
            {icon} {verdict_text}
        </span>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# LOAD STORED RESULTS
# =========================================================

def load_stored_results():

    submissions_file = os.path.join(
        PROJECT_ROOT,
        "data",
        "submissions.jsonl",
    )

    results = []

    if not os.path.exists(
        submissions_file
    ):
        return results

    try:

        with open(
            submissions_file,
            "r",
            encoding="utf-8",
        ) as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                try:

                    data = json.loads(line)

                    if isinstance(data, dict):
                        results.append(data)

                except json.JSONDecodeError:
                    continue

    except Exception:

        return results

    return results


# =========================================================
# SINGLE RESULT DISPLAY
# =========================================================

def display_single_result(result):

    st.markdown(
        "### 📋 Evaluation Result"
    )

    overall_score = safe_score(
        result.get(
            "overall_score",
            0,
        )
    )

    verdict = result.get(
        "verdict",
        "UNKNOWN",
    )

    reason = result.get(
        "verdict_reason",
        "",
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Overall Score",
            percentage(overall_score),
        )
    with col2:

        st.markdown(
            "**Verdict**"
        )

        display_verdict(
            verdict
        )

    if reason:

        st.markdown(
            "#### Verdict Explanation"
        )

        st.info(
            reason
        )

    # -----------------------------------------------------
    # DIMENSION SCORES
    # -----------------------------------------------------

    st.markdown(
        "### 📊 Dimension Scores"
    )

    relevance = safe_score(
        get_nested(
            result,
            "relevance",
            "score",
            default=0,
        )
    )

    accuracy = safe_score(
        get_nested(
            result,
            "accuracy",
            "score",
            default=0,
        )
    )

    hallucination = safe_score(
        get_nested(
            result,
            "hallucination",
            "score",
            default=0,
        )
    )

    completeness = safe_score(
        get_nested(
            result,
            "completeness",
            "score",
            default=0,
        )
    )

    score_columns = st.columns(4)

    score_data = [
        ("Relevance", relevance),
        ("Accuracy", accuracy),
        (
            "Hallucination Safety",
            hallucination,
        ),
        ("Completeness", completeness),
    ]

    for column, (
        label,
        value,
    ) in zip(
        score_columns,
        score_data,
    ):

        with column:

            st.metric(
                label,
                percentage(value),
            )  

    # -----------------------------------------------------
    # RELEVANCE
    # -----------------------------------------------------

    relevance_explanation = get_nested(
        result,
        "relevance",
        "explanation",
        default="",
    )

    if relevance_explanation:

        with st.expander(
            "🔎 Relevance Evaluation",
            expanded=True,
        ):

            st.write(
                relevance_explanation
            )

    # -----------------------------------------------------
    # ACCURACY
    # -----------------------------------------------------

    accuracy_explanation = get_nested(
        result,
        "accuracy",
        "explanation",
        default="",
    )

    accuracy_evidence = get_nested(
        result,
        "accuracy",
        "evidence",
        default="",
    )

    if (
        accuracy_explanation
        or accuracy_evidence
    ):

        with st.expander(
            "🎯 Accuracy Evaluation",
            expanded=True,
        ):

            if accuracy_explanation:
                st.write(
                    accuracy_explanation
                )

            if accuracy_evidence:

                st.markdown(
                    "**Supporting Evidence**"
                )

                st.write(
                    accuracy_evidence
                )

    # -----------------------------------------------------
    # HALLUCINATION
    # -----------------------------------------------------

    hallucination_details = get_nested(
        result,
        "hallucination",
        "details",
        default={},
    )

    unsupported_claims = []

    if isinstance(
        hallucination_details,
        dict,
    ):

        unsupported_claims = (
            hallucination_details.get(
                "unsupported_claims",
                [],
            )
        )

    with st.expander(
        "🛡️ Hallucination Detection",
        expanded=True,
    ):

        if unsupported_claims:

            st.warning(
                "Unsupported claims detected."
            )

            if isinstance(
                unsupported_claims,
                list,
            ):

                for claim in unsupported_claims:

                    st.write(
                        f"• {claim}"
                    )

            else:

                st.write(
                    unsupported_claims
                )

        else:

            st.success(
                "No unsupported claims detected."
            )

    # -----------------------------------------------------
    # COMPLETENESS
    # -----------------------------------------------------

    completeness_details = get_nested(
        result,
        "completeness",
        "details",
        default={},
    )

    with st.expander(
        "📋 Completeness Evaluation",
        expanded=True,
    ):

        if isinstance(
            completeness_details,
            dict,
        ):

            addressed = (
                completeness_details.get(
                    "addressed",
                    [],
                )
            )

            partial = (
                completeness_details.get(
                    "partial",
                    [],
                )
            )

            missing = (
                completeness_details.get(
                    "missing",
                    [],
                )
            )

            st.markdown(
                "**Addressed**"
            )

            st.write(
                addressed if addressed else "None"
            )

            st.markdown(
                "**Partially Addressed**"
            )

            st.write(
                partial if partial else "None"
            )

            st.markdown(
                "**Missing**"
            )

            st.write(
                missing if missing else "None"
            )

        else:

            st.write(
                completeness_details
            )

    # -----------------------------------------------------
    # RETRIEVED EVIDENCE
    # -----------------------------------------------------

    retrieved_evidence = result.get(
        "retrieved_evidence"
    )

    if retrieved_evidence:

        with st.expander(
            "📚 Retrieved Evidence",
            expanded=False,
        ):

            st.write(
                retrieved_evidence
            )

    # -----------------------------------------------------
    # SUBMISSION ID
    # -----------------------------------------------------

    submission_id = result.get(
        "submission_id"
    )

    if submission_id:

        st.caption(
            f"Submission ID: {submission_id}"
        )


# =========================================================
# PDF REPORT
# =========================================================

def create_pdf_report(
    dashboard_df
):

    pdf_buffer = BytesIO()

    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER
    title_style.fontSize = 20
    title_style.leading = 24

    heading_style = styles["Heading2"]
    heading_style.fontSize = 13
    heading_style.leading = 16
    heading_style.spaceBefore = 8
    heading_style.spaceAfter = 8

    body_style = styles["BodyText"]
    body_style.fontSize = 9
    body_style.leading = 12

    table_text_style = ParagraphStyle(
        "TableText",
        parent=body_style,
        fontSize=8,
        leading=10,
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=body_style,
        fontSize=8,
        leading=10,
        textColor=colors.white,
    )

    story = []

    # =====================================================
    # TITLE
    # =====================================================

    story.append(
        Paragraph(
            "AI Response Validation System",
            title_style,
        )
    )

    story.append(
        Spacer(1, 5)
    )

    story.append(
        Paragraph(
            "Evaluation Scoring Report",
            heading_style,
        )
    )

    story.append(
        Spacer(1, 12)
    )

    # =====================================================
    # NO DATA
    # =====================================================

    if (
        dashboard_df is None
        or dashboard_df.empty
    ):

        story.append(
            Paragraph(
                "No evaluation results are available.",
                body_style,
            )
        )

        document.build(
            story
        )

        return pdf_buffer.getvalue()

    # =====================================================
    # VERDICT COUNTS
    # =====================================================

    total = len(
        dashboard_df
    )

    passed = 0
    needs_improvement = 0
    failed = 0

    for verdict in dashboard_df[
        "verdict"
    ].astype(str):

        verdict_upper = (
            verdict.strip().upper()
        )

        # PASS / VALID
        if (
            "PASS" in verdict_upper
            or verdict_upper == "VALID"
        ):

            passed += 1

        # NEEDS IMPROVEMENT
        elif (
            "NEEDS IMPROVEMENT"
            in verdict_upper
            or "IMPROVEMENT"
            in verdict_upper
            or "IMPROVE"
            in verdict_upper
            or "WARNING"
            in verdict_upper
        ):

            needs_improvement += 1

        # FAIL / BLOCK / REJECT
        elif (
            "FAIL" in verdict_upper
            or "BLOCK" in verdict_upper
            or "REJECT" in verdict_upper
        ):

            failed += 1

    # =====================================================
    # EVALUATION SUMMARY
    # =====================================================

    story.append(
        Paragraph(
            "Evaluation Summary",
            heading_style,
        )
    )

    summary_data = [
        [
            Paragraph(
                "<b>Metric</b>",
                table_header_style,
            ),
            Paragraph(
                "<b>Value</b>",
                table_header_style,
            ),
        ],
        [
            Paragraph(
                "Total Evaluations",
                table_text_style,
            ),
            Paragraph(
                str(total),
                table_text_style,
            ),
        ],
        [
            Paragraph(
                "Passed",
                table_text_style,
            ),
            Paragraph(
                str(passed),
                table_text_style,
            ),
        ],
        [
            Paragraph(
                "Needs Improvement",
                table_text_style,
            ),
            Paragraph(
                str(needs_improvement),
                table_text_style,
            ),
        ],
        [
            Paragraph(
                "Failed",
                table_text_style,
            ),
            Paragraph(
                str(failed),
                table_text_style,
            ),
        ],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[
            300,
            120,
        ],
        repeatRows=1,
    )

    summary_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(
                        "#1f2937"
                    ),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(
        summary_table
    )

    story.append(
        Spacer(1, 18)
    )

    # =====================================================
    # AVERAGE DIMENSION SCORES
    # =====================================================

    avg_relevance = safe_score(
        dashboard_df[
            "relevance_score"
        ].mean()
    )

    avg_accuracy = safe_score(
        dashboard_df[
            "accuracy_score"
        ].mean()
    )

    avg_hallucination = safe_score(
        dashboard_df[
            "hallucination_score"
        ].mean()
    )

    avg_completeness = safe_score(
        dashboard_df[
            "completeness_score"
        ].mean()
    )

    avg_overall = safe_score(
        dashboard_df[
            "overall_score"
        ].mean()
    )

    story.append(
        Paragraph(
            "Dimension Breakdown",
            heading_style,
        )
    )

    dimension_data = [
        [
            Paragraph(
                "<b>Dimension</b>",
                table_header_style,
            ),
            Paragraph(
                "<b>Average Score</b>",
                table_header_style,
            ),
        ],
        [
            Paragraph(
                "Relevance",
                table_text_style,
            ),
            Paragraph(
                f"{avg_relevance * 100:.1f}%",
                table_text_style,
            ),
        ],
        [
            Paragraph(
                "Accuracy",
                table_text_style,
            ),
            Paragraph(
                f"{avg_accuracy * 100:.1f}%",
                table_text_style,
            ),
        ],
        [
            Paragraph(
                "Hallucination Safety",
                table_text_style,
            ),
            Paragraph(
                f"{avg_hallucination * 100:.1f}%",
                table_text_style,
            ),
        ],
        [
            Paragraph(
                "Completeness",
                table_text_style,
            ),
            Paragraph(
                f"{avg_completeness * 100:.1f}%",
                table_text_style,
            ),
        ],
        [
            Paragraph(
                "Overall Score",
                table_text_style,
            ),
            Paragraph(
                f"{avg_overall * 100:.1f}%",
                table_text_style,
            ),
        ],
    ]

    dimension_table = Table(
        dimension_data,
        colWidths=[
            300,
            120,
        ],
        repeatRows=1,
    )

    dimension_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(
                        "#1f2937"
                    ),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(
        dimension_table
    )

    story.append(
        Spacer(1, 18)
    )

    # =====================================================
    # FLAGGED RESPONSES
    # =====================================================

    story.append(
        Paragraph(
            "Flagged Responses",
            heading_style,
        )
    )

    flagged = dashboard_df[
        (
            dashboard_df[
                "overall_score"
            ] < 0.70
        )
        |
        (
            dashboard_df[
                "hallucination_score"
            ] < 0.70
        )
        |
        (
            dashboard_df[
                "verdict"
            ].astype(str).str.contains(
                "FAIL|IMPROVE|BLOCK|REJECT",
                case=False,
                regex=True,
                na=False,
            )
        )
    ].copy()

    if flagged.empty:

        story.append(
            Paragraph(
                "No flagged responses were found.",
                body_style,
            )
        )

    else:

        flagged_data = [
            [
                Paragraph(
                    "<b>Question</b>",
                    table_header_style,
                ),
                Paragraph(
                    "<b>Overall</b>",
                    table_header_style,
                ),
                Paragraph(
                    "<b>Hallucination Safety</b>",
                    table_header_style,
                ),
                Paragraph(
                    "<b>Verdict</b>",
                    table_header_style,
                ),
            ]
        ]

        for _, row in flagged.iterrows():

            question = str(
                row.get(
                    "question",
                    "",
                )
            ).strip()

            if (
                not question
                or question.lower()
                in [
                    "nan",
                    "none",
                    "null",
                    "evaluation",
                ]
            ):
                question = "Question not available"

            overall_value = safe_score(
                row.get(
                    "overall_score",
                    0,
                )
            )

            hallucination_value = safe_score(
                row.get(
                    "hallucination_score",
                    0,
                )
            )

            verdict_value = str(
                row.get(
                    "verdict",
                    "UNKNOWN",
                )
            ).strip()

            flagged_data.append(
                [
                    Paragraph(
                        question,
                        table_text_style,
                    ),
                    Paragraph(
                        f"{overall_value * 100:.1f}%",
                        table_text_style,
                    ),
                    Paragraph(
                        f"{hallucination_value * 100:.1f}%",
                        table_text_style,
                    ),
                    Paragraph(
                        verdict_value,
                        table_text_style,
                    ),
                ]
            )

        flagged_table = Table(
            flagged_data,
            colWidths=[200, 65, 95, 80],
            repeatRows=1,
        )

        flagged_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#1e293b"),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "LEADING",
                        (0, 0),
                        (-1, -1),
                        10,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.HexColor("#cbd5e1"),
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                ]
            )
        )

        story.append(flagged_table)

    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    story.append(
        Paragraph(
            "Recommendations",
            heading_style,
        )
    )

    recommendations = []

    if avg_relevance < 0.70:

        recommendations.append(
            "Improve relevance by ensuring responses directly address the user's question."
        )

    if avg_accuracy < 0.70:

        recommendations.append(
            "Improve accuracy by grounding responses in verified evidence."
        )

    if avg_hallucination < 0.70:

        recommendations.append(
            "Review hallucination-flagged responses and strengthen evidence validation."
        )

    if avg_completeness < 0.70:

        recommendations.append(
            "Improve completeness by covering all important aspects of the question."
        )

    if not recommendations:

        recommendations.append(
            "All average evaluation dimensions are currently above the 0.70 quality threshold."
        )

    for recommendation in recommendations:

        story.append(
            Paragraph(
                "• " + recommendation,
                body_style,
            )
        )

        story.append(
            Spacer(1, 5)
        )

    # =====================================================
    # BUILD PDF
    # =====================================================

    document.build(
        story
    )

    return pdf_buffer.getvalue()

    # -----------------------------------------------------
    # COUNTS
    # -----------------------------------------------------

    total = len(
        dashboard_df
    )

    passed = 0
    needs_improvement = 0
    failed = 0

    for verdict in dashboard_df[
        "verdict"
    ].astype(str):

        verdict_upper = (
            verdict.strip().upper()
        )

        if (
            "PASS" in verdict_upper
            and "BLOCK" not in verdict_upper
            and "FAIL" not in verdict_upper
        ):

            passed += 1

        elif (
            "IMPROVE" in verdict_upper
            or "NEEDS IMPROVEMENT"
            in verdict_upper
        ):

            needs_improvement += 1

        elif (
            "FAIL" in verdict_upper
            or "BLOCK" in verdict_upper
            or "REJECT" in verdict_upper
        ):

            failed += 1

    summary_data = [
        ["Metric", "Value"],
        [
            "Total Evaluations",
            str(total),
        ],
        [
            "Passed",
            str(passed),
        ],
        [
            "Needs Improvement",
            str(needs_improvement),
        ],
        [
            "Failed",
            str(failed),
        ],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[
            250,
            150,
        ],
    )

    summary_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(
                        "#1f2937"
                    ),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    story.append(
        Paragraph(
            "Evaluation Summary",
            heading_style,
        )
    )

    story.append(
        summary_table
    )

    story.append(
        Spacer(1, 15)
    )

    # -----------------------------------------------------
    # DIMENSIONS
    # -----------------------------------------------------

    avg_relevance = dashboard_df[
        "relevance_score"
    ].mean()

    avg_accuracy = dashboard_df[
        "accuracy_score"
    ].mean()

    avg_hallucination = dashboard_df[
        "hallucination_score"
    ].mean()

    avg_completeness = dashboard_df[
        "completeness_score"
    ].mean()

    avg_overall = dashboard_df[
        "overall_score"
    ].mean()

    dimension_data = [
        [
            "Dimension",
            "Average Score",
        ],
        [
            "Relevance",
            f"{avg_relevance:.2f}",
        ],
        [
            "Accuracy",
            f"{avg_accuracy:.2f}",
        ],
        [
            "Hallucination Safety",
            f"{avg_hallucination:.2f}",
        ],
        [
            "Completeness",
            f"{avg_completeness:.2f}",
        ],
        [
            "Overall Score",
            f"{avg_overall:.2f}",
        ],
    ]

    dimension_table = Table(
        dimension_data,
        colWidths=[
            250,
            150,
        ],
    )

    dimension_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(
                        "#1f2937"
                    ),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    story.append(
        Paragraph(
            "Dimension Breakdown",
            heading_style,
        )
    )

    story.append(
        dimension_table
    )

    story.append(
        Spacer(1, 15)
    )

    # -----------------------------------------------------
    # FLAGGED RESPONSES
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "Flagged Responses",
            heading_style,
        )
    )

    flagged = dashboard_df[
        (
            dashboard_df[
                "overall_score"
            ] < 0.70
        )
        |
        (
            dashboard_df[
                "hallucination_score"
            ] < 0.70
        )
        |
        (
            dashboard_df[
                "verdict"
            ].astype(str).str.contains(
                "FAIL|IMPROVE|BLOCK|REJECT",
                case=False,
                regex=True,
                na=False,
            )
        )
    ]

    if flagged.empty:

        story.append(
            Paragraph(
                "No flagged responses were found.",
                body_style,
            )
        )

    else:

        flagged_data = [
            [
                "Question",
                "Overall",
                "Hallucination",
                "Verdict",
            ]
        ]

        for _, row in flagged.iterrows():

            question = str(
                row["question"]
            )

            if len(question) > 60:
                question = (
                    question[:57]
                    + "..."
                )

            flagged_data.append(
                [
                    question,
                    f"{safe_score(row['overall_score']):.2f}",
                    f"{safe_score(row['hallucination_score']):.2f}",
                    str(row["verdict"]),
                ]
            )

        flagged_table = Table(
            flagged_data,
            colWidths=[
                220,
                70,
                80,
                80,
            ],
        )

        flagged_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor(
                            "#1f2937"
                        ),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "PADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                ]
            )
        )

        story.append(
            flagged_table
        )

    story.append(
        Spacer(1, 15)
    )

    # -----------------------------------------------------
    # RECOMMENDATIONS
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "Recommendations",
            heading_style,
        )
    )

    recommendations = []

    if avg_relevance < 0.70:
        recommendations.append(
            "Improve relevance by ensuring responses directly address the question."
        )

    if avg_accuracy < 0.70:
        recommendations.append(
            "Improve accuracy by grounding responses in verified evidence."
        )

    if avg_hallucination < 0.70:
        recommendations.append(
            "Review hallucination-flagged responses and strengthen evidence validation."
        )

    if avg_completeness < 0.70:
        recommendations.append(
            "Improve completeness by covering all important aspects of the question."
        )

    if not recommendations:

        recommendations.append(
            "All average evaluation dimensions are currently above the 0.70 quality threshold."
        )

    for recommendation in recommendations:

        story.append(
            Paragraph(
                "• " + recommendation,
                body_style,
            )
        )

        story.append(
            Spacer(1, 5)
        )

    document.build(
        story
    )

    return pdf_buffer.getvalue()


# =========================================================
# SINGLE EVALUATION
# =========================================================

if (
    st.session_state.selected_mode
    == "Single Evaluation"
):

    st.markdown(
        """
        <div class="page-title">
            📝 Single Evaluation
        </div>

        <div class="page-description">
            Evaluate one AI-generated response against
            available evidence.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-label">INPUT</div>',
        unsafe_allow_html=True,
    )

    question = st.text_area(
        "Question",
        placeholder=(
            "Enter the question being answered..."
        ),
        height=100,
    )

    ai_response = st.text_area(
        "AI Response",
        placeholder=(
            "Enter the AI-generated response..."
        ),
        height=180,
    )

    reference_answer = st.text_area(
        "Reference Answer (Optional)",
        placeholder=(
            "Enter a trusted reference answer if available..."
        ),
        height=130,
    )

    source_document = st.text_area(
        "Source Document (Optional)",
        placeholder=(
            "Paste supporting source material or evidence..."
        ),
        height=180,
    )

    validate_button = st.button(
        "🔍 VALIDATE AI RESPONSE",
        type="primary",
        use_container_width=True,
    )

    if validate_button:

        if not question.strip():

            st.error(
                "Please enter a question."
            )

        elif not ai_response.strip():

            st.error(
                "Please enter the AI response."
            )

        else:

            payload = {
                "question": question,
                "ai_response": ai_response,
                "reference_answer": (
                    reference_answer
                ),
                "source_document": (
                    source_document
                ),
            }

            with st.spinner(
                "Validating AI response..."
            ):

                try:

                    response = requests.post(
                        API_URL,
                        json=payload,
                        timeout=120,
                    )

                    if response.status_code in [
                        200,
                        201,
                    ]:

                        result = response.json()

                        st.session_state.single_result = (
                            result
                        )

                        st.success(
                            "Evaluation completed successfully."
                        )

                    else:

                        st.error(
                            f"API Error: {response.status_code}"
                        )

                        try:

                            st.json(
                                response.json()
                            )

                        except Exception:

                            st.code(
                                response.text
                            )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Could not connect to the backend API. "
                        "Please make sure the FastAPI server is running."
                    )

                except requests.exceptions.Timeout:

                    st.error(
                        "The evaluation request timed out."
                    )

                except Exception as error:

                    st.error(
                        f"Unexpected error: {error}"
                    )

    if st.session_state.single_result:

        st.markdown("---")

        display_single_result(
            st.session_state.single_result
        )


# =========================================================
# BATCH EVALUATION
# =========================================================

elif (
    st.session_state.selected_mode
    == "Batch Evaluation"
):

    st.markdown(
        """
        <div class="page-title">
            📊 Batch Evaluation
        </div>

        <div class="page-description">
            Evaluate multiple question-answer pairs
            from a CSV file.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-label">CSV INPUT</div>',
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"],
        help=(
            "Required columns: question, ai_response. "
            "Optional columns: reference_answer, source_document."
        ),
    )

    st.info(
        "Required columns: question, ai_response\n\n"
        "Optional columns: reference_answer, source_document"
    )

    if uploaded_file is not None:

        try:

            dataframe = pd.read_csv(
                uploaded_file
            )

            required_columns = [
                "question",
                "ai_response",
            ]

            missing_columns = [
                column
                for column in required_columns
                if column not in dataframe.columns
            ]

            if missing_columns:

                st.error(
                    "Missing required columns: "
                    + ", ".join(
                        missing_columns
                    )
                )

            else:

                st.markdown(
                    "### Preview"
                )

                display_dataframe = dataframe.copy()

                score_columns = [
                    "overall_score",
                    "relevance_score",
                    "accuracy_score",
                    "hallucination_score",
                    "completeness_score",
                ]

                for column in score_columns:
                    if column in display_dataframe.columns:
                        display_dataframe[column] = display_dataframe[column].apply(
                            percentage
                        )

                st.dataframe(
                    display_dataframe,
                    use_container_width=True,
                    hide_index=True,
                )
                st.caption(
                    f"{len(dataframe)} row(s) loaded."
                )

                evaluate_csv = st.button(
                    "📊 EVALUATE CSV",
                    type="primary",
                    use_container_width=True,
                )

                if evaluate_csv:

                    results = []

                    progress = st.progress(
                        0
                    )

                    status_text = st.empty()

                    total_rows = len(
                        dataframe
                    )

                    for index, row in dataframe.iterrows():

                        status_text.write(
                            f"Evaluating row "
                            f"{index + 1} of "
                            f"{total_rows}..."
                        )

                        payload = {
                            "question": str(
                                row.get(
                                    "question",
                                    "",
                                )
                            ),

                            "ai_response": str(
                                row.get(
                                    "ai_response",
                                    "",
                                )
                            ),

                            "reference_answer": str(
                                row.get(
                                    "reference_answer",
                                    "",
                                )
                            ),

                            "source_document": str(
                                row.get(
                                    "source_document",
                                    "",
                                )
                            ),
                        }

                        try:

                            response = requests.post(
                                API_URL,
                                json=payload,
                                timeout=120,
                            )

                            if response.status_code in [
                                200,
                                201,
                            ]:

                                result = response.json()

                                results.append(
                                    {
                                        "question": payload[
                                            "question"
                                        ],

                                        "ai_response": payload[
                                            "ai_response"
                                        ],

                                        "overall_score": safe_score(
                                            result.get(
                                                "overall_score",
                                                0,
                                            )
                                        ),

                                        "relevance_score": safe_score(
                                            get_nested(
                                                result,
                                                "relevance",
                                                "score",
                                                default=0,
                                            )
                                        ),

                                        "accuracy_score": safe_score(
                                            get_nested(
                                                result,
                                                "accuracy",
                                                "score",
                                                default=0,
                                            )
                                        ),

                                        "hallucination_score": safe_score(
                                            get_nested(
                                                result,
                                                "hallucination",
                                                "score",
                                                default=0,
                                            )
                                        ),

                                        "completeness_score": safe_score(
                                            get_nested(
                                                result,
                                                "completeness",
                                                "score",
                                                default=0,
                                            )
                                        ),

                                        "verdict": result.get(
                                            "verdict",
                                            "UNKNOWN",
                                        ),
                                    }
                                )

                            else:

                                results.append(
                                    {
                                        "question": payload[
                                            "question"
                                        ],
                                        "ai_response": payload[
                                            "ai_response"
                                        ],
                                        "overall_score": 0,
                                        "relevance_score": 0,
                                        "accuracy_score": 0,
                                        "hallucination_score": 0,
                                        "completeness_score": 0,
                                        "verdict": (
                                            f"API ERROR "
                                            f"{response.status_code}"
                                        ),
                                    }
                                )

                        except Exception as error:

                            results.append(
                                {
                                    "question": payload[
                                        "question"
                                    ],
                                    "ai_response": payload[
                                        "ai_response"
                                    ],
                                    "overall_score": 0,
                                    "relevance_score": 0,
                                    "accuracy_score": 0,
                                    "hallucination_score": 0,
                                    "completeness_score": 0,
                                    "verdict": (
                                        f"ERROR: {error}"
                                    ),
                                }
                            )

                        progress.progress(
                            (index + 1)
                            / total_rows
                        )

                    status_text.empty()

                    # =====================================================
                    # SAVE BATCH RESULTS
                    # =====================================================

                    batch_df = pd.DataFrame(results)

                    # Store results in Streamlit session
                    st.session_state.batch_results = batch_df

                    # Save results permanently so they can be reused
                    # after navigation / dashboard refresh
                    batch_results_path = os.path.join(
                        PROJECT_ROOT,
                        "data",
                        "batch_evaluation_results.csv",
                    )

                    try:
                        batch_df.to_csv(
                            batch_results_path,
                            index=False,
                        )

                        st.success(
                            f"Batch evaluation completed successfully. "
                            f"{len(batch_df)} result(s) generated."
                        )

                    except Exception as error:

                        st.warning(
                            f"Batch evaluation completed, but results "
                            f"could not be saved to CSV: {error}"
                        )

        except Exception as error:

            st.error(
                f"Could not read the CSV file: {error}"
            )

    # =====================================================
    # DISPLAY BATCH RESULTS
    # =====================================================

    if (
        st.session_state.batch_results
        is not None
        and not st.session_state.batch_results.empty
    ):

        st.markdown("---")

        st.markdown(
            "### 📋 Batch Results"
        )

        batch_df = (
            st.session_state.batch_results.copy()
        )

        # Display percentage values
        display_batch_df = batch_df.copy()

        score_columns = [
            "overall_score",
            "relevance_score",
            "accuracy_score",
            "hallucination_score",
            "completeness_score",
        ]

        for column in score_columns:

            if column in display_batch_df.columns:

                display_batch_df[column] = (
                    display_batch_df[column].apply(
                        percentage
                    )
                )

        st.success(
            f"{len(batch_df)} evaluation result(s) available."
        )

        st.dataframe(
            display_batch_df,
            use_container_width=True,
            hide_index=True,
        )

        # -------------------------------------------------
        # DOWNLOAD RESULTS
        # -------------------------------------------------

        csv_data = batch_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download Results CSV",
            data=csv_data,
            file_name=(
                "batch_evaluation_results.csv"
            ),
            mime="text/csv",
            use_container_width=True,
        )

    else:

        st.info(
            "No batch evaluation results are available yet. "
            "Upload a CSV file and click "
            "'📊 EVALUATE CSV'."
        )

        # =====================================================
        # DOWNLOAD BATCH RESULTS
        # =====================================================

        if (
            st.session_state.batch_results is not None
            and not st.session_state.batch_results.empty
        ):

            batch_df = st.session_state.batch_results.copy()

            csv_data = batch_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="⬇️ Download Results CSV",
                data=csv_data,
                file_name="batch_evaluation_results.csv",
                mime="text/csv",
                use_container_width=True,
            )
# =========================================================
# DASHBOARD - MILESTONE 4
# =========================================================

elif (
    st.session_state.selected_mode
    == "Dashboard"
):

    st.markdown(
        """
        <div class="page-title">
            📊 Evaluation Scoring Dashboard
        </div>

        <div class="page-description">
            Monitor evaluation performance, verdicts,
            dimension scores and hallucination safety trends.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =====================================================
    # LOAD RESULTS
    # =====================================================

    stored_results = load_stored_results()

    dashboard_records = []
    
    # -----------------------------------------------------
    # EXTRACTORS
    # -----------------------------------------------------

    def find_value(data, possible_keys):
        if not isinstance(data, dict):
            return None

        # Check the current dictionary first
        for key in possible_keys:
            if key in data:
                value = data[key]

                if value is not None:
                    value_str = str(value).strip()

                    if value_str.lower() not in [
                        "",
                        "none",
                        "null",
                    ]:
                        return value

        # Search nested dictionaries
        for value in data.values():

            if isinstance(value, dict):

                found = find_value(
                    value,
                    possible_keys
                )

                if found is not None:
                    return found

        return None

    def extract_score(
        data,
        dimension,
    ):

        if not isinstance(
            data,
            dict,
        ):
            return 0.0

        dimension_data = data.get(
            dimension
        )

        if isinstance(
            dimension_data,
            dict,
        ):

            score = dimension_data.get(
                "score"
            )

            if score is not None:
                return safe_score(
                    score
                )

        if dimension_data is not None:

            return safe_score(
                dimension_data
            )

        value = find_value(
            data,
            [
                f"{dimension}_score",
                f"{dimension}Score",
            ],
        )

        return safe_score(
            value
        )


    def extract_overall(
        data
    ):

        return safe_score(
            find_value(
                data,
                [
                    "overall_score",
                    "overallScore",
                    "overall",
                ],
            )
        )


    def extract_verdict(
        data
    ):

        value = find_value(
            data,
            [
                "verdict",
                "final_verdict",
                "finalVerdict",
            ],
        )

        if value is None:
            return "UNKNOWN"

        return str(
            value
        ).strip().upper()


    def extract_question(data):
        if not isinstance(data, dict):
            return "Question not available"

        # Question is normally stored directly in the submission
        question = data.get("question")

        if question is not None:
            question = str(question).strip()

            if question.lower() not in [
                "",
                "nan",
                "none",
                "null",
                "evaluation",
            ]:
                return question

        # Check common alternative field names
        for key in ["query", "prompt"]:
            value = data.get(key)

            if value is not None:
                value = str(value).strip()

                if value.lower() not in [
                    "",
                    "nan",
                    "none",
                    "null",
                    "evaluation",
                ]:
                    return value

        # Check retrieved evidence as a final fallback
        retrieved = data.get("retrieved_evidence")

        if isinstance(retrieved, list):
            for item in retrieved:

                if isinstance(item, dict):
                    value = item.get("question")

                    if value is not None:
                        value = str(value).strip()

                        if value.lower() not in [
                            "",
                            "nan",
                            "none",
                            "null",
                            "evaluation",
                        ]:
                            return value

        return "Question not available"

    # -----------------------------------------------------
    # STORED RESULTS
    # -----------------------------------------------------

    for result in stored_results:

        if isinstance(
            result,
            dict,
        ):

            dashboard_records.append(
                {
                    "question": extract_question(
                        result
                    ),

                    "overall_score": extract_overall(
                        result
                    ),

                    "relevance_score": extract_score(
                        result,
                        "relevance",
                    ),

                    "accuracy_score": extract_score(
                        result,
                        "accuracy",
                    ),

                    "hallucination_score": extract_score(
                        result,
                        "hallucination",
                    ),

                    "completeness_score": extract_score(
                        result,
                        "completeness",
                    ),
                    "completeness": result.get(
                        "completeness",
                        {}
                    ),
                    "verdict": extract_verdict(
                        result
                    ),
                }
            )

    # -----------------------------------------------------
    # CURRENT SINGLE RESULT
    # -----------------------------------------------------

    if st.session_state.single_result:

        result = (
            st.session_state.single_result
        )

        dashboard_records.append(
            {
                "question": extract_question(
                    result
                ),

                "overall_score": extract_overall(
                    result
                ),

                "relevance_score": extract_score(
                    result,
                    "relevance",
                ),

                "accuracy_score": extract_score(
                    result,
                    "accuracy",
                ),

                "hallucination_score": extract_score(
                    result,
                    "hallucination",
                ),

                "completeness_score": extract_score(
                    result,
                    "completeness",
                ),

                "verdict": extract_verdict(
                    result
                ),
            }
        )

    # -----------------------------------------------------
    # CURRENT BATCH
    # -----------------------------------------------------

    if (
        st.session_state.batch_results
        is not None
        and not st.session_state.batch_results.empty
    ):

        for _, row in (
            st.session_state.batch_results
            .iterrows()
        ):

            dashboard_records.append(
                {
                    "question": str(
                        row.get(
                            "question",
                            "Batch Evaluation",
                        )
                    ),

                    "overall_score": safe_score(
                        row.get(
                            "overall_score",
                            0,
                        )
                    ),

                    "relevance_score": safe_score(
                        row.get(
                            "relevance_score",
                            0,
                        )
                    ),

                    "accuracy_score": safe_score(
                        row.get(
                            "accuracy_score",
                            0,
                        )
                    ),

                    "hallucination_score": safe_score(
                        row.get(
                            "hallucination_score",
                            0,
                        )
                    ),

                    "completeness_score": safe_score(
                        row.get(
                            "completeness_score",
                            0,
                        )
                    ),
                    "completeness": row.get(
                        "completeness",
                        row.get("completeness_details", {})
                    ),
                    "verdict": str(
                        row.get(
                            "verdict",
                            "UNKNOWN",
                        )
                    ).upper(),
                }
            )

    # -----------------------------------------------------
    # DATAFRAME
    # -----------------------------------------------------

    columns = [
        "question",
        "overall_score",
        "relevance_score",
        "accuracy_score",
        "hallucination_score",
        "completeness_score",
        "verdict",
    ]

    if dashboard_records:

        dashboard_df = pd.DataFrame(
            dashboard_records
        )

        dashboard_df = (
            dashboard_df.drop_duplicates(
                subset=columns,
                keep="last",
            )
        )

    else:

        dashboard_df = pd.DataFrame(
            columns=columns
        )

    # =====================================================
    # REFRESH
    # =====================================================

    refresh_col, _ = st.columns(
        [1, 5]
    )

    with refresh_col:

        if st.button(
            "🔄 Refresh Dashboard",
            use_container_width=True,
        ):

            st.rerun()

    # =====================================================
    # NO DATA
    # =====================================================

    if dashboard_df.empty:

        st.markdown(
            "### 📊 Evaluation Overview"
        )

        cols = st.columns(4)

        empty_values = [
            ("Total Evaluations", 0),
            ("Passed", 0),
            ("Needs Improvement", 0),
            ("Failed", 0),
        ]

        for column, (
            label,
            value,
        ) in zip(
            cols,
            empty_values,
        ):

            with column:

                st.metric(
                    label,
                    value,
                )

        st.markdown(
            "### 📈 Average Dimension Scores"
        )

        cols = st.columns(4)

        for column, label in zip(
            cols,
            [
                "Relevance",
                "Accuracy",
                "Hallucination Safety",
                "Completeness",
            ],
        ):

            with column:

                st.metric(
                    label,
                    "0.00",
                )

        st.info(
            "No evaluation results are available yet. "
            "Run a Single Evaluation or Batch Evaluation first."
        )

    # =====================================================
    # DASHBOARD WITH DATA
    # =====================================================

    else:

        total_evaluations = len(
            dashboard_df
        )
        # -------------------------------------------------
        # COMPLETENESS / MISSING INFORMATION STATISTICS
        # -------------------------------------------------

        missing_evaluation_count = 0
        total_missing_aspects = 0
        total_partial_aspects = 0

        for record in dashboard_records:

            completeness = record.get(
                "completeness",
                {}
            )

            if not isinstance(completeness, dict):
                continue

            details = completeness.get(
                "details",
                {}
            )

            if not isinstance(details, dict):
                continue

            missing_aspects = details.get(
                "missing_aspects",
                []
            )

            partial_aspects = details.get(
                "partially_addressed_aspects",
                []
            )

            if not isinstance(missing_aspects, list):
                missing_aspects = []

            if not isinstance(partial_aspects, list):
                partial_aspects = []

            valid_missing = [
                str(item).strip()
                for item in missing_aspects
                if str(item).strip().lower()
                not in ["", "nan", "none", "null"]
            ]

            valid_partial = [
                str(item).strip()
                for item in partial_aspects
                if str(item).strip().lower()
                not in ["", "nan", "none", "null"]
            ]

            if valid_missing:
                missing_evaluation_count += 1

            total_missing_aspects += len(
                valid_missing
            )

            total_partial_aspects += len(
                valid_partial
            )

        
        # -------------------------------------------------
        # VERDICT COUNTS
        # -------------------------------------------------
        passed = 0
        needs_improvement = 0
        failed = 0
        
        for verdict in dashboard_df[
            "verdict"
        ].astype(str):

            verdict_upper = (
                verdict.strip().upper()
            )

            # PASS
            if (
                "PASS" in verdict_upper
                or verdict_upper == "VALID"
            ):

                passed += 1

            # NEEDS IMPROVEMENT
            elif (
                "NEEDS IMPROVEMENT"
                in verdict_upper
                or "IMPROVEMENT"
                in verdict_upper
                or "IMPROVE"
                in verdict_upper
                or "WARNING"
                in verdict_upper
            ):

                needs_improvement += 1

            # FAIL
            elif (
                "FAIL" in verdict_upper
                or "BLOCK" in verdict_upper
                or "REJECT" in verdict_upper
            ):

                
                failed += 1

        # -------------------------------------------------
        # EVALUATION OVERVIEW
        # -------------------------------------------------

        st.markdown(
            "### 📊 Evaluation Overview"
        )

        cols = st.columns(4)

        overview = [

            (
                "Total Evaluations",
                total_evaluations,
            ),

            (
                "Passed",
                f"{passed} ({(passed / total_evaluations * 100):.1f}%)",
            ),

            (
                "Needs Improvement",
                f"{needs_improvement} ({(needs_improvement / total_evaluations * 100):.1f}%)",
            ),

            (
                "Failed",
                f"{failed} ({(failed / total_evaluations * 100):.1f}%)",
            ),

        ]

        for column, (
            label,
            value,
        ) in zip(
            cols,
            overview,
        ):

            with column:

                st.metric(
                    label,
                    value,
                )

        # -------------------------------------------------
        # AVERAGE DIMENSION SCORES
        # -------------------------------------------------

        avg_relevance = dashboard_df[
            "relevance_score"
        ].mean()

        avg_accuracy = dashboard_df[
            "accuracy_score"
        ].mean()

        avg_hallucination = dashboard_df[
            "hallucination_score"
        ].mean()

        avg_completeness = dashboard_df[
            "completeness_score"
        ].mean()

        st.markdown(
            "### 📈 Average Dimension Scores"
        )

        cols = st.columns(4)

        averages = [
            (
                "Relevance",
                avg_relevance,
            ),
            (
                "Accuracy",
                avg_accuracy,
            ),
            (
                "Hallucination Safety",
                avg_hallucination,
            ),
            (
                "Completeness",
                avg_completeness,
            ),
        ]

        for column, (
            label,
            value,
        ) in zip(
            cols,
            averages,
        ):

            with column:

                st.metric(
                    label,
                    percentage(value),
                )    

        
        # -------------------------------------------------
        # SCORE DISTRIBUTION
        # -------------------------------------------------

        st.markdown("### 📊 Score Distribution")

        distribution_data = pd.DataFrame(
            {
                "Relevance": dashboard_df["relevance_score"],
                "Accuracy": dashboard_df["accuracy_score"],
                "Hallucination Safety": dashboard_df["hallucination_score"],
                "Completeness": dashboard_df["completeness_score"],
            }
        )

        distribution_data = distribution_data * 100

        st.bar_chart(
            distribution_data,
            height=350,
            use_container_width=True,
        )
        # -------------------------------------------------
        # VERDICT DISTRIBUTION
        # -------------------------------------------------

        st.markdown(
            "### 🎯 Verdict Distribution"
        )

        verdict_chart = pd.DataFrame(
            {
                "Passed": [passed],
                "Needs Improvement": [
                    needs_improvement
                ],
                "Failed": [failed],
            }
        )

        st.bar_chart(
            verdict_chart,
            use_container_width=True,
        )

        # -------------------------------------------------
        # HALLUCINATION STATISTICS
        # -------------------------------------------------

        hallucination_scores = (
            dashboard_df[
                "hallucination_score"
            ]
        )

        hallucination_safe = int(
            (
                hallucination_scores
                >= 0.70
            ).sum()
        )

        hallucination_flagged = int(
            (
                hallucination_scores
                < 0.70
            ).sum()
        )

        hallucination_average = (
            hallucination_scores.mean()
        )

        # -------------------------------------------------
        # HALLUCINATION SAFETY STATISTICS
        # -------------------------------------------------

        st.markdown(
            "### 🛡️ Hallucination Safety Statistics"
        )

        cols = st.columns(3)

        hallucination_metrics = [
            (
                "Average Safety",
                percentage(hallucination_average),
            ),
            (
                "Safe Evaluations",
                hallucination_safe,
            ),
            (
                "Flagged Evaluations",
                hallucination_flagged,
            ),
        ]

        for column, (
            label,
            value,
        ) in zip(
            cols,
            hallucination_metrics,
        ):

            with column:

                st.metric(
                    label,
                    value,
                )


        # -------------------------------------------------
        # MISSING / INCOMPLETE INFORMATION STATISTICS
        # -------------------------------------------------

        st.markdown(
            "### ⚠️ Missing / Incomplete Information"
        )

        missing_evaluation_count = 0
        total_missing_aspects = 0
        total_partial_aspects = 0

        for record in dashboard_records:

            completeness = record.get(
                "completeness",
                {}
            )

            details = completeness.get(
                "details",
                {}
            )

            missing_aspects = details.get(
                "missing_aspects",
                []
            )

            partial_aspects = details.get(
                "partially_addressed_aspects",
                []
            )

            valid_missing = [
                str(item).strip()
                for item in missing_aspects
                if str(item).strip()
                and str(item).strip().lower()
                not in ["nan", "none", "null"]
            ]

            valid_partial = [
                str(item).strip()
                for item in partial_aspects
                if str(item).strip()
                and str(item).strip().lower()
                not in ["nan", "none", "null"]
            ]

            if valid_missing:

                missing_evaluation_count += 1

            total_missing_aspects += len(
                valid_missing
            )

            total_partial_aspects += len(
                valid_partial
            )

        missing_stats = [
            (
                "Evaluations With Missing Information",
                missing_evaluation_count,
            ),
            (
                "Total Missing Aspects",
                total_missing_aspects,
            ),
            (
                "Partially Addressed Aspects",
                total_partial_aspects,
            ),
        ]

        missing_cols = st.columns(3)

        for index, (
            label,
            value,
        ) in enumerate(
            missing_stats
        ):

            with missing_cols[index]:

                st.metric(
                    label,
                    value,
                )

        # -------------------------------------------------
        # HALLUCINATION TREND
        # -------------------------------------------------

        st.markdown(
            "### 📉 Hallucination Safety Trend"
        )

        trend_df = pd.DataFrame(
            {
                "Evaluation": range(
                    1,
                    len(
                        hallucination_scores
                    ) + 1,
                ),

                "Hallucination Safety": (
                    hallucination_scores
                    .tolist()
                ),
            }
        )

        if len(trend_df) > 1:

            st.line_chart(
                trend_df.set_index(
                    "Evaluation"
                ),
                use_container_width=True,
            )

        else:

            st.info(
                "Run more evaluations to display "
                "the hallucination safety trend."
            )

        # -------------------------------------------------
        # FLAGGED RESPONSES
        # -------------------------------------------------
        st.markdown(
            "### ⚠️ Flagged Responses"
        )

        flagged_df = dashboard_df[
            (
                dashboard_df["hallucination_score"] < 0.70
            )
            |
            (
                dashboard_df["overall_score"] < 0.70
            )
            |
            (
                dashboard_df["verdict"]
                .astype(str)
                .str.contains(
                    "FAIL|IMPROVE|BLOCK|REJECT",
                    case=False,
                    regex=True,
                    na=False,
                )
            )
        ].copy()


        if flagged_df.empty:

            st.success(
                "✅ No flagged responses found."
            )

        else:

            st.warning(
                f"⚠️ {len(flagged_df)} flagged response(s) require attention."
            )

            display_flagged = flagged_df[
                [
                    "question",
                    "overall_score",
                    "hallucination_score",
                    "verdict",
                ]
            ].copy()

            # Convert scores to percentages
            display_flagged[
                "overall_score"
            ] = (
                display_flagged[
                    "overall_score"
                ] * 100
            ).round(1)

            display_flagged[
                "hallucination_score"
            ] = (
                display_flagged[
                    "hallucination_score"
                ] * 100
            ).round(1)

            # Rename columns for a cleaner dashboard
            display_flagged = display_flagged.rename(
                columns={
                    "question": "Question",
                    "overall_score": "Overall Score (%)",
                    "hallucination_score": "Hallucination Safety (%)",
                    "verdict": "Verdict",
                }
            )

            st.dataframe(
                display_flagged,
                use_container_width=True,
                hide_index=True,
            )
        

       
        # -------------------------------------------------
        # RECENT RESULTS
        # -------------------------------------------------
        
        st.markdown(
            "### 📝 Recent Evaluation Results"
        )

        recent_df = dashboard_df.tail(
            10
        ).copy()

        score_columns = [
            "overall_score",
            "relevance_score",
            "accuracy_score",
            "hallucination_score",
            "completeness_score",
        ]

        for column in score_columns:

            recent_df[column] = (
                recent_df[column]
                .round(2)
            )

        recent_display = recent_df[
            [
                "question",
                "overall_score",
                "relevance_score",
                "accuracy_score",
                "hallucination_score",
                "completeness_score",
                "verdict",
            ]
        ].copy()

        recent_display["overall_score"] = (
            recent_display["overall_score"] * 100
        ).round(1)

        recent_display["relevance_score"] = (
            recent_display["relevance_score"] * 100
        ).round(1)

        recent_display["accuracy_score"] = (
            recent_display["accuracy_score"] * 100
        ).round(1)

        recent_display["hallucination_score"] = (
            recent_display["hallucination_score"] * 100
        ).round(1)

        recent_display["completeness_score"] = (
            recent_display["completeness_score"] * 100
        ).round(1)

        recent_display = recent_display.rename(
            columns={
                "question": "Question",
                "overall_score": "Overall Score (%)",
                "relevance_score": "Relevance (%)",
                "accuracy_score": "Accuracy (%)",
                "hallucination_score": "Hallucination Safety (%)",
                "completeness_score": "Completeness (%)",
                "verdict": "Verdict",
            }
        )

        st.dataframe(
            recent_display,
            use_container_width=True,
            hide_index=True,
        )

        # -------------------------------------------------
        # RECOMMENDATIONS
        # -------------------------------------------------

        st.markdown(
            "### 💡 Recommendations"
        )

        recommendations = []

        if avg_relevance < 0.70:

            recommendations.append(
                "Improve relevance by ensuring responses directly address the user's question."
            )

        if avg_accuracy < 0.70:

            recommendations.append(
                "Improve accuracy by grounding responses in verified evidence."
            )

        if avg_hallucination < 0.70:

            recommendations.append(
                "Review hallucination-flagged responses and strengthen evidence validation."
            )

        if avg_completeness < 0.70:

            recommendations.append(
                "Improve completeness by covering all important aspects of the question."
            )

        if not recommendations:

            st.success(
                "All average evaluation dimensions are currently "
                "above the 0.70 quality threshold."
            )

        else:

            for recommendation in recommendations:

                st.warning(
                    recommendation
                )

        # -------------------------------------------------
        # PDF EXPORT
        # -------------------------------------------------

        st.markdown(
            "### 📄 Export Evaluation Report"
        )

        st.caption(
            "Generate a structured PDF containing "
            "evaluation summaries, dimension scores, "
            "flagged responses and recommendations."
        )

        if st.button(
            "📄 Generate PDF Report",
            use_container_width=True,
        ):

            try:

                pdf_data = create_pdf_report(
                    dashboard_df
                )

                st.download_button(
                    label="⬇️ Download PDF Report",
                    data=pdf_data,
                    file_name=(
                        "AI_Response_Validation_Milestone4_Report.pdf"
                    ),
                    mime="application/pdf",
                    use_container_width=True,
                )

                st.success(
                    "PDF report generated successfully."
                )

            except Exception as error:

                st.error(
                    f"Unable to generate PDF report: {error}"
                )