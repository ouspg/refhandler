# Refhandler backend

## How to use backend API

### Authentication

1. Create login JSON payload `{"username": user_email,"password": user_password}`. Note the login credentials are `email:password`, but FastAPI security library uses Oauth2 password flow, which is why the payload key is `username` instead of `email`.
2. POST the login payload to `/api/login/access-token`
3. If login credentials are valid, the API generates and sends back a JWT token as a string
4. Add the JWT token to API requests as a header: `Authorization: Bearer <token>`

### /api/users

- `GET /api/users/me` Get user information for the **currently authenticated user**
- `GET /api/users/user_id` Get the user information for **user with UUID matching `user_id`**
- `POST /api/users/signup` **Register a new user account** by sending a POST request with a JSON payload matching the pydantic model `UserCreate` (see `/backend/app/models.py` for details)

### /api/pdfs

- `POST /api/pdfs/` Accepts POST requests with a **PDF file in the `multipart/form-data` format**. If the file passes malware scanning, it is stored on disk and the API responds with pydantic model `Pdf` of the file (see `/backend/app/models.py` for details).
- `GET /api/pdfs/file_id`: Get the **PDF file matching the UUID `file_id`** from disk.
- `DELETE /api/pdfs/file_id`: Delete the **PDF file matching the UUID `file_id`** from disk.

### Swagger UI

In development mode, in-depth API documentation available in the auto-generated Swagger UI at `/api/docs`.

## Running unit tests

**TODO:** find easier way to run tests without manually installing python 3.12 and py

Tests work for at least python versions 3.12 and 3.14

### Linux

```bash
# Activate Python virtual environment
python -m venv venv
source venv/bin/activate

# Install required python packages into the virtual environment
pip install -r backend/requirements-dev.txt

# Run unit tests
pytest /backend/tests/
```

### Windows

```ps1
# Activate Python virtual environment
python -m venv venv
./venv/Scripts/activate.ps1

# Install required python packages into the virtual environment
pip install -r backend/requirements-dev.txt

# Run unit tests
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

## Components

1. Alembic: makes sure that when pdf returns additional parameters that isn't in pdf_model, it doesn't run in error
2. Pdfs: configurations for taking pdf in
3. Dependencies: a
4. Scanners: run pdf through clamav and (virustotal -> if api key not provided)
5. Models: database table models
6. Tests: test pdf, scanner with mockup setup in conftest
    test_pdfs: test for uploading pdf successfully, test post with missing data and test infected mockup pdf
    test_scanners: test clamav scan and (virustotal -> if api key not provided)