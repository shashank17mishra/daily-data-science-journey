# Portfolio Project 3: Data Science & ML REST API

## Overview
A lightweight REST API serving machine learning model inference using Python standard library HTTP handling or FastAPI conventions.

## Key Features
- `/health` endpoint for readiness/liveness checks.
- `/predict` endpoint for scoring machine learning feature payloads.
- JSON response payload schema validation.

## How to Run
```bash
python projects/ml-api/app.py
pytest projects/ml-api/test_app.py
```
