from typing import Callable

from httpx import AsyncClient

from app.core.config import settings


async def test_analysis(client: AsyncClient) -> None:
    resp = await client.post(
        f"{settings.API_PATH}/analysis", json={"input": "https://example.com"}
    )
    data = resp.json()
    assert resp.status_code == 201
    assert data["prediction"] == 0


async def test_analysis_stored_in_db(
    client: AsyncClient, create_prediction: Callable
) -> None:
    prediction = await create_prediction("https://example.org", 1)

    resp = await client.post(
        f"{settings.API_PATH}/analysis", json={"input": "https://example.org"}
    )
    data = resp.json()
    prediction = data["prediction"]
    assert resp.status_code == 201
    assert prediction == 1


async def test_analysis_force(client: AsyncClient, create_prediction: Callable) -> None:
    prediction = await create_prediction("https://example.net", 1)

    resp = await client.post(
        f"{settings.API_PATH}/analysis/force", json={"input": "https://example.net"}
    )
    data = resp.json()
    prediction = data["prediction"]
    assert resp.status_code == 201
    assert prediction == 0
