
import re
from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.knowledge_base import search_documents

app = FastAPI(
    title="UIU Freshers AI Guide",
    description="AI-powered assistant for public UIU information",
    version="0.4.0",
)


class AskRequest(BaseModel):
    question: str = Field(min_length=2, max_length=500)


def is_bengali(text: str) -> bool:
    return bool(re.search(r"[\u0980-\u09FF]", text))


def get_bengali_answer(title: str) -> str:
    answers = {
        "UIU Student Clubs": (
            "UIU-তে বিভিন্ন শিক্ষার্থী ক্লাব রয়েছে। এর মধ্যে "
            "ডিবেট ক্লাব, কালচারাল ক্লাব, থিয়েটার অ্যান্ড ফিল্ম ক্লাব, "
            "বিজনেস ক্লাব, কম্পিউটার ক্লাব, ফটোগ্রাফি ক্লাব, "
            "স্পোর্টস ক্লাব, রোবোটিক্স ক্লাব এবং মডেল ইউনাইটেড "
            "নেশনস ক্লাব রয়েছে। সর্বশেষ তালিকার জন্য UIU-এর "
            "অফিসিয়াল ওয়েবসাইট দেখুন।"
        ),
        "UIU Undergraduate Programs": (
            "UIU-তে ব্যবসায় প্রশাসন, অর্থনীতি, কম্পিউটার সায়েন্স "
            "অ্যান্ড ইঞ্জিনিয়ারিং, ডেটা সায়েন্স, সিভিল ইঞ্জিনিয়ারিং, "
            "ইলেকট্রিক্যাল অ্যান্ড ইলেকট্রনিক ইঞ্জিনিয়ারিং, ইংরেজি, "
            "মিডিয়া স্টাডিজ অ্যান্ড জার্নালিজম, ফার্মেসি এবং "
            "বায়োটেকনোলজি অ্যান্ড জেনেটিক ইঞ্জিনিয়ারিংসহ বিভিন্ন "
            "স্নাতক প্রোগ্রাম রয়েছে। বর্তমান তালিকার জন্য UIU-এর "
            "অফিসিয়াল ওয়েবসাইট দেখুন।"
        ),
        "UIU Student Welfare and Support Services": (
            "UIU শিক্ষার্থীদের ক্যারিয়ার সহায়তা, কাউন্সেলিং, "
            "কর্মশালা, সেমিনার, প্রশিক্ষণ এবং ইন্টার্নশিপ ও "
            "চাকরির প্রস্তুতিতে সহায়তা প্রদান করে। শিক্ষার্থী "
            "কল্যাণের অন্যান্য সুবিধা সম্পর্কে জানতে UIU-এর "
            "অফিসিয়াল ওয়েবসাইট দেখুন।"
        ),
        "UIU Mental Health and Psychological Counselling Center": (
            "UIU-তে মানসিক স্বাস্থ্য ও মনোসামাজিক কাউন্সেলিং "
            "সেন্টার রয়েছে। শিক্ষার্থীরা মানসিক ও শিক্ষাসংক্রান্ত "
            "চ্যালেঞ্জ নিয়ে কাউন্সেলিং সহায়তা পেতে পারেন। "
            "বর্তমান সময়সূচি ও অ্যাপয়েন্টমেন্টের জন্য অফিসিয়াল "
            "ওয়েবসাইট দেখুন।"
        ),
    }

    return answers.get(
        title,
        "দুঃখিত, এই প্রশ্নের জন্য নির্দিষ্ট বাংলা উত্তর প্রস্তুত নেই। "
        "নিচের অফিসিয়াল source link থেকে বিস্তারিত জানতে পারবেন।"
    )


@app.get("/")
def home():
    return {
        "project": "UIU Freshers AI Guide",
        "status": "running",
        "message": "Ask questions about UIU information.",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "gpu_required": False}


@app.post("/ask")
def ask_question(request: AskRequest):
    question = request.question.strip()
    results = search_documents(question)
    bengali_question = is_bengali(question)

    if not results:
        answer = (
            "দুঃখিত, বর্তমান তথ্যভান্ডারে আপনার প্রশ্নের উত্তর পাইনি। "
            "অনুগ্রহ করে UIU-এর অফিসিয়াল ওয়েবসাইট দেখুন।"
            if bengali_question
            else
            "I could not find relevant information in the current "
            "knowledge base. Please check the official UIU website."
        )
        return {
            "question": question,
            "answer": answer,
            "sources": [],
        }

    best_match = results[0]

    answer = (
        get_bengali_answer(best_match["title"])
        if bengali_question
        else best_match["text"]
    )

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
            "বাংলা উত্তর নির্দিষ্ট template থেকে দেওয়া হয়েছে। "
            "তথ্যের জন্য official source যাচাই করুন।"
            if bengali_question
            else
            "This prototype uses keyword matching, not an AI-generated "
            "answer. Verify the source information before relying on it."
        ),
    }
