from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from housing_prices import predicting
from housing_prices.settings import settings

from .schemas import PredictRequest, PredictResponse


# Setup token auth
def validate_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Security(HTTPBearer())],
):
    """Check if the provided token matches our secret AUTH_TOKEN."""
    if credentials.credentials != settings.auth_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials


# Helper for ML model
def get_configured_model():
    return predicting.get_model(settings.model_name)


# Setup routes
router = APIRouter()


@router.get("/health", response_model=dict)
def health():
    return {"status": "ok"}


@router.post(
    "/predict-price",
    response_model=PredictResponse,
    dependencies=[Security(validate_token)],
)
def predict_price(request_json: PredictRequest, model=Depends(get_configured_model)):
    input_df = predicting.prepare_input_df(request_json.model_dump())
    price = predicting.predict_price(model, input_df)
    return PredictResponse(house_price=price)
