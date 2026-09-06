import re
import os
from pathlib import Path
from typing import List, Tuple
from src.automation.utils import logger

# Regex patterns for detecting common secrets and API tokens
SECRET_PATTERNS = [
    (r"AIzaSy[A-Za-z0-9_-]{33}", "Google Gemini API Key"),
    (r"ghp_[A-Za-z0-9]{36}", "GitHub Personal Access Token (Classic)"),
    (r"github_pat_[A-Za-z0-9]{22}_[A-Za-z0-9]{59}", "GitHub Fine-Grained Personal Access Token"),
    (r"gho_[A-Za-z0-9]{36}", "GitHub OAuth Access Token"),
    (r"ghs_[A-Za-z0-9]{36}", "GitHub App Secret"),
    (r"-----BEGIN (RSA|EC|DSA|OPENSSH|PRIVATE) KEY-----", "Private Key Header"),
    (r"AKIA[0-9A-Z]{16}", "AWS Access Key ID"),
    (r"(?i)api[_-]?key\s*[:=]\s*['\"]?([A-Za-z0-9_\-]{16,})['\"]?", "Generic API Key assignment"),
    (r"(?i)password\s*[:=]\s*['\"]?([^'\"\s]{8,})['\"]?", "Hardcoded Password assignment"),
    (r"(?i)secret[_-]?key\s*[:=]\s*['\"]?([^'\"\s]{16,})['\"]?", "Secret Key assignment"),
    (r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}", "JSON Web Token (JWT)")
]

FORBIDDEN_FILENAME_PATTERNS = [
    r"^\.env.*$",
    r"^.*\.pem$",
    r"^.*\.key$",
    r"^.*id_rsa.*$"
]

FORBIDDEN_DIR_NAMES = {"secrets", "credentials", ".venv", "__pycache__"}

class SecurityScanner:
    """Basic secret scanner to prevent accidental leakage of sensitive credentials."""

    def scan_content(self, content: str, filename: str = "") -> List[str]:
        """Scans string content for secret patterns."""
        findings = []
        for pattern, desc in SECRET_PATTERNS:
            matches = re.findall(pattern, content)
            if matches:
                # Do NOT log the secret itself!
                findings.append(f"Detected potential {desc} pattern in '{filename}'")
        return findings

    def scan_file(self, file_path: Path) -> List[str]:
        """Scans a single file for secret patterns and forbidden name rules."""
        findings = []
        if not file_path.exists() or not file_path.is_file():
            return findings

        # Check filename pattern
        name = file_path.name
        for pattern in FORBIDDEN_FILENAME_PATTERNS:
            if re.match(pattern, name, re.IGNORECASE):
                findings.append(f"Forbidden file detected: {file_path.relative_to(file_path.anchor)}")

        # Check parent directory names
        for part in file_path.parts:
            if part in FORBIDDEN_DIR_NAMES and part not in {".venv", "__pycache__"}:
                findings.append(f"File located inside forbidden directory '{part}': {file_path}")

        # Scan text content
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            findings.extend(self.scan_content(content, str(file_path)))
        except Exception as e:
            logger.warning(f"Could not read file {file_path} for security scan: {e}")

        return findings

    def scan_directory(self, root_dir: Path) -> List[str]:
        """Scans directory recursively for secrets in trackable source files."""
        all_findings = []
        ignored_dirs = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", "node_modules"}

        for dirpath, dirnames, filenames in os.walk(root_dir):
            dirnames[:] = [d for d in dirnames if d not in ignored_dirs]
            for fname in filenames:
                fpath = Path(dirpath) / fname
                findings = self.scan_file(fpath)
                all_findings.extend(findings)

        return all_findings
