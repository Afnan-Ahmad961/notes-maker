"""Command-line entry point that wires the pieces together."""

import questionary

from . import config, extract, git_ops, notes, prompts, summarize, youtube

# A transcript with at least this many words is treated as a "long" video
# (roughly 30+ minutes of speech) and gets an in-note index of major topics.
LONG_TRANSCRIPT_WORDS = 3500


def _gather_source() -> tuple[str, str, str | None]:
    """Prompt for the input type and return (body_text, system_prompt, source_url)."""
    input_type = questionary.select(
        "How do you want to input the source?",
        choices=["URL", "YouTube", "Raw Text"],
    ).ask()

    if input_type is None:
        print("Cancelled.")
        raise SystemExit(0)

    if input_type == "URL":
        url = questionary.text("Paste the article URL:").ask()
        if not url or not url.strip():
            print("No URL provided. Exiting.")
            raise SystemExit(1)
        url = url.strip()
        _title, body_text = extract.extract_from_url(url)
        return body_text, prompts.ARTICLE_SYSTEM_PROMPT, url

    if input_type == "YouTube":
        url = questionary.text("Paste the YouTube video URL:").ask()
        if not url or not url.strip():
            print("No URL provided. Exiting.")
            raise SystemExit(1)
        url = url.strip()
        video_id = youtube.extract_video_id(url)
        if not video_id:
            print("Could not find a video id in that URL. Exiting.")
            raise SystemExit(1)
        body_text = youtube.fetch_transcript(video_id)
        system_prompt = prompts.YOUTUBE_SYSTEM_PROMPT
        word_count = len(body_text.split())
        if word_count >= LONG_TRANSCRIPT_WORDS:
            system_prompt += prompts.YOUTUBE_INDEX_INSTRUCTIONS
            print(f"Long video detected ({word_count} words) — adding a topic index.")
        return body_text, system_prompt, url

    body_text = extract.read_raw_text()
    return body_text, prompts.ARTICLE_SYSTEM_PROMPT, None


def main() -> None:
    print("\n📝  Notes Maker — Article & Video Summarizer\n")

    # ── Configuration (prompts on first run) ─────────────────────────────
    config.load()
    config.ensure_api_key()
    repo_path = config.ensure_repo_path()
    nd = notes.notes_dir(repo_path)

    # ── Step 1: gather the source ────────────────────────────────────────
    body_text, system_prompt, source_url = _gather_source()
    print(f"\nExtracted {len(body_text)} characters of text.")

    # ── Step 2: choose the destination note file ─────────────────────────
    target_file = notes.select_target_file(nd)

    # ── Step 3: summarize ────────────────────────────────────────────────
    summary = summarize.summarize(body_text, system_prompt)
    print("\nSummary generated successfully!\n")

    # Parse the title from the first line of the summary.
    title = "Untitled"
    first_line = summary.split("\n")[0].strip()
    if first_line.startswith("# "):
        title = first_line.replace("# ", "", 1).strip()
        summary = "\n".join(summary.split("\n")[1:]).strip()

    # ── Step 4: save to the chosen file ──────────────────────────────────
    notes.append_summary(target_file, title, source_url, summary)
    print(f"Summary appended to {target_file}")

    # ── Step 5: git commit & push (runs inside the notes/ directory) ──────
    do_git = questionary.confirm("Commit and push to Git?", default=True).ask()
    if do_git:
        if not git_ops.commit_and_push(nd, target_file):
            print("\n⚠️  Git step did not complete. Your notes were saved locally.\n")
            raise SystemExit(1)
    else:
        print("Skipping git. You can commit manually later.")

    print("\n✅  Done!\n")


if __name__ == "__main__":
    main()
