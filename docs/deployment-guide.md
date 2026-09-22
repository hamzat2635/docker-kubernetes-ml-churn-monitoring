kubectl apply -f kubernetes/postgres-secret.yaml
kubectl apply -f kubernetes/postgres-pvc.yaml
kubectl apply -f kubernetes/postgres-deployment.yaml
kubectl apply -f kubernetes/postgres-service.yaml

kubectl apply -f kubernetes/inference-deployment.yaml
kubectl apply -f kubernetes/inference-service.yaml

kubectl apply -f kubernetes/monitoring-configmap.yaml
kubectl apply -f kubernetes/monitoring-deployment.yaml
kubectl apply -f kubernetes/monitoring-service.yaml