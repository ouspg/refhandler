"""
Unit tests for backend.app.crud
"""
# pylint: disable=invalid-name, missing-function-docstring
import uuid
from sqlmodel import Session
from fastapi import UploadFile
from backend.app.models import UserCreate, Pdf, PdfCreate, PdfUpdate
from backend.app.api import pdf_crud
from backend.app.api.scanners import get_sha256_hash

test_email = "foo@bar.com"
test_password = "foobarbaz"
test_user = UserCreate(email=test_email, password=test_password)

test_pdf = PdfCreate(original_filename="foo.pdf", content_hash="foohash",
                     uploaded_by=uuid.uuid4(), scan_result_id=uuid.uuid4())


def test_create_pdf(session: Session):
    db_pdf = pdf_crud.create_pdf(session, test_pdf)
    Pdf.model_validate(db_pdf)

    hash_pdf = pdf_crud.get_pdf_by_sha256_hash(session, db_pdf.content_hash)
    assert db_pdf == hash_pdf

def test_update_pdf(session: Session):
    db_pdf = pdf_crud.create_pdf(session, test_pdf)
    new_filename = "new_filename.pdf"
    new_data = PdfUpdate(original_filename=new_filename)

    updated_pdf = pdf_crud.update_pdf(session, db_pdf, new_data)
    assert updated_pdf == Pdf.model_validate(
        db_pdf, update={"original_filename": new_filename})


def test_delete_pdf(session: Session):
    db_pdf = pdf_crud.create_pdf(session, test_pdf)
    pdf_crud.delete_pdf(session, db_pdf)
    assert pdf_crud.get_pdf_by_id(session, db_pdf.id) is None


def test_get_pdf_by_id(session: Session):
    db_pdf = pdf_crud.create_pdf(session, test_pdf)
    pdf_by_id = pdf_crud.get_pdf_by_id(session, db_pdf.id)
    assert db_pdf == pdf_by_id

    # Try to get invalid pdf_id
    invalid_pdf_by_id = pdf_crud.get_pdf_by_id(session, "foobar")
    assert invalid_pdf_by_id is None

def test_save_to_disk():
    with open("backend/tests/api/test.pdf", "rb") as pdf_file:
        upload_file = UploadFile(pdf_file)
        assert pdf_crud.is_valid_pdf(upload_file)

        pdf_id = uuid.uuid4()
        pdf_crud.save_to_disk(pdf_id, upload_file)
        assert pdf_crud.get_file_path(pdf_id) is not None
