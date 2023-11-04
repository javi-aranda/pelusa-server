from typing import Callable

import numpy as np
from httpx import AsyncClient
from pytest_mock import MockerFixture

from app.core.config import settings


async def test_analysis(client: AsyncClient, mocker: MockerFixture) -> None:
    # Assume that the model will always predict 0 (legitimate)
    mocker.patch("app.api.predictions.analyze_url", return_value=(np.zeros(5), 0))

    resp = await client.post(
        f"{settings.API_PATH}/analysis", json={"input": "https://example.es"}
    )
    data = resp.json()
    assert resp.status_code == 201
    assert data["prediction"] == 0


async def test_analysis_stored_in_db(
    client: AsyncClient, create_prediction: Callable, mocker: MockerFixture
) -> None:
    # Assume that the model will always predict 0 (legitimate) but it's already stored as 1 (phishing)
    mocker.patch("app.api.predictions.analyze_url", return_value=(np.zeros(5), 0))

    prediction = await create_prediction("https://example.org", 1)

    resp = await client.post(
        f"{settings.API_PATH}/analysis", json={"input": "https://example.org"}
    )
    data = resp.json()
    prediction = data["prediction"]
    assert resp.status_code == 201
    assert prediction == 1


async def test_analysis_force(
    client: AsyncClient, create_prediction: Callable, mocker: MockerFixture
) -> None:
    # Assume that the model will always predict 0 (legitimate) but it's already stored as 1 (phishing), but we force the analysis
    mocker.patch("app.api.predictions.analyze_url", return_value=(np.zeros(5), 0))
    prediction = await create_prediction("https://example.net", 1)

    resp = await client.post(
        f"{settings.API_PATH}/analysis/force", json={"input": "https://example.net"}
    )
    data = resp.json()
    prediction = data["prediction"]
    assert resp.status_code == 201
    assert prediction == 0


async def test_analysis_bulk_without_db_caching(
    client: AsyncClient, mocker: MockerFixture
) -> None:
    # Assume that the model will always predict 0 (legitimate)
    mocker.patch("app.api.predictions.analyze_url", return_value=(np.zeros(5), 0))

    resp = await client.post(
        f"{settings.API_PATH}/analysis/bulk",
        json=["https://example.eu", "https://example.co.uk", "https://example.it"],
    )
    data = resp.json()
    assert resp.status_code == 201
    assert data[0]["prediction"] == 0
    assert data[1]["prediction"] == 0
    assert data[2]["prediction"] == 0


async def test_analysis_bulk_with_db_caching(
    client: AsyncClient, create_prediction: Callable, mocker: MockerFixture
) -> None:
    # Assume that the model will always predict 0 (legitimate) but some items are already stored as 1 (phishing)
    mocker.patch("app.api.predictions.analyze_url", return_value=(np.zeros(5), 0))

    await create_prediction("https://example.fr", 1)
    await create_prediction("https://example.com.ar", 1)

    resp = await client.post(
        f"{settings.API_PATH}/analysis/bulk",
        json=["https://example.fr", "https://example.com.ar", "https://example.pl"],
    )
    data = resp.json()
    assert resp.status_code == 201
    assert data[0]["prediction"] == 1
    assert data[1]["prediction"] == 1
    assert data[2]["prediction"] == 0
