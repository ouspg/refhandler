# pylint: disable=missing-function-docstring, pointless-string-statement, missing-module-docstring, missing-class-docstring, unused-variable, fixme
import os
import hashlib
import requests
from requests.exceptions import Timeout
from fastapi import UploadFile, HTTPException


CLAMAV_PORT = os.environ.get("CLAMAV_PORT", 'NO CLAMAV_PORT IN ENVIRONMENT')
CLAMAV_SCAN_URL = f"http://clamav-rest:{CLAMAV_PORT}/v2/scan"

VIRUSTOTAL_MALICIOUS_CUTOFF = int(os.environ.get(
    "VIRUSTOTAL_MALICIOUS_CUTOFF", 'NO VIRUSTOTAL_MALICIOUS_CUTOFF IN ENVIRONMENT'))
VIRUSTOTAL_API_KEY = os.environ.get(
    "VIRUSTOTAL_API_KEY", 'NO VIRUSTOTAL_API_KEY IN ENVIRONMENT')
VIRUSTOTAL_URL = "https://www.virustotal.com/api/v3/files/"

# Class for calling file scanner APIs


class Scanners:
    # Scan files using locally hosted ClamAV-rest container
    # https://github.com/ajilach/clamav-rest?tab=readme-ov-file#quick-start
    async def clamav_scan(self, file: UploadFile):
        files = {
            'files': file.file
        }

        try:
            response = requests.post(CLAMAV_SCAN_URL, files=files, timeout=20)
        except Timeout as e:
            raise HTTPException(408, "ClamAV API call timed out") from e
        return response

        # TODO: add print for results to show in terminal

    # Scan files using VirusTotal API
    async def virustotal_scan(self, pdf_content_hash: str):
        # Skip scanning if no API key is provided
        if VIRUSTOTAL_API_KEY == 'NO VIRUSTOTAL_API_KEY IN ENVIRONMENT' or VIRUSTOTAL_API_KEY == "":
            return {
                "status_code": 401,
                "results": "No API key provided"
            }

        headers = {
            "accept": "application/json",
            "x-apikey": VIRUSTOTAL_API_KEY
        }

        try:
            # Call Virustotal file API and parse response
            response = requests.get(
                VIRUSTOTAL_URL + pdf_content_hash, headers=headers, timeout=20)
        except Timeout as e:
            raise HTTPException(408, "Virustotal API call timed out") from e
        
        # Check if Virustotal responded with an error
        if "error" in response.json():
            code, message = response.json()["error"].values()
            return {"status_code": 401,
                "results": f"Virustotal API error: {code}:{message}"
                }
        
        # Determine if file is malicious based on scan results
        results = parse_virustotal_json(response.json())
        malicious, suspicious = results["malicious"], results["suspicious"]
        if malicious > VIRUSTOTAL_MALICIOUS_CUTOFF:
            return {
                "status_code": 406,
                "results": results
            }
        else:
            return {
                "status_code": 200,
                "results": results
            }

    # Run all scanners
    async def scan(self, file: UploadFile, pdf_content_hash: str = "") -> dict[str, dict]:
        if pdf_content_hash == "":
            pdf_content_hash = await get_sha256_hash(file)

        # Run all scanners and return responses
        clamav_response = await self.clamav_scan(file)
        virustotal_response = await self.virustotal_scan(pdf_content_hash)

        scan_results = {}
        scan_results["clamav"] = {"status_code": clamav_response.status_code,
                                  "results": clamav_response.text}
        scan_results["virustotal"] = {"status_code": virustotal_response["status_code"],
                                      "results": virustotal_response["results"]}

        return scan_results


async def get_sha256_hash(file: UploadFile):
    file_bytes = await file.read()
    await file.seek(0)
    return hashlib.sha256(file_bytes).hexdigest()

"""
Example Virustotal API response

{
  "malicious": 1,
  "suspicious": 0,
  "undetected": 70,
  "harmless": 0,
  "timeout": 1,
  "confirmed-timeout": 0,
  "failure": 0,
  "type-unsupported": 4
}
"""

def parse_virustotal_json(response_json: dict):
    return response_json["data"]["attributes"]["last_analysis_stats"]
