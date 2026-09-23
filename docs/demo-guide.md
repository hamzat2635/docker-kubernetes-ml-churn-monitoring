# Demo Guide

This is the order I plan to use for the 5 to 10 minute assignment video.

## Before Recording

Check that Kubernetes is running:

```bash
kubectl get deployments
kubectl get pods
kubectl get services
kubectl get pvc
```

For the scaling part, I can use:

```bash
kubectl scale deployment inference --replicas=3
kubectl scale deployment monitoring --replicas=2
```

The dashboard should open at:

```text
http://localhost:30081/
```

## 1. Introduction

I will explain that the project predicts customer churn.

It uses:

- FastAPI
- Logistic Regression
- PostgreSQL
- Docker
- Kubernetes

The main parts are:

```text
Monitoring Service
Inference Service
PostgreSQL
```

## 2. Architecture

I will show this flow:

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
Logistic Regression

Monitoring Service
   |
   v
PostgreSQL
```

I will explain that the Monitoring Service calls the Inference Service through REST and stores the result in PostgreSQL.

## 3. Kubernetes Resources

Run:

```bash
kubectl get deployments
kubectl get pods
kubectl get services
kubectl get pvc
```

I will explain:

- Monitoring and Inference are separate Deployments
- they can scale separately
- PostgreSQL has one replica
- Monitoring uses NodePort
- Inference and PostgreSQL stay internal
- PostgreSQL uses a PVC

## 4. Show the Dashboard

Open:

```text
http://localhost:30081/
```

Enter a customer and click **Predict Churn**.

Then click **Load Prediction History**.

I will explain the request flow:

1. browser sends data to Monitoring
2. Monitoring calls Inference
3. Inference runs the model
4. Inference returns prediction and probability
5. Monitoring saves the result in PostgreSQL
6. Monitoring shows the result in the browser

## 5. Show the REST APIs

Open:

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

For the Inference API:

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

## 6. Show Logs

Run:

```bash
kubectl logs deployment/monitoring --tail=20
kubectl logs deployment/inference --tail=20
```

I will explain that these logs show requests handled by the services.

## 7. Show Scaling

Run:

```bash
kubectl get deployments
```

I will show:

```text
Inference:   3 replicas
Monitoring:  2 replicas
PostgreSQL:  1 replica
```

I will mention that the project is small and does not really need this scale. I am using it to show that the two application services can scale independently.

## 8. Show Self-Healing

List the Inference Pods:

```bash
kubectl get pods -l app=inference
```

Delete one:

```bash
kubectl delete pod <inference-pod-name>
```

Then check again:

```bash
kubectl get pods -l app=inference
```

I will explain that Kubernetes creates a replacement Pod automatically.

## 9. Explain Persistence

Show:

```bash
kubectl get pvc
```

I will explain the test:

1. I saved prediction records
2. I deleted the PostgreSQL Pod
3. Kubernetes created a new PostgreSQL Pod
4. the old prediction records were still available

## 10. Show the YAML Files

I will briefly open these files:

```text
inference-deployment.yaml
inference-service.yaml
monitoring-deployment.yaml
monitoring-service.yaml
monitoring-configmap.yaml
postgres-deployment.yaml
postgres-service.yaml
postgres-pvc.yaml
postgres-secret.example.yaml
```

I will point out:

- Docker Hub image names
- replica settings
- container ports
- health checks
- ConfigMap values
- Secret values
- NodePort
- PVC

## 11. Security and Finish

I will mention:

- database credentials use a Kubernetes Secret
- the real Secret file is ignored by Git
- PostgreSQL is internal
- Inference is internal
- only Monitoring is exposed outside Kubernetes

For production, I would also add HTTPS, authentication, NetworkPolicies, RBAC and better secret management.

I will finish by saying that the project shows REST APIs, Docker, Kubernetes, scaling, self-healing and persistent storage.
