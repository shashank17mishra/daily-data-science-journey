import pytest
from pathlib import Path
from src.automation.validator import TaskValidator

def test_validator_payload_structure():
    val = TaskValidator()
    invalid_payload = {"title": "Incomplete"}
    with pytest.raises(ValueError, match="missing required field"):
        val.validate_payload_structure(invalid_payload)

def test_validator_python_syntax(tmp_path):
    val = TaskValidator(repo_root=tmp_path)
    good_file = tmp_path / "good.py"
    good_file.write_text("x = 1 + 2\n")
    val.validate_python_syntax(good_file)  # Should pass without error

    bad_file = tmp_path / "bad.py"
    bad_file.write_text("def broken_func(\n")
    with pytest.raises(ValueError, match="Syntax error"):
        val.validate_python_syntax(bad_file)
