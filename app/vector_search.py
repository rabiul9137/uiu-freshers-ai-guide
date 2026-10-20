
import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "seed_documents.json"

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

_model = None
_index = None
_documents = None


def get_model():
    """Load the embedding model only when needed."""
    global _model

    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)

    return _model


def load_vector_index():
    """Load documents and build an in-memory FAISS index."""
    global _index, _documents

    if _index is not None:
        return _index, _documents

    with DATA_FILE.open("r", encoding="utf-8") as file:
        documents = json.load(file)

    if not documents:
        return None, []

    texts = [
        f"{doc.get('title', '')}. "
        f"{doc.get('category', '')}. "
        f"{doc.get('text', '')}"
        for doc in documents
    ]

    model = get_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    embeddings = np.asarray(embeddings, dtype=np.float32)

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    _index = index
    _documents = documents

    return _index, _documents


def search_vectors(
    query: str,
    limit: int = 3,
    min_score: float = 0.40,
) -> list[dict]:
    """Retrieve relevant documents using semantic similarity."""
    query = query.strip()

    if not query:
        return []

    index, documents = load_vector_index()

    if index is None or not documents:
        return []

    query_embedding = get_model().encode(
        [query],
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype=np.float32,
    )

    search_limit = min(limit, len(documents))
    scores, indices = index.search(query_embedding, search_limit)

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx < 0 or float(score) < min_score:
            continue

        results.append({
            **documents[int(idx)],
            "score": round(float(score), 3),
        })

    return results
