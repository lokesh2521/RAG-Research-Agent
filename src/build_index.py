# build_index.py - builds FAISS index from local docs using sentence-transformers or OpenAI embeddings
import os, json, pickle
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import faiss
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(__file__))
from utils import create_chunks_from_files

load_dotenv = None
EMBEDDING_MODE = os.getenv('EMBEDDING_MODE', 'local') if 'os' in globals() else 'local'
MODEL_NAME_LOCAL = 'all-MiniLM-L6-v2'  # 384-dim
INDEX_PATH = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'index.faiss')
META_PATH = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'index_meta.json')

if EMBEDDING_MODE == 'local':
    embedder = SentenceTransformer(MODEL_NAME_LOCAL)
else:
    raise NotImplementedError('OpenAI embedding mode not implemented in this script. Use local or add wrapper.')

def build_index(data_dir=None, chunk_size=1000, overlap=200):
    if data_dir is None:
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'sample_docs')
    data_dir = os.path.abspath(data_dir)
    os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'outputs'), exist_ok=True)
    print('Creating chunks...')
    chunks = list(create_chunks_from_files(data_dir, chunk_size, overlap))
    texts = [c['text'] for c in chunks]
    print(f'Embedding {len(texts)} chunks with model {MODEL_NAME_LOCAL} ...')
    embeddings = embedder.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    # FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  # cosine-like if vectors normalized
    # normalize vectors
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    INDEX_PATH_ABS = os.path.abspath(INDEX_PATH)
    faiss.write_index(index, INDEX_PATH_ABS)

    # save ordered meta
    ordered_meta = []
    for c in chunks:
        m = c.copy()
        ordered_meta.append(m)
    with open(META_PATH, 'w', encoding='utf-8') as f:
        json.dump(ordered_meta, f, ensure_ascii=False, indent=2)
    print('Saved index and metadata to outputs/.')

if __name__ == '__main__':
    build_index()
