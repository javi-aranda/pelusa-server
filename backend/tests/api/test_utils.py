from httpx import AsyncClient

from app.core.config import settings


async def test_healthy(client: AsyncClient) -> None:
    resp = await client.get(f"{settings.API_PATH}/healthy")
    data = resp.json()
    assert resp.status_code == 200
    assert data["msg"] == "healthy"
    assert data["ct"] is not None
