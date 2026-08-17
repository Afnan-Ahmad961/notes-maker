"""Git automation for the notes repository."""

import subprocess
from datetime import datetime
from pathlib import Path


# Every git invocation is bounded so a hung network push can't block forever.
GIT_TIMEOUT = 120  # seconds


def _run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=GIT_TIMEOUT
        )
    except subprocess.TimeoutExpired:
        # Surface as a normal failure so the caller's error path handles it.
        return subprocess.CompletedProcess(
            cmd,
            returncode=124,
            stdout="",
            stderr=f"git command timed out after {GIT_TIMEOUT}s: {' '.join(cmd)}",
        )


def is_git_repo(repo_dir: Path) -> bool:
    return _run(["git", "rev-parse", "--is-inside-work-tree"], repo_dir).returncode == 0


def ensure_git_repo(repo_dir: Path) -> bool:
    """Ensure ``repo_dir`` is a git repo, initializing one if needed. Returns success."""
    if is_git_repo(repo_dir):
        return True
    print(f"Initializing a new git repository in {repo_dir}")
    result = _run(["git", "init"], repo_dir)
    if result.returncode != 0:
        print(f"Git error: {result.stderr.strip()}")
        return False
    return True


def commit_and_push(repo_dir: Path, target_file: Path) -> bool:
    """Stage the target note file, commit and push. Returns True on success."""
    if not ensure_git_repo(repo_dir):
        return False

    # Stage only the file we just wrote, and only if it lives inside the repo.
    try:
        rel = target_file.resolve().relative_to(repo_dir.resolve())
    except ValueError:
        print(f"Refusing to stage {target_file}: it is outside {repo_dir}.")
        return False

    commands = [
        ["git", "add", str(rel)],
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
                return True
            print(f"Git error: {result.stderr.strip()}")
            if cmd[1] == "push":
                print(
                    "Push failed. Ensure a remote is configured "
                    "(git remote add origin <url>) and run 'git push' later."
                )
            return False

    print("Changes committed and pushed successfully!")
    return True
