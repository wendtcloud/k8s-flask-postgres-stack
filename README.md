# Kubernetes Flask PostgreSQL Stack

A multi-tier containerized application deployed on Kubernetes (Minikube), featuring stateful data persistence, self-healing health probes, and path-based ingress routing.

## Architecture & Components

- **Backend:** Python Flask API deployed via a Kubernetes Deployment, utilizing custom HTTP liveness and readiness probes.
- **Database:** PostgreSQL deployed as a StatefulSet with a PersistentVolumeClaim (`volumeClaimTemplates`, 1Gi) ensuring data durability across pod restarts.
- **Networking:** NGINX Ingress Controller configured to route traffic based on URL path prefixes (`/` for frontend/root, `/api/*` for backend endpoints).
- **Security:** Kubernetes Secrets utilized for secure database credential injection.

## Quick Start

1. Build and load the application image into Minikube:
   ```bash
   docker build -t flask-backend:latest ./app
   minikube image load flask-backend:latest
