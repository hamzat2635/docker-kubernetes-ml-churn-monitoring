import os
import requests

from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from database import create_table, get_predictions, save_prediction


app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Local address is used when the environment variable is not set
INFERENCE_SERVICE_URL = os.getenv(
    "INFERENCE_SERVICE_URL",
    "http://127.0.0.1:8000/predict"
)


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


@app.on_event("startup")
def startup():
    create_table()


@app.get("/")
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Monitoring Service"
    }


@app.post("/analyze")
def analyze_customer(customer: CustomerData):
    # Ask the inference service to make the prediction
    try:
        response = requests.post(
            INFERENCE_SERVICE_URL,
            json=customer.model_dump(),
            timeout=10
        )
        response.raise_for_status()
    except requests.RequestException as error:
        raise HTTPException(
            status_code=503,
            detail=f"Inference service error: {error}"
        )

    prediction_result = response.json()

    # Save the result in PostgreSQL
    try:
        save_prediction(
            customer,
            prediction_result["prediction"],
            prediction_result["churn_probability"]
        )
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {error}"
        )

    return prediction_result


@app.get("/predictions")
def prediction_history():
    try:
        return get_predictions()
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {error}"
        )
