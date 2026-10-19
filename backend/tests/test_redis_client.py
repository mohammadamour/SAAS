import asyncio
import pytest
from app.core.redis_client import get_cached_dossier, set_cached_dossier, get_cache_stats


@pytest.mark.asyncio
async def test_set_and_get_cached_dossier():
    test_domain = "test-company.io"
    sample_payload = {
        "domain": test_domain,
        "brand": {"name": "Test Company", "primary_color": "#00F0FF"},
        "network": {"cloud_host": "Cloudflare", "ttfb_ms": 34.2},
    }

    # Store
    saved = await set_cached_dossier(test_domain, sample_payload, ttl=60)
    assert saved is True

    # Retrieve
    cached = await get_cached_dossier(test_domain)
    assert cached is not None
    assert cached["domain"] == test_domain
    assert cached["brand"]["name"] == "Test Company"
    assert cached["network"]["cloud_host"] == "Cloudflare"


@pytest.mark.asyncio
async def test_cache_stats():
    stats = await get_cache_stats()
    assert "status" in stats
    assert "cached_dossiers_count" in stats
    assert stats["cached_dossiers_count"] >= 1
