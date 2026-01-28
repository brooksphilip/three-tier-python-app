# Three-Tier Python Application

A three-tier microservices course registration application with **Python Flask frontend and backend**, PostgreSQL database, and Nginx reverse proxy.

## Architecture

- **Frontend**: Python Flask web server serving static HTML/JS files (port 3000)
- **Backend**: Python Flask REST API (port 5000)
- **Database**: PostgreSQL
- **Reverse Proxy**: Nginx (port 80)

## Prerequisites

### Required
- **Docker**: Container runtime ([Install Docker](https://docs.docker.com/get-docker/))
- **Docker Compose**: Multi-container orchestration ([Install Docker Compose](https://docs.docker.com/compose/install/))
- **Grype**: Binary Level Container Scanner ([Grype Github](https://github.com/anchore/grype))
- **Trivy**: Package Level Container Scanner ([Trivy Getting Started](https://trivy.dev/docs/latest/getting-started/))


## Project Structure

```
├── frontend/              # Python Flask frontend
│   ├── src/
│   │   └── server.py     # Flask server
│   ├── public/           # Static HTML/JS files
│   ├── requirements.txt  # Python dependencies (easily modifiable)
│   └── Dockerfile
├── backend/              # Python Flask backend
│   ├── app/
│   ├── requirements.txt  # Python dependencies
│   └── Dockerfile
├── db/                   # PostgreSQL initialization
│   └── Dockerfile
├── nginx/                # Nginx configuration
│   └── Dockerfile
├── docker-compose.yaml   # Standard Docker Compose
└── docker-compose-chainguard.yaml  # Hardened Chainguard images
```

## Quick Start

## Clone Repo
```bash
git clone https://github.com/brooksphilip/three-tier-python-app
cd three-tier-python-app
```

### Using Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Or use the Chainguard hardened version
docker-compose -f docker-compose-chainguard.yaml up --build
```
The application will be available at http://localhost

# Appendix 

### Running Frontend Locally

```bash
cd frontend
pip install -r requirements.txt
python src/server.py
```

## Modifying Dependencies

The frontend and backend both use `requirements.txt` files where you can easily add, remove, or update Python packages:

**Frontend** (`frontend/requirements.txt`):
- Flask (web framework)
- gunicorn (production WSGI server)
- Optional packages commented out (CORS, requests, etc.)

**Backend** (`backend/requirements.txt`):
- Flask
- psycopg2 (PostgreSQL adapter)
- Other backend dependencies

Simply edit the requirements.txt files and rebuild the containers to apply changes.

## Security Comparison

This repository includes two versions:
- **docker-compose.yaml**: Uses standard upstream images
- **docker-compose-chainguard.yaml**: Uses minimal, hardened Chainguard images

The Chainguard version demonstrates significant security improvements with ~99% CVE reduction and ~83% size reduction.

## Security Scanning

After building the images, scan them for vulnerabilities to compare security postures:

### Scan Standard Images
```bash
# Build standard images first
docker-compose build

# Scan with Grype
grype three-tier-frontend-legacy:latest
grype three-tier-backend-legacy:latest
grype three-tier-db-legacy:latest
grype three-tier-nginx-legacy:latest

# Scan with Trivy
trivy image three-tier-frontend-legacy:latest
trivy image three-tier-backend-legacy:latest
trivy image three-tier-db-legacy:latest
trivy image three-tier-nginx-legacy:latest
```

### Scan Chainguard Images
```bash
# Build Chainguard images first
docker-compose -f docker-compose-chainguard.yaml build

# Scan with Grype
grype three-tier-frontend-cg:latest
grype three-tier-backend-cg:latest
grype three-tier-db-cg:latest
grype three-tier-nginx-cg:latest

# Scan with Trivy
trivy image three-tier-frontend-cg:latest
trivy image three-tier-backend-cg:latest
trivy image three-tier-db-cg:latest
trivy image three-tier-nginx-cg:latest
```

### Compare Results
```bash
# Generate detailed comparison reports
grype three-tier-frontend-legacy:latest -o json > frontend-legacy-grype.json
grype three-tier-frontend-cg:latest -o json > frontend-cg-grype.json

trivy image --format json three-tier-backend-legacy:latest > backend-legacy-trivy.json
trivy image --format json three-tier-backend-cg:latest > backend-cg-trivy.json
```

## License

MIT License - see LICENSE file for details
