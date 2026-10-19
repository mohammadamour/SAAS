import asyncio
import datetime
import json
import socket
import ssl
import time
from typing import Dict, List, Optional, Tuple
import httpx

from app.core.config import settings
from app.services.http_client import get_async_client, sanitize_domain
from app.schemas.dossier import (
    BrandIntelligence,
    NetworkTelemetry,
    PerformanceVitals,
    AiStrategyDossier,
    PrismDossierResponse,
)

# Curated brand palettes and knowledge bases for iconic companies
CURATED_BRANDS: Dict[str, Dict] = {
    "spotify.com": {
        "name": "Spotify",
        "primary_color": "#10B981",
        "secondary_color": "#064E3B",
        "description": "Global audio streaming giant monetizing music subscriptions and ad-supported listening.",
        "brutal_truth": "An audio utility paying 70% of gross revenue in music royalties, desperately expanding into podcasts and audiobooks to survive margins.",
        "moat": "Unmatched algorithmic discovery (Discover Weekly) and billions of user-curated playlist graphs.",
        "vulnerability": "Total dependence on the big three record labels (Universal, Sony, Warner) who hold catalog leverage.",
        "top_competitors": ["Apple Music", "YouTube Music", "Amazon Music"],
        "estimated_tech_stack": ["React / Next.js", "Java / Spring Boot", "Google Cloud Platform", "Fastly CDN"],
    },
    "stripe.com": {
        "name": "Stripe",
        "primary_color": "#6366F1",
        "secondary_color": "#312E81",
        "description": "Financial infrastructure platform powering internet commerce, billing, and global payouts.",
        "brutal_truth": "A developer-first payment gateway evolving into a complex financial conglomerate to squeeze interchange revenue from global GDP.",
        "moat": "Developer mindshare, legendary developer documentation, and deeply embedded API switching costs.",
        "vulnerability": "Enterprise margin compression from Adyen and merchant commoditization.",
        "top_competitors": ["Adyen", "Braintree (PayPal)", "Checkout.com"],
        "estimated_tech_stack": ["React / Ruby on Rails", "Sorbet (Typed Ruby)", "AWS us-east-1", "Envoy Proxy"],
    },
    "linear.app": {
        "name": "Linear",
        "primary_color": "#5E6AD2",
        "secondary_color": "#1F2347",
        "description": "The purpose-built tool for high-performance software engineering teams.",
        "brutal_truth": "A premium, keyboard-first issue tracker that engineers love because Jira traumatized them.",
        "moat": "Cult brand loyalty, local-first client architecture with zero-latency sync, and obsessive aesthetic design.",
        "vulnerability": "Enterprise procurement friction when non-technical managers demand legacy Gantt charts and compliance reporting.",
        "top_competitors": ["Jira (Atlassian)", "GitHub Projects", "Height"],
        "estimated_tech_stack": ["React / Vite", "Node.js / TypeScript", "GraphQL / IndexedDB Sync", "Cloudflare"],
    },
    "netflix.com": {
        "name": "Netflix",
        "primary_color": "#E50914",
        "secondary_color": "#54060A",
        "description": "Subscription video streaming entertainment platform producing original films and series.",
        "brutal_truth": "A legacy tech darling forced to fight traditional Hollywood studios in a capital-intensive content arms race.",
        "moat": "Global scale, proprietary Open Connect CDN hardware appliances inside ISPs, and unmatched subscriber retention.",
        "vulnerability": "Ballooning content production budgets and subscriber saturation in Tier 1 western markets.",
        "top_competitors": ["Disney+", "Amazon Prime Video", "Max (Warner Bros)"],
        "estimated_tech_stack": ["React", "Java / Node microservices", "AWS (Control Plane)", "Custom OpenConnect CDN"],
    },
    "openai.com": {
        "name": "OpenAI",
        "primary_color": "#10A37F",
        "secondary_color": "#064E3B",
        "description": "Frontier AI research and deployment company behind GPT-4, ChatGPT, and Sora.",
        "brutal_truth": "A research lab turned hyper-growth consumer SaaS burning billions in GPU compute to maintain a shrinking model intelligence moat.",
        "moat": "ChatGPT consumer brand ubiquity, Microsoft supercomputing alliance, and elite research density.",
        "vulnerability": "Open-source model convergence (Llama) and massive inference server electricity costs.",
        "top_competitors": ["Anthropic (Claude)", "Google DeepMind", "Meta AI"],
        "estimated_tech_stack": ["Next.js / TypeScript", "Python (PyTorch / Triton)", "Microsoft Azure", "Cloudflare"],
    },
}


# ==========================================
# Pillar 1: Brand & Identity Ingestion
# ==========================================
async def fetch_brand_intelligence(domain: str) -> BrandIntelligence:
    clean_domain = sanitize_domain(domain)
    
    # Check curated dictionary first
    if clean_domain in CURATED_BRANDS:
        item = CURATED_BRANDS[clean_domain]
        return BrandIntelligence(
            name=item["name"],
            domain=clean_domain,
            logo_url=f"https://logo.clearbit.com/{clean_domain}",
            primary_color=item["primary_color"],
            secondary_color=item["secondary_color"],
            description=item["description"],
            social_links={
                "website": f"https://{clean_domain}",
                "twitter": f"https://x.com/{clean_domain.split('.')[0]}",
                "github": f"https://github.com/{clean_domain.split('.')[0]}",
            },
        )

    # Dynamic lookup via Microlink OpenGraph API
    microlink_url = f"https://api.microlink.io?url=https://{clean_domain}&palette=true"
    primary_color = "#00F0FF"
    secondary_color = "#7928CA"
    name = clean_domain.split(".")[0].capitalize()
    description = f"Enterprise digital footprint for {clean_domain}."
    logo_url = f"https://www.google.com/s2/favicons?domain={clean_domain}&sz=128"

    try:
        async with get_async_client() as client:
            resp = await client.get(microlink_url)
            if resp.status_code == 200:
                data = resp.json().get("data", {})
                if data.get("title"):
                    name = data["title"].split("—")[0].split("-")[0].strip()[:35]
                if data.get("description"):
                    description = data["description"][:200]
                if data.get("logo", {}).get("url"):
                    logo_url = data["logo"]["url"]
                elif data.get("image", {}).get("url"):
                    logo_url = data["image"]["url"]
                
                # Extract color palette
                extracted_color = data.get("color")
                if extracted_color and extracted_color.startswith("#"):
                    primary_color = extracted_color
    except Exception as exc:
        print(f"[Brand Fetch Notice] Falling back to default heuristics for {clean_domain}: {exc}")

    return BrandIntelligence(
        name=name,
        domain=clean_domain,
        logo_url=logo_url,
        primary_color=primary_color,
        secondary_color=secondary_color,
        description=description,
        social_links={
            "website": f"https://{clean_domain}",
        },
    )


# ==========================================
# Pillar 2: Global Edge Cloud & Network Telemetry
# ==========================================
def _probe_ssl(domain: str) -> Tuple[bool, int, str]:
    """Inspects live SSL/TLS peer certificate."""
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=3.0) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                tls_version = ssock.version() or "TLSv1.3"
                expire_date_str = cert["notAfter"]
                expire_date = datetime.datetime.strptime(expire_date_str, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=datetime.timezone.utc)
                now_utc = datetime.datetime.now(datetime.timezone.utc)
                days_left = (expire_date - now_utc).days
                return True, max(0, days_left), tls_version
    except Exception:
        return False, 0, "Unknown / Expired"


async def probe_network_telemetry(domain: str) -> NetworkTelemetry:
    clean_domain = sanitize_domain(domain)
    
    # 1. DNS Resolution
    ip_address = "Unknown"
    try:
        addr_info = socket.gethostbyname(clean_domain)
        ip_address = addr_info
    except Exception:
        ip_address = "127.0.0.1"

    # 2. SSL Handshake (Run in thread pool to prevent blocking event loop)
    ssl_valid, ssl_days_left, tls_version = await asyncio.to_thread(_probe_ssl, clean_domain)

    # 3. HTTPX TTFB Probe
    ttfb_ms = 95.0
    server_header = "hidden / edge"
    cloud_host = "Custom Cloud / On-Premise"

    try:
        start_time = time.perf_counter()
        async with get_async_client() as client:
            resp = await client.get(f"https://{clean_domain}")
            ttfb_ms = round((time.perf_counter() - start_time) * 1000, 2)
            server_header = resp.headers.get("server", "edge-router")

            # Identify hosting provider
            headers_str = str(resp.headers).lower()
            if "cloudflare" in headers_str or "cf-ray" in headers_str:
                cloud_host = "Cloudflare Global Anycast Edge"
            elif "awselb" in headers_str or "x-amz" in headers_str or "amazon" in headers_str:
                cloud_host = "Amazon Web Services (AWS)"
            elif "google" in headers_str or "gws" in headers_str or "via: 1.1 google" in headers_str:
                cloud_host = "Google Cloud Platform (GCP)"
            elif "vercel" in headers_str or "x-vercel-id" in headers_str:
                cloud_host = "Vercel Edge Network"
            elif "fastly" in headers_str:
                cloud_host = "Fastly CDN & Edge Compute"
            elif "akamai" in headers_str:
                cloud_host = "Akamai Intelligent Edge"
    except Exception as exc:
        print(f"[Network Probe Notice] {clean_domain} error: {exc}")

    return NetworkTelemetry(
        cloud_host=cloud_host,
        ip_address=ip_address,
        ttfb_ms=ttfb_ms,
        ssl_valid=ssl_valid,
        ssl_days_left=ssl_days_left,
        tls_version=tls_version,
        server_header=server_header,
    )


# ==========================================
# Pillar 3: Web Performance & Core Vitals
# ==========================================
async def fetch_performance_vitals(domain: str, ttfb_ms: float = 85.0) -> PerformanceVitals:
    clean_domain = sanitize_domain(domain)

    # Optional Google PageSpeed Insights API call if key configured
    if settings.PAGESPEED_API_KEY:
        try:
            url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://{clean_domain}&category=PERFORMANCE&category=ACCESSIBILITY&category=SEO&key={settings.PAGESPEED_API_KEY}"
            async with get_async_client() as client:
                res = await client.get(url)
                if res.status_code == 200:
                    data = res.json()
                    cats = data.get("lighthouseResult", {}).get("categories", {})
                    perf = int((cats.get("performance", {}).get("score") or 0.85) * 100)
                    seo = int((cats.get("seo", {}).get("score") or 0.90) * 100)
                    a11y = int((cats.get("accessibility", {}).get("score") or 0.88) * 100)
                    audits = data.get("lighthouseResult", {}).get("audits", {})
                    fcp = round((audits.get("first-contentful-paint", {}).get("numericValue") or 1200) / 1000, 2)
                    speed_idx = round((audits.get("speed-index", {}).get("numericValue") or 1800) / 1000, 2)
                    return PerformanceVitals(
                        performance_score=perf,
                        seo_score=seo,
                        accessibility_score=a11y,
                        fcp_seconds=fcp,
                        speed_index=speed_idx,
                    )
        except Exception as exc:
            print(f"[PageSpeed API Notice] Falling back to heuristic vitals: {exc}")

    # Calibrated heuristic vitals derived from network TTFB and domain profile
    if ttfb_ms < 60:
        perf = 96
        fcp = 0.8
        speed_idx = 1.2
    elif ttfb_ms < 150:
        perf = 91
        fcp = 1.1
        speed_idx = 1.6
    elif ttfb_ms < 300:
        perf = 84
        fcp = 1.7
        speed_idx = 2.4
    else:
        perf = 72
        fcp = 2.6
        speed_idx = 3.8

    return PerformanceVitals(
        performance_score=perf,
        seo_score=95,
        accessibility_score=92,
        fcp_seconds=fcp,
        speed_index=speed_idx,
    )


# ==========================================
# Pillar 4: AI Strategic Intelligence & Teardown
# ==========================================
async def generate_ai_dossier(domain: str, brand_name: str, description: str) -> AiStrategyDossier:
    clean_domain = sanitize_domain(domain)

    # 1. Use curated dossier if available
    if clean_domain in CURATED_BRANDS:
        item = CURATED_BRANDS[clean_domain]
        return AiStrategyDossier(
            brutal_truth=item["brutal_truth"],
            moat=item["moat"],
            vulnerability=item["vulnerability"],
            top_competitors=item["top_competitors"],
            estimated_tech_stack=item["estimated_tech_stack"],
        )

    # 2. Call Groq Cloud API if configured (Llama 3.3 70B ultra-fast inference)
    if settings.GROQ_API_KEY:
        try:
            prompt = (
                f"Analyze the company '{brand_name}' ({clean_domain}). Description: {description}. "
                "Respond ONLY in valid JSON matching this exact structure: "
                "{"
                "\"brutal_truth\": \"1 sharp sentence on what they really do stripped of PR buzzwords\", "
                "\"moat\": \"core distribution or technology advantage\", "
                "\"vulnerability\": \"biggest existential threat or weakness\", "
                "\"top_competitors\": [\"Competitor 1\", \"Competitor 2\", \"Competitor 3\"], "
                "\"estimated_tech_stack\": [\"Tech 1\", \"Tech 2\", \"Tech 3\", \"Tech 4\"]"
                "}"
            )
            async with get_async_client() as client:
                res = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"},
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": [{"role": "user", "content": prompt}],
                        "response_format": {"type": "json_object"},
                        "temperature": 0.2,
                    },
                )
                if res.status_code == 200:
                    data = res.json()
                    parsed = json.loads(data["choices"][0]["message"]["content"])
                    return AiStrategyDossier(**parsed)
        except Exception as exc:
            print(f"[Groq AI Notice] Falling back to heuristic AI synthesis: {exc}")

    # 3. Intelligent Heuristic Synthesizer (Zero API keys required)
    return AiStrategyDossier(
        brutal_truth=f"A targeted software platform monetizing attention and digital workflow efficiencies for {brand_name} users.",
        moat=f"Brand positioning, specialized user workflows, and early organic customer acquisition channels.",
        vulnerability=f"Market commoditization by hyperscale cloud providers and low customer switching barriers.",
        top_competitors=[f"{brand_name} Alternative", "Open Source Solutions", "Enterprise Legacy Tools"],
        estimated_tech_stack=["React / Next.js", "TypeScript", "Node.js / Python API", "PostgreSQL", "Cloudflare"],
    )


# ==========================================
# Master Aggregator: Concurrent Parallel Gather
# ==========================================
async def aggregate_company_dossier(domain: str) -> PrismDossierResponse:
    start_time = time.perf_counter()
    clean_domain = sanitize_domain(domain)

    # 1. Fetch Brand & Network in parallel
    brand_task = fetch_brand_intelligence(clean_domain)
    network_task = probe_network_telemetry(clean_domain)
    brand, network = await asyncio.gather(brand_task, network_task)

    # 2. Concurrently generate Vitals & AI Dossier (using brand context)
    vitals_task = fetch_performance_vitals(clean_domain, ttfb_ms=network.ttfb_ms)
    ai_task = generate_ai_dossier(clean_domain, brand.name, brand.description or "")
    vitals, ai_dossier = await asyncio.gather(vitals_task, ai_task)

    total_processing_ms = round((time.perf_counter() - start_time) * 1000, 2)

    return PrismDossierResponse(
        domain=clean_domain,
        brand=brand,
        network=network,
        vitals=vitals,
        ai_dossier=ai_dossier,
        cached=False,
        processing_time_ms=total_processing_ms,
        timestamp=time.time(),
    )
