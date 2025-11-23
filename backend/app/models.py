import uuid
from sqlmodel import Field, SQLModel

##############################################
# WARNING
# If you make change to SQLModels with table=True,
# you must generate matching database migration scripts:
# /backend/README.md#Running database migrations with alembic
##############################################

# Post is a placefolder model for testing
class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    db_text: str
    
class PostCreate(SQLModel):
    db_text: str

class PostPublic(SQLModel):
    id: int
    db_text: str

# Pdf database table model
class Pdf(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True)
    original_filename: str
    uploaded_by: int | None = None
    parsed: bool = False
    virustotal_scan: bool | None = None

# For receiving pdf metadata
class PdfCreate(SQLModel):
    id: uuid.UUID
    original_filename: str
    uploaded_by: int | None = None

# for sending pdf metadata
class PdfPublic(SQLModel):
    id: uuid.UUID
    original_filename: str
    uploaded_by: int | None = None