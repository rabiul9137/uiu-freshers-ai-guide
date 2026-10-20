
import json
from pathlib import Path

DATA_FILE = Path("data/seed_documents.json")

NEW_DOCUMENTS = [
    {
        "id": "uiu_undergraduate_programs",
        "title": "UIU Undergraduate Programs",
        "url": "https://www.uiu.ac.bd/admission/undergraduate-program/",
        "category": "academic_programs",
        "language": "English",
        "source_type": "official_website",
        "verified_on": "2026-10-20",
        "text": (
            "United International University (UIU) lists undergraduate "
            "programs under four schools. The School of Business and "
            "Economics includes Bachelor of Business Administration (BBA), "
            "BBA in Accounting and Information Systems (BBA in AIS), "
            "and Bachelor of Science in Economics. The School of Science "
            "and Engineering includes Civil Engineering, Computer Science "
            "and Engineering (CSE), Data Science, and Electrical and "
            "Electronic Engineering (EEE). The School of Humanities and "
            "Social Sciences includes Environment and Development Studies, "
            "Media Studies and Journalism, and English. The School of Life "
            "Sciences includes Pharmacy and Biotechnology and Genetic "
            "Engineering. Consult the official UIU page for the current "
            "program list and admission details."
        ),
    },
    {
        "id": "uiu_student_welfare",
        "title": "UIU Student Welfare and Support Services",
        "url": "https://ciac.uiu.ac.bd/study-at-uiu/student-welfare",
        "category": "student_support",
        "language": "English",
        "source_type": "official_website",
        "verified_on": "2026-10-20",
        "text": (
            "The UIU student welfare information page describes support "
            "provided through the Career Counseling Center (CCC) and the "
            "Directorate of Student Affairs (DSA). The Career Counseling "
            "Center supports career skills development, internship "
            "placement, job search and placement, workshops, seminars, "
            "training, company visits, and on-campus interviews. The "
            "Directorate of Student Affairs supports co-curricular and "
            "extra-curricular activities, counselling service, loan "
            "facility, scholarships, gymnasium, games room, and female "
            "common room. For current availability and details, consult "
            "the official UIU source."
        ),
    },
]


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Knowledge base not found: {DATA_FILE}")

    with DATA_FILE.open("r", encoding="utf-8") as file:
        documents = json.load(file)

    if not isinstance(documents, list):
        raise ValueError("Knowledge base must contain a JSON list.")

    existing_ids = {doc.get("id") for doc in documents}
    added = 0

    for document in NEW_DOCUMENTS:
        if document["id"] in existing_ids:
            print(f"Already exists; skipped: {document['id']}")
            continue

        documents.append(document)
        existing_ids.add(document["id"])
        added += 1
        print(f"Added: {document['title']}")

    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            documents,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print(f"\nAdded documents: {added}")
    print(f"Total documents: {len(documents)}")


if __name__ == "__main__":
    main()
