from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

# --------------------------------------------------
# Test 1: Health Check Endpoint
# --------------------------------------------------
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "API is running"}


# --------------------------------------------------
# Test 2: Prediction Endpoint (Valid Input)
# --------------------------------------------------
def test_prediction_endpoint():

    sample_input = {
        "age": 35,
        "job": "admin.",
        "marital": "married",
        "education": "university.degree",
        "default": "no",
        "balance": 1200,
        "housing": "yes",
        "loan": "no",
        "contact": "cellular",
        "day_of_week": "mon",
        "month": "may",
        "campaign": 1,
        "pdays": 999,
        "previous": 0,
        "poutcome": "unknown"
    }

    response = client.post("/predict", json=sample_input)

    assert response.status_code == 200

    result = response.json()

    # Validate keys
    assert "prediction" in result
    assert "subscription_probability" in result
    assert "business_decision" in result

    # Validate types
    assert isinstance(result["prediction"], int)
    assert isinstance(result["subscription_probability"], float)
    assert result["business_decision"] in ["Target Customer", "Do Not Target"]

    # Probability bounds
    assert 0.0 <= result["subscription_probability"] <= 1.0
    