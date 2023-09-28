from typing import Any
from app.deps.predictions import analyze_url

from fastapi import APIRouter

from app.deps.db import CurrentAsyncSession
from app.models.prediction import Prediction
from app.schemas.prediction import PredictionCreate, PredictionResponse

router = APIRouter(prefix="/analysis")

@router.post("", response_model=PredictionResponse, status_code=201)
async def create_prediction(
    prediction_in: PredictionCreate,
    session: CurrentAsyncSession,
) -> Any:
    features, predicted_result = await analyze_url(prediction_in.input)
    prediction = Prediction(**prediction_in.dict())
    prediction.set_features(features)
    prediction.prediction = predicted_result
    session.add(prediction)
    await session.commit()
    return PredictionResponse(prediction=predicted_result)
