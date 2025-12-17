# pylint: disable=missing-function-docstring, pointless-string-statement, missing-module-docstring, missing-class-docstring, unused-variable, fixme
import os
import hashlib
import requests
from requests.exceptions import Timeout
from httpx import Response
from fastapi import UploadFile, HTTPException


CLAMAV_PORT = os.environ["CLAMAV_PORT"]
CLAMAV_SCAN_URL = f"http://clamav-rest:{CLAMAV_PORT}/v2/scan"

VIRUSTOTAL_MALICIOUS_CUTOFF = int(os.environ["VIRUSTOTAL_MALICIOUS_CUTOFF"])
VIRUSTOTAL_API_KEY = os.environ["VIRUSTOTAL_API_KEY"]
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
    async def virustotal_scan(self, pdf_content_hash: str) -> Response:
        # Skip scanning if no API key is provided
        if VIRUSTOTAL_API_KEY == "":
            return Response(401, text="Missing VIRUSTOTAL_API_KEY")

        try:
            # Call Virustotal file API and parse response
            headers = {
            "accept": "application/json",
            "x-apikey": VIRUSTOTAL_API_KEY
            }
            response = requests.get(VIRUSTOTAL_URL + pdf_content_hash,
                                    headers=headers, timeout=20)
        except Timeout as e:
            return Response(408, text="Virustotal API call timed out")
        
        # Check if Virustotal responded with an error
        if "error" in response.json():
            code, message = response.json()["error"].values()
            return Response(500, text=f"Virustotal returned {code}: {message}")
        
        # Determine if file is malicious based on scan results
        results = parse_virustotal_json(response.json())
        malicious, suspicious = results["malicious"], results["suspicious"]
        if malicious > VIRUSTOTAL_MALICIOUS_CUTOFF:
            return Response(406, json={"results": results})
        else:
            return Response(200, json={"results": results})

    # Run all scanners
    async def scan(self, file: UploadFile, pdf_content_hash: str = "") -> dict[str, Response]:
        if pdf_content_hash == "":
            pdf_content_hash = await get_sha256_hash(file)

        # Run all scanners and return results
        scan_results = {}
        scan_results["clamav"] = await self.clamav_scan(file)
        scan_results["virustotal"] = await self.virustotal_scan(pdf_content_hash)

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

def parse_virustotal_json(response_json: dict) -> dict[str, int]:
    return response_json["data"]["attributes"]["last_analysis_stats"]
