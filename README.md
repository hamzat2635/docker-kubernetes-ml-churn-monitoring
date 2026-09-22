# Docker & Kubernetes ML Churn Monitoring

A cloud-native machine learning application for customer churn prediction,
built with FastAPI, PostgreSQL, Docker and Kubernetes.

## Highlights

- Two independently scalable FastAPI microservices
- Programmatic REST API communication
- Logistic Regression churn prediction
- PostgreSQL persistent storage
- Dockerized services published to Docker Hub
- Kubernetes Deployments and Services
- ConfigMap and Secret configuration
- Horizontal scaling
- Kubernetes self-healing
- Persistent data across PostgreSQL Pod replacement
- Browser-based monitoring dashboard


## Documentation

- [Architecture and Software Design](docs/architecture.md)
- [Benefits, Challenges and Security](docs/design-discussion.md)
- [Deployment Guide](docs/deployment-guide.md)
- [Demo Guide](docs/demo-guide.md)



# Cloud-Native Customer Churn Prediction & Monitoring

A cloud-native machine learning application that predicts customer churn using a trained Logistic Regression model.

The project uses a microservice architecture with FastAPI, PostgreSQL, Docker, and Kubernetes. It demonstrates REST API communication, persistent database storage, horizontal scaling, and Kubernetes self-healing.

## Project Overview

The application allows a user to enter customer information through a web dashboard.

The Monitoring Service sends the customer data to the ML Inference Service through a REST API.

The Inference Service uses a trained Logistic Regression model to predict whether the customer is likely to churn.

The prediction and customer information are then stored in PostgreSQL and can be viewed through the prediction history section of the dashboard.

## Architecture

```text
Browser
   |
   v
Monitoring Service
   |
   | REST API
   v
Inference Service
   |
   v
Logistic Regression Model

Monitoring Service
   |
   | SQL
   v
PostgreSQL
   |
   v
Persistent Storage
```

When deployed with Kubernetes:

```text
Browser
   |
   v
NodePort :30081
   |
   v
Monitoring Service
   |
   +----> Monitoring Pods
   |
   | REST
   v
Inference Service
   |
   +----> Inference Pods
   |
   v
Logistic Regression Model

Monitoring Pods
   |
   | SQL
   v
PostgreSQL Service
   |
   v
PostgreSQL Pod
   |
   v
PersistentVolumeClaim
```

## Microservices

### 1. Inference Service

The Inference Service is responsible for machine learning predictions.

Technology:

- Python
- FastAPI
- pandas
- scikit-learn
- joblib

REST endpoints:

```text
GET  /health
POST /predict
```

Example prediction response:

```json
{
  "prediction": "Churn",
  "churn_probability": 0.7847
}
```

### 2. Monitoring Service

The Monitoring Service provides the web dashboard and communicates with both the Inference Service and PostgreSQL.

Technology:

- Python
- FastAPI
- Jinja2
- HTML/CSS/JavaScript
- psycopg
- requests

REST endpoints:

```text
GET  /
GET  /health
POST /analyze
GET  /predictions
```

The `/analyze` endpoint programmatically consumes the `/predict` REST API provided by the Inference Service.

### 3. PostgreSQL

PostgreSQL stores:

- Customer information
- Prediction result
- Churn probability
- Prediction timestamp

Persistent storage is provided in Kubernetes using a PersistentVolumeClaim.

## Machine Learning Model

Dataset:

Telco Customer Churn dataset.

Two classification models were evaluated:

- Logistic Regression
- Random Forest

Final Logistic Regression results:

| Metric | Result |
|---|---:|
| Accuracy | 0.737 |
| Precision | 0.503 |
| Recall | 0.807 |
| F1 Score | 0.620 |
| ROC AUC | 0.839 |

Logistic Regression was selected because it achieved higher recall, F1 score, and ROC-AUC in the evaluated configuration.

The deployed model accepts these features:

- tenure
- InternetService
- Contract
- MonthlyCharges
- TotalCharges
- TechSupport
- OnlineSecurity
- PaperlessBilling
- PaymentMethod

## Docker

The two custom microservices are containerized separately.

Docker images:

```text
hamza2635/churn-inference:1.0
hamza2635/churn-monitoring:1.1
```

PostgreSQL uses the official:

```text
postgres:16
```

image.

## Kubernetes

The application is deployed using Kubernetes.

Kubernetes resources include:

```text
Inference Deployment
Inference Service

Monitoring Deployment
Monitoring Service

PostgreSQL Deployment
PostgreSQL Service
PostgreSQL PersistentVolumeClaim

ConfigMap
Secret
```

The Monitoring Service is externally accessible using a NodePort:

```text
http://localhost:30081/
```

## Horizontal Scaling

The application microservices can be scaled independently.

Example:

```bash
kubectl scale deployment inference --replicas=3
kubectl scale deployment monitoring --replicas=2
```

The tested deployment used:

```text
Inference:   3 replicas
Monitoring:  2 replicas
PostgreSQL:  1 replica
```

## Self-Healing

Kubernetes self-healing was tested by manually deleting an Inference Pod.

Kubernetes automatically created a replacement Pod while the remaining replicas continued serving requests.

The PostgreSQL Pod was also deleted during testing. Kubernetes recreated the Pod automatically.

## Persistent Storage

PostgreSQL uses a Kubernetes PersistentVolumeClaim:

```text
postgres-pvc
```

Database persistence was verified by:

1. Creating prediction records.
2. Deleting the PostgreSQL Pod.
3. Allowing Kubernetes to create a replacement Pod.
4. Confirming that the previously stored predictions were still available.

## Configuration

Non-sensitive configuration is provided through a Kubernetes ConfigMap.

Examples:

```text
INFERENCE_SERVICE_URL
DB_HOST
DB_PORT
DB_NAME
```

Database credentials are provided through a Kubernetes Secret.

The real Secret file is excluded from Git.

Use:

```text
kubernetes/postgres-secret.example.yaml
```

as a template and create your own:

```text
kubernetes/postgres-secret.yaml
```

before deploying.

## Project Structure

```text
Cloud ML/
|
|-- inference-service/
|   |-- model/
|   |   `-- logistic_regression.joblib
|   |-- app.py
|   |-- Dockerfile
|   `-- requirements.txt
|
|-- monitoring-service/
|   |-- templates/
|   |   `-- index.html
|   |-- app.py
|   |-- database.py
|   |-- Dockerfile
|   `-- requirements.txt
|
|-- kubernetes/
|   |-- inference-deployment.yaml
|   |-- inference-service.yaml
|   |-- monitoring-configmap.yaml
|   |-- monitoring-deployment.yaml
|   |-- monitoring-service.yaml
|   |-- postgres-deployment.yaml
|   |-- postgres-pvc.yaml
|   |-- postgres-secret.example.yaml
|   `-- postgres-service.yaml
|
|-- model/
|   `-- logistic_regression.joblib
|
|-- churn_practice.py
|-- train_models.py
|-- .gitignore
`-- README.md
```

## Running the Kubernetes Application

Check the Kubernetes cluster:

```bash
kubectl get nodes
```

Create the database Secret using the example file first.

Then deploy the Kubernetes resources.

Check the application:

```bash
kubectl get deployments
kubectl get pods
kubectl get services
kubectl get pvc
```

When all Pods are running, open:

```text
http://localhost:30081/
```

## Features Demonstrated

This project demonstrates:

- Microservice architecture
- REST API implementation
- Programmatic REST API consumption
- Machine learning inference
- Docker containerization
- Docker Hub image distribution
- Kubernetes Deployments
- Kubernetes Services
- ConfigMaps
- Secrets
- PersistentVolumeClaims
- Horizontal scaling
- Independent microservice scaling
- Kubernetes self-healing
- Persistent PostgreSQL storage
- Browser-accessible web dashboard

## Security Considerations

Database credentials are stored using Kubernetes Secrets rather than being hard-coded into the Deployment manifests.

Sensitive Secret files are excluded from Git using `.gitignore`.

For a production deployment, additional measures would include:

- TLS/HTTPS
- Authentication and authorization
- NetworkPolicies
- Restricted database access
- Secret encryption at rest
- Resource limits
- Input validation
- Regular dependency updates

## Author

Hamza

MSc Computer Science  
Blekinge Institute of Technology