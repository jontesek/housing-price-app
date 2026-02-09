from typing import Annotated

from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from slowapi import Limiter

from housing_prices.prediction import get_model
from housing_prices.settings import settings


def get_configured_model():
    return get_model(settings.model_name)


def validate_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Security(HTTPBearer())],
) -> str:
    """Check if the provided token matches our secret AUTH_TOKEN."""
    if credentials.credentials != settings.auth_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials


limiter = Limiter(key_func=lambda: "global_api_limit")
