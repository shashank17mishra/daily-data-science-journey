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

def test_validator_run_pytest_validation_includes_failure_details(tmp_path):
    from unittest.mock import patch, MagicMock
    val = TaskValidator(repo_root=tmp_path)
    test_file = tmp_path / "tests" / "test_sample.py"
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_text("def test_fail(): assert False\n")

    mock_res = MagicMock(
        returncode=1,
        stdout="FAILED tests/test_sample.py::test_fail - assert False\nassert False",
        stderr=""
    )
    with patch("src.automation.validator.subprocess.run", return_value=mock_res):
        with pytest.raises(RuntimeError) as exc_info:
            val.run_pytest_validation([test_file])
        err_msg = str(exc_info.value)
        assert "exit code 1" in err_msg
        assert "FAILED tests/test_sample.py::test_fail" in err_msg

