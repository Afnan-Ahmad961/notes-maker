"""Dynamic note-file routing: the notes/ directory, file selection, and indexing."""

import re
from datetime import datetime
from pathlib import Path

import questionary

INDEX_START_MARKER = "<!-- INDEX START -->"
INDEX_END_MARKER = "<!-- INDEX END -->"

_CREATE_NEW = "➕  Create a new file"


def notes_dir(repo_path: Path) -> Path:
    """Return (and create) the notes/ directory inside the repository."""
    nd = repo_path / "notes"
    nd.mkdir(parents=True, exist_ok=True)
    return nd


def list_note_files(nd: Path) -> list[Path]:
    """List existing .md files inside the notes directory, sorted by name."""
    return sorted(nd.glob("*.md"))


def generate_anchor(title: str) -> str:
    """Generate a GitHub-compatible anchor from a title string."""
    anchor = title.lower().strip()
    anchor = re.sub(r"[^\w\s-]", "", anchor)
    anchor = re.sub(r"\s+", "-", anchor)
    return anchor


_HEADING_RE = re.compile(r"^#{1,6}\s+(.*\S)\s*$")


def anchor_for_last_heading(content: str, title: str) -> str:
    """Return the anchor GitHub assigns to the LAST ``title`` heading in ``content``.

    When two headings render to the same slug, GitHub keeps the first as ``#slug``
    and suffixes later ones as ``#slug-1``, ``#slug-2``, … To link the file's Table
    of Contents to the note that was just appended (rather than an earlier note with
    the same title), we replay that numbering over every heading in document order
    and return the anchor computed at this note's own heading.
    """
    base = generate_anchor(title)
    counts: dict[str, int] = {}
    result = base
    for line in content.splitlines():
        match = _HEADING_RE.match(line)
        if not match:
            continue
        heading_text = match.group(1).strip()
        slug = generate_anchor(heading_text)
        seen = counts.get(slug, 0)
        anchor = slug if seen == 0 else f"{slug}-{seen}"
        counts[slug] = seen + 1
        if heading_text == title:
            result = anchor  # keep the last occurrence — the note just appended
    return result


def _title_from_filename(path: Path) -> str:
    stem = path.stem.replace("-", " ").replace("_", " ").strip()
    return stem.title() if stem else "Notes"


def initialize_note_file(path: Path) -> None:
    """Create a note file with the header, TOC and index markers if it's empty/missing."""
    if path.exists() and path.stat().st_size > 0:
        return
    content = f"""# {_title_from_filename(path)}

> Auto-generated summaries from articles and videos. Last updated: {datetime.now().strftime("%Y-%m-%d")}.

## Table of Contents

{INDEX_START_MARKER}
{INDEX_END_MARKER}

---

"""
    path.write_text(content, encoding="utf-8")


def select_target_file(nd: Path) -> Path:
    """Ask which note file to append to, creating a new one on request."""
    files = list_note_files(nd)
    choices = [f.name for f in files] + [_CREATE_NEW]

    choice = questionary.select(
        "Which file should this summary go into?",
        choices=choices,
    ).ask()

    if choice is None:
        print("Cancelled.")
        raise SystemExit(0)

    if choice != _CREATE_NEW:
        return nd / choice

    name = questionary.text("New file name (e.g. system-design):").ask()
    if not name or not name.strip():
        print("No filename provided. Exiting.")
        raise SystemExit(1)

    name = Path(name.strip()).name  # strip any path separators
    if not name.endswith(".md"):
        name += ".md"

    target = nd / name
    initialize_note_file(target)
    return target


def append_summary(
    path: Path,
    title: str,
    source_url: str | None,
    summary: str,
    update_index: bool = True,
) -> None:
    """Append a summary section to ``path``.

    When ``update_index`` is True the file's Table of Contents is updated with an
    entry for this note. It is set False for long videos, where the summary itself
    already contains a Gemini-generated ``## Contents`` index.
    """
    initialize_note_file(path)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # ── Build and append the new section ─────────────────────────────────
    new_section = f"\n## {title}\n\n"
    new_section += f"*Added: {timestamp}*\n\n"
    if source_url:
        new_section += f"**Source:** [{source_url}]({source_url})\n\n"
    new_section += summary.strip() + "\n\n"
    new_section += "---\n"

    with open(path, "a", encoding="utf-8") as f:
        f.write(new_section)

    if not update_index:
        return

    # ── Update the Table of Contents index ───────────────────────────────
    content = path.read_text(encoding="utf-8")
    # Anchor is computed from the whole file so a note sharing a title with an
    # earlier one links to its own (#slug-1, #slug-2, …) heading, not the first.
    anchor = anchor_for_last_heading(content, title)
    new_entry = f"- [{title}](#{anchor}) — *{timestamp}*"

    pattern = re.compile(
        rf"({re.escape(INDEX_START_MARKER)})(.*?)({re.escape(INDEX_END_MARKER)})",
        re.DOTALL,
    )
    match = pattern.search(content)
    if not match:
        print(f"Warning: Could not find index markers in {path.name}. Skipping TOC update.")
        return

    existing_entries = match.group(2).strip()
    updated_entries = existing_entries + "\n" + new_entry if existing_entries else new_entry
    updated_index = f"{INDEX_START_MARKER}\n{updated_entries}\n{INDEX_END_MARKER}"
    content = pattern.sub(updated_index, content)

    path.write_text(content, encoding="utf-8")
    print(f"Updated Table of Contents in {path.name} with: {title}")
