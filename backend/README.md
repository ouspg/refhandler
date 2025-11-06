# Refhandler backend

## Running unit tests

### Linux

```bash
# Activate Python virtual environment and install requirements
py -3.12 -m venv venv
source venv/bin/activate
pip install -r backend/requirements-dev.txt

# Run unit tests
pytest /backend/tests/
```

### Windows

```ps1
# Activate Python virtual environment and install requirements
py -3.12 -m venv venv
./venv/Scripts/activate.ps1
pip install -r backend/requirements-dev.txt

# Run unit tests.
pytest ./backend/tests/
```
