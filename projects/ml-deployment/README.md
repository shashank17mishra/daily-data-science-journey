# Portfolio Project 4: ML Model Container Deployment

## Overview
Demonstrates production Docker containerization of an ML inference service.

## Key Features
- Production Dockerfile setup with multi-stage build guide.
- Health check configurations.
- Minimal dependency footprint.

## How to Run
```bash
docker build -t ml-deployment:latest -f projects/ml-deployment/Dockerfile .
docker run -p 8080:8080 ml-deployment:latest
```
