# Architecture Benefits, Challenges and Security

## Benefits

### Separation of concerns

The Monitoring Service, Inference Service, and PostgreSQL database have different responsibilities. The web interface and prediction history are separated from machine learning inference, while persistent state is handled by PostgreSQL.

This makes each part easier to understand and allows a component to be changed without placing all application logic in one process.

### Independent horizontal scaling

Monitoring and Inference are separate Kubernetes Deployments, so their replica counts can be changed independently.

For example, if machine learning inference becomes the most expensive part of the application, additional Inference Pods can be created without also creating more Monitoring Pods.

The current project is small and does not need multiple replicas for real traffic. The scaling demonstration shows how the design could support a larger workload.

### Self-healing

Kubernetes Deployments maintain the desired number of application Pods. When an Inference Pod was manually deleted during testing, Kubernetes created a replacement Pod automatically.

This reduces dependence on a specific container instance.

### Stable service discovery

The application communicates through Kubernetes Service names such as:

```text
inference-service
postgres-service
```

The application therefore does not need to know individual Pod IP addresses.

### Deployment consistency

Docker images package the application and its dependencies. Kubernetes can pull the same images from Docker Hub each time a Pod is created.

### Persistent data

PostgreSQL uses a PersistentVolumeClaim. The PostgreSQL Pod can be replaced without intentionally deleting the stored prediction history.

## Challenges

### Increased system complexity

A microservice design introduces more moving parts than a single application. The browser, Monitoring Service, Inference Service, PostgreSQL, Kubernetes Services, configuration, and storage must all work together.

A failure in one dependency can affect the complete request flow.

**Mitigation:** clear service responsibilities, health endpoints, Kubernetes probes, simple REST interfaces, and documented deployment steps reduce this complexity.

### Network dependency

The Monitoring Service depends on a network call to the Inference Service. If the Inference Service is unavailable or slow, a prediction request cannot complete normally.

**Current mitigation:** the Monitoring Service uses an HTTP timeout and returns a service error when the inference request fails. Kubernetes can also run multiple Inference replicas.

**Further mitigation:** retries with backoff, circuit breakers, and better observability could be added in a production system.

### Database availability

PostgreSQL currently runs as one replica. Persistent storage protects data from ordinary Pod replacement, but it does not make the database highly available.

**Mitigation for this project:** Kubernetes recreates the PostgreSQL Pod and remounts the PVC.

**Production option:** use a managed highly available PostgreSQL service or a properly configured replicated database system.

### Local storage limitations

The assignment deployment uses Docker Desktop's `hostpath` StorageClass. This is suitable for a local Kubernetes demonstration but is not equivalent to durable multi-node cloud storage.

**Production option:** use a cloud PersistentVolume implementation or managed database storage.

### Model updates

The trained model is packaged with the Inference Service image. Replacing the model currently requires building and deploying a new image.

This is simple and reproducible for the assignment, but frequent model updates would require a more mature model lifecycle.

**Production option:** use model versioning, an artifact registry, automated validation, and controlled rollout strategies.

### Operational overhead

Microservices require more deployment, networking, configuration, monitoring, and troubleshooting than a simple monolithic application.

For a small application, this overhead may be greater than the practical benefit. In this project the architecture is intentionally used to demonstrate cloud computing concepts.

## Business Implications

The architecture allows resources to be assigned to the component that needs them. In a larger churn platform, prediction traffic could require more compute resources than the web interface. Independent scaling can therefore avoid scaling every component equally.

Containerized deployment can also improve consistency between development and deployment environments.

However, microservices introduce additional engineering and operational cost. For a small business application with low traffic, a monolith may be cheaper and simpler. The business case becomes stronger when there is enough traffic, independent workload variation, deployment frequency, or team separation to justify the additional complexity.

The current project should therefore be understood as a small demonstration of an architecture that becomes more useful at larger scale.

## Security

### Measures already used

The project includes several basic security decisions:

- PostgreSQL credentials are provided through a Kubernetes Secret rather than being written directly in the Deployment YAML.
- The real `postgres-secret.yaml` file is excluded from Git.
- A placeholder `postgres-secret.example.yaml` file is provided for repository users.
- PostgreSQL is only exposed through an internal Kubernetes Service.
- The Inference Service is also internal.
- Only the Monitoring Service is exposed outside the cluster.

These choices reduce unnecessary external exposure and avoid committing the real database credentials to the repository.

### Limitations

A Kubernetes Secret is a better configuration mechanism than hard-coding credentials, but it should not be treated as complete secret protection by itself. Kubernetes Secrets are not automatically equivalent to a dedicated encrypted secret-management system.

The demonstration application also does not currently implement:

- User authentication
- Role-based application authorization
- HTTPS/TLS termination
- Kubernetes NetworkPolicies
- Rate limiting
- Production secret management
- Detailed audit logging

The NodePort endpoint is therefore appropriate for a local assignment demonstration, not a public production service.

### Further security improvements

A production deployment could add:

- HTTPS through an Ingress or cloud LoadBalancer.
- Authentication and authorization for the dashboard and APIs.
- Kubernetes NetworkPolicies restricting which Pods may communicate.
- Least-privilege Kubernetes RBAC.
- Encryption of secrets at rest or an external secret manager.
- Container image and dependency vulnerability scanning.
- Non-root containers and restricted security contexts.
- CPU and memory requests/limits.
- Rate limiting.
- More restrictive input validation.
- Centralized logging and security monitoring.
- Regular image and dependency updates.

## Summary

The architecture demonstrates important cloud-native benefits such as separation of responsibilities, independent scaling, service discovery, self-healing, and persistent state.

The trade-off is additional operational complexity. The design is intentionally larger than required by the current amount of traffic because the assignment is demonstrating how these patterns work and how they could support a larger real-world workload.
