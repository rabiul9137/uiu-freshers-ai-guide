
import json
import re
from pathlib import Path

DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "seed_documents.json"
)

# Common English words that usually add little meaning to a search.
STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were",
    "what", "where", "when", "who", "how", "which",
    "for", "to", "of", "in", "on", "at", "and",
    "or", "do", "does", "can", "i", "you", "my",
    "me", "please", "find", "tell", "about",
}


def load_documents() -> list[dict]:
    """Load knowledge-base documents from the JSON file."""
    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r", encoding="utf-8") as file:
        documents = json.load(file)

    if not isinstance(documents, list):
        raise ValueError("Knowledge base must contain a JSON list.")

    return documents


def tokenize(text: str) -> set[str]:
    """Convert text to lowercase keywords and remove common words."""
    words = set(re.findall(r"\b\w+\b", text.lower()))
    return words - STOP_WORDS


def search_documents(
    query: str,
    limit: int = 3,
    min_score: float = 0.50,
) -> list[dict]:
    """
    Find documents matching the query.

    Score = number of matched query keywords / total query keywords.
    Documents below min_score are excluded.
    """
    documents = load_documents()
    query_terms = tokenize(query)

    if not query_terms:
        return []

    results = []

    for document in documents:
        searchable_text = " ".join([
            document.get("title", ""),
            document.get("category", ""),
            document.get("text", ""),
        ])

        document_terms = tokenize(searchable_text)
        matched_terms = query_terms.intersection(document_terms)

        score = len(matched_terms) / len(query_terms)

        if score < min_score:
            continue

        results.append({
            **document,
            "score": round(score, 3),
            "matched_terms": sorted(matched_terms),
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results[:limit]
