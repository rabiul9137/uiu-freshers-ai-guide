
import json
import unicodedata
from pathlib import Path

DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "seed_documents.json"
)

STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were",
    "what", "where", "when", "who", "how", "which",
    "for", "to", "of", "in", "on", "at", "and",
    "or", "do", "does", "can", "i", "you", "my",
    "me", "please", "find", "tell", "about",
    "কি", "কী", "কেন", "কীভাবে", "কিভাবে",
    "আছে", "হয়", "হয়", "হবে", "তে", "এ",
    "এর", "ও", "এবং", "জন্য",
}

BENGALI_TO_ENGLISH = {
    "ইউআইইউ": "uiu",
    "বিশ্ববিদ্যালয়": "university",
    "বিশ্ববিদ্যালয়ে": "university",
    "বিশ্ববিদ্যালয়ে": "university",
    "স্টুডেন্ট": "student",
    "শিক্ষার্থী": "student",
    "শিক্ষার্থীদের": "student",
    "ছাত্র": "student",
    "ছাত্রী": "student",
    "ক্লাব": "clubs",
    "ক্লাবগুলো": "clubs",
    "ক্লাবের": "clubs",
    "ভর্তি": "admission",
    "অ্যাডমিশন": "admission",
    "স্নাতক": "undergraduate",
    "প্রোগ্রাম": "programs",
    "প্রোগ্রামগুলো": "programs",
    "কোর্স": "programs",
    "ক্যারিয়ার": "career",
    "ক্যারিয়ার": "career",
    "চাকরি": "job",
    "কাউন্সেলিং": "counseling",
    "পরামর্শ": "counseling",
    "সহায়তা": "support",
    "সহায়তা": "support",
    "সেবা": "services",
    "ল্যাব": "lab",
    "কম্পিউটার": "computer",
    "রুম": "room",
    "কক্ষ": "room",
    "কোথায়": "where",
    "কোথায়": "where",
    "কখন": "when",
    "কীভাবে": "how",
    "কিভাবে": "how",
}


def split_words(text: str) -> list[str]:
    """Split text into Unicode words without breaking Bengali letters."""
    words = []
    current = []

    for char in unicodedata.normalize("NFC", text.lower()):
        category = unicodedata.category(char)

        # Letters and combining marks are part of a word.
        if category.startswith("L") or category.startswith("M") or category == "Nd":
            current.append(char)
        elif current:
            words.append("".join(current))
            current = []

    if current:
        words.append("".join(current))

    return words


def load_documents() -> list[dict]:
    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r", encoding="utf-8") as file:
        documents = json.load(file)

    if not isinstance(documents, list):
        raise ValueError("Knowledge base must contain a JSON list.")

    return documents


def tokenize(text: str) -> set[str]:
    words = set(split_words(text))
    expanded_words = set()

    for word in words:
        translated = BENGALI_TO_ENGLISH.get(word, word)
        expanded_words.update(split_words(translated))

    return expanded_words - STOP_WORDS


def search_documents(
    query: str,
    limit: int = 3,
    min_score: float = 0.75,
) -> list[dict]:
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

    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:limit]
