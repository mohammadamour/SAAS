import pytest
from app.services.intelligence_service import aggregate_company_dossier, sanitize_domain


def test_sanitize_domain():
    assert sanitize_domain("https://www.spotify.com/us/premium?ref=1") == "spotify.com"
    assert sanitize_domain("HTTP://STRIPE.COM/docs") == "stripe.com"
    assert sanitize_domain("linear.app/#features") == "linear.app"


@pytest.mark.asyncio
async def test_aggregate_curated_company_dossier():
    dossier = await aggregate_company_dossier("spotify.com")
    
    # Pillar 1
    assert dossier.domain == "spotify.com"
    assert dossier.brand.name == "Spotify"
    assert dossier.brand.primary_color == "#10B981"
    
    # Pillar 2
    assert dossier.network.ttfb_ms >= 0
    assert isinstance(dossier.network.ssl_valid, bool)
    
    # Pillar 3
    assert dossier.vitals.performance_score > 0
    assert dossier.vitals.seo_score > 0
    
    # Pillar 4
    assert "royalties" in dossier.ai_dossier.brutal_truth.lower()
    assert len(dossier.ai_dossier.top_competitors) == 3
    assert len(dossier.ai_dossier.estimated_tech_stack) > 0
    
    # Metadata
    assert dossier.cached is False
    assert dossier.processing_time_ms > 0
