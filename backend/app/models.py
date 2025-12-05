import uuid
from sqlmodel import Field, SQLModel, Relationship

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


class VirusScanResult(SQLModel, table=True):

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    pdf: "Pdf" = Relationship(back_populates="scan_results", sa_relationship_kwargs={'uselist': False})
    scan_results: str

# Pdf database table model
class Pdf(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True)
    original_filename: str
    uploaded_by: int | None = None
    parsed: bool = False
    scan_results_id: uuid.UUID | None = Field(foreign_key="virusscanresult.id")
    scan_results: VirusScanResult = Relationship(back_populates="pdf")

# For receiving pdf metadata
class PdfCreate(SQLModel):
    id: uuid.UUID
    original_filename: str
    uploaded_by: int | None = None

# for sending pdf metadata
class PdfPublic(SQLModel):
    id: uuid.UUID
    original_filename: str
    uploaded_by: int | None
    parsed: bool = False
    scan_results: VirusScanResult
