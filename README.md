# Daily Data Science Journey 🚀

An automated, lightweight, production-quality learning engine and technical portfolio built to cultivate consistent, high-value Data Science, Machine Learning, and DevOps skills over 365 progressive days.

> **Honest Portfolio Commitment**  
> This repository uses automation to support genuine daily learning and portfolio development. It **does not** create empty or artificial commits solely to manipulate GitHub contribution statistics. Every commit contains functional, tested code, real exercises, or portfolio project enhancements.

---

## 📌 Project Overview & Goals

The goal of `daily-data-science-journey` is to build a structured, real-world Data Science portfolio while maintaining continuous learning habits.

The automation system executes **ONE** structured learning task per day using **GitHub Actions** and the official **Google Gemini API** (`google-genai`), validating all generated code and unit tests before making a git commit.

---

## 🛠️ Technology Stack

- **Language:** Python 3.11+ (Standard library prioritized)
- **AI Engine:** Google Gemini API (`google-genai` SDK)
- **Orchestration:** GitHub Actions CI/CD Scheduler
- **Testing & Quality:** `pytest`, Python AST Compilation, Custom Security Scanner
- **Data & ML Libraries:** NumPy, Pandas, Scikit-learn, SQL (SQLite)

---

## 🗺️ 365-Day Progressive Learning Roadmap

The learning path spans **17 core technical domains**:

```
Days 001–030: Python Fundamentals
Days 031–060: Advanced Python & Data Structures / Algorithms (DSA)
Days 061–090: SQL & Statistical Analysis
Days 091–120: NumPy & Pandas Data Wrangling
Days 121–160: Exploratory Data Analysis (EDA) & Data Visualization
Days 161–220: Machine Learning (Supervised, Unsupervised, Time Series)
Days 221–250: Advanced Machine Learning & Deep Learning Foundations
Days 251–280: Deep Learning Architectures (CNNs, RNNs, Transformers)
Days 281–300: Generative AI, RAG & LLM Engineering
Days 301–320: Web Development & REST APIs (FastAPI)
Days 321–340: Docker Containerization, Git & DevOps
Days 341–355: Data Engineering & MLOps Pipelines
Days 356–365: Portfolio Project Capstones
```

---

## 📂 Repository Structure

```
daily-data-science-journey/
│
├── README.md                  # Project overview & documentation
├── SETUP.md                   # Setup and usage guide
├── LICENSE                    # MIT License
├── .gitignore                 # Standard git ignore rules
├── requirements.txt           # Minimal automation dependencies
├── pyproject.toml             # Project metadata & pytest config
├── roadmap.json               # Structured 365-day curriculum
├── progress.json              # Progress tracking state
│
├── src/
│   └── automation/            # Core automation engine
│       ├── __init__.py
│       ├── main.py            # Orchestrator CLI entrypoint
│       ├── gemini.py          # Gemini API integration wrapper
│       ├── roadmap.py         # Roadmap & progress state manager
│       ├── generator.py       # File writer & path sanitizer
│       ├── validator.py       # Syntax, test & safety validator
│       ├── git.py             # Safe Git workflow wrapper
│       ├── security.py        # Secret pattern scanner
│       └── utils.py           # Timezone (IST) & helper utilities
│
├── learning/                  # 17 Category learning directories
│   ├── python/
│   ├── dsa/
│   ├── sql/
│   ├── statistics/
│   ├── numpy/
│   ├── pandas/
│   ├── data-analysis/
│   ├── machine-learning/
│   ├── deep-learning/
│   ├── generative-ai/
│   ├── web-development/
│   ├── apis/
│   ├── git-github/
│   ├── docker/
│   ├── data-engineering/
│   └── mlops/
│
├── projects/                  # Foundation portfolio capstones
│   ├── sales-analysis/       # E-Commerce sales metrics pipeline
│   ├── customer-churn/       # Customer churn classifier model
│   ├── ml-api/               # REST inference service
│   └── ml-deployment/        # Containerized Docker ML service
│
├── tests/                     # Unit test suites
│   ├── test_roadmap.py
│   ├── test_generator.py
│   ├── test_validator.py
│   ├── test_security.py
│   └── test_git.py
│
└── .github/
    └── workflows/
        └── daily-learning.yml # GitHub Actions workflow schedule
```

---

## ⚙️ How Automation Works

```
GitHub Actions (00:30 UTC / 06:00 IST)
      │
      ▼
Python Orchestrator (src/automation/main.py)
      │
      ├──> Calculate current day (START_DATE=2026-09-07, Asia/Kolkata)
      ├──> Check progress.json (Idempotency check)
      │
      ▼
Fetch Day Task Specification from roadmap.json
      │
      ▼
Google Gemini API (google-genai)
      │
      ▼
Parse Structured JSON Output (Implementation Code + Pytest Suite)
      │
      ▼
Task Generator (Write files to learning/ or projects/)
      │
      ▼
Validation Engine
      ├── 1. Verify JSON payload structure
      ├── 2. Verify file non-emptiness
      ├── 3. AST Python Syntax compilation
      ├── 4. Security Secret Scanner check
      └── 5. Pytest execution on generated tests
      │
      ▼
Git Automation (Stage, commit with descriptive message, push on CI)
```

---

## 🔒 Security Architecture

The automation includes a custom built-in `SecurityScanner` in `src/automation/security.py` that actively prevents key leaks:
- Detects API key formats (Google Gemini `AIzaSy...`, GitHub PATs `ghp_...`, AWS credentials `AKIA...`, Private Keys).
- Blocks sensitive files (`.env`, `*.pem`, `*.key`, `secrets/`).
- Enforces strict path validation restricting generated outputs to `learning/`, `projects/`, and `tests/`.

---

## 🚀 Quick Start & Local Execution

### 1. Clone & Setup Virtual Environment
```bash
git clone https://github.com/your-username/daily-data-science-journey.git
cd daily-data-science-journey
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Tests Locally
```bash
pytest
```

### 3. Run Automation in Dry-Run Mode (No Commit)
```bash
export GEMINI_API_KEY="your-gemini-api-key"
python -m src.automation.main --dry-run
```

---

## 🔑 GitHub Actions Setup

1. In your GitHub repository, go to **Settings > Secrets and variables > Actions**.
2. Add a new Repository Secret:
   - Name: `GEMINI_API_KEY`
   - Value: Your Google Gemini API Key
3. (Optional) Set Repository Variables:
   - `START_DATE`: Defaults to `2026-09-07`
   - `GEMINI_MODEL`: Defaults to `gemini-2.5-flash`

---

## 📜 License

Distributed under the [MIT License](LICENSE).
