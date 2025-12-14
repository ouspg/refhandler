# pylint: disable=missing-function-docstring, missing-module-docstring
import os
import pytest
from backend.app.db import POSTGRES_URL

BACKEND_PORT = int(os.environ.get("BACKEND_PORT", 'NO BACKEND_PORT IN ENVIRONMENT'))
FRONTEND_PORT = int(os.environ.get("FRONTEND_PORT", 'NO BACKEND_PORT IN ENVIRONMENT'))
POSTGRES_PORT = int(os.environ.get("POSTGRES_PORT", 'NO BACKEND_PORT IN ENVIRONMENT'))
ADMINER_PORT = int(os.environ.get("ADMINER_PORT", 'NO ADMINER_PORT IN ENVIRONMENT'))
CLAMAV_PORT = int(os.environ.get("CLAMAV_PORT", 'NO CLAMAV_PORT IN ENVIRONMENT'))


# Override docker compose file used by docker_services fixture (default: /tests/docker-compose.yml)
@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join(str(pytestconfig.rootdir), "compose.yaml")

# Change project name to seperate it's networks and volumes from the real deployment.
# Important because we delete docker volumes after running tests
@pytest.fixture(scope="session")
def docker_compose_project_name() -> str:
    return "refhandler-integration-test"

# Stop the stack and delete volumes before starting a new one
@pytest.fixture(scope="session")
def docker_setup():
    return ["down -v", "up --build --wait"]


@pytest.fixture(scope="session")
def frontend_url(docker_ip):
    return f"http://{docker_ip}:{FRONTEND_PORT}"

@pytest.fixture(scope="session")
def api_url(docker_ip):
    return f"http://{docker_ip}:{FRONTEND_PORT}/api"

@pytest.fixture(scope="session")
def backend_url(docker_ip):
    return f"http://{docker_ip}:{BACKEND_PORT}"

@pytest.fixture(scope="session")
def postgres_url():
    return "http://" + POSTGRES_URL

@pytest.fixture(scope="session")
def adminer_url(docker_ip):
    return f"http://{docker_ip}:{ADMINER_PORT}"

@pytest.fixture(scope="session")
def clamav_url(docker_ip):
    return f"http://{docker_ip}:{CLAMAV_PORT}"
