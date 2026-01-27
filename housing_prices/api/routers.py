from fastapi import APIRouter

from .schemas import PredictInput, PredictResponse

router = APIRouter()


@router.get("/health", response_model=dict)
def get_sites():
    return {"status": "ok"}


@router.post("/predict", response_model=PredictResponse)
def get_site(input_json: PredictInput):
    pass
