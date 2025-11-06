import uuid
from sqlmodel import Field, SQLModel

# For testing backend, not part of Refhandler
class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    db_text: str
    
class PostCreate(SQLModel):
    db_text: str

class PostPublic(SQLModel):
    id: int
    db_text: str

class Pdf(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True)
    original_filename: str
    uploaded_by: int | None = None
    parsed: bool = False
    virustotal_scan: bool | None = None
    
class PdfCreate(SQLModel):
    id: uuid.UUID
    original_filename: str
    uploaded_by: int | None
    
class PdfPublic(SQLModel):
    id: uuid.UUID
    original_filename: str
    uploaded_by: int | None