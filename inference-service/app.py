import joblib
import pandas as pd

from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel


# Create FastAPI application
app = FastAPI()


# Find the model file
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "logistic_regression.joblib"


# Load trained model
model_data = joblib.load(MODEL_PATH)

model = model_data["pipeline"]


# Customer input
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


# Health check
@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "model": model_data["model_name"],
        "version": model_data["model_version"]
    }


# Make prediction
@app.post("/predict")
def predict_churn(customer: CustomerData):

    customer_data = pd.DataFrame(
        [customer.model_dump()]
    )

    prediction = model.predict(
        customer_data
    )[0]

    probability = model.predict_proba(
        customer_data
    )[0][1]

    if prediction == 1:
        result = "Churn"
    else:
        result = "Stay"

    return {
        "prediction": result,
        "churn_probability": round(
            float(probability),
            4
        )
    }