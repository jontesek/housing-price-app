from fastapi import APIRouter, Depends, Request, Security

from housing_prices import predicting
from housing_prices.settings import settings

from .dependencies import get_configured_model, limiter, validate_token
from .schemas import PredictRequest, PredictResponse

router = APIRouter()


@router.get("/health", response_model=dict)
def health():
    """Check that app is running."""
    return {"status": "ok"}


@router.post(
    "/predict-price",
    response_model=PredictResponse,
    dependencies=[Security(validate_token)],
)
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
def predict_price(
    request: Request, request_data: PredictRequest, model=Depends(get_configured_model)
):
    """Receive house data, return house price."""
    input_df = predicting.prepare_input_df(request_data.model_dump())
    price = predicting.predict_price(model, input_df)
    return PredictResponse(house_price=price)
