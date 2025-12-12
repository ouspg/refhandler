# pylint: disable=import-error, missing-function-docstring, missing-module-docstring, missing-class-docstring, unused-variable, fixme
import os
import uuid
import json
from fastapi import UploadFile, APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.api.depdendancies import SessionDep, ScannersDep
from app.api.scanners import get_sha256_hash
from app.models import Pdf, PdfPublic, VirusScanResult

UPLOAD_DIR = os.environ.get("UPLOAD_DIR", 'NO UPLOAD_DIR IN ENVIRONMENT')
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()


@router.get("/{file_id}")
async def get_pdf(file_id: str):
    file = f"{UPLOAD_DIR}/{file_id}.pdf"

    # Return {file_id}.pdf, if it exists on disk
    if os.path.isfile(file):
        return FileResponse(file, headers={"Content-Type": "application/pdf"})
    else:
        raise HTTPException(404, "File not found")


@router.post("/", response_model=PdfPublic)
async def upload_pdf(session: SessionDep, scanners: ScannersDep, pdf_file: UploadFile):
    # Reject files with wrong content type or no filename
    # TODO: More checking. Check magic bytes?
    if pdf_file.content_type != "application/pdf" or pdf_file.filename == None:
        raise HTTPException(422, "Invalid PDF file")

    # Scan file for viruses
    pdf_content_hash = await get_sha256_hash(pdf_file)
    scan_results = await scanners.scan(pdf_file, pdf_content_hash)
    scan_results_db = await ScannerUtils.add_to_db(session, scan_results)

    for scanner, result in scan_results.items():
        if result["status_code"] == 406:
            raise HTTPException(406, {"details": f"{pdf_file.filename} is not safe",
                                      "pdf": "",
                                      "scan_result": result
                                      })

    # File was found safe, save it to disk
    new_filename = await PdfUtils.add_to_disk(pdf_file)

    # Add file metadata to database
    return await PdfUtils.add_to_db(session, new_filename, pdf_file.filename, scan_results_db.id)


@router.delete("/{file_id}")
async def get_file(file_id: str):
    file = f"{UPLOAD_DIR}/{file_id}.pdf"

    # If {file_id}.pdf exists, delete it from disk
    if os.path.isfile(file):
        return os.remove(file)
    else:
        raise HTTPException(404, "File not found")


class PdfUtils:
    @staticmethod
    async def add_to_db(session: SessionDep, new_filename: uuid.UUID,
                        original_filename: str, scan_results_id: uuid.UUID):
        db_pdf = Pdf(id=new_filename, original_filename=original_filename,
                     scan_results_id=scan_results_id)
        session.add(db_pdf)
        session.commit()
        session.refresh(db_pdf)
        return db_pdf

    @staticmethod
    async def add_to_disk(pdf_file: UploadFile):
        new_filename = uuid.uuid4()
        file_location = os.path.join(UPLOAD_DIR, str(new_filename) + ".pdf")
        with open(file_location, "wb") as f:
            pdf_file.file.seek(0)
            f.write(pdf_file.file.read())
        return new_filename


class ScannerUtils:
    @staticmethod
    async def add_to_db(session: SessionDep, scan_results):
        scan_results_string = json.dumps(scan_results)
        db_scan_result = VirusScanResult(scan_results=scan_results_string)
        session.add(db_scan_result)
        session.commit()
        session.refresh(db_scan_result)
        return db_scan_result
