from typing import Annotated

from fastapi import APIRouter, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from housing_prices.predict import load_model, predict_price, prepare_input_df
from housing_prices.settings import settings

from .schemas import PredictRequest, PredictResponse

# Setup token auth
security_scheme = HTTPBearer()


def validate_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Security(security_scheme)],
):
    """Check if the provided token matches our secret AUTH_TOKEN."""
    if credentials.credentials != settings.auth_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials


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
def predict(request_json: PredictRequest):
    model = load_model(settings.model_name)
    input_df = prepare_input_df(request_json.model_dump())
    price = predict_price(model, input_df)
    return PredictResponse(house_price=price)
