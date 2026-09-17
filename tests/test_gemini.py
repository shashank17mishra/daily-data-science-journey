import pytest
from unittest.mock import MagicMock, patch
from src.automation.gemini import (
    extract_json_str,
    parse_gemini_json,
    generate_daily_task,
    is_transient_error,
    TaskPayload
)

def test_extract_json_str_markdown():
    text = "Here is the response:\n```json\n{\"title\": \"Day 16\"}\n```\nHope that helps!"
    assert extract_json_str(text) == '{"title": "Day 16"}'

def test_extract_json_str_no_fences():
    text = "Prefix {\"title\": \"Day 16\"} suffix"
    assert extract_json_str(text) == '{"title": "Day 16"}'

def test_parse_gemini_json_clean():
    sample = {
        "title": "Day 016: Dataclasses & Structured Data",
        "category": "python",
        "description": "Exercise description",
        "learning_objectives": ["Obj 1"],
        "files": [{"path": "learning/python/day_016.py", "content": "print('hello')"}],
        "explanation": "Notes",
        "commit_message": "day-016: practice"
    }
    import json
    raw = json.dumps(sample)
    parsed = parse_gemini_json(raw)
    assert parsed["title"] == sample["title"]
    assert len(parsed["files"]) == 1

def test_parse_gemini_json_with_control_characters():
    # Simulate unescaped raw newlines and tabs inside strings (the exact error from Gemini)
    raw = '{\n  "title": "Day 016: Dataclasses",\n  "files": [\n    {\n      "path": "learning/day_16.py",\n      "content": "line1' + chr(10) + 'line2\twith tab"\n    }\n  ]\n}'
    parsed = parse_gemini_json(raw)
    assert parsed["files"][0]["content"] == "line1\nline2\twith tab"

def test_parse_gemini_json_with_invalid_backslash_escapes():
    # Python regex with unescaped backslashes inside JSON string: \d+ and \s+
    raw = '{"content": "pattern = re.compile(r\'' + chr(92) + 'd+' + chr(92) + 's+\')"}'
    parsed = parse_gemini_json(raw)
    assert "\\d+\\s+" in parsed["content"]

def test_parse_gemini_json_with_trailing_commas():
    raw = '{"title": "Day 16", "learning_objectives": ["Item 1", "Item 2", ], }'
    parsed = parse_gemini_json(raw)
    assert len(parsed["learning_objectives"]) == 2

def test_parse_gemini_json_empty_raises():
    with pytest.raises(ValueError, match="empty response"):
        parse_gemini_json("")
    with pytest.raises(ValueError, match="empty response"):
        parse_gemini_json("   ")

def test_parse_gemini_json_invalid_raises():
    with pytest.raises(ValueError, match="Invalid JSON response"):
        parse_gemini_json("not json at all {broken")

def test_generate_daily_task_missing_api_key():
    with patch.dict("os.environ", {}, clear=True):
        with pytest.raises(ValueError, match="GEMINI_API_KEY environment variable is not set"):
            generate_daily_task(
                day=16,
                category="python",
                topic="Dataclasses",
                difficulty="Intermediate",
                learning_objectives=[],
                expected_output=""
            )

def test_generate_daily_task_mocked_success():
    mock_client = MagicMock()
    mock_response = MagicMock()
    # Response contains raw unescaped newline in content
    mock_response.text = '```json\n{\n  "title": "Day 016: Dataclasses",\n  "category": "python",\n  "description": "Desc",\n  "learning_objectives": ["Obj1"],\n  "files": [{"path": "learning/python/day_016.py", "content": "from dataclasses import dataclass' + chr(10) + '@dataclass\nclass Item: pass"}],\n  "explanation": "Notes",\n  "commit_message": "day-016: dataclasses"\n}\n```'
    mock_client.models.generate_content.return_value = mock_response

    with patch("google.genai.Client", return_value=mock_client):
        result = generate_daily_task(
            day=16,
            category="python",
            topic="Dataclasses & Structured Data",
            difficulty="Intermediate",
            learning_objectives=["Master dataclasses"],
            expected_output="Python code and tests",
            api_key="fake-test-key"
        )
        assert result["title"] == "Day 016: Dataclasses"
        assert "@dataclass" in result["files"][0]["content"]
        assert mock_client.models.generate_content.called

def test_is_transient_error():
    assert is_transient_error(Exception("503 UNAVAILABLE: High demand"))
    assert is_transient_error(Exception("429 RESOURCE_EXHAUSTED: Quota exceeded"))
    assert is_transient_error(Exception("500 Internal Server Error"))
    assert is_transient_error(Exception("504 Gateway Timeout"))
    assert not is_transient_error(ValueError("Invalid argument value"))

def test_generate_daily_task_with_feedback():
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = '{"title": "Day 020", "category": "python", "description": "Desc", "learning_objectives": [], "files": [{"path": "learning/python/day_020.py", "content": "print(1)"}], "explanation": "Notes", "commit_message": "day-020: fix"}'
    mock_client.models.generate_content.return_value = mock_response

    with patch("google.genai.Client", return_value=mock_client):
        result = generate_daily_task(
            day=20,
            category="python",
            topic="CSV Parsing",
            difficulty="Intermediate",
            learning_objectives=[],
            expected_output="",
            api_key="fake-test-key",
            feedback="Syntax error on line 7"
        )
        assert result["title"] == "Day 020"
        call_args = mock_client.models.generate_content.call_args
        contents = call_args.kwargs.get("contents", "")
        assert "CRITICAL FIX REQUIRED" in contents
        assert "Syntax error on line 7" in contents

def test_generate_daily_task_transient_retry():
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = '{"title": "Day 020", "category": "python", "description": "Desc", "learning_objectives": [], "files": [{"path": "learning/python/day_020.py", "content": "print(1)"}], "explanation": "Notes", "commit_message": "day-020: fix"}'

    # First call fails with 503 UNAVAILABLE, second succeeds
    mock_client.models.generate_content.side_effect = [
        Exception("503 UNAVAILABLE: High demand"),
        mock_response
    ]

    with patch("google.genai.Client", return_value=mock_client), patch("time.sleep") as mock_sleep:
        result = generate_daily_task(
            day=20,
            category="python",
            topic="CSV Parsing",
            difficulty="Intermediate",
            learning_objectives=[],
            expected_output="",
            api_key="fake-test-key"
        )
        assert result["title"] == "Day 020"
        assert mock_client.models.generate_content.call_count == 2
        assert mock_sleep.called

