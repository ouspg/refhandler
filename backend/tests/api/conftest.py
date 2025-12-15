"""
Contains pytest fixtures that are used by API unit tests.
Used to override dependancies such as Postges with unit-testable mockups.
"""
# pylint: disable=missing-function-docstring, import-outside-toplevel
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from backend.app.api.depdendancies import get_session
from backend.app.main import app

# Mock database with sqlite in-memory database
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

# Inject mock database into app for test client
@pytest.fixture(name="client")
def client_fixture(session: Session):
    # Imports moved here to avoid circular import error


    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()