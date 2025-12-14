"""
Contains pytest fixtures that are used for other tests.
Used to override dependancies such as Postges with unit-testable mockups.
"""
# pylint: disable=missing-function-docstring, import-outside-toplevel
import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

# Mock database with sqlite in-memory database
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
