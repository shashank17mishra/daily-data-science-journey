import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from src.automation.utils import get_repo_root, logger

ALLOWED_ROOT_DIRS = {"learning", "projects", "tests"}


def sanitize_code_content(path_str: str, content: str) -> str:
    """
    Cleans up file content before writing:
    - Strips markdown code fences (```python ... ```) if wrapped around code files.
    - Strips intro/preamble markdown fences or stray fence lines.
    - Ensures clean whitespace.
    """
    text = content.strip()
    if path_str.endswith(".py"):
        # Case 1: Entire content enclosed in ```python ... ``` or ``` ... ```
        m = re.match(r"^```(?:python|py)?\s*\n([\s\S]*?)\n```\s*$", text)
        if m:
            text = m.group(1).strip()
        else:
            # Case 2: Code blocks preceded by preamble text (e.g. "Here is the code:\n```python\n...\n```")
            blocks = re.findall(r"```(?:python|py)?\s*\n([\s\S]*?)\n```", text)
            if blocks:
                text = "\n\n".join(b.strip() for b in blocks)
            else:
                # Case 3: Stray markdown fences inside code (e.g. ```python or ``` on isolated lines)
                lines = text.splitlines()
                cleaned = [line for line in lines if not line.strip().startswith("```")]
                text = "\n".join(cleaned)
    return text


class TaskGenerator:
    """Writes generated task files to disk inside authorized directories."""

    def __init__(self, repo_root: Optional[Path] = None):
        self.repo_root = repo_root or get_repo_root()

    def cleanup_files(self, file_paths: List[Path]) -> None:
        """Removes written files from disk if generation or validation fails."""
        for path in file_paths:
            try:
                if path.exists() and path.is_file():
                    path.unlink()
                    try:
                        rel = path.relative_to(self.repo_root)
                    except ValueError:
                        rel = path
                    logger.info(f"Cleaned up file: {rel}")
            except Exception as e:
                logger.warning(f"Failed to cleanup file {path}: {e}")

    def write_task_files(self, task_data: Dict[str, Any]) -> List[Path]:
        """
        Validates paths and writes file content to disk.
        Returns a list of created absolute Path objects.
        """
        files = list(task_data.get("files", []))
        if not files:
            raise ValueError("Task data contains no files to write.")

        # If detailed explanation exists and no markdown file is in files, generate study notes doc
        has_doc = any(f.get("path", "").endswith(".md") for f in files)
        explanation = task_data.get("explanation")
        if not has_doc and explanation:
            category = task_data.get("category", "python")
            title = task_data.get("title", "Daily Practice")
            desc = task_data.get("description", "")
            objectives = task_data.get("learning_objectives", [])

            day_num = None
            for f in files:
                m = re.search(r"day_(\d+)", f.get("path", ""))
                if m:
                    day_num = int(m.group(1))
                    break

            day_prefix = f"day_{day_num:03d}" if day_num is not None else "daily"
            notes_path = f"learning/{category}/{day_prefix}_notes.md"
            obj_list = "\n".join(f"- {o}" for o in objectives) if objectives else "- Core conceptual mastery"
            notes_content = f"# {title}\n\n## Overview\n{desc}\n\n## Objectives\n{obj_list}\n\n## Key Concepts\n{explanation}\n"
            files.append({"path": notes_path, "content": notes_content})

        written_paths = []

        for file_info in files:
            rel_path_str = file_info.get("path")
            content = file_info.get("content", "")

            if not rel_path_str:
                raise ValueError("File entry missing 'path' property.")

            rel_path = Path(rel_path_str)

            # Prevent path traversal attacks
            parts = rel_path.parts
            if not parts or parts[0] not in ALLOWED_ROOT_DIRS:
                raise ValueError(
                    f"Forbidden file target '{rel_path_str}'. Files must reside in {ALLOWED_ROOT_DIRS}."
                )

            full_path = (self.repo_root / rel_path).resolve()

            # Ensure path is within repo_root
            try:
                full_path.relative_to(self.repo_root)
            except ValueError:
                raise ValueError(f"Path traversal detected for file '{rel_path_str}'.")

            # Create parent directories
            full_path.parent.mkdir(parents=True, exist_ok=True)

            # Sanitize and write content
            clean_content = sanitize_code_content(rel_path_str, content)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(clean_content.strip() + "\n")

            logger.info(f"Successfully wrote file: {full_path.relative_to(self.repo_root)}")
            written_paths.append(full_path)

        return written_paths
