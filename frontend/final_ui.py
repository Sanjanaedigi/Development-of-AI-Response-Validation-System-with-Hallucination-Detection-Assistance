import requests
import streamlit as st

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

                if verdict == "VALID":

                    st.success(
                        f"🟢 ALL FILTERS PASSED | "
                        f"Overall Score: "
                        f"{data['overall_score'] * 100:.1f}%"
                    )

                else:

                    st.error(
                        f"🔴 FILTER BLOCKED | "
                        f"Overall Score: "
                        f"{data['overall_score'] * 100:.1f}%"
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