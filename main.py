import os
import re
import subprocess
import sys
from datetime import datetime

import questionary
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from google import genai

# ── Configuration ────────────────────────────────────────────────────────────

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NOTES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes.md")
MODEL = "gemini-2.5-flash"

SYSTEM_PROMPT = """You are an expert technical writer who creates clear, concise, and high-level article summaries.

Your task:
- Create a short, high-level overview of the provided article. Do NOT output too much text and do not leave any topic.
- Use simple, easy-to-understand language.
- Provide a brief "Overview" section capturing the core idea.
- Only include the most critical points using proper headings. Do NOT output granular details.
- Do NOT overuse bullet points and NEVER use tables.
- Output ONLY the summary in Markdown format. Do not include any preamble like "Here is the summary".
"""

# ── Step 1: Interactive CLI Menu ─────────────────────────────────────────────


def get_user_input():
    """Display the interactive CLI menu and capture user input."""
    option = questionary.select(
        "How do you want to input the article?",
        choices=["URL", "Raw Text"],
    ).ask()

    if option is None:
        print("Cancelled.")
        sys.exit(0)

    if option == "URL":
        url = questionary.text("Paste the article URL:").ask()
        if not url:
            print("No URL provided. Exiting.")
            sys.exit(1)
        return "url", url.strip()
    else:
        print("Paste your article text below (press Enter twice on an empty line to finish):")
        lines = []
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
        return "text", text


# ── Step 2: Content Extraction ───────────────────────────────────────────────


def extract_from_url(url):
    """Download a web page and extract the article title and body text."""
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

    # Extract title
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else "Untitled Article"

    # Extract article body — try <article> first, then fall back to all <p> tags
    article = soup.find("article")
    if article:
        paragraphs = article.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "pre", "code", "blockquote"])
    else:
        # Fall back: grab all paragraph and heading tags from <main> or <body>
        main = soup.find("main") or soup.find("body")
        if main:
            paragraphs = main.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "pre", "code", "blockquote"])
        else:
            paragraphs = soup.find_all("p")

    body_text = "\n\n".join(tag.get_text(strip=True) for tag in paragraphs if tag.get_text(strip=True))

    if not body_text:
        print("Warning: Could not extract meaningful text from the page.")
        # Last resort — grab all visible text
        body_text = soup.get_text(separator="\n", strip=True)

    return title, body_text


def extract_content(input_type, input_value):
    """Route extraction based on input type. Returns (title, body_text, source)."""
    if input_type == "url":
        title, body_text = extract_from_url(input_value)
        return title, body_text, input_value
    else:
        return "Pasted Article", input_value, None


# ── Step 3: Gemini API Call ──────────────────────────────────────────────────


def summarize_with_gemini(article_text):
    """Send article text to Gemini and return the markdown summary."""
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_api_key_here.":
        print("Error: Please set a valid GEMINI_API_KEY in your .env file.")
        sys.exit(1)

    client = genai.Client(api_key=GEMINI_API_KEY)

    print("Sending to Gemini for summarization...")

    response = client.models.generate_content(
        model=MODEL,
        contents=article_text,
        config=genai.types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.3,
        ),
    )

    summary = response.text
    if not summary:
        print("Error: Gemini returned an empty response.")
        sys.exit(1)

    return summary


# ── Step 4: Markdown File Management & Indexing ──────────────────────────────

INDEX_START_MARKER = "<!-- INDEX START -->"
INDEX_END_MARKER = "<!-- INDEX END -->"


def generate_anchor(title):
    """Generate a GitHub-compatible anchor from a title string."""
    anchor = title.lower().strip()
    anchor = re.sub(r"[^\w\s-]", "", anchor)
    anchor = re.sub(r"\s+", "-", anchor)
    return anchor


def initialize_notes_file():
    """Create the notes.md file with the initial structure if it's empty or missing."""
    if not os.path.exists(NOTES_FILE) or os.path.getsize(NOTES_FILE) == 0:
        initial_content = f"""# System Design & Tech Notes

> Auto-generated summaries from articles. Last updated: {datetime.now().strftime("%Y-%m-%d")}.

## Table of Contents

{INDEX_START_MARKER}
{INDEX_END_MARKER}

---

"""
        with open(NOTES_FILE, "w", encoding="utf-8") as f:
            f.write(initial_content)


def append_summary(title, source_url, summary):
    """Append a new article summary to notes.md and update the index."""
    initialize_notes_file()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    anchor = generate_anchor(title)

    # ── Build the new section ────────────────────────────────────────────
    new_section = f"\n## {title}\n\n"
    new_section += f"*Added: {timestamp}*\n\n"
    if source_url:
        new_section += f"**Source:** [{source_url}]({source_url})\n\n"
    new_section += summary.strip() + "\n\n"
    new_section += "---\n"

    # ── Append the summary to the file ───────────────────────────────────
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(new_section)

    # ── Update the Table of Contents index ───────────────────────────────
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Build the new index entry
    new_entry = f"- [{title}](#{anchor}) — *{timestamp}*"

    # Find the index block and insert the new entry
    pattern = re.compile(
        rf"({re.escape(INDEX_START_MARKER)})(.*?)({re.escape(INDEX_END_MARKER)})",
        re.DOTALL,
    )

    match = pattern.search(content)
    if match:
        existing_entries = match.group(2).strip()
        if existing_entries:
            updated_entries = existing_entries + "\n" + new_entry
        else:
            updated_entries = new_entry

        updated_index = f"{INDEX_START_MARKER}\n{updated_entries}\n{INDEX_END_MARKER}"
        content = pattern.sub(updated_index, content)

        with open(NOTES_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated Table of Contents with: {title}")
    else:
        print("Warning: Could not find index markers in notes.md. Skipping TOC update.")


# ── Step 5: Git Automation ───────────────────────────────────────────────────


def git_commit_and_push():
    """Stage, commit, and push changes using subprocess."""
    repo_dir = os.path.dirname(os.path.abspath(__file__))

    commands = [
        ["git", "add", "."],
        ["git", "commit", "-m", f"notes: auto-update {datetime.now().strftime('%Y-%m-%d %H:%M')}"],
        ["git", "push"],
    ]

    for cmd in commands:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=repo_dir, capture_output=True, text=True)

        if result.returncode != 0:
            # git commit returns 1 if there's nothing to commit — that's fine
            if cmd[1] == "commit" and "nothing to commit" in result.stdout:
                print("Nothing new to commit.")
                return
            print(f"Git error: {result.stderr.strip()}")
            if cmd[1] == "push":
                print("Push failed. You can manually run 'git push' later.")
            return

    print("Changes committed and pushed successfully!")


# ── Main ─────────────────────────────────────────────────────────────────────


def main():
    print("\n📝  Notes Maker — Article Summarizer\n")

    # Step 1: Get input
    input_type, input_value = get_user_input()

    # Step 2: Extract content
    print("\nExtracting content...")
    title, body_text, source_url = extract_content(input_type, input_value)
    print(f"Title: {title}")
    print(f"Extracted {len(body_text)} characters of text.")

    # Step 3: Summarize with Gemini
    summary = summarize_with_gemini(body_text)
    print("\nSummary generated successfully!\n")

    # Step 4: Save to notes.md
    append_summary(title, source_url, summary)
    print(f"Summary appended to {NOTES_FILE}")

    # Step 5: Git commit & push
    do_git = questionary.confirm("Commit and push to Git?", default=True).ask()
    if do_git:
        git_commit_and_push()
    else:
        print("Skipping git. You can commit manually later.")

    print("\n✅  Done!\n")


if __name__ == "__main__":
    main()
