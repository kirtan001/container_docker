from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

# --------------------------------------------------
# Load artifacts at startup (BEST PRACTICE)
# --------------------------------------------------
model = joblib.load("models/gb_model.pkl")
feature_columns = joblib.load("models/feature_columns.pkl")
business_threshold = joblib.load("models/business_threshold.pkl")

app = FastAPI(title="Bank Marketing Subscription API")

# --------------------------------------------------
# Input schema (STRICT & VALIDATED)
# --------------------------------------------------
class CustomerInput(BaseModel):
    age: int
    job: str
    marital: str
    education: str
    default: str
    balance: int
    housing: str
    loan: str
    contact: str
    day_of_week: str
    month: str
    campaign: int
    pdays: int
    previous: int
    poutcome: str


# --------------------------------------------------
# Feature Engineering (SAME AS TRAINING)
# --------------------------------------------------
def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["campaign_intensity"] = df["campaign"] / (df["previous"] + 1)
    df["had_previous_contact"] = (df["previous"] > 0).astype(int)

    df["age_group"] = pd.cut(
        df["age"],
        bins=[18, 30, 45, 60, 100],
        labels=["young", "adult", "mid", "senior"]
    )

    return df


# --------------------------------------------------
# Prediction Endpoint
# --------------------------------------------------
@app.post("/predict")
def predict_subscription(customer: CustomerInput):

    # Convert input to DataFrame
    input_df = pd.DataFrame([customer.dict()])

    # Feature engineering
    input_df = feature_engineering(input_df)

    # One-hot encoding
    input_encoded = pd.get_dummies(input_df)

    # Align columns with training schema
    input_encoded = input_encoded.reindex(
        columns=feature_columns,
        fill_value=0
    )

    # Model inference
    probability = model.predict_proba(input_encoded)[:, 1][0]
    prediction = int(probability >= business_threshold)

    return {
        "prediction": prediction,
        "subscription_probability": round(probability, 4),
        "business_decision": "Target Customer" if prediction == 1 else "Do Not Target"
    }


# --------------------------------------------------
# Health check (CI/CD friendly)
# --------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "API is running"}
