"""
Portfolio Project 3: Lightweight ML Model Inference Server logic.
"""
from typing import Dict, Any

def handle_health_check() -> Dict[str, str]:
    """Returns service health status status."""
    return {"status": "healthy", "service": "ml-api", "version": "1.0.0"}

def handle_predict_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates payload features and produces inference score.
    Expected payload: {"features": [f1, f2, f3]}
    """
    if "features" not in payload:
        return {"error": "Missing 'features' key in payload.", "code": 400}

    features = payload["features"]
    if not isinstance(features, list) or len(features) == 0:
        return {"error": "'features' must be a non-empty list of numbers.", "code": 400}

    # Dummy weighted linear model scoring
    score = sum(val * (i + 1) for i, val in enumerate(features)) / len(features)
    prediction = 1 if score > 5.0 else 0

    return {
        "status": "success",
        "score": round(score, 4),
        "prediction": prediction
    }
