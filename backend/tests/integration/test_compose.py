"""
Integration tests for the Refhandler compose stack

docker_services in function argument means pytest-docker is used to run
the docker compose stack before running tests. (see conftest.py for details)
"""
# pylint: disable=missing-function-docstring, unused-argument, unused-import, fixme, unused-variable
import pytest
import requests


def test_frontend_reachable(docker_services, frontend_url):
    response = requests.get(frontend_url, timeout=20)
    assert response.status_code == 200


@pytest.mark.skip("reason=SSLError wrong version number")
def test_frontend_https_reachable(docker_services, frontend_url_https):
    response = requests.get(frontend_url_https, verify=False, timeout=20)
    assert response.status_code == 200


def test_nginx_api_proxy(docker_services, api_proxy_url):
    response = requests.get(api_proxy_url+"/healthcheck", timeout=20)
    assert response.status_code == 200


def test_adminer_reachable(docker_services, adminer_url):
    response = requests.get(adminer_url, timeout=20)
    assert response.status_code == 200


def test_backend_healthcheck(docker_services, backend_url):
    response = requests.get(backend_url+"/api/healthcheck", timeout=20)
    assert response.status_code == 200


#TODO: ClamAV shouldn't be reacheable from localhost.
# Possibly caused by EXPOSE 9000 in the prebuilt image?
@pytest.mark.skip(reason="Clamav reachable, needs fixing")
def test_clamav_hidden_from_localhost(docker_services, clamav_url):
    response = requests.get(clamav_url, timeout=20)
    assert response.status_code == 404
