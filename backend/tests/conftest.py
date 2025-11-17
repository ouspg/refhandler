import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi.responses import Response
from fastapi import UploadFile
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.api.deps import get_session
from app.api.scanners import Scanners

# Mock database with sqlite in-memory database
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

# Mock Scanners
class ScannersOverride(Scanners):
    @staticmethod
    async def clamav_scan(file: UploadFile):
        return Response()

# Inject mocks into app for test client
@pytest.fixture(name="client")  
def client_fixture(session: Session):  
    def get_session_override():  
        return session
    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[Scanners] = ScannersOverride
    client = TestClient(app)  
    yield client  
    app.dependency_overrides.clear() 
    