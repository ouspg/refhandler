"""
Contains SQLModel data structures for:
- defining database tables (models with table=True)
- validating incoming JSON objects at API endpoints
"""
# pylint: disable=missing-function-docstring, missing-class-docstring, invalid-name
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
    pdf: "Pdf" = Relationship(
        back_populates="scan_result",
        sa_relationship_kwargs={'uselist': False})
    scan_results: str


# For receiving pdf metadata
class PdfCreate(SQLModel):
    original_filename: str
    content_hash: str
    uploaded_by: uuid.UUID = Field(foreign_key="user.id")
    scan_result_id: uuid.UUID = Field(foreign_key="virusscanresult.id")

# Pdf database table model
class Pdf(PdfCreate, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    parsed: bool = False
    scan_result_id: uuid.UUID = Field(foreign_key="virusscanresult.id")
    scan_result: VirusScanResult = Relationship(back_populates="pdf")



# for sending pdf metadata
class PdfPublic(SQLModel):
    id: uuid.UUID
    original_filename: str
    uploaded_by: uuid.UUID
    parsed: bool
    scan_result: VirusScanResult


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
    role: UserRole = Field(default=UserRole.user,
                           sa_column=Column(Enum(UserRole)))


class UserCreate(UserBase, use_enum_values=True):
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(UserBase):
    email: EmailStr | None
    password: str | None = Field(default=None, min_length=8, max_length=128)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
