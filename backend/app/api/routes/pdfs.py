# pylint: disable=missing-function-docstring, missing-module-docstring, missing-class-docstring, unused-variable, fixme, unused-argument
import os
from fastapi import UploadFile, APIRouter, HTTPException
from fastapi.responses import FileResponse, Response

from backend.app.api import pdf_crud
from backend.app.api.depdendancies import SessionDep, ScannersDep, CurrentUser
from backend.app.api.scanners import get_sha256_hash
from backend.app.models import PdfCreate, PdfPublic, UserRole


router = APIRouter()


@router.get("/{file_id}")
async def get_pdf_file(session: SessionDep, current_user: CurrentUser, file_id: str):
    # If file_id doesn't end in .pdf, get the pdf entry from database
    if file_id[-4:] != ".pdf":
        db_pdf = pdf_crud.get_pdf_by_id(session, file_id)
        if db_pdf is None:
            raise HTTPException(404, "Pdf file not found in database")
        return db_pdf

    # file_id ended in .pdf, get the pdf file from disk
    file_id = file_id[:-4]
    file_path = pdf_crud.get_file_path(file_id)
    db_pdf = pdf_crud.get_pdf_by_id(session, file_id)
    if file_path is None or db_pdf is None:
        raise HTTPException(404, "Pdf file not found on disk")

    header = {"Content-Type": "application/pdf"}
    return FileResponse(file_path, filename=db_pdf.original_filename, headers=header)

@router.post("/", response_model=PdfPublic)
async def upload_pdf(session: SessionDep, scanners: ScannersDep,
                    current_user: CurrentUser, pdf_file: UploadFile,
                    response: Response):
    # Reject files with wrong content type or no filename
    # TODO: More checking. Check magic bytes?
    if pdf_file.content_type != "application/pdf" or pdf_file.filename is None:
        raise HTTPException(422, "Invalid PDF file")

    pdf_content_hash = await get_sha256_hash(pdf_file)
    existing_pdf = pdf_crud.get_pdf_by_sha256_hash(session, pdf_content_hash)

    if existing_pdf:
        response.status_code = 409
        return existing_pdf

    # Scan file for viruses
    scan_results = await scanners.scan(pdf_file, pdf_content_hash)
    scan_results_db = pdf_crud.create_virus_scan_result(session, scan_results)

    # Abort if any scanner found the file dangerous
    for scanner, result in scan_results.items():
        if result["status_code"] == 406:
            raise HTTPException(406, {"details": f"{pdf_file.filename} is not safe",
                                      "pdf": "",
                                      "scan_result": result
                                      })

    # File was safe, safe it to db and disk
    pdf_create = PdfCreate(original_filename=pdf_file.filename,
                           uploaded_by=current_user.id,
                           scan_result_id=scan_results_db.id,
                           content_hash=pdf_content_hash)
    db_pdf = pdf_crud.create_pdf(session, pdf_create)
    pdf_crud.save_to_disk(db_pdf, pdf_file)

    return db_pdf


@router.delete("/{file_id}")
async def get_file(session: SessionDep, current_user: CurrentUser, file_id: str):
    db_pdf = pdf_crud.get_pdf_by_id(session, file_id)
    file_path = pdf_crud.get_file_path(file_id)

    if not db_pdf or not file_path:
        raise HTTPException(404, "File not found")
    if db_pdf.uploaded_by != current_user.id:
        if current_user.role != UserRole.admin:
            raise HTTPException(403, "Only admins can delete other user's files")
    
    # File was found and belongs to current_user, deleting it from db and disk
    pdf_crud.delete_pdf(session, db_pdf)
    os.remove(file_path)