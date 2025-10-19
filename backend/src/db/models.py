import uuid
from sqlmodel import Field, SQLModel

# For testing backend, not part of Refhandler
class Post(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    db_text: str
class PDF(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)