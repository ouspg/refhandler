"""
Database and filesystem operations for (CRUD) creating, reading, updating and deleting PDFs

Based on: 
https://github.com/fastapi/full-stack-fastapi-template/blob/e4022a9502a6b61c857e3cbdaddc69e7219c9d53/backend/app/crud.py
"""
# pylint: disable=missing-function-docstring, line-too-long, fixme

import uuid
import os
import json
from sqlmodel import Session, select
from fastapi import UploadFile
from backend.app.models import Pdf, PdfCreate, VirusScanResult

UPLOAD_DIR = os.environ.get("UPLOAD_DIR", 'NO UPLOAD_DIR IN ENVIRONMENT')
os.makedirs(UPLOAD_DIR, exist_ok=True)


def create_pdf(session: Session, pdf_create: PdfCreate) -> Pdf:
    db_pdf = Pdf.model_validate(pdf_create)
    session.add(db_pdf)
    session.commit()
    session.refresh(db_pdf)
    return db_pdf


def update_pdf(session: Session, target_pdf: Pdf) -> Pdf:
    new_data = target_pdf.model_dump(exclude_unset=True)

    target_pdf.sqlmodel_update(new_data)
    session.add(target_pdf)
    session.commit()
    session.refresh(target_pdf)
    return target_pdf


def delete_pdf(session: Session,  target_pdf: Pdf):
    session.delete(target_pdf)
    session.commit()


def get_pdf_by_id(session: Session, pdf_id_in: str):
    try:
        pdf_id = uuid.UUID(pdf_id_in)
    except ValueError:
        return None

    db_pdf = session.get(Pdf, pdf_id)
    return db_pdf


def get_pdf_by_sha256_hash(session: Session, content_hash: str) -> Pdf | None:
    pdf_with_hash = select(Pdf).where(Pdf.content_hash == content_hash)
    db_pdf = session.exec(pdf_with_hash).first()
    return db_pdf


def save_to_disk(pdf: Pdf, pdf_file: UploadFile):
    filename = str(pdf.id)
    file_location = os.path.join(UPLOAD_DIR, f"{filename}.pdf")
    with open(file_location, "wb") as f:
        pdf_file.file.seek(0)
        f.write(pdf_file.file.read())
        

def get_file_path(file_id: str) -> str | None:
    file = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
    if os.path.isfile(file):
        return file
    else:
        return None


def create_virus_scan_result(session: Session, scan_results: dict) -> VirusScanResult:
    scan_results_string = json.dumps(scan_results)
    db_scan_result = VirusScanResult(scan_results=scan_results_string)
    session.add(db_scan_result)
    session.commit()
    session.refresh(db_scan_result)
    return db_scan_result
