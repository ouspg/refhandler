from fastapi import UploadFile, Response
import requests
import os

CLAMAV_PORT = os.environ.get("CLAMAV_PORT", 'NO CLAMAV_PORT IN ENVIRONMENT')
CLAMAV_SCAN_URL = f"http://clamav-rest:{CLAMAV_PORT}/v2/scan"

# TODO: Add virustotal API. Skip if VIRUSTOTAL_API_KEY == ""

# Class for calling file scanner APIs
# If file is safe: return HTTP 200
# else return HTTP 406
class Scanners:
    
    # Scan files using locally hosted ClamAV-rest container
    # https://github.com/ajilach/clamav-rest?tab=readme-ov-file#quick-start
    async def clamav_scan(self, file: UploadFile):
        files = {
            'files': (file.filename, await file.read(), file.content_type)
        }
        
        response = requests.post(CLAMAV_SCAN_URL, files=files)
        return response
    
    # Run all scanners
    async def scan(self, file: UploadFile):
        responses = []
        
        # Run all scanners and store response in a list
        responses.append(await self.clamav_scan(file))
        
        # Iterate over list and return HTTP 406 if any scanners flagged the file
        for response in responses:
            if response.status_code == 406:
                return response
            
        # No scanners flagged the file, return HTTP 200
        return Response()
