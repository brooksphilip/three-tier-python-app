# Three-Tier Python Application

A three-tier microservices course registration application with **Python Flask frontend and backend**, PostgreSQL database, and Nginx reverse proxy.

## Architecture

- **Frontend**: Python Flask web server serving static HTML/JS files (port 3000)
- **Backend**: Python Flask REST API (port 5000)
- **Database**: PostgreSQL
- **Reverse Proxy**: Nginx (port 80)

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

### Using Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Or use the Chainguard hardened version
docker-compose -f docker-compose-chainguard.yaml up --build
```

The application will be available at http://localhost

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
