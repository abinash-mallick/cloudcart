# CloudCart — Docker + GitHub Actions + Kubernetes Practice Project

CloudCart is a deliberately small e-commerce application designed for learning:

- Dockerfile
- Docker image creation
- Docker networking
- Docker Compose
- PostgreSQL
- GitHub Actions
- Docker Hub
- Kubernetes Deployments and Services
- Kubernetes ConfigMaps and Secrets
- Kubernetes persistent storage
- Rolling updates

## Architecture

Browser
   |
   v
Flask application
   |
   v
PostgreSQL database

The Flask app exposes:

- `GET /` — web page
- `GET /health` — health check
- `GET /api/products` — product API
- `POST /api/products` — create a product

## Environment variables

The application reads:

- `DB_HOST`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_PORT`

Defaults are included for local development.

## Your hands-on tasks

Do NOT add Kubernetes manifests yet.

### Phase 1 — Run without Docker

Create a Python virtual environment, install `requirements.txt`, start PostgreSQL, set the DB variables, and run:

    python app.py

### Phase 2 — Dockerfile

Write your own Dockerfile.

Goal:

    docker build -t cloudcart:1.0 .

Then run the application container. At this stage you can use a PostgreSQL container separately.

### Phase 3 — Docker Compose

Write your own `compose.yaml` with:

- `app` service
- `db` service
- PostgreSQL volume
- application/database network
- environment variables

Goal:

    docker compose up -d

Then open:

    http://localhost:5000

Useful commands:

    docker compose ps
    docker compose logs -f
    docker compose down
    docker compose down -v

### Phase 4 — GitHub Actions

Create a workflow that:

1. Checks out the repository.
2. Builds the Docker image.
3. Logs in to Docker Hub using GitHub Secrets.
4. Tags the image.
5. Pushes it to Docker Hub.

### Phase 5 — Kubernetes

Later we will create:

- Namespace
- ConfigMap
- Secret
- PostgreSQL Deployment
- PostgreSQL Service
- PersistentVolumeClaim
- CloudCart Deployment
- CloudCart Service
- readiness/liveness probes
- resource requests/limits

Then GitHub Actions can build and push the image, and Kubernetes can deploy the new version.

## Important learning rule

Try to write the Dockerfile and Compose file yourself first. Ask for help one step at a time rather than copying the complete solution immediately.
