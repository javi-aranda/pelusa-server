from typing import Any, List

from fastapi import APIRouter, HTTPException
from sqlalchemy.future import select

from app.core.config import settings
from app.deps.db import CurrentAsyncSession
from app.deps.predictions import analyze_url
from app.models.prediction import Prediction
from app.schemas.prediction import (
    BulkPredictionResponse,
    PredictionCreate,
    PredictionResponse,
)

router = APIRouter(prefix="/analysis")


async def retrieve_db_prediction(
    prediction_in: str | PredictionCreate, session: CurrentAsyncSession
) -> Any:
    input = (
        prediction_in.input
        if isinstance(prediction_in, PredictionCreate)
        else prediction_in
    )

    existing_prediction = await session.execute(
        select(Prediction).filter_by(input=input)
    )
    db_prediction = existing_prediction.scalars().first()
    return db_prediction


async def create_prediction_mixin(
    prediction_in: str | PredictionCreate, session: CurrentAsyncSession
) -> bool:
    input = (
        prediction_in.input
        if isinstance(prediction_in, PredictionCreate)
        else prediction_in
    )
    features, predicted_result = await analyze_url(input)

    prediction = Prediction(input=input)
    prediction.set_features(features)
    prediction.prediction = predicted_result

    session.add(prediction)
    await session.commit()
    return predicted_result


async def create_single_prediction_helper(
    prediction_in: PredictionCreate,
    session: CurrentAsyncSession,
) -> PredictionResponse:
    predicted_result = await create_prediction_mixin(prediction_in, session)

    return PredictionResponse(prediction=predicted_result)


@router.post("", response_model=PredictionResponse, status_code=201)
async def create_prediction(
    prediction_in: PredictionCreate,
    session: CurrentAsyncSession,
) -> Any:
    db_prediction = await retrieve_db_prediction(prediction_in, session)

    if db_prediction:
        return PredictionResponse(prediction=db_prediction.prediction)

    return await create_single_prediction_helper(prediction_in, session)


@router.post("/bulk", response_model=List[BulkPredictionResponse], status_code=201)
async def bulk_create_predictions(
    bulk_input: List[str],
    session: CurrentAsyncSession,
) -> List[BulkPredictionResponse]:

    if len(bulk_input) > settings.MAX_BULK_PREDICTIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Bulk request exceeds maximum allowed predictions: {settings.MAX_BULK_PREDICTIONS}",
        )

    results = []
    for input in bulk_input:
        db_prediction = await retrieve_db_prediction(input, session)
        if db_prediction:
            results.append(
                BulkPredictionResponse(input=input, prediction=db_prediction.prediction)
            )
        else:
            predicted_result = await create_prediction_mixin(input, session)
            results.append(
                BulkPredictionResponse(input=input, prediction=predicted_result)
            )

    await session.commit()

    return results


@router.post("/force", response_model=PredictionResponse, status_code=201)
async def force_create_prediction(
    prediction_in: PredictionCreate,
    session: CurrentAsyncSession,
) -> Any:
    return await create_single_prediction_helper(prediction_in, session)
