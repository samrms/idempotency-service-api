import pytest
from fastapi.testclient import TestClient

from src.infrastructure.database.models import Base
from src.infrastructure.database.session import SessionLocal, engine
from src.main import app


@pytest.fixture(scope="session", autouse=True)
def database():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def clean_database():
    yield
    with SessionLocal() as session:
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()
