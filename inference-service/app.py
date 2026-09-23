import joblib
import pandas as pd

from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

# Load the trained model when the service starts
model_path = Path(__file__).resolve().parent / "model" / "logistic_regression.joblib"
model_data = joblib.load(model_path)
model = model_data["pipeline"]


class CustomerData(BaseModel):
    tenure: int
    InternetService: str
    Contract: str
    MonthlyCharges: float
    TotalCharges: float
    TechSupport: str
    OnlineSecurity: str
    PaperlessBilling: str
    PaymentMethod: str


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model": model_data["model_name"],
        "version": model_data["model_version"]
    }


@app.post("/predict")
def predict_churn(customer: CustomerData):
    # The model expects a DataFrame with one customer row
    customer_data = pd.DataFrame([customer.model_dump()])

    prediction = model.predict(customer_data)[0]
    probability = model.predict_proba(customer_data)[0][1]

    if prediction == 1:
        result = "Churn"
    else:
        result = "Stay"

    return {
        "prediction": result,
        "churn_probability": round(float(probability), 4)
    }
