# Using Custom PyPI Index with pip.conf

## Quick Start

1. **Create pip.conf from the example:**
   ```bash
   cp pip.example pip.conf
   ```

2. **Edit pip.conf with your dev machine IP:**
   ```bash
   vim pip.conf
   ```

   Replace `YOUR_DEV_IP` with your actual dev machine IP or hostname:
   ```ini
   [global]
   index-url = http://192.168.1.100:8080/simple/
   trusted-host = 192.168.1.100

   [install]
   trusted-host = 192.168.1.100
   ```

3. **Build and run with Chainguard images:**
   ```bash
   docker-compose -f docker-compose-chainguard.yaml up --build
   ```

That's it! Everything else (creating venv, installing packages) happens automatically inside the Docker containers.

## How It Works

The Chainguard Dockerfiles (`Dockerfile-chainguard`) will:
- Copy `pip.conf` to `/etc/pip.conf` in the builder stage
- Use this configuration when installing packages from `requirements.cg.txt`
- Pull packages from your custom PyPI index instead of the public PyPI

## Requirements Files

- **Standard build**: Uses `requirements.txt` (for `docker-compose.yaml`)
- **Chainguard build**: Uses `requirements.cg.txt` (for `docker-compose-chainguard.yaml`)

The `.cg.txt` files contain Chainguard-specific package versions (e.g., `aiohttp==3.9.1+cgr.2`).

## Security Note

**Important:** The `pip.conf` file is already in `.gitignore` and should NOT be committed to version control if it contains:
- Private IP addresses
- Authentication credentials
- Internal network details

Keep `pip.example` as a template for other developers.
