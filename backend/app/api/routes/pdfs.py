from fastapi import File, UploadFile, APIRouter, HTTPException
import os, uuid
from app.api.deps import SessionDep
from app.models.models import Pdf, PdfCreate, PdfPublic

UPLOAD_DIR = os.environ.get("UPLOAD_DIR", 'NO UPLOAD_DIR IN ENVIRONMENT')
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

@router.post("/")
async def upload_pdf(session: SessionDep, files: list[UploadFile]):
    return_files = []

    for file in files:
        if file.content_type != "application/pdf" or file.filename == None:
            raise HTTPException(status_code=422, detail="Invalid PDF file")
        
        new_filename = uuid.uuid4()
        file_location = os.path.join(UPLOAD_DIR, str(new_filename) + ".pdf")
        with open(file_location, "wb") as f:
            f.write(file.file.read())
        
        db_pdf = Pdf(id = new_filename, original_filename=file.filename)
        session.add(db_pdf)
        session.commit()
        session.refresh(db_pdf)
        return_files.append(db_pdf.model_copy(deep=True))

    return return_files