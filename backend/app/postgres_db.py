# pylint: disable=missing-function-docstring, missing-module-docstring, line-too-long
import os
from sqlmodel import SQLModel, create_engine, Session
from backend.app.api import user_crud


POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_DB = os.environ["POSTGRES_DB"]
POSTGRES_SERVER = os.environ["POSTGRES_SERVER"]
POSTGRES_PORT = os.environ["POSTGRES_PORT"]
POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

ADMIN_EMAIL = os.environ["ADMIN_EMAIL"]

engine = create_engine(POSTGRES_URL)

def init_db_tables(_engine = engine):
    # Initialize database tables using SQLMOdels from /backend/app/models.py
    SQLModel.metadata.create_all(bind=_engine)

def create_default_admin(_engine = engine):
    with Session(_engine) as session:
        # Create default admin account if it doesn't exist yet
        if user_crud.get_user_by_email(session, ADMIN_EMAIL) is None:
            user_crud.create_default_admin(session)