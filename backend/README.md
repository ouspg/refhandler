# Refhandler backend

API documentation available at the `/api/docs` endpoint.

## Running unit tests

### TODO

- find easier way to run tests without manually installing python 3.12 and py

Tests work for at least python versions 3.12 and 3.14

### Linux

```bash
# Activate Python virtual environment and install requirements
python -m venv venv
source venv/bin/activate
pip install -r backend/requirements-dev.txt

# Run unit tests
pytest /backend/tests/
```

### Windows

```ps1
# Activate Python virtual environment and install requirements
python -m venv venv
./venv/Scripts/activate.ps1
pip install -r backend/requirements-dev.txt

# Run unit tests.
pytest ./backend/tests/
```

## Running database migrations with alembic

Making changes to SQLModels in `/backend/app/models.py` will lead to a conflict between new and existing database tables.

To update the existing database tables to the new models without losing data, migration scripts can be generated using alembic.

Because backend and postgres containers are running in a docker network that isn't connected to localhost, the alembic commands must be run inside the backend container.

```bash
# Start the compose file
docker compose up

# Open bash inside the backend container
docker compose exec backend bash

# Run alembic revision to autogenerate migration scripts
alembic revision --autogenerate -m "revision name here"

```
## Troubleshooting start-up errors
1. If the some of the docker containers don't build up, run "Docker-compose down" and delete "refhandler_postgres_data" in volumes

## Components
1. Alembic: makes sure that when pdf returns additional parameters that isn't in pdf_model, it doesn't run in error
2. Pdfs: configurations for taking pdf in
3. Dependencies: a
4. Scanners: run pdf through clamav and (virustotal -> if api key not provided)
5. Models: database table models
6. Tests: test pdf, scanner with mockup setup in conftest
    test_pdfs: test for uploading pdf successfully, test post with missing data and test infected mockup pdf
    test_scanners: test clamav scan and (virustotal -> if api key not provided)