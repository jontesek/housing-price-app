import pytest
from fastapi.testclient import TestClient

from housing_prices.app import app


@pytest.fixture
def client():
    # Reset rate limit before each test
    if hasattr(app.state, "limiter"):
        app.state.limiter._storage.storage.clear()

    with TestClient(app) as c:
        yield c
