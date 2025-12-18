"""
Database and filesystem operations for creating, reading, updating and deleting PDFs

Based on: 
https://github.com/fastapi/full-stack-fastapi-template/blob/e4022a9502a6b61c857e3cbdaddc69e7219c9d53/backend/app/crud.py
"""
# pylint: disable=missing-function-docstring, line-too-long, fixme

import uuid
import os
import json
from sqlmodel import Session, select
from fastapi import UploadFile
from httpx import Response
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from backend.app.models import Pdf, PdfCreate, PdfUpdate, VirusScanResult

UPLOAD_DIR = os.environ["UPLOAD_DIR"]
os.makedirs(UPLOAD_DIR, exist_ok=True)


def create_pdf(session: Session, pdf_create: PdfCreate) -> Pdf:
    """Inserts db_pdf into database with values from pdf_create"""
    db_pdf = Pdf.model_validate(pdf_create)
    session.add(db_pdf)
    session.commit()
    session.refresh(db_pdf)
    return db_pdf


def update_pdf(session: Session, target_pdf: Pdf, pdf_update: PdfUpdate) -> Pdf:
    """Updates target_pdf database entry with new values from pdf_update"""
    new_data = pdf_update.model_dump(exclude_unset=True)

    target_pdf.sqlmodel_update(new_data)
    session.add(target_pdf)
    session.commit()
    session.refresh(target_pdf)
    return target_pdf

def delete_pdf(session: Session,  target_pdf: Pdf):
    session.delete(target_pdf)
    session.commit()


def get_pdf_by_id(session: Session, pdf_id: uuid.UUID | str):
    """Retrieves Pdf database entry matching pdf_id, None if it wasn't found"""
    try:
        if isinstance(pdf_id, str):
            pdf_id = uuid.UUID(pdf_id)
    except ValueError:
        return None

    db_pdf = session.get(Pdf, pdf_id)
    return db_pdf


def get_pdf_by_sha256_hash(session: Session, content_hash: str) -> Pdf | None:
    """Retrieves Pdf database entry using sha256 hash of the file's content"""
    pdf_with_hash = select(Pdf).where(Pdf.content_hash == content_hash)
    db_pdf = session.exec(pdf_with_hash).first()
    return db_pdf


def save_to_disk(pdf_id: uuid.UUID | str, pdf_file: UploadFile):
    """Saves pdf_file to disk with filename pdf_id.pdf"""
    file_location = os.path.join(UPLOAD_DIR, f"{str(pdf_id)}.pdf")
    with open(file_location, "wb") as f:
        pdf_file.file.seek(0)
        f.write(pdf_file.file.read())



def is_valid_pdf(pdf_file: UploadFile) -> bool:
    """Validates pdf_file using PDFParser"""
    try:
        document = PDFDocument(PDFParser(pdf_file.file))
        return True
    except:
        return False


def ends_in_dot_pdf(string: str) -> bool:
    """Returns True if the string ends in .pdf"""
    return string[-4:] == ".pdf"

def strip_dot_pdf(string: str):
    """Strips .pdf from the end of string, if it exists"""
    if ends_in_dot_pdf(string):
        return string[:-4]
    else:
        return string


def get_file_path(pdf_id: uuid.UUID | str) -> str | None:
    """Returns the full file path of Pdf file matching pdf_id"""
    file = os.path.join(UPLOAD_DIR, f"{str(pdf_id)}.pdf")
    if os.path.isfile(file):
        return file
    else:
        return None


def create_virus_scan_result(session: Session, scan_results: dict[str, Response]) -> VirusScanResult:
    """Converts the results of scanners.scan() into VirusScanResult and inserts it into the database"""
    scan_results_json = {}
    for scanner, response in scan_results.items():
        scan_results_json[scanner] = response.text
    db_scan_result = VirusScanResult(scan_results=json.dumps(scan_results_json))
    session.add(db_scan_result)
    session.commit()
    session.refresh(db_scan_result)
    return db_scan_result
