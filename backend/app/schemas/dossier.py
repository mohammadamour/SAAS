from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class BrandIntelligence(BaseModel):
    name: str = Field(..., description="Company or product display name")
    domain: str = Field(..., description="Cleaned domain identifier")
    logo_url: Optional[str] = Field(None, description="Vector or high-res logo URL")
    primary_color: str = Field("#00F0FF", description="Primary brand accent color in hex format")
    secondary_color: str = Field("#7928CA", description="Secondary brand accent color in hex format")
    description: Optional[str] = Field(None, description="Official company bio or elevator pitch")
    social_links: Dict[str, str] = Field(default_factory=dict, description="Verified social links")


class NetworkTelemetry(BaseModel):
    cloud_host: str = Field(..., description="Detected cloud infrastructure or edge provider")
    ip_address: str = Field(..., description="Resolved primary IPv4 / anycast address")
    ttfb_ms: float = Field(..., description="Time To First Byte latency in milliseconds")
    ssl_valid: bool = Field(..., description="Whether SSL/TLS certificate is currently valid")
    ssl_days_left: int = Field(..., description="Days remaining until SSL certificate expiration")
    tls_version: str = Field(..., description="Negotiated TLS protocol version")
    server_header: str = Field(..., description="Edge server response header")


class PerformanceVitals(BaseModel):
    performance_score: int = Field(..., ge=0, le=100, description="Overall Performance score (0-100)")
    seo_score: int = Field(..., ge=0, le=100, description="SEO audit score (0-100)")
    accessibility_score: int = Field(..., ge=0, le=100, description="Accessibility audit score (0-100)")
    fcp_seconds: float = Field(..., description="First Contentful Paint in seconds")
    speed_index: float = Field(..., description="Visual speed index in seconds")


class AiStrategyDossier(BaseModel):
    brutal_truth: str = Field(..., description="1-sentence unfiltered reality of what the company does")
    moat: str = Field(..., description="Core competitive moat or distribution advantage")
    vulnerability: str = Field(..., description="Biggest existential threat or vulnerability")
    top_competitors: List[str] = Field(default_factory=list, description="Top 3 direct industry rivals")
    estimated_tech_stack: List[str] = Field(default_factory=list, description="Inferred core technologies and infrastructure")


class PrismDossierResponse(BaseModel):
    domain: str
    brand: BrandIntelligence
    network: NetworkTelemetry
    vitals: PerformanceVitals
    ai_dossier: AiStrategyDossier
    cached: bool = False
    processing_time_ms: float
    timestamp: float
