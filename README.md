# Docker & Kubernetes ML Churn Monitoring

This is a cloud computing project for customer churn prediction.

The application uses FastAPI, PostgreSQL, Docker, Kubernetes and a Logistic Regression model.

A user enters customer information in a web dashboard. The Monitoring Service sends the data to the Inference Service through a REST API. The Inference Service makes the churn prediction. The Monitoring Service then saves the result in PostgreSQL and shows it in the dashboard.

## Main Features

- Two FastAPI microservices
- REST API communication between services
- Logistic Regression churn prediction
- PostgreSQL database
- Docker images on Docker Hub
- Kubernetes deployment
- Horizontal scaling
- Kubernetes self-healing
- Persistent database storage
- Browser-based dashboard

## Documentation

- [Architecture](docs/architecture.md)
- [Design Discussion](docs/design-discussion.md)
- [Deployment Guide](docs/deployment-guide.md)
- [Demo Guide](docs/demo-guide.md)

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

## Microservices

### Monitoring Service

The Monitoring Service is the main service used by the user.

It:

- shows the web dashboard
- receives customer data
- sends customer data to the Inference Service
- saves predictions in PostgreSQL
- loads prediction history

REST endpoints:

```text
GET  /
GET  /health
POST /analyze
GET  /predictions
```

### Inference Service

The Inference Service is responsible for the machine learning prediction.

It:

- loads the trained model
- receives customer data
- predicts Churn or Stay
- returns the churn probability

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

### PostgreSQL

PostgreSQL stores:

- customer input
- prediction result
- churn probability
- timestamp

The database uses a PersistentVolumeClaim in Kubernetes.

## Machine Learning

The project uses the Telco Customer Churn dataset.

I tested Logistic Regression and Random Forest.

Final Logistic Regression results:

| Metric | Result |
|---|---:|
| Accuracy | 0.737 |
| Precision | 0.503 |
| Recall | 0.807 |
| F1 Score | 0.620 |
| ROC AUC | 0.839 |

I selected Logistic Regression because it gave better recall, F1 score and ROC AUC in my test.

The final model uses these features:

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

```text
hamza2635/churn-inference:1.0
hamza2635/churn-monitoring:1.1
postgres:16
```

## Kubernetes

The project includes:

- Inference Deployment and Service
- Monitoring Deployment and Service
- PostgreSQL Deployment and Service
- PersistentVolumeClaim
- ConfigMap
- Secret example file

The dashboard is available at:

```text
http://localhost:30081/
```

## Scaling

The two application services can be scaled separately.

Example:

```bash
kubectl scale deployment inference --replicas=3
kubectl scale deployment monitoring --replicas=2
```

I tested the project with:

```text
Inference:   3 replicas
Monitoring:  2 replicas
PostgreSQL:  1 replica
```

The project is small, so it does not really need this many replicas. I used this setup to show that the services can scale independently.

## Self-Healing

I tested Kubernetes self-healing by deleting an Inference Pod.

Kubernetes created a new Pod automatically because the Deployment still required the same number of replicas.

## Persistent Storage

PostgreSQL uses:

```text
postgres-pvc
```

I tested persistence by:

1. creating prediction records
2. deleting the PostgreSQL Pod
3. waiting for Kubernetes to create a new Pod
4. checking that the old prediction records were still there

## Security

Database credentials are stored in a Kubernetes Secret.

The real file:

```text
kubernetes/postgres-secret.yaml
```

is ignored by Git.

The repository only includes:

```text
kubernetes/postgres-secret.example.yaml
```

The Inference Service and PostgreSQL are internal services. Only the Monitoring Service is exposed outside Kubernetes.

More security improvements are discussed in [docs/design-discussion.md](docs/design-discussion.md).

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
|-- monitoring-service/
|-- kubernetes/
|-- model/
|
|-- churn_practice.py
|-- train_models.py
|-- .gitignore
`-- README.md
```

## Assignment Requirements

| Requirement | How it is covered |
|---|---|
| Kubernetes deployment | Kubernetes YAML files are included |
| Two microservices | Monitoring Service and Inference Service |
| REST API | Both services use FastAPI |
| External access | Monitoring Service uses NodePort 30081 |
| Independent scaling | Monitoring and Inference are separate Deployments |
| Docker Hub images | Both custom images are on Docker Hub |
| Separate database | PostgreSQL runs separately |
| Persistent storage | PostgreSQL uses a PVC |
| Database does not need scaling | PostgreSQL uses one replica |
| Programmatic REST API use | Monitoring calls Inference with requests.post() |

## Author

Hamza

MSc Computer Science  
Blekinge Institute of Technology
