from fastapi import UploadFile
import requests
import os

CLAMAV_PORT = os.environ.get("CLAMAV_PORT", 'NO CLAMAV_PORT IN ENVIRONMENT')
CLAMAV_SCAN_URL = f"http://clamav-rest:{CLAMAV_PORT}/v2/scan"

class Scanners:

    @staticmethod
    async def clamav_scan(file: UploadFile):
        files = {
            'files': (file.filename, await file.read(), file.content_type)
        }
        
        response = requests.post(CLAMAV_SCAN_URL, files=files)
        return response