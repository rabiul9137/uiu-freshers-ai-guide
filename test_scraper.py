from app.scraper import scrape_page, save_page

url = "https://www.uiu.ac.bd/"

page = scrape_page(url)
saved_path = save_page(page)

print("Page title:", page["title"])
print("Source URL:", page["url"])
print("Extracted text length:", len(page["text"]))
print("Saved to:", saved_path)
print("Text preview:", page["text"][:500])