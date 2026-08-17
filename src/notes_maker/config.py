"""Global configuration: config directory, the shared .env, API key and repo path.

Everything Notes Maker remembers between runs lives in a single global ``.env``
inside the OS-standard user config directory (see :func:`config_dir`). Change the
:data:`MODEL` constant below to switch the Gemini model used for summaries.
"""

import os
from pathlib import Path

import questionary
from dotenv import load_dotenv, set_key
from platformdirs import user_config_dir

APP_NAME = "notes-maker"

# ── The Gemini model used for every summary. Change this to switch models. ────
MODEL = "gemini-2.5-flash"

# Keys stored in the global .env
GEMINI_API_KEY = "GEMINI_API_KEY"
NOTES_REPO_PATH = "NOTES_REPO_PATH"


def config_dir() -> Path:
    """Return the global config directory, creating it if necessary."""
    path = Path(user_config_dir(APP_NAME))
    path.mkdir(parents=True, exist_ok=True)
    return path


def env_path() -> Path:
    """Path to the global .env that stores the API key and repo path."""
    return config_dir() / ".env"


def load() -> None:
    """Load the global .env into the process environment (creating it if missing)."""
    path = env_path()
    if not path.exists():
        path.touch()
    load_dotenv(path, override=True)


def _save(key: str, value: str) -> None:
    set_key(str(env_path()), key, value)
    os.environ[key] = value


def ensure_api_key() -> str:
    """Return a valid Gemini API key, prompting and saving it on first run."""
    key = os.getenv(GEMINI_API_KEY)
    if key and key.strip() and key != "your_api_key_here.":
        return key.strip()

    print("No Gemini API key found. Create one at https://aistudio.google.com/apikey")
    key = questionary.password("Paste your Gemini API key:").ask()
    if not key or not key.strip():
        print("A Gemini API key is required. Exiting.")
        raise SystemExit(1)

    key = key.strip()
    _save(GEMINI_API_KEY, key)
    print(f"Saved to {env_path()}")
    return key


def ensure_repo_path() -> Path:
    """Return the configured notes repository path, prompting on first run."""
    raw = os.getenv(NOTES_REPO_PATH)
    if raw and raw.strip():
        path = Path(raw).expanduser()
        path.mkdir(parents=True, exist_ok=True)
        return path

    print("First-time setup: choose where your notes repository lives.")
    print("Tip: point this at a git repo with a GitHub remote so notes can be pushed.")
    raw = questionary.path("Notes Repository Path:").ask()
    if not raw or not raw.strip():
        print("A notes repository path is required. Exiting.")
        raise SystemExit(1)

    path = Path(raw.strip()).expanduser().resolve()
    path.mkdir(parents=True, exist_ok=True)
    _save(NOTES_REPO_PATH, str(path))
    print(f"Notes repository set to {path}")
    return path
