import os
import sys
import streamlit as st

# --- Ensure src/ is on the Python path ---
# This makes imports work whether you run from project root or src/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.query_pipeline import run_pipeline   # ✅ import works now

# --- Streamlit UI ---
st.set_page_config(page_title="RAG Research Agent", layout="wide")

st.title("📑 Multi-Document Research Agent")
st.write("Ask a research question and let the pipeline plan, retrieve, summarize, and synthesize a report.")

query = st.text_area("Enter your research question:", height=100)

if st.button("Run Research"):
    if not query.strip():
        st.warning("⚠️ Please enter a research question first.")
    else:
        with st.spinner("Running research pipeline..."):
            try:
                result = run_pipeline(query, top_k=4)

                st.subheader("Research Report")
                st.markdown(result["report_md"])

                st.subheader("Step Summaries")
                for i, step in enumerate(result["step_summaries"]):
                    with st.expander(f"Step {i+1}: {step['step']}"):
                        st.markdown(step["summary"])

                st.subheader("Sources")
                for src, v in result["citations"].items():
                    st.write(f"- {v['source']} (page {v['page']})")

            except Exception as e:
                st.error(f"Pipeline failed: {e}")
