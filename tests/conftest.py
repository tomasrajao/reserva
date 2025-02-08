import pytest
from fastapi.testclient import TestClient

from reserva.app import app


@pytest.fixture
def client():
    return TestClient(app)
