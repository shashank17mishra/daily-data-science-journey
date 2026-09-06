from app import handle_health_check, handle_predict_request

def test_health_check():
    res = handle_health_check()
    assert res["status"] == "healthy"

def test_predict_request_success():
    res = handle_predict_request({"features": [2.0, 4.0, 6.0]})
    assert res["status"] == "success"
    assert "prediction" in res

def test_predict_request_invalid():
    res = handle_predict_request({})
    assert "error" in res
    assert res["code"] == 400
