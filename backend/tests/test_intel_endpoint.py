import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_get_presets_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/presets")
        assert resp.status_code == 200
        data = resp.json()
        assert "presets" in data
        assert len(data["presets"]) >= 5
        domains = [p["domain"] for p in data["presets"]]
        assert "spotify.com" in domains
        assert "stripe.com" in domains


@pytest.mark.asyncio
async def test_cache_telemetry_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/cache/stats")
        assert resp.status_code == 200
        data = resp.json()
        assert "status" in data
        assert "cached_dossiers_count" in data


@pytest.mark.asyncio
async def test_intel_endpoint_cache_miss_and_hit():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # First query (Cache MISS or fresh)
        resp1 = await client.get("/api/v1/intel/linear.app")
        assert resp1.status_code == 200
        data1 = resp1.json()
        assert data1["domain"] == "linear.app"
        assert data1["brand"]["name"] == "Linear"
        assert data1["brand"]["primary_color"] == "#5E6AD2"
        assert "brutal_truth" in data1["ai_dossier"]
        assert data1["network"]["cloud_host"] != ""

        # Second query (Cache HIT from Redis / memory)
        resp2 = await client.get("/api/v1/intel/linear.app")
        assert resp2.status_code == 200
        data2 = resp2.json()
        assert data2["domain"] == "linear.app"
        assert data2["cached"] is True
        assert data2["processing_time_ms"] < 100.0


@pytest.mark.asyncio
async def test_intel_invalid_domain():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/intel/invalid_domain_without_dot")
        assert resp.status_code == 400
        assert "Invalid domain format" in resp.json()["detail"]
