# utils.py - helpers for ingestion, chunking, metadata
import os, json, uuid, re
from typing import List, Dict
try:
    import fitz  # pymupdf
except Exception:
    fitz = None
from markdown import markdown

def load_pdf_text(path: str) -> List[Dict]:
    """Return list of pages: [{'text':..., 'page_no':i}]"""
    if fitz is None:
        raise RuntimeError("pymupdf not installed or not available. Install pymupdf to parse PDFs.")
    doc = fitz.open(path)
    pages = []
    for i in range(len(doc)):
        text = doc[i].get_text("text")
        pages.append({"text": text, "page": i+1, "source": os.path.basename(path)})
    return pages

def load_md_text(path: str) -> List[Dict]:
    txt = open(path, "r", encoding="utf-8").read()
    # Keep the raw text (strip code blocks for ingest)
    text = re.sub(r'```.*?```', '', txt, flags=re.S)
    pages = [{"text": text, "page": 1, "source": os.path.basename(path)}]
    return pages

def chunk_text(text:str, chunk_size:int=800, overlap:int=200) -> List[str]:
    """Simple character-based chunking with overlap."""
    text = text.replace("\n", " ").strip()
    chunks = []
    start = 0
    length = len(text)
    while start < length:
        end = min(start + chunk_size, length)
        chunk = text[start:end].strip()
        if len(chunk) > 50:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def create_chunks_from_files(data_dir:str, chunk_size:int=1000, overlap:int=200):
    """Yield chunk dicts with metadata"""
    for fname in os.listdir(data_dir):
        path = os.path.join(data_dir, fname)
        if not os.path.isfile(path): continue
        if fname.lower().endswith(".pdf"):
            pages = load_pdf_text(path)
        elif fname.lower().endswith(".md") or fname.lower().endswith('.markdown'):
            pages = load_md_text(path)
        else:
            # skip unknown files
            continue
        for p in pages:
            page_text = p["text"]
            page_no = p["page"]
            chunks = chunk_text(page_text, chunk_size=chunk_size, overlap=overlap)
            for i, c in enumerate(chunks):
                yield {
                    "chunk_id": str(uuid.uuid4()),
                    "source": p["source"],
                    "page": page_no,
                    "chunk_index": i,
                    "text": c
                }
