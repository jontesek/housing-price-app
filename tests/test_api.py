from unittest.mock import MagicMock

import pytest

from housing_prices.api.dependencies import get_configured_model
from housing_prices.app import app
from housing_prices.settings import settings

# Constants
TEST_PAYLOAD = {
    "longitude": -122.64,
    "latitude": 38.01,
    "housing_median_age": 36.0,
    "total_rooms": 1336.0,
    "total_bedrooms": 258.0,
    "population": 678.0,
    "households": 249.0,
    "median_income": 5.5789,
    "ocean_proximity": "NEAR OCEAN",
}
AUTH_TOKEN = "test-token"  # noqa: S105


# Prepare
@pytest.fixture(autouse=True)
def force_test_settings():
    """Set testing values in settings."""
    settings.auth_token = AUTH_TOKEN
    settings.rate_limit_per_minute = 10


@pytest.fixture
def mock_fast_model():
    """Return a mock model that doesn't do any real work."""
    model = MagicMock()
    model.predict.return_value = [320202]
    return model


# Actual tests
def test_predict_price_wrong_token(client):
    headers = {"Authorization": "Bearer wrong-token"}
    response = client.post("/predict-price", json={}, headers=headers)
    assert response.status_code == 401


def test_predict_price_real_model(client):
    # Prepare request
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    # Send request
    response = client.post("/predict-price", json=TEST_PAYLOAD, headers=headers)
    # Check result
    assert response.status_code == 200
    data = response.json()
    price = round(data["house_price"])
    assert price == 320202


def test_predict_price_rate_limit(client, mock_fast_model):
    # Replace real model with mock model
    app.dependency_overrides[get_configured_model] = lambda: mock_fast_model
    # Do some requests
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    limit = settings.rate_limit_per_minute
    for _ in range(limit):
        response = client.post("/predict-price", json=TEST_PAYLOAD, headers=headers)
        assert response.status_code == 200
    # The next request should be blocked
    response = client.post("/predict-price", json=TEST_PAYLOAD, headers=headers)
    assert response.status_code == 429
