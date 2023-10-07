from typing import Any

from fastapi import APIRouter
from sqlalchemy.future import select

from app.deps.db import CurrentAsyncSession
from app.deps.predictions import analyze_url
from app.models.prediction import Prediction
from app.schemas.prediction import PredictionCreate, PredictionResponse

router = APIRouter(prefix="/analysis")


async def create_prediction_helper(
    prediction_in: PredictionCreate,
    session: CurrentAsyncSession,
) -> PredictionResponse:
    features, predicted_result = await analyze_url(prediction_in.input)

    prediction = Prediction(**prediction_in.dict())
    prediction.set_features(features)
    prediction.prediction = predicted_result

    session.add(prediction)
    await session.commit()

    return PredictionResponse(prediction=predicted_result)


@router.post("", response_model=PredictionResponse, status_code=201)
async def create_prediction(
    prediction_in: PredictionCreate,
    session: CurrentAsyncSession,
) -> Any:
    existing_prediction = await session.execute(
        select(Prediction).filter_by(input=prediction_in.input)
    )
    db_prediction = existing_prediction.scalars().first()

    if db_prediction:
        return PredictionResponse(prediction=db_prediction.prediction)

    return await create_prediction_helper(prediction_in, session)


@router.post("/force", response_model=PredictionResponse, status_code=201)
async def force_create_prediction(
    prediction_in: PredictionCreate,
    session: CurrentAsyncSession,
) -> Any:
    return await create_prediction_helper(prediction_in, session)
