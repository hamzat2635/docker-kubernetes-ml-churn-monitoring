# Software Architecture

## Software Description

This project predicts if a telecom customer is likely to churn.

The user enters customer information in a web dashboard. The Monitoring Service receives the data and sends it to the Inference Service with a REST request. The Inference Service runs the trained Logistic Regression model and returns a prediction and probability.

The Monitoring Service saves the result in PostgreSQL. The user can also load old predictions from the dashboard.

The application is containerized with Docker and deployed with Kubernetes.

## Architecture Overview

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

The application has three main parts:

1. Monitoring Service
2. Inference Service
3. PostgreSQL

## Monitoring Service

The Monitoring Service is the service used by the browser.

Its jobs are:

- show the dashboard
- receive customer input
- call the Inference Service
- save prediction results
- return prediction history

REST endpoints:

```text
GET  /
GET  /health
POST /analyze
GET  /predictions
```

The Monitoring Service does not run the machine learning model itself.

## Inference Service

The Inference Service only handles machine learning prediction.

Its jobs are:

- load the saved Logistic Regression model
- receive customer data
- run the prediction
- return Churn or Stay
- return churn probability

REST endpoints:

```text
GET  /health
POST /predict
```

Example:

```json
{
  "prediction": "Churn",
  "churn_probability": 0.7847
}
```

## PostgreSQL

PostgreSQL runs separately from the two application services.

It stores:

- customer input
- prediction
- churn probability
- timestamp

The Monitoring Service connects to PostgreSQL through:

```text
postgres-service
```

## REST Communication

The project shows both creating and using REST APIs.

The browser sends customer data to:

```text
POST /analyze
```

The Monitoring Service then calls:

```text
POST http://inference-service:8000/predict
```

The Inference Service returns the result as JSON.

The flow is:

```text
Browser
   |
   v
Monitoring Service
   |
   v
Inference Service
   |
   v
Monitoring Service
   |
   +----> PostgreSQL
   |
   v
Browser
```

## Kubernetes Service Discovery

Kubernetes Services give stable names to the application.

The Monitoring Service uses:

```text
inference-service
postgres-service
```

This means the application does not need to know the IP address of each Pod.

If a Pod is replaced, the Service name stays the same.

## External Access

The Monitoring Service uses a NodePort.

The dashboard can be opened at:

```text
http://localhost:30081/
```

The Inference Service and PostgreSQL stay inside Kubernetes.

## Horizontal Scaling

The Monitoring Service and Inference Service are separate Deployments.

They can be scaled separately:

```bash
kubectl scale deployment inference --replicas=3
kubectl scale deployment monitoring --replicas=2
```

I tested:

```text
Inference:   3 replicas
Monitoring:  2 replicas
PostgreSQL:  1 replica
```

The application is small, so this amount of scaling is not needed for real traffic. It is used to show how Kubernetes scaling works.

## Persistent Storage

PostgreSQL uses:

```text
postgres-pvc
```

The PVC is mounted at:

```text
/var/lib/postgresql/data
```

I tested persistence by saving predictions, deleting the PostgreSQL Pod and checking the data again after Kubernetes created a new Pod.

The data was still available.

## Self-Healing

The Monitoring and Inference Services have health endpoints.

Their Deployments use readiness and liveness probes.

I also tested self-healing by deleting an Inference Pod. Kubernetes automatically created another Pod.

## Configuration

The Monitoring Service gets normal configuration from a ConfigMap:

```text
INFERENCE_SERVICE_URL
DB_HOST
DB_PORT
DB_NAME
```

Database username and password come from a Kubernetes Secret.

The real Secret file is not stored in Git.

## Component Mapping

| Component | Runs as | Job |
|---|---|---|
| Dashboard | Monitoring Service | User interface |
| Monitoring API | Monitoring Service | Receives requests and connects other parts |
| ML prediction | Inference Service | Runs the model |
| Prediction history | Monitoring Service | Reads and writes database records |
| Database | PostgreSQL | Stores predictions |
| Persistent data | PVC | Keeps database files |
| Internal networking | Kubernetes Services | Connects Pods |
| External access | NodePort | Opens the dashboard in a browser |

## Architecture Ideas Used

The project uses some simple cloud architecture ideas:

- Each service has its own job.
- Monitoring and Inference can scale separately.
- Kubernetes Services give stable internal names.
- Application Pods do not store important data.
- Configuration is passed with ConfigMaps and Secrets.
- Kubernetes can replace failed Pods.
- PostgreSQL data is stored outside the Pod with a PVC.
- Docker images make the application easier to run in the same way in different environments.
