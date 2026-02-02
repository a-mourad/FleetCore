import pytest


from sqlalchemy import create_engine
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.deps import get_db, get_current_user
from app.db.database import metadata
from app.core.config import settings
import warnings


warnings.filterwarnings("ignore")


engine = create_engine(settings.test_database_url)



@pytest.fixture(scope="session")
def db_connection():
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture
def db_transaction(db_connection):
    transaction = db_connection.begin()
    yield db_connection
    transaction.rollback()


def get_test_db(db_transaction):
    yield db_transaction



def fake_current_user():
    # minimal fake user for tests
    return {"id": "test-user", "email": "test@example.com"}


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)


@pytest.fixture
def client(db_transaction):
    app.dependency_overrides[get_db] = lambda: db_transaction
    app.dependency_overrides[get_current_user] = fake_current_user
    yield TestClient(app)
    app.dependency_overrides.clear()

