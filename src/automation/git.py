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

    def ensure_git_identity(self) -> None:
        """Configures git user.name and user.email for CI environments."""
        if os.getenv("GITHUB_ACTIONS") == "true":
            author_name = os.getenv("GIT_AUTHOR_NAME", "shashank mishra")
            author_email = os.getenv("GIT_AUTHOR_EMAIL", "shashank17oct2003@gmail.com")
            self._run(["git", "config", "user.name", author_name])
            self._run(["git", "config", "user.email", author_email])

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

    def stage_and_commit(self, file_paths: List[Path], message: str) -> bool:
        """
        Stages specific files and creates a commit if staged changes exist.
        Returns True if a commit was created.
        """
        if not file_paths:
            return False

        bad_messages = {"update", "test", "daily commit", "random changes", "commit"}
        clean_msg = message.strip()
        if clean_msg.lower() in bad_messages or len(clean_msg) < 5:
            raise ValueError(f"Invalid or generic commit message rejected: '{message}'")

        rel_paths = []
        for p in file_paths:
            try:
                rel = str(p.relative_to(self.repo_root))
            except ValueError:
                rel = str(p)
            rel_paths.append(rel)

        self._run(["git", "add"] + rel_paths)
        staged = self._run(["git", "diff", "--cached", "--name-only"])
        if not staged:
            logger.warning(f"No staged changes for '{clean_msg}'. Skipping commit.")
            return False

        self.ensure_git_identity()
        logger.info(f"Creating commit: '{clean_msg}'")
        self._run(["git", "commit", "-m", clean_msg])
        logger.info(f"Successfully created commit: '{clean_msg}'")
        return True

    def commit(self, message: str) -> bool:
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
            return False

        logger.info(f"Creating commit: '{clean_msg}'")
        self.ensure_git_identity()
        self._run(["git", "commit", "-m", clean_msg])
        logger.info("Git commit created successfully.")
        return True

    def create_daily_commits(
        self,
        day: int,
        topic: str,
        category: str,
        written_paths: List[Path]
    ) -> int:
        """
        Creates 4 structured, semantic commits for the daily task:
        1. feat: Implementation code file
        2. test: Unit test suite
        3. docs: Study notes and concepts
        4. chore: Progress tracker update
        """
        self.ensure_git_identity()
        created_count = 0

        # Separate files by role
        impl_files = []
        test_files = []
        doc_files = []

        for p in written_paths:
            p_str = str(p).replace("\\", "/")
            if "test_" in p.name or "/tests/" in p_str:
                test_files.append(p)
            elif p.suffix == ".md" or "notes" in p.name:
                doc_files.append(p)
            else:
                impl_files.append(p)

        progress_path = self.repo_root / "progress.json"

        # Commit 1: Implementation code
        if impl_files:
            msg = f"feat(day-{day:03d}): implement {topic} in {category}"
            if self.stage_and_commit(impl_files, msg):
                created_count += 1

        # Commit 2: Unit test suite
        if test_files:
            msg = f"test(day-{day:03d}): add unit test suite for {topic}"
            if self.stage_and_commit(test_files, msg):
                created_count += 1

        # Commit 3: Documentation and study notes
        if doc_files:
            msg = f"docs(day-{day:03d}): add study notes and concept overview for {topic}"
            if self.stage_and_commit(doc_files, msg):
                created_count += 1

        # Commit 4: Progress Tracker
        if progress_path.exists():
            msg = f"chore(day-{day:03d}): update progress tracker for day {day}"
            if self.stage_and_commit([progress_path], msg):
                created_count += 1

        # Fallback if any uncommitted changes remain
        if not self.is_working_tree_clean():
            self._run(["git", "add", "-A"])
            staged = self._run(["git", "diff", "--cached", "--name-only"])
            if staged:
                msg = f"chore(day-{day:03d}): finalize learning artifacts for day {day}"
                if self.commit(msg):
                    created_count += 1

        return created_count

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
