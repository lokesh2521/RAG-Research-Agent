# RAG Research Agent - Starter Repo

This repository contains a ready-to-use skeleton for a Retrieval-Augmented Generation (RAG) research agent that:
- ingests local documents (Markdown/PDF),
- chunks and embeds them,
- stores embeddings in a FAISS index,
- runs a planning → retrieve → summarize → synthesize pipeline,
- and returns a traceable, citation-linked report.

## Repo structure
```
rag-research-agent/
├─ sample_docs/
│  ├─ quantum_intro.md
│  ├─ cyber_case_study.md
├─ src/
│  ├─ utils.py
│  ├─ ingest.py
│  ├─ build_index.py
│  ├─ query_pipeline.py
│  ├─ app_streamlit.py
│  └─ templates.py
├─ outputs/
│  ├─ (index files created after running build_index)
├─ .env.example
├─ requirements.txt
└─ README.md
```

## Quick start (step-by-step)

1. Create a Python virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Put your local docs into `sample_docs/` (Markdown or PDF). Two example markdown files are already included.
4. Build the FAISS index:
   ```bash
   python src/build_index.py
   ```
   This will create `outputs/index.faiss` and `outputs/index_meta.json`.
5. Run a test query:
   ```bash
   python src/query_pipeline.py
   ```
   Or run the Streamlit demo:
   ```bash
   streamlit run src/app_streamlit.py
   ```

## Files to edit
- `src/templates.py` — tweak prompt templates for planner/summarizer.
- `.env` — add `OPENAI_API_KEY` if you want to use OpenAI for planning/summarization.

## Notes
- If you don't have OpenAI API access, the repo uses `sentence-transformers` for embeddings and a simple local summarizer fallback.
- To convert `.md` to `.pdf`, you can use `pandoc` or print-to-PDF from editors.

## Demo video checklist
- Show repo layout.
- Run `python src/build_index.py` and explain it.
- Run a query via `python src/query_pipeline.py` or Streamlit and show the plan, retrieved evidence, and final report.
- Explain how citations map back to original documents.

Enjoy — if you want, I can also:
- create a `.env` template with placeholders,
- pre-build the index and include `outputs/index.faiss` (if you want a fully runnable zip),
- or convert the markdown sample documents into PDFs for you.
