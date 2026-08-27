import streamlit as st
import requests

st.set_page_config(page_title="Multi-Agent Validation Funnel", layout="wide")
st.title("🛡️ Multi-Agent Validation Funnel Engine")

left_panel, right_panel = st.columns(2)

with left_panel:
    st.subheader("📥 Audit Submission Ingestion Panel")
    q = st.text_input("User Question")
    ans = st.text_area("AI Response to Audit")
    
    with st.expander("🔍 Optional Context Materials"):
        ref = st.text_input("Reference Gold Answer")
        doc = st.text_area("Source Evidence text snippet")

    if st.button("🚀 Run Sequenced Pipeline Funnel", use_container_width=True):
        if not q or not ans:
            st.error("Question and AI response values are mandatory entries.")
        else:
            with st.spinner("Executing filtering steps across LangGraph routing states..."):
                payload = {"question": q, "ai_response": ans, "reference_answer": ref, "source_document": doc}
                try:
                    res = requests.post("http://127.0.0", json=payload)
                    if res.status_code == 201:
                        st.session_state["pipeline_results"] = res.json()
                        st.success("Analysis Complete!")
                    else:
                        st.error(f"API Connection Exception flag error code: {res.status_code}")
                except Exception as e:
                    st.error(f"Cannot communicate with backend server: {e}")

with right_panel:
    st.subheader("📊 Funnel Reports & Telemetry Views")
    if "pipeline_results" in st.session_state:
        data = st.session_state["pipeline_results"]
        
        status_flag = data["verdict"]
        if "🟢" in status_flag:
            st.success(f"### Verdict: {status_flag}")
        else:
            st.error(f"### Verdict: {status_flag}")
            
        st.caption(f"**Audit Record Reference Identification Guid Token:** {data['submission_id']}")
        
        for metric, score in data["scores"].items():
            st.metric(label=f"🎯 Metric: {metric.upper()}", value=f"{score*100:.1f} %")
            st.write(f"*Agent Justification Summary:* {data['reasoning'].get(metric)}")
            st.divider()
    else:
        st.info("Awaiting task configuration pipeline logs run execution triggers.")
