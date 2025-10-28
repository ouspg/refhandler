import uuid
from sqlmodel import Field, SQLModel

# For testing backend, not part of Refhandler
class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    db_text: str
    
class PDF(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True)
    original_filename: str | None = None
    parsed: bool = False