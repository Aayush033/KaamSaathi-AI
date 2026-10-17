import os
# Ensure test environment controls are set before application modules load
os.environ["ENVIRONMENT"] = "testing"
os.environ["ALLOW_TEST_SESSION_HEADER"] = "true"

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db

@pytest.fixture(scope="session", autouse=True)
def setup_test_db(tmp_path_factory):
    """Sets up an isolated, temporary SQLite database for test execution."""
    test_db_dir = tmp_path_factory.mktemp("test_db")
    test_db_path = test_db_dir / "test_kaamsaathi.db"
    
    os.environ["DATABASE_PATH"] = str(test_db_path)
    init_db()
    
    yield
    
    # Cleanup env
    if "DATABASE_PATH" in os.environ:
        del os.environ["DATABASE_PATH"]

@pytest.fixture
def client():
    # Fresh TestClient per test function
    return TestClient(app)
