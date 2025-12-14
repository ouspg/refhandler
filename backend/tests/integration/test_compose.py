"""
Integration tests for the Refhandler compose stack

docker_services in function argument means pytest-docker is used to run a docker compose stack
before running tests. (see /backend/tests/integration/conftest.py for details)
"""
# pylint: disable=missing-function-docstring, unused-argument, unused-import, fixme, unused-variable
import pytest
import requests


def test_frontend_reachable(docker_services, frontend_url):
    response = requests.get(frontend_url, timeout=20)
    assert response.status_code == 200


def test_adminer_reachable(docker_services, adminer_url):
    response = requests.get(adminer_url, timeout=20)
    assert response.status_code == 200


def test_backend_hidden_from_localhost(docker_services, backend_url):
    response = requests.get(backend_url, timeout=20)
    assert response.status_code == 404


@pytest.mark.skip(reason="Test isn't meaningful, /api endpoint doesn't respond anyway")
def test_api_hidden_from_localhost(docker_services, api_url):
    response = requests.get(api_url, timeout=20)
    assert response.status_code == 404


@pytest.mark.skip(reason="Test isn't meaningful, can't send raw requests to postgres")
def test_postgres_hidden_from_localhost(docker_services, postgres_url):
    with pytest.raises(requests.exceptions.ConnectionError):
        response = requests.get(postgres_url, timeout=20)


@pytest.mark.skip(reason="Clamav reachable, needs fixing") #TODO
def test_clamav_hidden_from_localhost(docker_services, clamav_url):
    response = requests.get(clamav_url, timeout=20)
    assert response.status_code == 404

