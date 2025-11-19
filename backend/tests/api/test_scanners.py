import pytest
from fastapi import Response, UploadFile
from app.api.scanners import Scanners

@pytest.mark.asyncio
async def test_clamav_scan_mockup(mocker):
    scanners = Scanners()
    with open("backend/tests/api/test.pdf", "rb") as pdf_file:
        
        # Mock ClamAV scan result with safe file
        mocker.patch("app.api.scanners.requests.post", return_value=Response("",200))
        
        response = await scanners.scan(UploadFile(pdf_file))
        assert response.status_code == 200
        
        # Mock ClamAV scan result with infected file
        mocker.patch("app.api.scanners.requests.post", return_value=Response("",406))
        
        response = await scanners.scan(UploadFile(pdf_file))
        assert response.status_code == 406