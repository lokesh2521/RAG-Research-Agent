# ingest.py - produce a debugging JSON of chunks (without building the index)
import os, json
import sys
sys.path.append(os.path.dirname(__file__))
from utils import create_chunks_from_files

def main():
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'sample_docs')
    data_dir = os.path.abspath(data_dir)
    out = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'chunks_preview.json')
    chunks = list(create_chunks_from_files(data_dir, chunk_size=1000, overlap=200))
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(chunks)} chunks to {out}")

if __name__ == '__main__':
    main()
