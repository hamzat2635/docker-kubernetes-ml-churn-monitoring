# Docker & Kubernetes ML Churn Monitoring

A cloud-native machine learning application for customer churn prediction, built with FastAPI, PostgreSQL, Docker, and Kubernetes.

The project demonstrates a microservice architecture with REST API communication, persistent database storage, independent horizontal scaling, service discovery, and Kubernetes self-healing.

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

## Project Overview

The application allows a user to enter telecom customer information through a web dashboard.

The Monitoring Service receives the request, sends the customer data to the ML Inference Service through a REST API, receives the churn prediction, stores the result in PostgreSQL, and returns it to the browser.

The Inference Service uses a trained Logistic Regression pipeline to predict whether the customer is likely to churn and returns a churn probability.

## Architecture

```text
Browser
   |
   v
NodePort :30081
   |
   v
Monitoring Service
   |
   +------ REST ------> Inference Service
   |                        |
   |                        v
   |                 Logistic Regression
   |
   +------ SQL -------> PostgreSQL Service
                            |
                            v
                       PostgreSQL Pod
                            |
                            v
                    PersistentVolumeClaim
```

For the full design and component responsibilities, see [docs/architecture.md](docs/architecture.md).

## Microservices

### Inference Service

Responsible for machine learning inference.

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

Example response:

```json
{
  "prediction": "Churn",
  "churn_probability": 0.7847
}
```

### Monitoring Service

Provides the web dashboard and coordinates communication between the browser, Inference Service, and PostgreSQL.

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

### PostgreSQL

PostgreSQL stores:

- Customer information
- Prediction result
- Churn probability
- Prediction timestamp

Persistent storage is provided through a Kubernetes PersistentVolumeClaim.

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

The deployed model accepts:

- tenure
- InternetService
- Contract
- MonthlyCharges
- TotalCharges
- TechSupport
- OnlineSecurity
- PaperlessBilling
- PaymentMethod

## Docker Images

Custom images:

```text
hamza2635/churn-inference:1.0
hamza2635/churn-monitoring:1.1
```

Database image:

```text
postgres:16
```

## Kubernetes

The repository contains Kubernetes configuration for:

```text
Inference Deployment
Inference Service

Monitoring Deployment
Monitoring Service

PostgreSQL Deployment
PostgreSQL Service
PostgreSQL PersistentVolumeClaim

ConfigMap
Secret template
```

The dashboard is externally accessible through:

```text
http://localhost:30081/
```

## Horizontal Scaling

The application services can be scaled independently:

```bash
kubectl scale deployment inference --replicas=3
kubectl scale deployment monitoring --replicas=2
```

A tested demonstration configuration used:

```text
Inference:   3 replicas
Monitoring:  2 replicas
PostgreSQL:  1 replica
```

The application is small enough that multiple replicas are not required for its current traffic. Scaling is demonstrated to show how the architecture could support a larger workload.

## Self-Healing and Persistence

Kubernetes self-healing was tested by deleting an Inference Pod. Kubernetes automatically created a replacement Pod while the Deployment maintained its desired replica count.

PostgreSQL persistence was tested by:

1. Creating prediction records.
2. Deleting the PostgreSQL Pod.
3. Allowing Kubernetes to create a replacement Pod.
4. Confirming that the previously stored records were still available.

PostgreSQL uses:

```text
postgres-pvc
```

## Configuration and Security

Non-sensitive runtime configuration is provided through a Kubernetes ConfigMap.

Database credentials are provided through a Kubernetes Secret.

The real:

```text
kubernetes/postgres-secret.yaml
```

is excluded from Git. The repository contains:

```text
kubernetes/postgres-secret.example.yaml
```

as a safe template.

For a fuller security discussion, see [docs/design-discussion.md](docs/design-discussion.md).

## Project Structure

```text
.
|-- docs/
|   |-- architecture.md
|   |-- design-discussion.md
|   |-- deployment-guide.md
|   `-- demo-guide.md
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

## Quick Start

For complete instructions, see the [Deployment Guide](docs/deployment-guide.md).

Check the cluster:

```bash
kubectl get nodes
```

After creating the local database Secret and applying the Kubernetes resources, verify:

```bash
kubectl get deployments
kubectl get pods
kubectl get services
kubectl get pvc
```

Then open:

```text
http://localhost:30081/
```

## Assignment Requirements Covered

| Requirement | Implementation |
|---|---|
| Kubernetes deployment | Kubernetes manifests included |
| At least two microservice types | Monitoring and Inference |
| REST API on each microservice | FastAPI endpoints on both services |
| External access | Monitoring NodePort on port 30081 |
| Independent horizontal scaling | Separate Monitoring and Inference Deployments |
| Images available to Kubernetes | Custom images published on Docker Hub |
| Separate database | PostgreSQL Deployment and Service |
| Persistent database storage | PostgreSQL PVC |
| Database scaling not required | PostgreSQL uses one replica |
| Programmatic REST API consumption | Monitoring calls Inference with an HTTP POST request |

## Author

Hamza

MSc Computer Science  
Blekinge Institute of Technology
