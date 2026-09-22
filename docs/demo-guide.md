# Demo Guide

This guide is designed for the required 5-10 minute project video.

## Before Recording

Make sure Kubernetes is running and the application is deployed.

A useful test configuration is:

```bash
kubectl scale deployment inference --replicas=3
kubectl scale deployment monitoring --replicas=2
```

Check:

```bash
kubectl get deployments
kubectl get pods
kubectl get services
kubectl get pvc
```

Also confirm that the dashboard opens at:

```text
http://localhost:30081/
```

## 1. Introduction - about 45 seconds

Explain:

- The project predicts telecom customer churn.
- It uses a trained Logistic Regression model.
- It is built as a microservice application.
- It uses FastAPI, PostgreSQL, Docker, and Kubernetes.

Mention the three main runtime components:

```text
Monitoring Service
Inference Service
PostgreSQL
```

## 2. Architecture - about 60 seconds

Show the architecture documentation or README.

Explain the request flow:

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
Logistic Regression

Monitoring Service
   |
   | SQL
   v
PostgreSQL
   |
   v
PersistentVolumeClaim
```

Important points to mention:

- Monitoring provides the UI and coordinates requests.
- Inference performs only ML prediction.
- PostgreSQL stores prediction history.
- Monitoring programmatically consumes the Inference REST API.

## 3. Kubernetes Resources - about 60 seconds

Run:

```bash
kubectl get deployments
kubectl get pods
kubectl get services
kubectl get pvc
```

Explain:

- Monitoring and Inference are separate Deployments.
- Their replica counts can be changed independently.
- PostgreSQL remains at one replica.
- `monitoring-service` is a NodePort.
- `inference-service` and `postgres-service` are internal.
- `postgres-pvc` provides persistent database storage.

## 4. User Interface and Prediction - about 60-90 seconds

Open:

```text
http://localhost:30081/
```

Enter a customer and click **Predict Churn**.

Explain what happens:

1. Browser sends data to `POST /analyze`.
2. Monitoring sends the same customer data to Inference `POST /predict`.
3. Inference runs the Logistic Regression pipeline.
4. Inference returns a prediction and probability.
5. Monitoring stores the result in PostgreSQL.
6. Monitoring returns the result to the browser.

Then click **Load Prediction History** to show stored database records.

## 5. REST API - about 45 seconds

Open the Monitoring FastAPI documentation:

```text
http://localhost:30081/docs
```

Show:

```text
GET  /
GET  /health
POST /analyze
GET  /predictions
```

Explain that `POST /analyze` uses Python `requests.post()` to programmatically consume the Inference REST API.

If you want to show the Inference API documentation, run:

```bash
kubectl port-forward service/inference-service 8000:8000
```

Then open:

```text
http://localhost:8000/docs
```

Show:

```text
GET  /health
POST /predict
```

## 6. Logs - about 30 seconds

Show application logs as required by the assignment:

```bash
kubectl logs deployment/monitoring --tail=20
kubectl logs deployment/inference --tail=20
```

Explain that the logs show HTTP requests handled by the FastAPI/Uvicorn services.

If multiple Pods are running and you want one specific Pod:

```bash
kubectl get pods
kubectl logs <pod-name> --tail=20
```

## 7. Scaling and Self-Healing - about 60 seconds

Show:

```bash
kubectl get deployments
```

Explain that a tested configuration uses:

```text
Inference:   3 replicas
Monitoring:  2 replicas
PostgreSQL:  1 replica
```

The application itself is too small to need these replicas for real traffic. The purpose is to demonstrate how independent horizontal scaling would work under a larger workload.

For self-healing, list Inference Pods:

```bash
kubectl get pods -l app=inference
```

Delete one:

```bash
kubectl delete pod <inference-pod-name>
```

Then:

```bash
kubectl get pods -l app=inference
```

Explain that Kubernetes creates a replacement because the Deployment maintains the desired replica count.

## 8. Persistence - about 45 seconds

Show:

```bash
kubectl get pvc
```

Explain the test already performed:

1. Prediction records were stored.
2. The PostgreSQL Pod was deleted.
3. Kubernetes created a replacement PostgreSQL Pod.
4. The old prediction records were still available.

This demonstrates persistence across Pod replacement.

If time allows, perform the deletion during the recording:

```bash
kubectl delete pod -l app=postgres
kubectl get pods -l app=postgres
```

Then reload prediction history.

## 9. Kubernetes YAML Walkthrough - about 60-90 seconds

Open the `kubernetes/` folder.

Briefly show:

### inference-deployment.yaml

Point out:

- Docker Hub image
- container port
- readiness probe
- liveness probe
- replicas

### inference-service.yaml

Explain that it gives Inference a stable internal address.

### monitoring-deployment.yaml

Point out:

- Docker Hub image
- ConfigMap values
- Secret values
- health probes

### monitoring-service.yaml

Point out:

```text
type: NodePort
nodePort: 30081
```

Explain that this makes the dashboard accessible from outside Kubernetes.

### postgres-deployment.yaml

Point out:

- `postgres:16`
- Secret-based credentials
- PVC volume mount

### postgres-pvc.yaml

Explain that it requests persistent storage.

### monitoring-configmap.yaml

Explain that non-sensitive runtime configuration is separated from application code.

### postgres-secret.example.yaml

Explain that the real Secret file is excluded from Git and only a safe example is committed.

## 10. Security and Conclusion - about 45 seconds

Mention current security decisions:

- Database credentials are stored in a Kubernetes Secret.
- The real Secret YAML is excluded from Git.
- PostgreSQL is internal.
- Inference is internal.
- Only Monitoring is externally exposed.

Mention production improvements:

- HTTPS
- Authentication and authorization
- NetworkPolicies
- RBAC
- stronger secret management
- container scanning
- resource limits

Finish by summarizing that the project demonstrates:

- REST API creation
- Programmatic REST API consumption
- Docker containerization
- Kubernetes deployment
- Independent horizontal scaling
- Service discovery
- Self-healing
- PostgreSQL persistence
- Browser access
