import os
import tempfile

import pytest
from fastapi.testclient import TestClient

# Point the app at a throwaway sqlite file before importing it.
_tmpdir = tempfile.mkdtemp(prefix="notebox-test-")
os.environ["NOTEBOX_DB_URL"] = f"sqlite:///{os.path.join(_tmpdir, 'test.db')}"

from app.db import init_db, engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(autouse=True)
def _fresh_db():
    # Recreate tables before each test for isolation.
    from app.db import Base
    Base.metadata.drop_all(bind=engine)
    init_db()
    yield


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)
