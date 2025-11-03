from fastapi import File, UploadFile, APIRouter
import os, uuid
from app.api.deps import SessionDep
from app.models.models import PDF

UPLOAD_DIR = os.environ.get("UPLOAD_DIR", 'NO UPLOAD_DIR IN ENVIRONMENT')
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/pdfs")

@router.post("/", response_model=PDF)
async def upload_pdf(session: SessionDep, pdf_file: UploadFile = File()):
    if pdf_file.content_type != "application/pdf":
        return {"error": "Only PDF files are allowed."}
    
    new_filename = uuid.uuid4()
    file_location = os.path.join(UPLOAD_DIR, str(new_filename) + ".pdf")
    print(file_location)
    with open(file_location, "wb") as f:
        f.write(pdf_file.file.read())
    
    pdf = PDF(id = new_filename, original_filename=pdf_file.filename)
    session.add(pdf)
    session.commit()
    session.refresh(pdf)
    return pdf