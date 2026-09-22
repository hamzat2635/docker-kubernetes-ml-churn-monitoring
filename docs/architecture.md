# Software Architecture

## 1. Software Description

This project is a cloud-native customer churn prediction and monitoring application.

A user enters telecom customer information in a web dashboard. The Monitoring Service receives the request and programmatically calls the Inference Service through a REST API. The Inference Service loads a trained Logistic Regression pipeline and returns a churn prediction together with a churn probability.

The Monitoring Service then stores the customer input, prediction, probability, and timestamp in PostgreSQL. Previous predictions can be loaded from the dashboard.

The application is containerized with Docker and deployed with Kubernetes.

## 2. Architecture Overview

```text
Browser
   |
   | HTTP
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

The application contains two application microservice types and one separate database component:

1. Monitoring Service
2. Inference Service
3. PostgreSQL

## 3. Monitoring Microservice

The Monitoring Service is the user-facing service and the main coordinator of the application.

Responsibilities:

- Serves the HTML dashboard.
- Exposes REST endpoints for analysis and prediction history.
- Accepts customer input from the browser.
- Programmatically calls the Inference Service.
- Stores prediction results in PostgreSQL.
- Reads prediction history from PostgreSQL.

REST endpoints:

```text
GET  /
GET  /health
POST /analyze
GET  /predictions
```

The Monitoring Service does not run the machine learning model itself. This keeps the web/database responsibilities separate from prediction logic.

## 4. Inference Microservice

The Inference Service is responsible only for machine learning inference.

Responsibilities:

- Loads the trained Logistic Regression pipeline.
- Validates incoming customer data through Pydantic.
- Converts the request into a pandas DataFrame.
- Runs model prediction and probability estimation.
- Returns the result as JSON.

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

The Inference Service has no database responsibility.

## 5. PostgreSQL Database

PostgreSQL runs as a separate Kubernetes Deployment with one replica.

It stores:

- Customer input features
- Prediction result
- Churn probability
- Creation timestamp

The Monitoring Service connects to PostgreSQL through the internal Kubernetes Service name:

```text
postgres-service
```

The database uses a PersistentVolumeClaim so that its data is not tied to the lifetime of a specific PostgreSQL Pod.

## 6. REST Communication

The project demonstrates both providing and consuming REST APIs.

The browser sends customer data to:

```text
POST /analyze
```

The Monitoring Service then makes a programmatic HTTP request to the Inference Service:

```text
POST http://inference-service:8000/predict
```

The flow is:

```text
Browser
   |
   v
Monitoring Service
   |
   | POST /predict
   v
Inference Service
   |
   | JSON prediction
   v
Monitoring Service
   |
   +----> PostgreSQL
   |
   v
Browser
```

This demonstrates the ability to program a REST API and programmatically consume a REST API.

## 7. Kubernetes Service Discovery

Kubernetes Services provide stable names for communication between Pods.

Internal services:

```text
inference-service
postgres-service
```

Pods can be deleted and recreated with different IP addresses without requiring application configuration changes. The Monitoring Service continues to use the stable Kubernetes Service names.

The Service for the Inference Deployment also distributes requests across available Inference Pods.

## 8. External Access

The Monitoring Service is exposed outside Kubernetes using a NodePort:

```text
http://localhost:30081/
```

The Inference Service and PostgreSQL use internal ClusterIP Services and are not intentionally exposed outside the cluster.

## 9. Horizontal Scaling

The application microservices are separate Kubernetes Deployments and can be scaled independently.

Example:

```bash
kubectl scale deployment inference --replicas=3
kubectl scale deployment monitoring --replicas=2
```

During testing, the application was run with:

```text
Inference:   3 replicas
Monitoring:  2 replicas
PostgreSQL:  1 replica
```

The YAML files use one replica by default, while scaling can be changed at runtime with Kubernetes.

The current student application does not generate enough traffic to require multiple replicas in practice. The scaling demonstration represents how the design could behave under a larger workload, for example when many customer predictions are requested at the same time.

## 10. Persistent Storage

PostgreSQL uses:

```text
postgres-pvc
```

The PVC is mounted at:

```text
/var/lib/postgresql/data
```

Persistence was tested by:

1. Creating prediction records.
2. Deleting the PostgreSQL Pod.
3. Allowing Kubernetes to create a replacement Pod.
4. Confirming that the previously stored records were still available.

This demonstrates that database data survives ordinary Pod replacement.

## 11. Self-Healing and Health Checks

The Monitoring and Inference Deployments use Kubernetes readiness and liveness probes against their `/health` endpoints.

Kubernetes self-healing was tested by deleting an Inference Pod. Kubernetes automatically created a replacement Pod because the Deployment still required the configured number of replicas.

This separates desired application state from the lifetime of individual containers.

## 12. Configuration Management

The Monitoring Service receives non-sensitive configuration from a Kubernetes ConfigMap:

```text
INFERENCE_SERVICE_URL
DB_HOST
DB_PORT
DB_NAME
```

Database credentials are provided through a Kubernetes Secret.

The real `kubernetes/postgres-secret.yaml` file is excluded from Git. The repository contains `postgres-secret.example.yaml` as a safe template.

## 13. Component-to-Microservice Mapping

| Software component | Kubernetes/runtime component | Responsibility |
|---|---|---|
| Web dashboard | Monitoring Service | Browser-based user interface |
| Monitoring REST API | Monitoring Service | Accept requests and coordinate the application |
| Prediction history | Monitoring Service | Read and write prediction records |
| ML preprocessing | Inference Service | Transform input for the trained pipeline |
| Churn prediction | Inference Service | Run Logistic Regression inference |
| Data storage | PostgreSQL | Store inputs, predictions, probabilities, and timestamps |
| Persistent storage | PersistentVolumeClaim | Preserve PostgreSQL data across Pod replacement |
| Internal routing | Kubernetes Services | Stable networking and service discovery |
| External access | NodePort Service | Expose the dashboard outside the cluster |

## 14. Architecture Principles and Cloud Patterns

The project uses several cloud-native principles:

- **Separation of concerns:** monitoring, inference, and storage have different responsibilities.
- **Independent scalability:** Monitoring and Inference Deployments can use different replica counts.
- **Service discovery:** Kubernetes Services provide stable internal endpoints.
- **Stateless application services:** application state is not stored inside Monitoring or Inference Pods.
- **Externalized configuration:** Kubernetes ConfigMaps and Secrets provide runtime configuration.
- **Health monitoring and self-healing:** probes and Deployments allow Kubernetes to detect and replace unhealthy application Pods.
- **Persistent state separation:** database data is stored through a PVC rather than inside the PostgreSQL container filesystem.
- **Container portability:** custom services are packaged as Docker images and pulled by Kubernetes from Docker Hub.
