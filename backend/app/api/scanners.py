from fastapi import UploadFile, Response
import requests
import os, hashlib

CLAMAV_PORT = os.environ.get("CLAMAV_PORT", 'NO CLAMAV_PORT IN ENVIRONMENT')
CLAMAV_SCAN_URL = f"http://clamav-rest:{CLAMAV_PORT}/v2/scan"

# TODO: Add virustotal API. Skip if VIRUSTOTAL_API_KEY == ""

VIRUSTOTAL_API_KEY = ""
url = "https://www.virustotal.com/api/v3/files/"  


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
    

    # Scan files using VirusTotal API
    async def virustotal_scan(self, file: UploadFile):
        headers = {
            "accept": "application/json",
            "x-apikey": VIRUSTOTAL_API_KEY
        }
        
        bytes = await file.read()
        readable_hash = hashlib.sha256(bytes).hexdigest()

        response = requests.get(url + readable_hash, headers=headers)
        return response
    

 # Run all scanners
    async def scan(self, file: UploadFile):
        responses = []
    
        # Run all scanners and store response in a list
        responses.append(await self.clamav_scan(file))
        responses.append(await self.virustotal_scan(file))
    
        # Iterate over list and return HTTP 406 if any scanners flagged the file
        for response in responses:
            if response.status_code == 406:
                return response
        
        # No scanners flagged the file, return HTTP 200
        return Response()