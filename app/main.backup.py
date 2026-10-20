
import re
from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.knowledge_base import search_documents


app = FastAPI(
    title="UIU Freshers AI Guide",
    description="AI-powered assistant for public UIU information",
    version="0.3.0",
)


class AskRequest(BaseModel):
    question: str = Field(min_length=2, max_length=500)


def is_bengali(text: str) -> bool:
    """Check whether the question contains Bengali characters."""
    return bool(re.search(r"[\u0980-\u09FF]", text))


def translate_common_terms_to_bengali(text: str) -> str:
    """
    Translate common English UIU terms into Bengali.
    This is a simple dictionary-based translation, not full translation.
    """
    replacements = {
        "United International University": "ইউনাইটেড ইন্টারন্যাশনাল ইউনিভার্সিটি (UIU)",
        "UIU Student Clubs": "UIU-এর শিক্ষার্থী ক্লাবসমূহ",
        "UIU Undergraduate Programs": "UIU-এর স্নাতক প্রোগ্রামসমূহ",
        "UIU Student Welfare and Support Services": "UIU-এর শিক্ষার্থী কল্যাণ ও সহায়তা সেবা",
        "UIU Mental Health and Psychological Counselling Center": "UIU-এর মানসিক স্বাস্থ্য ও মনোসামাজিক কাউন্সেলিং সেন্টার",
        "Career Counseling Center (CCC)": "ক্যারিয়ার কাউন্সেলিং সেন্টার (CCC)",
        "Directorate of Student Affairs (DSA)": "শিক্ষার্থী বিষয়ক অধিদপ্তর (DSA)",
        "student clubs": "শিক্ষার্থী ক্লাব",
        "undergraduate programs": "স্নাতক প্রোগ্রাম",
        "career support services": "ক্যারিয়ার সহায়তা সেবা",
        "counselling": "কাউন্সেলিং",
        "counseling": "কাউন্সেলিং",
        "scholarships": "বৃত্তি",
        "internship": "ইন্টার্নশিপ",
        "job search and placement": "চাকরি খোঁজা ও চাকরিতে নিয়োগ সহায়তা",
        "workshops": "কর্মশালা",
        "seminars": "সেমিনার",
        "training": "প্রশিক্ষণ",
        "company visits": "কোম্পানি পরিদর্শন",
        "on-campus interviews": "ক্যাম্পাসে চাকরির সাক্ষাৎকার",
        "confidential space": "গোপনীয় পরিবেশ",
        "emotional, psychological, and academic challenges": "আবেগগত, মানসিক ও শিক্ষাসংক্রান্ত চ্যালেঞ্জ",
        "Bachelor of Business Administration": "ব্যাচেলর অব বিজনেস অ্যাডমিনিস্ট্রেশন",
        "Computer Science and Engineering": "কম্পিউটার সায়েন্স অ্যান্ড ইঞ্জিনিয়ারিং",
        "Data Science": "ডেটা সায়েন্স",
        "Electrical and Electronic Engineering": "ইলেকট্রিক্যাল অ্যান্ড ইলেকট্রনিক ইঞ্জিনিয়ারিং",
        "Pharmacy": "ফার্মেসি",
        "Biotechnology and Genetic Engineering": "বায়োটেকনোলজি অ্যান্ড জেনেটিক ইঞ্জিনিয়ারিং",
    }

    translated_text = text

    # Replace longer phrases first to avoid partial replacements.
    for english, bengali in sorted(
        replacements.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    ):
        translated_text = re.sub(
            re.escape(english),
            bengali,
            translated_text,
            flags=re.IGNORECASE,
        )

    return translated_text


@app.get("/")
def home():
    return {
        "project": "UIU Freshers AI Guide",
        "status": "running",
        "message": "Ask questions about UIU information.",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "gpu_required": False,
    }


@app.post("/ask")
def ask_question(request: AskRequest):
    question = request.question.strip()
    results = search_documents(question)
    bengali_question = is_bengali(question)

    if not results:
        if bengali_question:
            answer = (
                "দুঃখিত, বর্তমান তথ্যভান্ডারে আপনার প্রশ্নের "
                "সংশ্লিষ্ট তথ্য খুঁজে পাইনি। অনুগ্রহ করে UIU-এর "
                "অফিসিয়াল ওয়েবসাইট দেখুন।"
            )
        else:
            answer = (
                "I could not find relevant information in the "
                "current knowledge base. Please check the official "
                "UIU website."
            )

        return {
            "question": question,
            "answer": answer,
            "sources": [],
        }

    best_match = results[0]
    answer = best_match["text"]

    if bengali_question:
        answer = translate_common_terms_to_bengali(answer)

    return {
        "question": question,
        "answer": answer,
        "sources": [
            {
                "title": result["title"],
                "url": result["url"],
                "relevance_score": result["score"],
            }
            for result in results
        ],
        "note": (
            "এই প্রোটোটাইপে keyword matching ব্যবহার করা হয়েছে। "
            "বাংলা উত্তরে কিছু ইংরেজি শব্দের অভিধানভিত্তিক অনুবাদ "
            "করা হয়; এটি পূর্ণাঙ্গ AI অনুবাদ নয়।"
            if bengali_question
            else
            "This prototype uses keyword matching, not an AI-generated "
            "answer. Verify the source information before relying on it."
        ),
    }
