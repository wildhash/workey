"""Basic API health check tests."""
import pytest
from httpx import AsyncClient, ASGITransport

from workey_api.database import create_tables
from workey_api.main import app


@pytest.fixture(autouse=True)
async def setup_db():
    await create_tables()
    yield


@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_list_jobs_empty():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/jobs")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
