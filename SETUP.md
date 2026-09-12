# Setup & Configuration Guide

Follow this guide to configure, run, test, and deploy the `daily-data-science-journey` repository.

---

## 📋 Prerequisites

1. **Python 3.11 or higher**: Download from [python.org](https://www.python.org/).
2. **Git**: Installed and configured on your system.
3. **Google Gemini API Key**: Free tier API key generated from [Google AI Studio](https://aistudio.google.com/).

---

## 🛠️ Step-by-Step Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/daily-data-science-journey.git
cd daily-data-science-journey
```

### Step 2: Create a Virtual Environment
```bash
# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 Configure Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/) and click **Get API key**.
2. Copy your key.
3. Set the environment variable locally:

**Linux / macOS:**
```bash
export GEMINI_API_KEY="AIzaSyYourSecretKeyHere"
```

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="AIzaSyYourSecretKeyHere"
```

**Windows (CMD):**
```cmd
set GEMINI_API_KEY=AIzaSyYourSecretKeyHere
```

---

## ⚙️ Configuring GitHub Actions Secret

To enable automated daily execution in GitHub Actions:

1. Open your repository on GitHub.
2. Go to **Settings** > **Secrets and variables** > **Actions**.
3. Under **Repository secrets**, click **New repository secret**.
4. Set:
   - **Name**: `GEMINI_API_KEY`
   - **Secret**: Paste your Gemini API key.
5. Click **Add secret**.

### Optional Variables (Configuration)
Under **Variables** (or as env vars):
- `START_DATE`: `2026-09-07` (The day Day 1 begins in IST)
- `GEMINI_MODEL`: `gemini-3.6-flash` (or `gemini-3.5-flash-lite`)

---

## 💻 Running Locally

### 1. Execute Unit Test Suite
Ensure all automation engine tests pass:
```bash
pytest
```

### 2. Run Automation in Dry-Run Mode
Test task generation and validation without creating a git commit:
```bash
python -m src.automation.main --dry-run
```

### 3. Run Automation for a Specific Date or Day
```bash
# Target specific date
python -m src.automation.main --date 2026-09-08 --dry-run

# Target specific day number
python -m src.automation.main --day 15 --dry-run
```

---

## ⚡ Manually Triggering GitHub Action Workflow

1. Go to the **Actions** tab in your GitHub repository.
2. Click **Daily Data Science Journey** on the left menu.
3. Click **Run workflow** on the right.
4. Select options:
   - `dry_run`: `true` or `false`
   - `custom_date`: `YYYY-MM-DD` (optional)
   - `force`: `true` or `false` (optional)
5. Click **Run workflow**.

---

## 🔍 Troubleshooting

| Issue | Cause | Solution |
|---|---|---|
| `ValueError: GEMINI_API_KEY environment variable is not set` | Missing API Key | Ensure `GEMINI_API_KEY` is exported or added as a GitHub secret. |
| `365-day roadmap completed` | Current date is past day 365 | Adjust `START_DATE` or use `--day N --force` for testing. |
| `Today's task is already completed` | Task ran previously today | Use `--force` flag to force re-execution. |
| `Syntax error in generated code file` | Gemini output syntax flaw | The validator stops invalid commits. Re-run or check Gemini output format. |
| `Security validation failed` | Secret detected in output | Ensure model is not outputting fake hardcoded keys. |
