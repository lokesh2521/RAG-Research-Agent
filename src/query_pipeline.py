# query_pipeline.py - plan -> retrieve -> summarize -> synthesize
import os, json, numpy as np, faiss
from sentence_transformers import SentenceTransformer
import sys
sys.path.append(os.path.dirname(__file__))
from pathlib import Path

INDEX_PATH = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'index.faiss')
META_PATH = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'index_meta.json')
MODEL_LOCAL = 'all-MiniLM-L6-v2'

# Load index & meta (ensure build_index.py has been run)
index = None
meta = None
if not os.path.exists(INDEX_PATH) or not os.path.exists(META_PATH):
    print('Index or metadata not found. Run `python src/build_index.py` first to create the index.')
else:
    index = faiss.read_index(os.path.abspath(INDEX_PATH))
    meta = json.load(open(META_PATH, 'r', encoding='utf-8'))

embedder = SentenceTransformer(MODEL_LOCAL)

def embed_query(q:str) -> np.ndarray:
    v = embedder.encode([q], convert_to_numpy=True)
    faiss.normalize_L2(v)
    return v

def retrieve(query:str, k=5):
    if index is None or meta is None:
        raise ValueError("FAISS index or metadata not loaded. Run `build_index.py` first.")
    
    v = embed_query(query)
    D, I = index.search(v, k)
    results = []
    for score, idx in zip(D[0].tolist(), I[0].tolist()):
        if idx < 0: continue
        chunk = meta[idx]
        results.append({
            "score": float(score),
            "chunk": chunk
        })
    return results

# --- Local fallback plan (no LLM) ---
def create_plan(query: str):
    return [
        "Provide a short overview and definition.",
        "Explain the effects/impacts on the domain (risks and changes).",
        "List mitigation strategies and best practices.",
        "Give practical examples or case studies and resources."
    ]

def summarize_step(step:str, retrieved):
    ctx_parts = []
    evidence = []
    for r in retrieved:
        ch = r["chunk"]
        ctx_parts.append(f"Source: {ch['source']} (page {ch['page']})\n{ch['text']}")
        evidence.append({"source": ch['source'], "page": ch['page'], "chunk_index": ch['chunk_index']})
    
    sentences = []
    for p in ctx_parts:
        sents = [s.strip() for s in p.split('. ') if len(s.strip())>50]
        sentences.extend(sents)
    
    summary_text = "\n".join(sentences[:6])
    summary_text += "\n\n[NOTE] Local summarizer fallback used (no OpenAI key)."

    return {
        "step": step,
        "summary": summary_text,
        "evidence": evidence
    }

def synthesize_report(query:str, step_summaries):
    md = [f"# Research Report: {query}\n"]
    citations = {}
    for i, s in enumerate(step_summaries):
        md.append(f"## Step {i+1}: {s['step']}\n")
        md.append(s['summary'] + "\n")
        for e in s['evidence']:
            key = f"{e['source']}:page{e['page']}"
            citations[key] = {"source": e['source'], "page": e['page']}

    md.append("\n## Sources and Evidence\n")
    for k,v in citations.items():
        md.append(f"- {v['source']} (page {v['page']})")
    md_text = "\n\n".join(md)
    return {
        "query": query,
        "report_md": md_text,
        "step_summaries": step_summaries,
        "citations": citations
    }

def run_pipeline(query:str, top_k=4):
    plan = create_plan(query)
    print("Plan:", plan)
    step_outputs = []
    for step in plan:
        retrieved = retrieve(step, k=top_k)
        out = summarize_step(step, retrieved)
        step_outputs.append(out)
    final = synthesize_report(query, step_outputs)
    return final

if __name__ == '__main__':
    q = "Explain how quantum computing affects cybersecurity and propose mitigation strategies"
    result = run_pipeline(q, top_k=4)
    print(result['report_md'])
