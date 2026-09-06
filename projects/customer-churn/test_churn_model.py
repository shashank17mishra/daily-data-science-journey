from churn_model import predict_churn_probability, classify_churn

def test_predict_churn_probability():
    prob_lo = predict_churn_probability(tenure_months=36, monthly_charges=30.0, support_tickets=0)
    assert prob_lo < 0.1

    prob_hi = predict_churn_probability(tenure_months=1, monthly_charges=120.0, support_tickets=4)
    assert prob_hi > 0.8

def test_classify_churn():
    assert classify_churn(0.75, 0.5) == 1
    assert classify_churn(0.25, 0.5) == 0
