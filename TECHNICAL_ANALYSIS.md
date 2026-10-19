# 🧬 PRISM // OS — Technical Analysis & Living Architectural Memory

> **System Designation**: Autonomous Corporate & Infrastructure Intelligence Terminal  
> **Repository**: [https://github.com/mohammadamour/SAAS](https://github.com/mohammadamour/SAAS)  
> **Status**: In Active Development — Phase 1 (Backend Aggregator & Caching) Complete through Step 1.4  
> **Core Stack**: Python 3.12 (FastAPI), Redis, Vue 3 (Vite), Docker & Docker Compose  

---

## 📑 Table of Contents
1. [Project Philosophy & Motivation](#1-project-philosophy--motivation)
2. [Master Architecture & Telemetry Topology](#2-master-architecture--telemetry-topology)
3. [Implemented Modules & Technical Specifications](#3-implemented-modules--technical-specifications)
   - [3.1 Configuration & Environment Binding](#31-configuration--environment-binding)
   - [3.2 Shared Async HTTP Client & Domain Sanitization](#32-shared-async-http-client--domain-sanitization)
   - [3.3 Pydantic Contracts & Data Schemas](#33-pydantic-contracts--data-schemas)
   - [3.4 Multi-Stream Async Intelligence Aggregator](#34-multi-stream-async-intelligence-aggregator)
   - [3.5 Redis Distributed Caching & In-Memory Fallback](#35-redis-distributed-caching--in-memory-fallback)
   - [3.6 Automated Test Suite & Quality Gates](#36-automated-test-suite--quality-gates)
4. [Discovered Quirks, Nuances & Solutions](#4-discovered-quirks-nuances--solutions)
5. [Active Engineering Roadmap](#5-active-engineering-roadmap)

---

## 1. Project Philosophy & Motivation

**PRISM // OS** is an ultra-high-density corporate and infrastructure intelligence terminal that concurrently analyzes any global company, domain, or product in real-time.

### Engineering Skill Shift Matrix
Designed to bridge the gap between traditional web application development (**Node.js, React, Next.js, Laravel, PostgreSQL, MySQL, TypeScript**) and high-performance backend systems:

| Dimension | Previous Stack | PRISM // OS Architecture |
| :--- | :--- | :--- |
| **Backend Runtime** | Node.js / PHP (Laravel) | **Python 3.12+ (Asyncio, Non-blocking I/O)** |
| **API Framework** | Express / Next API Routes | **FastAPI** (Pydantic v2 Rust engine, automatic Swagger/OpenAPI) |
| **In-Memory & Caching** | Direct DB queries | **Redis** (24h TTL caching, distributed token-bucket rate limiting) |
| **Frontend Framework** | React / Next.js | **Vue 3** (Composition API, Vite, custom CSS token engine) |
| **Design System** | Generic UI / Tailwind | **Obsidian Glassmorphism & Dynamic Chameleon Theming** |
| **Infrastructure** | Manual local servers | **Docker & Docker Compose** (multi-container orchestration) |

---

## 2. Master Architecture & Telemetry Topology

```mermaid
flowchart TD
    User([Visitor / Client]) -->|1. Types Domain or Clicks Chip| SearchBar[Search & Command Console]
    SearchBar -->|2. GET /api/v1/intel/{domain}| FastAPIGateway[FastAPI Gateway & SlowAPI Limiter]
    
    FastAPIGateway -->|3. Check Hash Key prism:dossier:{domain}| Redis[(Redis In-Memory Buffer)]
    
    Redis -->|Cache HIT < 1ms| ReturnPayload[Instant Telemetry Payload]
    
    Redis -->|Cache MISS| AggregatorEngine[Parallel Async Aggregator Engine]
    
    subgraph External_Feeds [4 Parallel External Intelligence Streams]
        AggregatorEngine -->|Async HTTPX| Stream1[Pillar 1: Brand & Logo Ingestion]
        AggregatorEngine -->|Native SSL & DNS Sockets| Stream2[Pillar 2: Cloud Host & SSL Telemetry]
        AggregatorEngine -->|Google PageSpeed REST / Heuristic| Stream3[Pillar 3: Performance & Core Vitals]
        AggregatorEngine -->|Groq LPU / Heuristic Synthesis| Stream4[Pillar 4: AI Strategic Teardown]
    end
    
    External_Feeds --> AggregatorEngine
    AggregatorEngine -->|4. Save with 24h TTL| Redis
    AggregatorEngine --> ReturnPayload
    
    ReturnPayload -->|5. Reactive JSON Payload| VueState[Vue 3 Intel Store]
    
    subgraph Chameleon_UI [Cybernetic Chameleon HUD]
        VueState -->|6. Smooth 0.8s CSS Transition| DynamicTheme[--brand-primary, --brand-glow, --brand-surface]
        VueState --> Q1[Quadrant 1: Brand & Logo Deck]
        VueState --> Q2[Quadrant 2: Cloud & SSL Telemetry]
        VueState --> Q3[Quadrant 3: Vitals & Score Rings]
        VueState --> Q4[Quadrant 4: AI Strategic Teardown]
    end
```

---

## 3. Implemented Modules & Technical Specifications

### 3.1 Configuration & Environment Binding
- **File**: `backend/app/core/config.py`
- **Class**: `Settings(BaseSettings)`
- **Configuration Pattern**: Uses Pydantic v2 `model_config = {"env_file": ".env", "extra": "ignore"}`.
- **Environment Bindings**:
  - `APP_NAME`: `"PRISM // OS Intelligence Engine"`
  - `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`, `REDIS_PASSWORD` (derived property `redis_url`).
  - `GROQ_API_KEY`: Optional API key for Llama 3.3 70B inference.
  - `GEMINI_API_KEY`: Optional API key for Google Gemini Flash inference.
  - `PAGESPEED_API_KEY`: Optional key for Google Lighthouse metrics.
  - `REQUEST_TIMEOUT_SECONDS`: Default `8.0` seconds for all external HTTP requests.

### 3.2 Shared Async HTTP Client & Domain Sanitization
- **File**: `backend/app/services/http_client.py`
- **Functions**:
  - `sanitize_domain(raw_input: str) -> str`: Normalizes messy user inputs (e.g. `https://www.spotify.com/us/premium?ref=1` -> `spotify.com`) using regex and delimiter splitting.
  - `get_async_client() -> httpx.AsyncClient`: Singleton factory providing browser-grade user agent headers (`Mozilla/5.0 ... PRISM-OS/1.0`) preventing bot blocking on public metadata endpoints.

### 3.3 Pydantic Contracts & Data Schemas
- **File**: `backend/app/schemas/dossier.py`
- **Models**:
  - `BrandIntelligence`: `name`, `domain`, `logo_url`, `primary_color` (hex), `secondary_color` (hex), `description`, `social_links`.
  - `NetworkTelemetry`: `cloud_host`, `ip_address`, `ttfb_ms`, `ssl_valid`, `ssl_days_left`, `tls_version`, `server_header`.
  - `PerformanceVitals`: `performance_score` (0-100), `seo_score`, `accessibility_score`, `fcp_seconds`, `speed_index`.
  - `AiStrategyDossier`: `brutal_truth`, `moat`, `vulnerability`, `top_competitors` (3 items), `estimated_tech_stack` (list).
  - `PrismDossierResponse`: Top-level contract encapsulating all 4 pillars plus `cached: bool`, `processing_time_ms: float`, and `timestamp: float`.

### 3.4 Multi-Stream Async Intelligence Aggregator
- **File**: `backend/app/services/intelligence_service.py`
- **Execution Pattern**: High-concurrency `asyncio.gather()` aggregating 4 data streams:
  1. **Pillar 1 (Brand & Identity)**: Queries Microlink OpenGraph API for dynamic vector logos and color palettes. Features curated instant profiles for iconic brands (Spotify, Stripe, Linear, Netflix, OpenAI).
  2. **Pillar 2 (Edge Cloud & Network)**: Direct socket SSL handshake inspection using `ssl.create_default_context()` run in an async worker thread (`asyncio.to_thread(_probe_ssl)`). Extracts exact TLS protocol, expiration date, and calculates remaining days. Direct DNS resolution and HTTPX TTFB latency measurement. Inspects response headers to identify hosting giants (AWS, Cloudflare, GCP, Fastly, Vercel, Akamai).
  3. **Pillar 3 (Performance & Core Vitals)**: PageSpeed Insights API integration with deterministic, latency-calibrated fallback engine for sub-millisecond calculation when offline or rate-limited.
  4. **Pillar 4 (AI Strategic Teardown)**: Groq Cloud LPU integration (Llama 3.3 70B with strict JSON mode) + built-in curated executive dossiers + heuristic dynamic analyzer.

### 3.5 Redis Distributed Caching & In-Memory Fallback
- **File**: `backend/app/core/redis_client.py`
- **Cache Invalidation & TTL**: 24-hour expiration (`86,400s`) keyed under `prism:dossier:{domain}`.
- **Resilient Fallback Layer**: If Redis is offline during local development, an internal in-memory dictionary buffer (`_local_memory_cache`) transparently stores tuples of `(payload, expire_timestamp)`, ensuring the backend **never throws 500 errors** even if Docker is not booted.
- **Telemetry Probe**: `get_cache_stats()` exposes live memory usage, cached dossier counts, and engine status (Redis cluster vs embedded RAM).

### 3.6 Automated Test Suite & Quality Gates
- **Tests Location**: `backend/tests/`
  - `test_health.py`: Validates `/health` system status and Redis connectivity.
  - `test_schemas.py`: Validates Pydantic serialization, field validation, and contract integrity.
  - `test_intelligence_service.py`: Validates domain sanitization and multi-stream aggregator for curated and dynamic entities.
  - `test_redis_client.py`: Validates cache set, get, TTL expiration, and telemetry stats.
  - `test_intel_endpoint.py`: Validates `/api/v1/intel/{domain}` cache-miss and cache-hit behavior, presets, and invalid domain handling.
- **Pass Rate**: **10/10 tests passing (100%)** in 4.73s with zero warnings.

### 3.8 Cybernetic Chameleon CSS Design System (`tokens.css`)
- **Files**: `frontend/src/assets/styles/tokens.css`, `frontend/src/style.css`, `frontend/index.html`
- **Dynamic Chameleon Theming**: Configured reactive CSS custom properties (`--brand-primary`, `--brand-primary-rgb`, `--brand-secondary`, `--brand-glow`, `--brand-surface`, `--brand-border`) that morph smoothly using a `0.8s cubic-bezier(0.16, 1, 0.3, 1)` easing curve.
- **Glassmorphism & HUD Tokens**: Frosted card classes (`.prism-card`), subtle glowing borders, status pills (`.prism-pill`), glowing pulse dots, background dot grid (`32px` interval), and ambient blurred glow spheres.
- **Typography Integration**: Linked Google Fonts (*Plus Jakarta Sans* for UI, *JetBrains Mono* for telemetry metrics). Built and verified clean production bundle.

### 3.9 Reactive Intel Store & Preset Engine (`useIntelStore.js`)
- **File**: `frontend/src/stores/useIntelStore.js`
- **Chameleon Mutator**: `applyBrandTheme(primaryHex, secondaryHex)` dynamically derives RGB channels and sets `--brand-primary`, `--brand-primary-rgb`, etc. directly on `document.documentElement.style`, activating the 0.8s fluid transition.
- **State Properties**: `activeDomain`, `dossier`, `isLoading`, `error`, `cacheStats`, `presets`.
- **Pre-seeded Corporate Presets**: Instant targets for **Spotify** (`#10B981`), **Stripe** (`#6366F1`), **Linear** (`#5E6AD2`), **Netflix** (`#E50914`), and **OpenAI** (`#10A37F`) allowing 1-click evaluation without typing. Built-in instant fallback payload ensures instantaneous initial paint.

### 3.10 Navigation Header & Command Search Console (`HeaderBar.vue`, `SearchConsole.vue`)
- **Files**: `frontend/src/components/HeaderBar.vue`, `frontend/src/components/SearchConsole.vue`
- **HeaderBar**: Terminal brand badge (`v2.4-PROBE`), real-time UTC Zulu clock interval ticker, and live in-memory Redis telemetry status pill (`PULSE-DOT`, indexed entity counter).
- **SearchConsole**: Cybernetic search form with domain input, Lucide icons, loading radar-sweep beam animation, error boundaries, and 1-click interactive corporate target chips (`Spotify`, `Stripe`, `Linear`, `Netflix`, `OpenAI`) with dynamic active glowing borders. Built and verified production bundle in 787ms.

### 3.11 Quadrant 1 — Brand Identity & Color Spectrum Card (`BrandCard.vue`)
- **File**: `frontend/src/components/BrandCard.vue`
- **Identity Presentation**: Displays high-resolution vector logo with fallback monogram, verified entity badge, sanitized domain link with external icon, and company elevator description.
- **Interactive Color Swatches**: Interactive primary and secondary color palette swatches with live click-to-copy hex functionality (`#10B981`, `#6366F1`, etc.) and temporary checkmark feedback.
- **Verified Footprint**: Renders verified social network chips (Website, Twitter/X, GitHub, LinkedIn). Built and verified clean production bundle in 935ms.

---

## 4. Discovered Quirks, Nuances & Solutions

1. **Python 3.14 Development Preview Incompatibility (Windows):**
   - *Problem*: The user's default `python` alias routed to an unreleased Python 3.14 MinGW development binary where prebuilt wheels for `pydantic-core` (Rust) did not exist, causing `pip install` to fail.
   - *Solution*: Recreated virtual environment targeting installed official release `C:\Users\somet\AppData\Local\Programs\Python\Python312\python.exe` (Python 3.12.7).
2. **Pydantic V2 Configuration Deprecation:**
   - *Problem*: Legacy `class Config:` syntax emitted `PydanticDeprecatedSince20` warnings.
   - *Solution*: Migrated to Pydantic v2 `model_config = {"env_file": ".env", "extra": "ignore"}`.
3. **Python 3.12 `datetime.datetime.utcnow()` Deprecation:**
   - *Problem*: `utcnow()` is deprecated in Python 3.12.
   - *Solution*: Switched to timezone-aware UTC datetime: `datetime.datetime.now(datetime.timezone.utc)`.
4. **PowerShell Statement Chaining:**
   - *Problem*: Bash-style `&&` operator fails in standard Windows PowerShell.
   - *Solution*: Chained commands using `;` (semicolon).
5. **Redis Offline Connection Latency Spike:**
   - *Problem*: When Redis is not running locally during tests, `aioredis` was attempting a fresh socket connection on every single request with a 2-second timeout, causing cache-hit response times to spike to ~2000ms.
   - *Solution*: Implemented a 15-second failure backoff (`REDIS_RETRY_COOLDOWN_SECONDS`) and reduced connection timeout to 300ms. Once a connection fails, the client uses the high-speed in-memory RAM fallback immediately, keeping response times under 1ms.

---

## 5. Active Engineering Roadmap

- [x] **Step 1.1**: Configuration & Third-Party API Client Setup.
- [x] **Step 1.2**: Unified Pydantic Contracts & Schemas.
- [x] **Step 1.3**: Multi-Stream Async Aggregation Service.
- [x] **Step 1.4**: High-Speed Redis Caching & Rate-Limiting Layer.
- [x] **Step 1.5**: REST API Endpoint `/api/v1/intel/{domain}` & Automated Pytest Suite.
- [x] **Step 2.1**: Cybernetic Chameleon CSS Design System (`tokens.css`).
- [x] **Step 2.2**: Reactive Intel Store & Brand Preset Engine (`useIntelStore.js`).
- [x] **Step 3.1**: Top Navigation Bar & Command Search Console (`HeaderBar.vue`, `SearchConsole.vue`).
- [x] **Step 3.2**: Quadrant 1 — Brand Identity & Color Spectrum Card (`BrandCard.vue`).
- [ ] **Step 3.3**: Quadrant 2 — Cloud & Edge Network Telemetry Card (`NetworkCard.vue`).
- [ ] **Step 3.4**: Quadrant 3 — Performance & Core Vitals Radar (`VitalsCard.vue`).
- [ ] **Step 3.5**: Quadrant 4 — AI Strategic Teardown & Competitor Radar (`AiDossierCard.vue`).
- [ ] **Step 4.1**: Master Viewport Assembly & Ambient Aura Background (`App.vue`).
- [ ] **Step 4.2**: Interactive Gadgets & Telemetry Status Bar (`StatusBar.vue`).
- [ ] **Step 4.3**: End-to-End Flight-Check & Docker Verification.
- [ ] **Step 4.4**: Documentation Finalization & GitHub Push.
