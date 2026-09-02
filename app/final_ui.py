import streamlit as st
import requests

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Response Validation System",
    page_icon="🛡️",
    layout="wide"
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #0b0f17;
}

.block-container {
    max-width: 1200px;
    padding-top: 30px;
}

.title {
    text-align: center;
    font-size: 38px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: #9ca3af;
    font-size: 16px;
    margin-bottom: 35px;
}

.section-title {
    font-size: 24px;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 15px;
}

.card {
    background-color: #111827;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #273244;
    margin-bottom: 20px;
}

.metric-card {
    background-color: #111827;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #273244;
    text-align: center;
}

.metric-title {
    color: #9ca3af;
    font-size: 14px;
}

.metric-value {
    font-size: 32px;
    font-weight: bold;
    margin-top: 8px;
}

.verdict {
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    font-size: 26px;
    font-weight: bold;
    margin: 20px 0;
}

.valid {
    background-color: #102a1b;
    border: 1px solid #22c55e;
    color: #4ade80;
}

.invalid {
    background-color: #2a1212;
    border: 1px solid #ef4444;
    color: #f87171;
}

.analysis {
    background-color: #111827;
    border: 1px solid #273244;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 12px;
}

.footer {
    text-align: center;
    color: #6b7280;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    '<div class="title">🛡️ AI Response Validation System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Validate • Verify • Detect Hallucinations • Explain AI Responses'
    '</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# Input Section
# --------------------------------------------------

st.markdown(
    '<div class="section-title">📝 Input Response</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        '<div class="card"><b>📝 User Question</b></div>',
        unsafe_allow_html=True
    )

    question = st.text_area(
        "User Question",
        placeholder="Example: What is photosynthesis?",
        height=150,
        label_visibility="collapsed"
    )

with col2:

    st.markdown(
        '<div class="card"><b>🤖 AI Generated Response</b></div>',
        unsafe_allow_html=True
    )

    ai_response = st.text_area(
        "AI Generated Response",
        placeholder="Enter the AI-generated answer here...",
        height=150,
        label_visibility="collapsed"
    )

# --------------------------------------------------
# Reference / Evidence
# --------------------------------------------------

st.markdown(
    '<div class="section-title">📚 Reference / Evidence</div>',
    unsafe_allow_html=True
)

reference = st.text_area(
    "Reference / Evidence",
    placeholder="Enter trusted reference information or source evidence...",
    height=120,
    label_visibility="collapsed"
)

# --------------------------------------------------
# Validate Button
# --------------------------------------------------

st.markdown("")

validate = st.button(
    "🔍 VALIDATE AI RESPONSE",
    type="primary",
    use_container_width=True
)

# --------------------------------------------------
# API Request
# --------------------------------------------------

if validate:

    if not question.strip():
        st.error("Please enter the User Question.")

    elif not ai_response.strip():
        st.error("Please enter the AI Generated Response.")

    else:

        payload = {
            "question": question,
            "ai_response": ai_response,
            "reference_answer": reference if reference.strip() else None,
            "source_document": reference if reference.strip() else None
        }

        API_URL = "http://127.0.0.1:8000/api/v1/evaluate"

        with st.spinner(
            "Checking relevance, hallucination and completeness..."
        ):

            try:

                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=120
                )

                if response.status_code == 201:

                    result = response.json()

                    st.success(
                        "Evaluation Completed Successfully!"
                    )

                    # ------------------------------------------
                    # Validation Results
                    # ------------------------------------------

                    st.markdown(
                        '<div class="section-title">'
                        '📊 Validation Results'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    scores = result.get("scores", {})

                    relevance = float(
                        scores.get("relevance", 0)
                    )

                    hallucination = float(
                        scores.get("hallucination", 0)
                    )

                    completeness = float(
                        scores.get("completeness", 0)
                    )

                    overall = (
                        relevance +
                        hallucination +
                        completeness
                    ) / 3

                    # ------------------------------------------
                    # Verdict
                    # ------------------------------------------

                    if overall >= 0.70:

                        st.markdown(
                            f"""
                            <div class="verdict valid">
                                🟢 RESPONSE VALID<br>
                                <span style="font-size:16px;">
                                Overall Score: {overall * 100:.1f}%
                                </span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    else:

                        st.markdown(
                            f"""
                            <div class="verdict invalid">
                                🔴 POSSIBLE HALLUCINATION<br>
                                <span style="font-size:16px;">
                                Overall Score: {overall * 100:.1f}%
                                </span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    # ------------------------------------------
                    # Score Cards
                    # ------------------------------------------

                    c1, c2, c3 = st.columns(3)

                    with c1:

                        st.markdown(
                            f"""
                            <div class="metric-card">
                                <div class="metric-title">
                                    🎯 RELEVANCE
                                </div>
                                <div class="metric-value">
                                    {relevance * 100:.1f}%
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with c2:

                        st.markdown(
                            f"""
                            <div class="metric-card">
                                <div class="metric-title">
                                    🛡️ HALLUCINATION SAFETY
                                </div>
                                <div class="metric-value">
                                    {hallucination * 100:.1f}%
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with c3:

                        st.markdown(
                            f"""
                            <div class="metric-card">
                                <div class="metric-title">
                                    📋 COMPLETENESS
                                </div>
                                <div class="metric-value">
                                    {completeness * 100:.1f}%
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    # ------------------------------------------
                    # Hallucination Analysis
                    # ------------------------------------------

                    st.markdown(
                        '<div class="section-title">'
                        '🔎 Hallucination Analysis'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    hallucination_reason = result.get(
                        "reasoning", {}
                    ).get(
                        "hallucination",
                        "No explanation available."
                    )

                    if hallucination >= 0.70:

                        st.markdown(
                            f"""
                            <div class="analysis">
                                <h3>✓ RESPONSE GROUNDED</h3>
                                <p>
                                The response is sufficiently
                                supported by the available context.
                                </p>
                                <b>Agent Explanation:</b>
                                <p>{hallucination_reason}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    else:

                        st.markdown(
                            f"""
                            <div class="analysis">
                                <h3>⚠ POSSIBLE HALLUCINATION</h3>
                                <p>
                                Some information in the response
                                may not be sufficiently supported
                                by the available evidence.
                                </p>
                                <b>Agent Explanation:</b>
                                <p>{hallucination_reason}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    # ------------------------------------------
                    # Validation Explanations
                    # ------------------------------------------

                    st.markdown(
                        '<div class="section-title">'
                        '💡 Validation Explanations'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    reasoning = result.get(
                        "reasoning", {}
                    )

                    st.markdown(
                        f"""
                        <div class="analysis">
                            <b>🎯 Relevance — {relevance * 100:.1f}%</b>
                            <p>
                            {reasoning.get(
                                "relevance",
                                "No explanation available."
                            )}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"""
                        <div class="analysis">
                            <b>🛡️ Hallucination /
                            Grounding — {hallucination * 100:.1f}%</b>
                            <p>
                            {reasoning.get(
                                "hallucination",
                                "No explanation available."
                            )}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"""
                        <div class="analysis">
                            <b>📋 Completeness —
                            {completeness * 100:.1f}%</b>
                            <p>
                            {reasoning.get(
                                "completeness",
                                "No explanation available."
                            )}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # ------------------------------------------
                    # Audited Response
                    # ------------------------------------------

                    st.markdown(
                        '<div class="section-title">'
                        '📄 Audited Response'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"""
                        <div class="analysis">
                            <b>Question:</b>
                            <p>{question}</p>

                            <b>AI Response:</b>
                            <p>{ai_response}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.caption(
                        "Validation Record ID: "
                        + result.get(
                            "submission_id",
                            "N/A"
                        )
                    )

                else:

                    st.error(
                        f"Server Error: {response.text}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to FastAPI backend."
                )

                st.info(
                    "Start the backend using:\n\n"
                    "uvicorn app.main:app --reload"
                )

            except Exception as e:

                st.error(
                    f"Unexpected error: {e}"
                )

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown(
    '<div class="footer">'
    'AI Response Validation System | '
    'Relevance • Hallucination Detection • Completeness'
    '</div>',
    unsafe_allow_html=True
)
