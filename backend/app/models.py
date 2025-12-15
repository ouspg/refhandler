"""
Contains SQLModel data structures for:
- defining database tables (models with table=True)
- validating incoming JSON objects at API endpoints (Create models)
- returning stripped down models from the database (Public models)
- storing fields that will be updated in the database model (Update models)

Process flow:
1. User sends JSON to API
2. JSON is validated and stored in ModelCreate
3. ModelCreate is used for creating Model database table
4. Model is retrieved from database and returned by API function
5. Before sending response, API uses response_model=ModelPublic to strip
    fields from Model that don't exist in ModelPublic
6. API returns ModelPublic as a JSON object
"""
# pylint: disable=missing-function-docstring, missing-class-docstring, invalid-name
import uuid
import enum
from sqlmodel import Field, SQLModel, Relationship, Enum, Column
from pydantic import EmailStr

##############################################
# WARNING
# If you make change to SQLModels with table=True,
# you must delete the postgres database OR
# generate matching database migration scripts:
# /backend/README.md#Running database migrations with alembic
##############################################


class VirusScanResult(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    pdf: "Pdf" = Relationship(
        back_populates="scan_result",
        sa_relationship_kwargs={'uselist': False})
    scan_results: str


# For creating Pdf models. Contains the fields required before database operations
class PdfCreate(SQLModel):
    original_filename: str
    content_hash: str
    uploaded_by: uuid.UUID = Field(foreign_key="user.id")
    scan_result_id: uuid.UUID = Field(foreign_key="virusscanresult.id")

# Pdf database table
class Pdf(PdfCreate, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    parsed: bool = False
    scan_result_id: uuid.UUID = Field(foreign_key="virusscanresult.id")
    scan_result: VirusScanResult = Relationship(back_populates="pdf")



# For returning Pdf objects. Hides fields we don't want to return
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


# Fields shared by User models
class UserBase(SQLModel):
    firstName: str | None = None
    middleName: str | None = None
    lastName: str | None = None
    email: EmailStr = Field(unique=True, index=True)
    phone: str | None = None
    status: str | None = None
    role: UserRole = Field(default=UserRole.user,
                           sa_column=Column(Enum(UserRole)))


# For creating users. Extends UserBase with plaintext password
class UserCreate(UserBase, use_enum_values=True):
    password: str = Field(min_length=8, max_length=128)

# For updating user information. Make sure all fields can be set to None
# so you can initialize the model with only the fields you want to update
class UserUpdate(UserBase):
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)

# User database table. Generates UUID and replaces plaintext password with hash
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str

# For returning User objects. Hides fields we don't want to return, such as password hash
class UserPublic(SQLModel):
    id: uuid.UUID
    firstName: str | None
    middleName: str | None
    lastName: str | None
    email: EmailStr
    phone: str | None
    status: str | None
    role: UserRole = Field(sa_column=Column(Enum(UserRole)))
