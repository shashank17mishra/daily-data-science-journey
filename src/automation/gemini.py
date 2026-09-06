import os
import json
from typing import Dict, Any, Optional
from src.automation.utils import logger

DEFAULT_MODEL = "gemini-2.5-flash"

SYSTEM_PROMPT = """
You are an expert Data Science, AI/ML, and DevOps educator.
Your task is to generate ONE complete, high-quality, practical coding exercise for a daily learning repository.

Return ONLY a valid JSON object strictly matching this format (no markdown fence outside JSON if possible):

{
  "title": "Day XXX: Topic Title",
  "category": "category_name",
  "description": "Detailed explanation of what this exercise implements.",
  "learning_objectives": ["Objective 1", "Objective 2"],
  "files": [
    {
      "path": "learning/category_name/day_XXX_topic.py",
      "content": "# Complete functional Python code with comments and docstrings"
    },
    {
      "path": "tests/test_day_XXX_topic.py",
      "content": "# Complete executable pytest unit tests for the implementation file"
    }
  ],
  "explanation": "Comprehensive breakdown of key concepts and implementation details.",
  "commit_message": "day-XXX: short descriptive git commit message"
}

REQUIREMENTS:
1. Code MUST be readable, follow PEP 8, and be fully functional (not pseudocode, not placeholders).
2. For Python/ML/DS tasks, generate at least one implementation file and one pytest unit test file.
3. NEVER hardcode API keys, credentials, or sensitive data.
4. Keep dependencies minimal and use standard library or common packages (numpy, pandas, scikit-learn, pytest) where standard.
5. All file paths must be relative to repository root.
"""

def generate_daily_task(
    day: int,
    category: str,
    topic: str,
    difficulty: str,
    learning_objectives: list,
    expected_output: str,
    api_key: Optional[str] = None,
    model_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Calls Google Gemini API using the official google-genai SDK to generate structured task files.
    """
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")

    if not model_name:
        model_name = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        raise ImportError("google-genai library is not installed. Install with `pip install google-genai`.")

    logger.info(f"Initializing Gemini API client with model '{model_name}' for Day {day} ({topic}).")
    client = genai.Client(api_key=api_key)

    user_prompt = f"""
Daily Learning Task Details:
- Day Number: {day}
- Category: {category}
- Topic: {topic}
- Difficulty Level: {difficulty}
- Learning Objectives: {json.dumps(learning_objectives)}
- Expected Output Specification: {expected_output}

Generate the implementation code and corresponding pytest unit test suite according to the JSON schema.
Ensure file paths follow the repository convention: `learning/{category}/day_{day:03d}_<topic_slug>.py` and `tests/test_day_{day:03d}_<topic_slug>.py`.
"""

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        response_mime_type="application/json",
        temperature=0.2,
    )

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=user_prompt,
            config=config
        )
    except Exception as e:
        logger.error(f"Gemini API request failed: {e}")
        raise RuntimeError(f"Gemini API call failed: {e}")

    raw_text = response.text
    if not raw_text:
        raise ValueError("Gemini returned an empty response.")

    # Parse JSON output
    cleaned_text = raw_text.strip()
    if cleaned_text.startswith("```json"):
        cleaned_text = cleaned_text[7:]
    if cleaned_text.startswith("```"):
        cleaned_text = cleaned_text[3:]
    if cleaned_text.endswith("```"):
        cleaned_text = cleaned_text[:-3]
    cleaned_text = cleaned_text.strip()

    try:
        task_data = json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Gemini response as JSON: {e}")
        raise ValueError(f"Invalid JSON response from Gemini model: {e}")

    return task_data
