
import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def scrape_page(url: str) -> dict:
    """Extract readable text from an accessible public webpage."""

    response = requests.get(
        url,
        timeout=20,
        headers={
            "User-Agent": "UIUFreshersAIGuide/0.1 (student capstone)"
        },
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    page_title = soup.title.get_text(" ", strip=True) if soup.title else ""
    page_text = soup.get_text(" ", strip=True)

    # Do not treat anti-bot verification pages as university content.
    blocked_phrases = [
        "one moment, please",
        "please wait while your request is being verified",
        "checking your browser",
    ]

    page_lower = page_text.lower()
    if any(phrase in page_lower for phrase in blocked_phrases):
        raise ValueError(
            "The website returned a verification page, not university content. "
            "Use another permitted official source or request access."
        )

    for element in soup(["script", "style", "nav", "footer", "header"]):
        element.decompose()

    page_text = soup.get_text(" ", strip=True)

    if len(page_text) < 200:
        raise ValueError(
            "Too little page text was extracted. Check the source before saving."
        )

    return {
        "title": page_title,
        "url": url,
        "text": page_text,
    }


def save_page(page: dict) -> Path:
    """Save verified page text and source metadata."""

    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "uiu_page.json"
    output_file.write_text(
        json.dumps(page, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return output_file
