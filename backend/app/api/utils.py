import datetime
from typing import Any

from fastapi import APIRouter

from app.schemas.healthy import CurrentTimeHealthy

router = APIRouter()


@router.get(
    "/healthy",
    response_model=CurrentTimeHealthy,
    status_code=200,
    include_in_schema=False,
)
def healthy() -> Any:
    return {"ct": str(datetime.datetime.utcnow()), "msg": "healthy"}
