"""Content extraction for article URLs and raw pasted text."""

import sys

import requests
from bs4 import BeautifulSoup

_CONTENT_TAGS = ["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "pre", "code", "blockquote"]


def extract_from_url(url: str) -> tuple[str, str]:
    """Download a web page and extract candidate titles plus the body text.

    Returns ``("Let Gemini Decide", body_text)`` — the model picks the best title
    from the candidates embedded in ``body_text``.
    """
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.text, "html.parser")

    # Collect candidate titles and let Gemini decide the best one.
    possible_titles: list[str] = []
    seen_titles: set[str] = set()
    for t in soup.find_all(["title", "h1"]):
        t_text = t.get_text(strip=True)
        if t_text and t_text not in seen_titles:
            possible_titles.append(t_text)
            seen_titles.add(t_text)

    # Prefer <article>, then <main>/<body>, then a bare <p> sweep.
    article = soup.find("article")
    if article:
        paragraphs = article.find_all(_CONTENT_TAGS)
    else:
        main = soup.find("main") or soup.find("body")
        paragraphs = main.find_all(_CONTENT_TAGS) if main else soup.find_all("p")

    body_text = "\n\n".join(
        tag.get_text(strip=True) for tag in paragraphs if tag.get_text(strip=True)
    )

    if not body_text:
        print("Warning: Could not extract meaningful text from the page.")
        body_text = soup.get_text(separator="\n", strip=True)

    if possible_titles:
        titles_block = "\n".join(f"- {t}" for t in possible_titles)
        body_text = f"Possible Titles:\n{titles_block}\n\nArticle Text:\n{body_text}"

    return "Let Gemini Decide", body_text


def read_raw_text() -> str:
    """Read multi-line pasted text from stdin (blank line twice to finish)."""
    print("Paste your article text below (press Enter twice on an empty line to finish):")
    lines: list[str] = []
    empty_count = 0
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "":
            empty_count += 1
            if empty_count >= 2:
                break
            lines.append(line)
        else:
            empty_count = 0
            lines.append(line)

    text = "\n".join(lines).strip()
    if not text:
        print("No text provided. Exiting.")
        sys.exit(1)
    return text
