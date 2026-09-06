import os
from pathlib import Path
from typing import Dict, Any, List
from src.automation.utils import get_repo_root, logger

ALLOWED_ROOT_DIRS = {"learning", "projects", "tests"}

class TaskGenerator:
    """Writes generated task files to disk inside authorized directories."""

    def __init__(self, repo_root: Path = None):
        self.repo_root = repo_root or get_repo_root()

    def write_task_files(self, task_data: Dict[str, Any]) -> List[Path]:
        """
        Validates paths and writes file content to disk.
        Returns a list of created absolute Path objects.
        """
        files = task_data.get("files", [])
        if not files:
            raise ValueError("Task data contains no files to write.")

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

            # Write content
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content.strip() + "\n")

            logger.info(f"Successfully wrote file: {full_path.relative_to(self.repo_root)}")
            written_paths.append(full_path)

        return written_paths
