"""Git automation for the notes repository."""

import subprocess
from datetime import datetime
from pathlib import Path


def _run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def is_git_repo(repo_dir: Path) -> bool:
    return _run(["git", "rev-parse", "--is-inside-work-tree"], repo_dir).returncode == 0


def ensure_git_repo(repo_dir: Path) -> None:
    if is_git_repo(repo_dir):
        return
    print(f"Initializing a new git repository in {repo_dir}")
    _run(["git", "init"], repo_dir)


def commit_and_push(repo_dir: Path) -> None:
    """Stage, commit and push everything in the notes repository."""
    ensure_git_repo(repo_dir)

    commands = [
        ["git", "add", "."],
        ["git", "commit", "-m", f"notes: auto-update {datetime.now().strftime('%Y-%m-%d %H:%M')}"],
        ["git", "push"],
    ]

    for cmd in commands:
        print(f"Running: {' '.join(cmd)}")
        result = _run(cmd, repo_dir)
        if result.returncode != 0:
            # `git commit` returns 1 when there's nothing to commit — that's fine.
            if cmd[1] == "commit" and "nothing to commit" in result.stdout:
                print("Nothing new to commit.")
                return
            print(f"Git error: {result.stderr.strip()}")
            if cmd[1] == "push":
                print(
                    "Push failed. Ensure a remote is configured "
                    "(git remote add origin <url>) and run 'git push' later."
                )
            return

    print("Changes committed and pushed successfully!")
