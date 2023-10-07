from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.prediction import Prediction


async def test_analysis(client: AsyncClient) -> None:
    resp = await client.post(
        f"{settings.API_PATH}/analysis", json={"input": "https://example.com"}
    )
    data = resp.json()
    assert resp.status_code == 201
    assert data["prediction"] == 0


async def test_analysis_stored_in_db(client: AsyncClient, db: AsyncSession) -> None:
    prediction = Prediction(
        id=5,
        input="https://example.com",
        features="[1, 2, 3]",
        prediction=True,
    )
    db.add(prediction)
    await db.commit()

    resp = await client.post(
        f"{settings.API_PATH}/analysis", json={"input": "https://example.com"}
    )
    data = resp.json()
    assert resp.status_code == 201
    assert data["prediction"] == 1


async def test_analysis_force(client: AsyncClient, db: AsyncSession) -> None:
    prediction = Prediction(
        id=5,
        input="https://example.com",
        features="[1, 2, 3]",
        prediction=True,
    )
    db.add(prediction)
    await db.commit()

    resp = await client.post(
        f"{settings.API_PATH}/analysis/force", json={"input": "https://example.com"}
    )
    data = resp.json()
    assert resp.status_code == 201
    assert data["prediction"] == 0
