"""
Unit tests for backend.app.api.scanners
"""
# pylint: disable=missing-function-docstring
import json
import pytest
from httpx import Response
from fastapi import UploadFile
from backend.app.api.scanners import Scanners, get_sha256_hash

scanners = Scanners()

@pytest.mark.asyncio
async def test_clamav_scan_mockup(mocker):
    with open("backend/tests/api/test.pdf", "rb") as pdf_file:

        # Mock ClamAV scan result with safe file
        mocker.patch("backend.app.api.scanners.requests.post", return_value=Response(200))

        response = await scanners.clamav_scan(UploadFile(pdf_file))
        assert response.status_code == 200

        # Mock ClamAV scan result with infected file
        mocker.patch("backend.app.api.scanners.requests.post", return_value=Response(406))

        response = await scanners.clamav_scan(UploadFile(pdf_file))
        assert response.status_code == 406


@pytest.mark.asyncio
async def test_virustotal_scan_without_apikey(mocker):
    mocker.patch("backend.app.api.scanners.VIRUSTOTAL_API_KEY", "")
    with open("backend/tests/api/test.pdf", "rb") as pdf_file:
        content_hash = await get_sha256_hash(UploadFile(pdf_file))

        response = await scanners.virustotal_scan(content_hash)
        # 401 if no API key provided
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_virustotal_scan_invalid_apikey(mocker):
    mocker.patch("backend.app.api.scanners.VIRUSTOTAL_API_KEY", "invalid")
    with open("backend/tests/api/test.pdf", "rb") as pdf_file:

        content_hash = await get_sha256_hash(UploadFile(pdf_file))
        response = await scanners.virustotal_scan(content_hash)
        # 500 API error
        assert response.status_code == 500


@pytest.mark.asyncio
async def test_virustotal_scan_file_scanned(mocker):
    mocker.patch("backend.app.api.scanners.VIRUSTOTAL_API_KEY", "invalid_but_exists")
    with open("backend/tests/api_utils/safe_virustotal_response.json", "rb") as file:
        response_json = json.load(file)
        mocker.patch("backend.app.api.scanners.requests.get",
                     return_value=Response(200, json=response_json))

        response = await scanners.virustotal_scan("doesnt_matter_response_mocked")
        assert response.status_code == 200
        data = response.json()
        assert data["results"]["malicious"] == 0
        assert data["results"]["suspicious"] == 0
