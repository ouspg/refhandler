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
