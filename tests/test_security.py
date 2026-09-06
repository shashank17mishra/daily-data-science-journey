import pytest
from pathlib import Path
from src.automation.security import SecurityScanner

def test_security_scanner_clean_content():
    scanner = SecurityScanner()
    findings = scanner.scan_content("def add(a, b):\n    return a + b\n")
    assert len(findings) == 0

def test_security_scanner_detects_gemini_key():
    scanner = SecurityScanner()
    fake_key = "AIzaSy" + "A" * 33
    findings = scanner.scan_content(f"GEMINI_API_KEY = '{fake_key}'")
    assert len(findings) > 0
    assert "Google Gemini API Key" in findings[0]

def test_security_scanner_detects_github_pat():
    scanner = SecurityScanner()
    fake_pat = "ghp_" + "x" * 36
    findings = scanner.scan_content(f"token = '{fake_pat}'")
    assert len(findings) > 0
    assert "GitHub Personal Access Token" in findings[0]

def test_security_scanner_forbidden_files(tmp_path):
    scanner = SecurityScanner()
    env_file = tmp_path / ".env"
    env_file.write_text("SECRET=123")
    findings = scanner.scan_file(env_file)
    assert len(findings) > 0
    assert "Forbidden file detected" in findings[0]
