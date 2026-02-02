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

#### Clone Repo & Set up pip
```bash
git clone https://github.com/brooksphilip/three-tier-python-app
cd three-tier-python-app
cp pip.default pip.conf
```


#### Using Docker Compose

```bash
# Build and start all services
docker compose up -d --build
```

#### Scan Standard Images
```bash
./scanner_diff.py three-tier-frontend-legacy three-tier-backend-legacy three-tier-db-legacy three-tier-nginx-legacy
```

#### Stop The Running Images
```bash
docker compose down
```

#### Use the Chainguard hardened version
```bash
docker-compose -f docker-compose-chainguard.yaml up --build -d
```

#### Scan Chainguard Images
```bash
# Scan with Grype
./scanner_diff.py three-tier-backend-cg three-tier-frontend-cg three-tier-db-cg three-tier-nginx-cg 
```

#### Stop The Running Images
```bash
docker compose down
```

#### Compare Results


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

## License

MIT License - see LICENSE file for details
