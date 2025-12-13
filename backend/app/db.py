# pylint: disable=missing-function-docstring, missing-module-docstring, line-too-long, import-error
import os
from sqlmodel import SQLModel, create_engine, Session
from backend.app.api import user_crud


POSTGRES_USER = os.environ.get("POSTGRES_USER", 'NO POSTGRES_USER IN ENVIRONMENT')
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", 'NO POSTGRES_PASSWORD IN ENVIRONMENT')
POSTGRES_DB = os.environ.get("POSTGRES_DB", 'NO POSTGRES_DB IN ENVIRONMENT')
POSTGRES_SERVER = os.environ.get("POSTGRES_SERVER", 'NO POSTGRES_SERVER IN ENVIRONMENT')
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 'NO POSTGRES_PORT IN ENVIRONMENT')
POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", 'NO ADMIN_EMAIL IN ENVIRONMENT')

engine = create_engine(POSTGRES_URL)


def init_db():
    # Initialize database tables using SQLMOdels from /backend/app/models.py
    SQLModel.metadata.create_all(bind=engine)

    with Session(engine) as session:
        # Create default admin account if it doesn't exist yet
        if user_crud.get_user_by_email(session, ADMIN_EMAIL) is None:
            user_crud.create_default_admin(session)
