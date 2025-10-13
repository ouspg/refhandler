
from sqlmodel import Session, SQLModel, create_engine
from os import environ

POSTGRES_USER = environ.get("POSTGRES_USER", 'NO POSTGRES_USER IN ENVIRONMENT')
POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD", 'NO POSTGRES_PASSWORD IN ENVIRONMENT')
POSTGRES_DB = environ.get("POSTGRES_DB", 'NO POSTGRES_DB IN ENVIRONMENT')
POSTGRES_SERVER = environ.get("POSTGRES_SERVER", 'NO POSTGRES_SERVER IN ENVIRONMENT')
POSTGRES_PORT = environ.get("POSTGRES_PORT", 'NO POSTGRES_PORT IN ENVIRONMENT')
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)

def initialize_db():
    SQLModel.metadata.create_all(bind=engine)
    
def get_session():
    with Session(engine) as session:
        yield session
