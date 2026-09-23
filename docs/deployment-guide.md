# Deployment Guide

This guide explains how I run the project with Docker Desktop Kubernetes.

## Requirements

You need:

- Docker Desktop
- Kubernetes enabled in Docker Desktop
- kubectl
- Git

The application images are already on Docker Hub:

```text
hamza2635/churn-inference:1.0
hamza2635/churn-monitoring:1.1
```

PostgreSQL uses:

```text
postgres:16
```

## 1. Clone the Repository

```bash
git clone https://github.com/hamzat2635/docker-kubernetes-ml-churn-monitoring.git
cd docker-kubernetes-ml-churn-monitoring
```

## 2. Check Kubernetes

```bash
kubectl config current-context
kubectl get nodes
```

With Docker Desktop, the context should normally be:

```text
docker-desktop
```

The node should show `Ready`.

## 3. Create the Database Secret

The real Secret file is not stored in Git.

Copy:

```text
kubernetes/postgres-secret.example.yaml
```

and create:

```text
kubernetes/postgres-secret.yaml
```

Add your own database username and password.

Do not commit this file.

## 4. Deploy PostgreSQL

```bash
kubectl apply -f kubernetes/postgres-secret.yaml
kubectl apply -f kubernetes/postgres-pvc.yaml
kubectl apply -f kubernetes/postgres-deployment.yaml
kubectl apply -f kubernetes/postgres-service.yaml
```

Check:

```bash
kubectl get pods
kubectl get pvc
```

The PVC should show `Bound`.

## 5. Deploy the Inference Service

```bash
kubectl apply -f kubernetes/inference-deployment.yaml
kubectl apply -f kubernetes/inference-service.yaml
```

## 6. Deploy the Monitoring Service

```bash
kubectl apply -f kubernetes/monitoring-configmap.yaml
kubectl apply -f kubernetes/monitoring-deployment.yaml
kubectl apply -f kubernetes/monitoring-service.yaml
```

## 7. Check Everything

```bash
kubectl get deployments
kubectl get pods
kubectl get services
kubectl get pvc
```

## 8. Open the Dashboard

Open:

```text
http://localhost:30081/
```

Enter customer information and click **Predict Churn**.

Use **Load Prediction History** to show saved predictions.

## 9. Check Logs

```bash
kubectl logs deployment/monitoring --tail=50
kubectl logs deployment/inference --tail=50
kubectl logs deployment/postgres --tail=50
```

## 10. Scale the Services

```bash
kubectl scale deployment inference --replicas=3
kubectl scale deployment monitoring --replicas=2
```

Check:

```bash
kubectl get deployments
kubectl get pods
```

PostgreSQL stays at one replica.

## 11. Test Self-Healing

First list the Inference Pods:

```bash
kubectl get pods -l app=inference
```

Delete one Pod:

```bash
kubectl delete pod <inference-pod-name>
```

Check again:

```bash
kubectl get pods -l app=inference
```

Kubernetes should create a replacement Pod.

## 12. Test Database Persistence

Create at least one prediction in the dashboard.

Delete the PostgreSQL Pod:

```bash
kubectl delete pod -l app=postgres
```

Wait for the new Pod:

```bash
kubectl get pods -l app=postgres
```

Open the dashboard again and load prediction history.

The old records should still be there because PostgreSQL uses the PVC.

## 13. FastAPI Documentation

Monitoring API:

```text
http://localhost:30081/docs
```

The Inference Service is internal.

To open its API documentation:

```bash
kubectl port-forward service/inference-service 8000:8000
```

Then open:

```text
http://localhost:8000/docs
```

Press `Ctrl+C` to stop port forwarding.

## Note About Storage

The included PVC uses the Docker Desktop `hostpath` StorageClass.

If you run this project on another Kubernetes cluster, you may need to change the StorageClass.
