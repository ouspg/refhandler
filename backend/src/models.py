from sqlmodel import Field, SQLModel

class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    db_text: str