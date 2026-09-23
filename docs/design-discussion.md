# Architecture Benefits, Challenges and Security

## Benefits

### Clear responsibilities

The project is split into separate parts.

The Monitoring Service handles the dashboard and database communication. The Inference Service handles machine learning prediction. PostgreSQL stores the data.

This makes it easier to understand what each part is doing.

### Independent scaling

Monitoring and Inference are separate Kubernetes Deployments.

If prediction becomes the busy part of the application, I can add more Inference Pods without adding more Monitoring Pods.

The project is small, so it does not really need many replicas. I used scaling to show how the architecture would work with more traffic.

### Self-healing

Kubernetes keeps the required number of Pods running.

I tested this by deleting an Inference Pod. Kubernetes created another one automatically.

### Service discovery

The services use names like:

```text
inference-service
postgres-service
```

The application does not need to know the IP address of every Pod.

### Persistent data

PostgreSQL uses a PersistentVolumeClaim.

This means the database data is not stored only inside the PostgreSQL Pod.

## Challenges

### More parts to manage

A microservice application has more parts than a simple single application.

For this project, the browser, Monitoring Service, Inference Service, PostgreSQL, Kubernetes Services and storage all need to work together.

This makes debugging and deployment more complicated.

To make this easier, I kept each service small and used simple REST endpoints.

### Network dependency

The Monitoring Service needs the Inference Service to answer before a prediction can finish.

If the Inference Service is down, the request will fail.

The Monitoring Service uses a timeout so it does not wait forever.

Running more than one Inference Pod can also help if one Pod fails.

### Database availability

PostgreSQL only has one replica.

The data survives a normal Pod replacement because of the PVC, but the database is still unavailable for a short time while the Pod is restarting.

For a real production system, a managed PostgreSQL service or a replicated database setup would be better.

### Local storage

This project uses Docker Desktop and the `hostpath` StorageClass.

This is fine for the assignment and local testing, but it is not the same as cloud storage used in a real production system.

### Model updates

The machine learning model is saved inside the Inference Service image.

If I want to replace the model, I need to build and deploy a new image.

This is simple for this project, but a larger system could use model versioning and a model registry.

## Business Implications

A microservice design can be useful when different parts of the application need different amounts of resources.

For example, if many predictions are being made, the Inference Service may need more replicas while the web interface may not.

This can help avoid using extra resources for parts of the application that do not need them.

The disadvantage is that microservices are more complex to manage.

For a very small system, a single application could be easier and cheaper.

For this assignment, I used microservices because the goal is to show cloud deployment, scaling and service communication.

## Security

### What I already did

The project includes some basic security steps:

- database credentials are stored in a Kubernetes Secret
- the real Secret file is ignored by Git
- PostgreSQL is not exposed outside Kubernetes
- the Inference Service is not exposed outside Kubernetes
- only the Monitoring Service is available from the browser

### Current limitations

This is a student project and not a production system.

It does not currently include:

- user login
- HTTPS
- application authorization
- NetworkPolicies
- rate limiting
- advanced secret management
- security monitoring

### What could be improved

For a production version, I would add:

- HTTPS
- user authentication
- authorization
- Kubernetes NetworkPolicies
- RBAC
- stronger secret storage
- image scanning
- CPU and memory limits
- better input validation
- centralized logs and monitoring
- regular dependency updates

## Summary

The main benefits of the architecture are separation of responsibilities, independent scaling, self-healing and persistent storage.

The main disadvantage is extra complexity.

The application is small, but it is useful for showing how these cloud concepts work in practice.
