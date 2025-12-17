"""
API definitions for /api/pdfs

If the API function has types CurrentUser or CurrentAdmin as an argument,
using the API endpoint requires a valid access token header.
CurrentAdmin additionally requires the user to have the role UserRole.admin.

(see API documentation in /backend/README.md for details)
"""
# pylint: disable=missing-function-docstring, missing-module-docstring, missing-class-docstring, unused-variable, fixme, unused-argument
import os
from fastapi import UploadFile, APIRouter, HTTPException
from fastapi.responses import FileResponse
from httpx import Response

from backend.app.api import pdf_crud
from backend.app.api.pdf_crud import ends_in_dot_pdf, strip_dot_pdf
from backend.app.api.depdendancies import SessionDep, ScannersDep, CurrentUser
from backend.app.api.scanners import get_sha256_hash
from backend.app.models import PdfCreate, PdfPublic, PdfUpdate, UserRole


router = APIRouter()

# Get pdf database object (file_id) or pdf file on disk (file_id.pdf)
@router.get("/{file_id}", response_model=PdfPublic)
async def get_pdf_file(session: SessionDep, current_user: CurrentUser, file_id: str):
    db_pdf = pdf_crud.get_pdf_by_id(session, strip_dot_pdf(file_id))
    if not db_pdf:
        raise HTTPException(404, "Pdf not found in database")
    
    if ends_in_dot_pdf(file_id):
        file_path = pdf_crud.get_file_path(strip_dot_pdf(file_id))
        if file_path is None:
            raise HTTPException(404, "Pdf file not found on disk")
        header = {"Content-Type": "application/pdf"}
        return FileResponse(file_path, filename=db_pdf.original_filename, headers=header)
    else:
        return db_pdf


@router.post("/", response_model=PdfPublic)
async def upload_pdf(session: SessionDep, scanners: ScannersDep,
                    current_user: CurrentUser, pdf_file: UploadFile):
    # Reject invalid PDF files
    if pdf_file.filename is None:
        raise HTTPException(400, "PDF file must have a name")
    
    # Checks if file matching content hash exists, return it from db if it does
    pdf_content_hash = await get_sha256_hash(pdf_file)
    existing_pdf = pdf_crud.get_pdf_by_sha256_hash(session, pdf_content_hash)
    if existing_pdf:
        return existing_pdf

    if not pdf_crud.is_valid_pdf(pdf_file):
        raise HTTPException(422, "Invalid PDF file")


    # Scan file for viruses
    scan_results = await scanners.scan(pdf_file, pdf_content_hash)
    scan_results_db = pdf_crud.create_virus_scan_result(session, scan_results)

    # Abort if any scanner found the file dangerous
    for scanner, scanner_response in scan_results.items():
        if scanner_response.status_code == 406:
            raise HTTPException(406, {"detail": f"{pdf_file.filename} is not safe. ",
                                    scanner: scanner_response.text}
            )

    # File was safe, safe it to db and disk
    pdf_create = PdfCreate(original_filename=pdf_file.filename,
                           uploaded_by=current_user.id,
                           scan_result_id=scan_results_db.id,
                           content_hash=pdf_content_hash)
    db_pdf = pdf_crud.create_pdf(session, pdf_create)
    pdf_crud.save_to_disk(db_pdf.id, pdf_file)

    return db_pdf

# Patch pdf db objects
@router.patch("/{file_id}", response_model=PdfPublic)
async def patch_pdf(session: SessionDep, current_user: CurrentUser,
                    file_id: str, pdf_update: PdfUpdate):
    db_pdf = pdf_crud.get_pdf_by_id(session, strip_dot_pdf(file_id))
    if not db_pdf:
        raise HTTPException(404, "Pdf not found in database")

    # Stop normal users from updating other user's files
    if db_pdf.uploaded_by != current_user.id:
        if current_user.role != UserRole.admin:
            raise HTTPException(403, "Only admins can patch other user's files")

    if ends_in_dot_pdf(file_id):
        raise HTTPException(51, "Patching pdf files is not implemented")
    else:
        updated_pdf = pdf_crud.update_pdf(session, db_pdf, pdf_update)
        return updated_pdf

# TODO: patch pdf files?

# Delete pdf database object (file_id) or pdf file on disk (file_id.pdf)
@router.delete("/{file_id}")
async def delete_pdf(session: SessionDep, current_user: CurrentUser, file_id: str):
    db_pdf = pdf_crud.get_pdf_by_id(session, strip_dot_pdf(file_id))
    if not db_pdf:
        raise HTTPException(404, "Pdf not found in database")
    
    # Stop normal users from deleting other user's files
    if db_pdf.uploaded_by != current_user.id:
        if current_user.role != UserRole.admin:
            raise HTTPException(403, "Only admins can delete other user's files")
    
    if ends_in_dot_pdf(file_id):
        file_path = pdf_crud.get_file_path(strip_dot_pdf(file_id))
        if file_path is None:
            raise HTTPException(404, "Pdf file not found on disk")
        # File found, deleting it from disk
        os.remove(file_path)
        return {"message": f"{db_pdf.original_filename} deleted sucessfully"}
    else:
        pdf_crud.delete_pdf(session, db_pdf)
        return {"message": f"{db_pdf.original_filename} deleted sucessfully"}
