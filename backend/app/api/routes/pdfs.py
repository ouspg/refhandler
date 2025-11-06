from fastapi import File, UploadFile, APIRouter, HTTPException
import os, uuid
from app.api.deps import SessionDep
from app.models.models import Pdf, PdfCreate, PdfPublic

UPLOAD_DIR = os.environ.get("UPLOAD_DIR", 'NO UPLOAD_DIR IN ENVIRONMENT')
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/pdfs")

@router.post("/", response_model=PdfPublic)
async def upload_pdf(session: SessionDep, pdf_file: UploadFile = File()):
    if pdf_file.content_type != "application/pdf" or pdf_file.filename == None:
        raise HTTPException(status_code=422, detail="Invalid PDF file")
    
    new_filename = uuid.uuid4()
    file_location = os.path.join(UPLOAD_DIR, str(new_filename) + ".pdf")
    with open(file_location, "wb") as f:
        f.write(pdf_file.file.read())
    
    db_pdf = Pdf(id = new_filename, original_filename=pdf_file.filename)
    session.add(db_pdf)
    session.commit()
    session.refresh(db_pdf)
    return db_pdf