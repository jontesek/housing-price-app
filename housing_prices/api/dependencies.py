from housing_prices.predicting import get_model
from housing_prices.settings import settings


def get_configured_model():
    return get_model(settings.model_name)
