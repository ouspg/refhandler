"""
Contains pytest fixtures that are used by integration tests.
"""
# pylint: disable=missing-function-docstring, missing-module-docstring
import os
import pytest
from backend.app.postgres_db import POSTGRES_URL

BACKEND_PORT = int(os.environ["BACKEND_PORT"])
FRONTEND_PORT = int(os.environ["FRONTEND_PORT"])
POSTGRES_PORT = int(os.environ["POSTGRES_PORT"])
ADMINER_PORT = int(os.environ["ADMINER_PORT"])
CLAMAV_PORT = int(os.environ["CLAMAV_PORT"])


# Overrides docker compose file used by docker_services fixture (default: /tests/docker-compose.yml)
@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join(str(pytestconfig.rootdir), "compose.yaml")

# Changes project name to seperate it's networks and volumes from the real deployment.
# Important because we delete the docker volumes after running tests
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
def adminer_url(docker_ip):
    return f"http://{docker_ip}:{ADMINER_PORT}"

@pytest.fixture(scope="session")
def clamav_url(docker_ip):
    return f"http://{docker_ip}:{CLAMAV_PORT}"
