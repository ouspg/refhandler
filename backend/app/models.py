import uuid
import enum
from sqlmodel import Field, SQLModel, Relationship, Enum, Column
from pydantic import EmailStr

##############################################
# WARNING
# If you make change to SQLModels with table=True,
# you must generate matching database migration scripts:
# /backend/README.md#Running database migrations with alembic
##############################################

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


class UserRole(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    user = "user"

class UserBase(SQLModel):
    firstName: str | None = None
    middleName: str | None = None
    lastName: str | None = None
    email: EmailStr = Field(unique=True, index=True)
    phone: str | None = None
    status: str | None = None
    role: UserRole = Field(default=UserRole.user, sa_column=Column(Enum(UserRole)))

class UserCreate(UserBase, use_enum_values=True):
    password: str = Field(min_length=8, max_length=128)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str