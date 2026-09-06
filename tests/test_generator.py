import pytest
from pathlib import Path
from src.automation.generator import TaskGenerator

def test_task_generator_valid(tmp_path):
    gen = TaskGenerator(repo_root=tmp_path)
    task_payload = {
        "title": "Day 001 Test",
        "files": [
            {
                "path": "learning/python/day_001.py",
                "content": "print('hello world')"
            }
        ]
    }
    written = gen.write_task_files(task_payload)
    assert len(written) == 1
    assert written[0].exists()
    assert written[0].read_text().strip() == "print('hello world')"

def test_task_generator_forbidden_path(tmp_path):
    gen = TaskGenerator(repo_root=tmp_path)
    task_payload = {
        "files": [
            {
                "path": "src/automation/hacked.py",
                "content": "bad"
            }
        ]
    }
    with pytest.raises(ValueError, match="Forbidden file target"):
        gen.write_task_files(task_payload)
