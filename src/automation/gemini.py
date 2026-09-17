import os
import json
import re
import time
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from src.automation.utils import logger

DEFAULT_MODEL = "gemini-3.6-flash"
FALLBACK_MODELS = [
    "gemini-3.5-flash",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-3.5-flash-lite",
]

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
6. In 'content', output ONLY raw source code. NEVER include markdown code fences (```python or ```) inside the content strings.
7. Python code must be syntactically valid with correct indentation, closed quotes/brackets, and valid imports.
"""


class TaskFile(BaseModel):
    path: str = Field(description="Relative path of file to create or update")
    content: str = Field(description="Full text content of the file")


class TaskPayload(BaseModel):
    title: str = Field(description="Day title, e.g. Day 016: Dataclasses & Structured Data")
    category: str = Field(description="Category name, e.g. python")
    description: str = Field(description="Detailed explanation of the exercise")
    learning_objectives: List[str] = Field(description="List of learning goals")
    files: List[TaskFile] = Field(description="List of files to generate")
    explanation: str = Field(description="Study notes and concept overview")
    commit_message: str = Field(description="Git commit message")


def extract_json_str(raw_text: str) -> str:
    """Extracts JSON substring from raw model response, handling markdown blocks and preambles."""
    text = raw_text.strip()

    # Match ```json ... ``` or ``` ... ```
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        candidate = match.group(1).strip()
        first_brace = candidate.find("{")
        last_brace = candidate.rfind("}")
        if first_brace != -1 and last_brace > first_brace:
            return candidate[first_brace : last_brace + 1].strip()

    # Find outermost braces { ... }
    first_brace = text.find("{")
    last_brace = text.rfind("}")
    if first_brace != -1 and last_brace > first_brace:
        return text[first_brace : last_brace + 1].strip()

    return text


def parse_gemini_json(raw_text: str) -> Dict[str, Any]:
    """
    Robustly parses JSON from Gemini model responses.
    Handles unescaped control characters (newlines, tabs in code strings),
    markdown code blocks, invalid backslash escapes, and trailing commas.
    """
    if not raw_text or not raw_text.strip():
        raise ValueError("Gemini returned an empty response.")

    json_str = extract_json_str(raw_text)

    # 1. Standard loads with strict=False (allows raw newlines/tabs inside strings)
    try:
        data = json.loads(json_str, strict=False)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass

    # 2. Fix invalid backslash escapes (e.g. \d, \s in python code strings)
    cleaned = re.sub(r'\\(?![/"\\bfnrtu]|u[0-9a-fA-F]{4})', r'\\\\', json_str)
    try:
        data = json.loads(cleaned, strict=False)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass

    # 3. Remove trailing commas in objects and arrays
    cleaned_no_commas = re.sub(r',\s*([}\]])', r'\1', cleaned)
    try:
        data = json.loads(cleaned_no_commas, strict=False)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass

    # 4. Strip non-printable control characters outside standard whitespace
    cleaned_ctrl = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', cleaned_no_commas)
    try:
        data = json.loads(cleaned_ctrl, strict=False)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Gemini response as JSON: {e}\nResponse snippet: {raw_text[:300]}")
        raise ValueError(f"Invalid JSON response from Gemini model: {e}")

    raise ValueError("Gemini response parsed to non-dictionary JSON.")


def is_transient_error(err: Exception) -> bool:
    """Checks whether an exception indicates a temporary server issue or rate limit."""
    err_str = str(err).lower()
    return any(term in err_str for term in [
        "503", "unavailable", "high demand", "temporarily unavailable",
        "429", "resource_exhausted", "quota", "rate limit", "500", "internal",
        "502", "bad gateway", "504", "gateway timeout", "deadline"
    ])


def generate_daily_task(
    day: int,
    category: str,
    topic: str,
    difficulty: str,
    learning_objectives: list,
    expected_output: str,
    api_key: Optional[str] = None,
    model_name: Optional[str] = None,
    feedback: Optional[str] = None
) -> Dict[str, Any]:
    """
    Calls Google Gemini API using the official google-genai SDK to generate structured task files.
    Includes exponential backoff for transient errors, fallback model cascade, and error feedback injection.
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

    feedback_section = ""
    if feedback:
        feedback_section = f"""
CRITICAL FIX REQUIRED (PREVIOUS ATTEMPT FAILED VALIDATION):
The previous code generation attempt failed validation with the following error:
{feedback}

Please carefully analyze and resolve this error.
Ensure all Python files have valid syntax (no missing quotes, unmatched parentheses, or syntax errors) and that all pytest unit tests pass cleanly.
"""

    user_prompt = f"""
Daily Learning Task Details:
- Day Number: {day}
- Category: {category}
- Topic: {topic}
- Difficulty Level: {difficulty}
- Learning Objectives: {json.dumps(learning_objectives)}
- Expected Output Specification: {expected_output}
{feedback_section}
Generate the implementation code and corresponding pytest unit test suite according to the JSON schema.
Ensure file paths follow the repository convention: `learning/{category}/day_{day:03d}_<topic_slug>.py` and `tests/test_day_{day:03d}_<topic_slug>.py`.
"""

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        response_mime_type="application/json",
        response_schema=TaskPayload,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
        temperature=0.2,
    )

    models_to_try = [model_name] + [m for m in FALLBACK_MODELS if m != model_name]
    response = None
    last_err = None
    MAX_RETRIES = 3

    for m in models_to_try:
        logger.info(f"Attempting content generation with model '{m}' for Day {day} ({topic})...")
        for retry in range(MAX_RETRIES):
            try:
                logger.info(f"Generating content with model '{m}' (attempt {retry + 1}/{MAX_RETRIES})...")
                response = client.models.generate_content(
                    model=m,
                    contents=user_prompt,
                    config=config
                )
                if response and response.text:
                    logger.info(f"Successfully received response from model '{m}'.")
                    break
            except Exception as e:
                last_err = e
                if is_transient_error(e) and retry < MAX_RETRIES - 1:
                    backoff = min(2 * (2 ** retry), 10)
                    logger.warning(
                        f"Model '{m}' encountered transient error: {e}. Retrying in {backoff}s ({retry + 1}/{MAX_RETRIES})..."
                    )
                    time.sleep(backoff)
                    continue

                logger.warning(f"Model '{m}' call with structured schema failed: {e}. Trying without response_schema...")
                try:
                    fallback_config = types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        response_mime_type="application/json",
                        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
                        temperature=0.2,
                    )
                    response = client.models.generate_content(
                        model=m,
                        contents=user_prompt,
                        config=fallback_config
                    )
                    if response and response.text:
                        logger.info(f"Successfully received response from model '{m}' (unstructured mode).")
                        break
                except Exception as e2:
                    last_err = e2
                    if is_transient_error(e2) and retry < MAX_RETRIES - 1:
                        backoff = min(2 * (2 ** retry), 10)
                        logger.warning(
                            f"Model '{m}' unstructured mode encountered transient error: {e2}. Retrying in {backoff}s..."
                        )
                        time.sleep(backoff)
                        continue
                    logger.warning(f"Model '{m}' call failed: {e2}. Moving to fallback model...")
                    break
        if response and response.text:
            break

    if not response or not response.text:
        raise RuntimeError(f"Gemini generation failed across models ({models_to_try}): {last_err}")

    raw_text = response.text
    return parse_gemini_json(raw_text)

