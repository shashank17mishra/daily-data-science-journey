import pytest
from pathlib import Path
from src.automation.generator import TaskGenerator, sanitize_code_content

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

def test_sanitize_code_content_enclosed_fences():
    raw_code = "```python\ndef test_fn():\n    assert 1 + 1 == 2\n```"
    cleaned = sanitize_code_content("tests/test_sample.py", raw_code)
    assert cleaned == "def test_fn():\n    assert 1 + 1 == 2"

def test_sanitize_code_content_preamble():
    raw_code = "Here is the implementation:\n```python\nx = 10\ny = 20\n```"
    cleaned = sanitize_code_content("learning/python/day_020.py", raw_code)
    assert "Here is the implementation" not in cleaned
    assert "x = 10\ny = 20" in cleaned

def test_sanitize_code_content_stray_fences():
    raw_code = "# Header comment\n```python\nx = 10\n```\n# Footer"
    cleaned = sanitize_code_content("learning/python/day_020.py", raw_code)
    assert "```" not in cleaned
    assert "x = 10" in cleaned

def test_task_generator_cleanup_files(tmp_path):
    gen = TaskGenerator(repo_root=tmp_path)
    file1 = tmp_path / "learning" / "python" / "test1.py"
    file1.parent.mkdir(parents=True, exist_ok=True)
    file1.write_text("print('temp')")
    assert file1.exists()

    gen.cleanup_files([file1])
    assert not file1.exists()

