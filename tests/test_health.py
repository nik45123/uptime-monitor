import pytest
from app.main import app
import httpx
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport

@pytest.mark.asyncio
async def test_health_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "uptime_seconds" in data
        assert "timestamp" in data
