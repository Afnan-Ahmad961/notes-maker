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


def _describe(result: subprocess.CompletedProcess) -> str:
    """Best available explanation for a failed git command (git often uses stdout)."""
    return (
        result.stderr.strip()
        or result.stdout.strip()
        or f"git exited with code {result.returncode}"
    )


def _current_branch(repo_dir: Path) -> str:
    return _run(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo_dir).stdout.strip() or "HEAD"


def _push(repo_dir: Path) -> bool:
    """Push, transparently setting the upstream on the first push of a branch."""
    print("Running: git push")
    result = _run(["git", "push"], repo_dir)

    combined = result.stdout + result.stderr
    if result.returncode != 0 and ("no upstream" in combined or "set-upstream" in combined):
        branch = _current_branch(repo_dir)
        print(f"No upstream set — retrying: git push -u origin {branch}")
        result = _run(["git", "push", "-u", "origin", branch], repo_dir)
        combined = result.stdout + result.stderr

    if result.returncode == 0:
        print("Changes committed and pushed successfully!")
        return True

    if "No configured push destination" in combined or "does not appear to be a git repository" in combined:
        print("No git remote is configured for this notes repository.")
        print("Add one and re-run, e.g.:  git remote add origin <your-repo-url>")
    else:
        print(f"Git error (push):\n{_describe(result)}")
    print("Your notes are committed locally; run 'git push' once the remote is fixed.")
    return False


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
    pathspec = rel.as_posix()  # git expects forward slashes on every platform

    print(f"Running: git add -- {pathspec}")
    add = _run(["git", "add", "--", pathspec], repo_dir)
    if add.returncode != 0:
        print(f"Git error (add):\n{_describe(add)}")
        return False

    print("Running: git commit")
    msg = f"notes: auto-update {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    commit = _run(["git", "commit", "-m", msg], repo_dir)
    if commit.returncode != 0:
        # `git commit` returns non-zero when there's nothing staged — not a failure;
        # fall through to push so any earlier unpushed commits still sync.
        if "nothing to commit" in (commit.stdout + commit.stderr):
            print("Nothing new to commit.")
        else:
            print(f"Git error (commit):\n{_describe(commit)}")
            return False

    return _push(repo_dir)
