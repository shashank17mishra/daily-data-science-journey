import ast
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from src.automation.utils import get_repo_root, logger
from src.automation.security import SecurityScanner

class TaskValidator:
    """Performs multi-stage code, syntax, test, security, and diff validation."""

    def __init__(self, repo_root: Optional[Path] = None):
        self.repo_root = repo_root or get_repo_root()
        self.security_scanner = SecurityScanner()

    def validate_payload_structure(self, task_data: Dict[str, Any]) -> None:
        """Validates that task_data has required fields."""
        required_fields = ["title", "category", "description", "files", "commit_message"]
        for field in required_fields:
            if field not in task_data or not task_data[field]:
                raise ValueError(f"Task payload missing required field: '{field}'")

        files = task_data.get("files", [])
        if not isinstance(files, list) or len(files) == 0:
            raise ValueError("Task payload must include at least one file entry.")

        for f in files:
            if "path" not in f or "content" not in f:
                raise ValueError("File entry missing 'path' or 'content' key.")
            if not f["content"].strip():
                raise ValueError(f"Generated file '{f.get('path')}' is empty.")

    def validate_python_syntax(self, file_path: Path) -> None:
        """Compiles python file with AST to catch syntax errors."""
        if file_path.suffix != ".py":
            return
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
            ast.parse(source, filename=str(file_path))
            logger.info(f"Python syntax valid: {file_path.name}")
        except SyntaxError as e:
            logger.error(f"Syntax error in {file_path}: {e}")
            raise ValueError(f"Syntax error in generated code file '{file_path.name}': {e}")

    def run_pytest_validation(self, file_paths: List[Path]) -> None:
        """Runs pytest on any test files in the file_paths or test directory."""
        test_files = [str(p) for p in file_paths if p.name.startswith("test_") or p.parent.name == "tests"]
        
        # If no test files were modified directly, run pytest on tests/ directory if it exists
        if not test_files and (self.repo_root / "tests").exists():
            test_files = [str(self.repo_root / "tests")]

        if not test_files:
            logger.info("No test files found for pytest execution.")
            return

        logger.info(f"Running pytest verification on: {test_files}")
        cmd = [sys.executable, "-m", "pytest"] + test_files + ["-v", "--tb=short"]
        
        res = subprocess.run(cmd, cwd=str(self.repo_root), capture_output=True, text=True)
        if res.returncode != 0:
            logger.error(f"Pytest verification failed:\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}")
            raise RuntimeError(f"Pytest verification failed with exit code {res.returncode}")
        
        logger.info("Pytest verification PASSED.")

    def scan_security(self, file_paths: List[Path]) -> None:
        """Scans updated files for secret patterns."""
        for path in file_paths:
            findings = self.security_scanner.scan_file(path)
            if findings:
                raise ValueError(f"Security validation failed for {path.name}: {'; '.join(findings)}")
        logger.info("Security scan PASSED cleanly.")

    def validate_all(self, task_data: Dict[str, Any], written_paths: List[Path]) -> None:
        """Executes full validation pipeline."""
        logger.info("Starting validation pipeline...")
        self.validate_payload_structure(task_data)

        for path in written_paths:
            if not path.exists():
                raise FileNotFoundError(f"Expected generated file missing: {path}")
            if path.stat().st_size == 0:
                raise ValueError(f"Generated file is empty: {path}")
            self.validate_python_syntax(path)

        self.scan_security(written_paths)
        self.run_pytest_validation(written_paths)
        logger.info("All validations completed successfully!")
