"""
Portfolio Project 2: Customer Churn Classification Model.
"""
import math
from typing import List, Tuple, Dict

def sigmoid(z: float) -> float:
    """Computes sigmoid activation function."""
    return 1.0 / (1.0 + math.exp(-z))

def predict_churn_probability(tenure_months: int, monthly_charges: float, support_tickets: int) -> float:
    """
    Computes churn probability using a pre-calibrated logistic regression decision function.
    Weights: tenure (-0.1), charges (+0.02), support_tickets (+0.5), intercept (-1.0).
    """
    w_tenure = -0.1
    w_charges = 0.02
    w_tickets = 0.5
    intercept = -1.0

    z = (w_tenure * tenure_months) + (w_charges * monthly_charges) + (w_tickets * support_tickets) + intercept
    return round(sigmoid(z), 4)

def classify_churn(probability: float, threshold: float = 0.5) -> int:
    """Converts probability to binary churn decision (1 = Churn, 0 = Retain)."""
    return 1 if probability >= threshold else 0
