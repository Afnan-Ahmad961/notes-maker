"""Content extraction for article URLs and raw pasted text."""

import sys

import requests
from bs4 import BeautifulSoup

_CONTENT_TAGS = ["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "pre", "code", "blockquote"]
_CONTENT_TAG_SET = set(_CONTENT_TAGS)


def _collect_blocks(container) -> list:
    """Return only the *top-level* content blocks inside ``container``.

    ``find_all`` matches parents and their descendants alike, so a
    ``<pre><code>…`` or a ``<li><p>…`` would otherwise have its text collected
    twice. We keep a matched tag only when none of its ancestors (up to, but not
    including, ``container``) is itself a content tag — the ancestor's text
    already covers the nested one.
    """
    blocks = []
    for tag in container.find_all(_CONTENT_TAGS):
        nested = False
        for parent in tag.parents:
            if parent is container:
                break
            if parent.name in _CONTENT_TAG_SET:
                nested = True
                break
        if not nested:
            blocks.append(tag)
    return blocks


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
    container = soup.find("article") or soup.find("main") or soup.find("body")
    blocks = _collect_blocks(container) if container else soup.find_all("p")

    # ``separator=" "`` keeps a space between inline children (e.g. a <code> span
    # inside a <p>), so words don't run together like "Item withinlinecode".
    body_text = "\n\n".join(
        text for tag in blocks if (text := tag.get_text(separator=" ", strip=True))
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
