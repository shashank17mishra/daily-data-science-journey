import os
import subprocess
from pathlib import Path
from typing import List
from src.automation.utils import get_repo_root, logger

class GitAutomation:
    """Safe Git wrapper for staging, committing, and conditional pushing."""

    def __init__(self, repo_root: Path = None):
        self.repo_root = repo_root or get_repo_root()

    def _run(self, cmd: List[str]) -> str:
        """Executes a git command and returns stdout."""
        res = subprocess.run(cmd, cwd=str(self.repo_root), capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Git command {' '.join(cmd)} failed:\nSTDERR: {res.stderr}")
        return res.stdout.strip()

    def check_git_installed(self) -> bool:
        """Verifies git CLI is installed and responsive."""
        try:
            out = self._run(["git", "--version"])
            logger.info(f"Git environment: {out}")
            return True
        except Exception as e:
            logger.error(f"Git command check failed: {e}")
            return False

    def is_working_tree_clean(self) -> bool:
        """Returns True if git status has no uncommitted changes."""
        status = self._run(["git", "status", "--porcelain"])
        return len(status) == 0

    def stage_files(self, file_paths: List[Path]) -> None:
        """Stages specified files and progress tracking file."""
        if not file_paths:
            raise ValueError("No files provided to stage.")

        rel_paths = [str(p.relative_to(self.repo_root)) for p in file_paths]
        
        # Always stage progress.json if present
        progress_path = self.repo_root / "progress.json"
        if progress_path.exists():
            rel_paths.append("progress.json")

        logger.info(f"Staging files: {rel_paths}")
        self._run(["git", "add"] + rel_paths)

    def commit(self, message: str) -> None:
        """
        Creates git commit with descriptive message.
        Guarantees non-empty commit.
        """
        bad_messages = {"update", "test", "daily commit", "random changes", "commit"}
        clean_msg = message.strip()
        if clean_msg.lower() in bad_messages or len(clean_msg) < 5:
            raise ValueError(f"Invalid or generic commit message rejected: '{message}'")

        # Check if there are staged changes
        staged = self._run(["git", "diff", "--cached", "--name-only"])
        if not staged:
            logger.warning("No staged changes found. Skipping commit creation.")
            return

        logger.info(f"Creating commit: '{clean_msg}'")
        
        # Configure git identity in CI if not set
        if os.getenv("GITHUB_ACTIONS") == "true":
            self._run(["git", "config", "user.name", "github-actions[bot]"])
            self._run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"])

        self._run(["git", "commit", "-m", clean_msg])
        logger.info("Git commit created successfully.")

    def push(self) -> None:
        """
        Pushes changes to remote origin ONLY when inside GitHub Actions workflow.
        """
        is_ci = os.getenv("GITHUB_ACTIONS") == "true"
        if not is_ci:
            logger.info("Local environment detected. Skipping git push.")
            return

        logger.info("GitHub Actions CI environment detected. Pushing commit to remote repository...")
        self._run(["git", "push", "origin", "HEAD"])
        logger.info("Git push completed successfully.")
