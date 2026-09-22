# Deployment Guide

This guide deploys the project to the Kubernetes cluster included with Docker Desktop.

## Prerequisites

Install and enable:

- Docker Desktop
- Docker Desktop Kubernetes
- `kubectl`
- Git

The custom application images are already available on Docker Hub:

```text
hamza2635/churn-inference:1.0
hamza2635/churn-monitoring:1.1
```

PostgreSQL uses the official `postgres:16` image.

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

The node should report `Ready`.

## 3. Create the Local Database Secret

The real secret is intentionally not committed to Git.

Copy:

```text
kubernetes/postgres-secret.example.yaml
```

to:

```text
kubernetes/postgres-secret.yaml
```

Then edit the local file and choose your database username and password.

Example structure:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secret
type: Opaque
stringData:
  POSTGRES_USER: your_database_user
  POSTGRES_PASSWORD: your_database_password
```

Do not commit the real secret file.

## 4. Deploy PostgreSQL

Apply the Secret and persistent storage first:

```bash
kubectl apply -f kubernetes/postgres-secret.yaml
kubectl apply -f kubernetes/postgres-pvc.yaml
```

Then deploy PostgreSQL and its Service:

```bash
kubectl apply -f kubernetes/postgres-deployment.yaml
kubectl apply -f kubernetes/postgres-service.yaml
```

Check:

```bash
kubectl get pods
kubectl get pvc
```

The PVC should be `Bound`.

> The included PVC uses Docker Desktop's `hostpath` StorageClass. On another Kubernetes environment, update `storageClassName` to a StorageClass available in that cluster.

## 5. Deploy the Inference Service

```bash
kubectl apply -f kubernetes/inference-deployment.yaml
kubectl apply -f kubernetes/inference-service.yaml
```

Check:

```bash
kubectl get deployment inference
kubectl get pods -l app=inference
```

## 6. Deploy the Monitoring Service

```bash
kubectl apply -f kubernetes/monitoring-configmap.yaml
kubectl apply -f kubernetes/monitoring-deployment.yaml
kubectl apply -f kubernetes/monitoring-service.yaml
```

Check:

```bash
kubectl get deployment monitoring
kubectl get pods -l app=monitoring
```

## 7. Verify the Complete Deployment

```bash
kubectl get deployments
kubectl get pods
kubectl get services
kubectl get pvc
```

The default YAML configuration starts one replica of each Deployment.

## 8. Open the Dashboard

Open:

```text
http://localhost:30081/
```

The Monitoring Service is exposed with a NodePort on port `30081`.

## 9. Test a Prediction

Enter customer information in the dashboard and select **Predict Churn**.

The request flow is:

```text
Browser
  -> Monitoring Service
  -> Inference Service
  -> Monitoring Service
  -> PostgreSQL
  -> Browser
```

Use **Load Prediction History** to retrieve records stored in PostgreSQL.

## 10. View Logs

Monitoring logs:

```bash
kubectl logs deployment/monitoring --tail=50
```

Inference logs:

```bash
kubectl logs deployment/inference --tail=50
```

PostgreSQL logs:

```bash
kubectl logs deployment/postgres --tail=50
```

For a deployment with multiple replicas, you can also list Pods and inspect one specific Pod:

```bash
kubectl get pods
kubectl logs <pod-name>
```

## 11. Horizontal Scaling

Scale the application services independently:

```bash
kubectl scale deployment inference --replicas=3
kubectl scale deployment monitoring --replicas=2
```

Verify:

```bash
kubectl get deployments
kubectl get pods
```

PostgreSQL remains at one replica.

## 12. Demonstrate Self-Healing

List Inference Pods:

```bash
kubectl get pods -l app=inference
```

Delete one Inference Pod:

```bash
kubectl delete pod <inference-pod-name>
```

Then watch Kubernetes create a replacement:

```bash
kubectl get pods -l app=inference -w
```

Press `Ctrl+C` to stop watching.

## 13. Verify Database Persistence

Create at least one prediction through the dashboard.

Optional SQL check:

```bash
kubectl exec deployment/postgres -- psql -U <database-user> -d churndb -c "SELECT id, prediction, churn_probability, created_at FROM predictions ORDER BY id DESC LIMIT 5;"
```

Delete the PostgreSQL Pod:

```bash
kubectl delete pod -l app=postgres
```

Wait for the replacement Pod:

```bash
kubectl get pods -l app=postgres
```

Reload the prediction history in the dashboard. Previously stored data should still be present because PostgreSQL uses the PVC.

## 14. Access FastAPI Documentation

Monitoring API documentation is available through the external service:

```text
http://localhost:30081/docs
```

The Inference Service is intentionally internal. To inspect its FastAPI documentation locally:

```bash
kubectl port-forward service/inference-service 8000:8000
```

Then open:

```text
http://localhost:8000/docs
```

Stop port forwarding with `Ctrl+C`.

## 15. Remove the Deployment

To remove the application resources:

```bash
kubectl delete -f kubernetes/monitoring-service.yaml
kubectl delete -f kubernetes/monitoring-deployment.yaml
kubectl delete -f kubernetes/monitoring-configmap.yaml
kubectl delete -f kubernetes/inference-service.yaml
kubectl delete -f kubernetes/inference-deployment.yaml
kubectl delete -f kubernetes/postgres-service.yaml
kubectl delete -f kubernetes/postgres-deployment.yaml
```

Delete the PVC only if you intentionally want to remove the persistent database storage:

```bash
kubectl delete -f kubernetes/postgres-pvc.yaml
```

The database Secret can be removed separately:

```bash
kubectl delete secret postgres-secret
```
