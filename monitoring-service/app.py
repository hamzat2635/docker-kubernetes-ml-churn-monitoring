import os
import requests

from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from database import (
    save_prediction,
    get_predictions,
    create_table
)


# Create the FastAPI application
app = FastAPI()


# HTML templates folder
templates = Jinja2Templates(
    directory="templates"
)


# Address of the inference service
# Local default is used when running outside Docker/Kubernetes
INFERENCE_SERVICE_URL = os.getenv(
    "INFERENCE_SERVICE_URL",
    "http://127.0.0.1:8000/predict"
)


# Customer information
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


# Create database table when service starts
@app.on_event("startup")
def startup():

    create_table()


# Web dashboard
@app.get("/")
def dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# Health check endpoint
@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "Monitoring Service"
    }


# Analyze customer
@app.post("/analyze")
def analyze_customer(customer: CustomerData):

    try:

        # Send customer information to inference service
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


    # Get prediction returned by inference service
    prediction_result = response.json()


    try:

        # Save customer information and prediction
        # in PostgreSQL
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


    # Return prediction to browser
    return prediction_result


# Get prediction history
@app.get("/predictions")
def prediction_history():

    try:

        predictions = get_predictions()

        return predictions

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {error}"
        )