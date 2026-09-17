import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from src.automation.main import run_daily_automation

def test_run_daily_automation_self_healing_retry(tmp_path):
    repo_root = tmp_path
    (repo_root / "learning" / "python").mkdir(parents=True, exist_ok=True)
    (repo_root / "tests").mkdir(parents=True, exist_ok=True)

    # Valid task spec in roadmap
    sample_roadmap = [
        {
            "day": 20,
            "category": "python",
            "topic": "CSV Parsing",
            "difficulty": "Intermediate",
            "learning_objectives": ["Parse CSV"],
            "expected_output": "code"
        }
    ]
    import json
    (repo_root / "roadmap.json").write_text(json.dumps(sample_roadmap), encoding="utf-8")
    (repo_root / "progress.json").write_text(json.dumps({"completed_days": [19], "current_day": 20}), encoding="utf-8")

    # Attempt 1: bad python syntax in test file
    bad_payload = {
        "title": "Day 020: CSV Parsing",
        "category": "python",
        "description": "Desc",
        "learning_objectives": ["Obj"],
        "files": [
            {"path": "learning/python/day_020_csv.py", "content": "x = 10\n"},
            {"path": "tests/test_day_020_csv.py", "content": "def broken(\n"}
        ],
        "explanation": "Notes",
        "commit_message": "day-020: test"
    }

    # Attempt 2: valid python syntax
    good_payload = {
        "title": "Day 020: CSV Parsing",
        "category": "python",
        "description": "Desc",
        "learning_objectives": ["Obj"],
        "files": [
            {"path": "learning/python/day_020_csv.py", "content": "x = 10\n"},
            {"path": "tests/test_day_020_csv.py", "content": "def test_ok(): assert True\n"}
        ],
        "explanation": "Notes",
        "commit_message": "day-020: test"
    }

    generate_mock = MagicMock(side_effect=[bad_payload, good_payload])

    with patch("src.automation.utils.get_repo_root", return_value=repo_root), \
         patch("src.automation.main.generate_daily_task", generate_mock), \
         patch("src.automation.validator.subprocess.run") as mock_sub:
        mock_sub.return_value = MagicMock(returncode=0, stdout="", stderr="")

        exit_code = run_daily_automation(dry_run=True, force_day=20, force_run=True)

        assert exit_code == 0
        assert generate_mock.call_count == 2
        # Check that attempt 2 received feedback about syntax error from attempt 1
        second_call_kwargs = generate_mock.call_args_list[1].kwargs
        feedback = second_call_kwargs.get("feedback")
        assert isinstance(feedback, str)
        assert "Syntax error" in feedback

def test_run_daily_automation_all_attempts_fail_clean_disk(tmp_path):
    repo_root = tmp_path
    (repo_root / "learning" / "python").mkdir(parents=True, exist_ok=True)
    (repo_root / "tests").mkdir(parents=True, exist_ok=True)

    sample_roadmap = [
        {
            "day": 20,
            "category": "python",
            "topic": "CSV Parsing",
            "difficulty": "Intermediate",
            "learning_objectives": ["Parse CSV"],
            "expected_output": "code"
        }
    ]
    import json
    (repo_root / "roadmap.json").write_text(json.dumps(sample_roadmap), encoding="utf-8")
    (repo_root / "progress.json").write_text(json.dumps({"completed_days": [19], "current_day": 20}), encoding="utf-8")

    bad_payload = {
        "title": "Day 020: CSV Parsing",
        "category": "python",
        "description": "Desc",
        "learning_objectives": ["Obj"],
        "files": [
            {"path": "learning/python/day_020_csv.py", "content": "x = 10\n"},
            {"path": "tests/test_day_020_csv.py", "content": "def broken(\n"}
        ],
        "explanation": "Notes",
        "commit_message": "day-020: test"
    }

    generate_mock = MagicMock(return_value=bad_payload)

    with patch("src.automation.utils.get_repo_root", return_value=repo_root), \
         patch("src.automation.main.generate_daily_task", generate_mock):

        exit_code = run_daily_automation(dry_run=True, force_day=20, force_run=True)

        assert exit_code == 1
        assert generate_mock.call_count == 3
        # Ensure temporary files were cleaned up from disk
        assert not (repo_root / "learning" / "python" / "day_020_csv.py").exists()
        assert not (repo_root / "tests" / "test_day_020_csv.py").exists()
