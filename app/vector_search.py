import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "seed_documents.json"

STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were",
    "what", "where", "when", "who", "how", "why",
    "about", "for", "of", "to", "in", "on", "and",
    "tell", "me", "please", "can", "you", "do",
    "does", "i", "my", "at", "with", "from"
}


def tokenize(text):
    words = re.findall(r"[^\W_]+", text.lower(), flags=re.UNICODE)
    return {word for word in words if word not in STOPWORDS}


def search_vectors(query, limit=3, min_score=0.40):
    query_tokens = tokenize(query)

    if not query_tokens:
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            documents = json.load(file)
    except (OSError, json.JSONDecodeError):
        return []

    results = []

    for doc in documents:
        title = str(doc.get("title", ""))
        category = str(doc.get("category", ""))
        content = str(doc.get("text", ""))

        searchable_text = f"{title} {category} {content}"
        document_tokens = tokenize(searchable_text)

        matched_tokens = query_tokens & document_tokens
        if not matched_tokens:
            continue

        score = len(matched_tokens) / len(query_tokens)

        # Title and category matches receive a small bonus.
        title_category_tokens = tokenize(f"{title} {category}")
        if query_tokens & title_category_tokens:
            score = min(1.0, score + 0.10)

        if score >= min_score:
            results.append({
                **doc,
                "score": round(score, 3)
            })

    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:max(0, limit)]