import pytest
from app.schemas.dossier import (
    BrandIntelligence,
    NetworkTelemetry,
    PerformanceVitals,
    AiStrategyDossier,
    PrismDossierResponse,
)


def test_prism_dossier_contract_serialization():
    brand = BrandIntelligence(
        name="Spotify",
        domain="spotify.com",
        logo_url="https://spotify.com/logo.svg",
        primary_color="#10B981",
        secondary_color="#064E3B",
        description="Digital music service giving access to millions of songs.",
        social_links={"twitter": "https://twitter.com/spotify"},
    )
    network = NetworkTelemetry(
        cloud_host="Google Cloud Platform",
        ip_address="35.186.224.25",
        ttfb_ms=42.5,
        ssl_valid=True,
        ssl_days_left=85,
        tls_version="TLSv1.3",
        server_header="envoy",
    )
    vitals = PerformanceVitals(
        performance_score=94,
        seo_score=98,
        accessibility_score=92,
        fcp_seconds=1.2,
        speed_index=1.8,
    )
    ai_dossier = AiStrategyDossier(
        brutal_truth="A media streaming utility that pays billions in royalties while trying to become an audio network.",
        moat="Personalized algorithmic discovery (Discover Weekly) and massive global catalog rights.",
        vulnerability="Dependency on major record label catalog licensing and high royalty margins.",
        top_competitors=["Apple Music", "YouTube Music", "Amazon Music"],
        estimated_tech_stack=["React", "Java / Spring Boot", "Google Cloud BigQuery", "Fastly CDN"],
    )

    dossier = PrismDossierResponse(
        domain="spotify.com",
        brand=brand,
        network=network,
        vitals=vitals,
        ai_dossier=ai_dossier,
        cached=False,
        processing_time_ms=1240.2,
        timestamp=1729320000.0,
    )

    json_dict = dossier.model_dump()
    assert json_dict["domain"] == "spotify.com"
    assert json_dict["brand"]["primary_color"] == "#10B981"
    assert json_dict["network"]["cloud_host"] == "Google Cloud Platform"
    assert json_dict["vitals"]["performance_score"] == 94
    assert len(json_dict["ai_dossier"]["top_competitors"]) == 3
