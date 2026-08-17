# Notes Maker

A command-line tool that turns **articles**, **raw text**, and **YouTube videos** into
clean, indexed Markdown notes using Google Gemini — then commits and pushes them to your
notes repository.

Give it a link, pick (or create) a note file, and it drops a titled, timestamped summary
into your notes and keeps a linked Table of Contents up to date.

---

## Installation

Install it as a global CLI with [uv](https://docs.astral.sh/uv/):

```bash
uv tool install git+https://github.com/Afnan-Ahmad961/notes-maker
```

This makes the `notes-maker` command available everywhere in your terminal.

To upgrade later:

```bash
uv tool upgrade notes-maker
```

You'll also need [`git`](https://git-scm.com/) on your PATH (used for commit & push) and a
free **Gemini API key** from <https://aistudio.google.com/apikey>.

---

## First run & configuration

The first time you run `notes-maker`, it walks you through a one-time setup and stores your
answers in a global `.env`:

1. **Gemini API key** — pasted and saved (hidden input).
2. **Notes Repository Path** — the folder where your notes live. Point this at a **git repo
   with a GitHub remote** so your notes can be pushed. Notes are always written here no
   matter which directory you launch the command from.

Both values are saved to the OS-standard config directory:

| OS       | Location                                             |
| -------- | ---------------------------------------------------- |
| Windows  | `%LOCALAPPDATA%\notes-maker\notes-maker\.env`        |
| macOS    | `~/Library/Application Support/notes-maker/.env`      |
| Linux    | `~/.config/notes-maker/.env`                         |

To change either value later, edit that `.env` (keys: `GEMINI_API_KEY`,
`NOTES_REPO_PATH`) or delete it to be re-prompted.

### Setting up your notes repository

All notes are written into a `notes/` subfolder of your Notes Repository Path, and **git
operations run inside that `notes/` folder** — so that is the directory you connect to
GitHub. The tool runs `git init` there for you on first push if it isn't a repo yet.
To actually push to GitHub, add a remote once:

```bash
cd /path/to/your/notes-repo/notes
git remote add origin https://github.com/<you>/<your-notes-repo>.git
git push -u origin main
```

After that, Notes Maker's automatic `git push` works on every run (it sets the upstream
automatically the first time).

---

## Usage

Just run:

```bash
notes-maker
```

Then follow the prompts:

1. **Choose an input type** — `URL`, `YouTube`, or `Raw Text`.
2. **Provide the source** — paste a link, or paste text (blank line twice to finish).
3. **Pick a destination file** — the tool lists every `.md` file in your `notes/`
   directory, or lets you **create a new one** (it's created with the boilerplate header,
   Table of Contents, and index markers).
4. **Gemini summarizes** the content and the summary is appended to the chosen file, with
   the Table of Contents updated automatically.
5. **Commit & push** — confirm to have the tool `git add`/`commit`/`push` your notes.

Notes are organized like this inside your repository:

```
your-notes-repo/
└── notes/
    ├── system-design.md
    ├── frontend.md
    └── ai.md
```

---

## How it works

The project is a small Python package under `src/notes_maker/`:

| Module          | Responsibility                                                        |
| --------------- | --------------------------------------------------------------------- |
| `cli.py`        | Entry point; wires the interactive flow together.                     |
| `config.py`     | Global config dir, the shared `.env`, API key & repo path prompts.    |
| `extract.py`    | Fetches article URLs (BeautifulSoup) and reads pasted raw text.       |
| `youtube.py`    | Parses the video id from a link and fetches its transcript.           |
| `summarize.py`  | Sends content to Gemini and returns Markdown.                         |
| `prompts.py`    | The system prompts (separate ones for articles vs. YouTube).          |
| `notes.py`      | The `notes/` directory, file selection, and Table-of-Contents index.  |
| `git_ops.py`    | `git init` / `add` / `commit` / `push` of the notes repo.             |

### YouTube handling

YouTube input uses [`youtube-transcript-api`](https://pypi.org/project/youtube-transcript-api/)
to pull the transcript by video id, then a **dedicated notes-oriented prompt** that tells
Gemini the text is a raw, unpunctuated transcript, to ignore sponsor reads / promos /
banter, and to produce proper study notes rather than a shallow summary.

---

## Customizing

- **Change the Gemini model:** edit `MODEL` in `src/notes_maker/config.py`
  (default: `gemini-2.5-flash`).
- **Change the tone/structure of notes:** edit the prompts in `src/notes_maker/prompts.py`
  (`ARTICLE_SYSTEM_PROMPT` and `YOUTUBE_SYSTEM_PROMPT`).
- **Adjust creativity:** the `temperature` is set in `src/notes_maker/summarize.py`.

After editing, reinstall from your local checkout:

```bash
uv tool install --force .
```

---

## Development

```bash
git clone https://github.com/Afnan-Ahmad961/notes-maker
cd notes-maker
uv sync
uv run notes-maker
```
