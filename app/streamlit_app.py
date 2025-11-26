# app/streamlit_app.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pdfplumber
from dotenv import load_dotenv

# Load .env (optional)
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# Orchestrator
from agents.orchestrator import Orchestrator
from memory.session_service import SessionService

st.set_page_config(page_title="AI Medical Summary Assistant", layout="wide")
st.title("🩺 AI Medical Summary Assistant")

st.markdown("**Disclaimer:** Educational tool — not a medical diagnosis. Consult a clinician.")

tab1, tab2 = st.tabs(["📄 Report Summarizer", "💬 Assistant Chat (post-summary)"])

# Shared session state
if "final_summary" not in st.session_state:
    st.session_state.final_summary = None
if "interpreted" not in st.session_state:
    st.session_state.interpreted = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with tab1:
    sex = st.selectbox("Sex", ["all", "male", "female"], index=0)
    uploaded = st.file_uploader("Upload PDF (optional)", type=["pdf"])
    text_input = st.text_area("Or paste report text here", height=300)

    # if PDF uploaded, extract text
    if uploaded is not None and not text_input.strip():
        try:
            with pdfplumber.open(uploaded) as pdf:
                pages = [p.extract_text() or "" for p in pdf.pages]
                text_input = "\n".join(pages)
        except Exception as e:
            st.error(f"Failed to read PDF: {e}")

    if st.button("Analyze Report"):
        if not text_input.strip():
            st.warning("Please paste text or upload a PDF.")
        else:
            # choose mode (offline default)
            mode = "offline"
            orch = Orchestrator(mode=mode)
            with st.spinner("Running multi-agent pipeline..."):
                out = orch.run_pipeline(text_input, sex=sex)
            st.session_state.final_summary = out["safe_summary"]
            st.session_state.interpreted = out["interpreted"]

            # show results
            st.subheader("Parameter Summary")
            for it in out["interpreted"]:
                st.markdown(f"**{it.get('name')}** — **{it.get('status').upper()}**")
                st.write(it.get("explanation"))

            st.subheader("Recommendations")
            for r in out["recommendations"]:
                st.write(f"• {r}")

            st.subheader("Safe Final Summary")
            st.text(out["safe_summary"])

            # save to session memory
            session = SessionService()
            saved = session.save_report({
                "summary": out["safe_summary"],
                "interpreted": out["interpreted"],
                "recommendations": out["recommendations"]
            })
            st.success(f"Saved session to {saved}")

with tab2:
    st.subheader("Medical Assistant (ask follow-up questions)")
    if st.session_state.final_summary is None:
        st.info("Please analyze a report in the 'Report Summarizer' tab first.")
    else:
        for msg in st.session_state.chat_history:
            role = "You" if msg["role"] == "user" else "Assistant"
            st.markdown(f"**{role}**: {msg['text']}")

        user_q = st.text_input("Ask a question about the summary")
        if st.button("Send"):
            if not user_q.strip():
                st.warning("Enter a question first")
            else:
                # Simple offline reply: echo summary + short answer using naive rules
                st.session_state.chat_history.append({"role":"user","text":user_q})
                # here we provide a simple rule-based answer (you can plug-in ADK/Gemini)
                answer = f"Based on the summary: {st.session_state.final_summary.splitlines()[0][:200]}... For medical decisions, consult a clinician."
                st.session_state.chat_history.append({"role":"assistant","text":answer})
                st.experimental_rerun()
