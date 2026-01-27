from fastapi import APIRouter

from housing_prices.predict import load_model, predict_price, prepare_input_df

from .schemas import PredictRequest, PredictResponse

router = APIRouter()


@router.get("/health", response_model=dict)
def health():
    return {"status": "ok"}


@router.post("/predict-price", response_model=PredictResponse)
def predict(request_json: PredictRequest):
    model = load_model("model.joblib")
    input_df = prepare_input_df(request_json.model_dump())
    price = predict_price(model, input_df)
    return PredictResponse(house_price=price)
