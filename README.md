# 🔮 PRISM // OS — Corporate & Infrastructure Intelligence Terminal

> **Autonomous cybernetic intelligence terminal that analyzes any global company, domain, or product in real time across four concurrent data streams with a dynamic chameleon theme engine.**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python 3.12](https://img.shields.io/badge/Python-3.12+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Vue 3](https://img.shields.io/badge/Vue-3.5+-4FC08D.svg?logo=vuedotjs&logoColor=white)](https://vuejs.org/)
[![Redis](https://img.shields.io/badge/Redis-7.0+-DC382D.svg?logo=redis&logoColor=white)](https://redis.io/)
[![Vite](https://img.shields.io/badge/Vite-8.3+-646CFF.svg?logo=vite&logoColor=white)](https://vitejs.dev/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/Tests-10%2F10%20Passing-brightgreen.svg)](https://pytest.org)

---

## ⚡ The Concept & Experience

**PRISM // OS** is an obsidian-glassmorphic intelligence command center (styled after Palantir and high-density cyberpunk terminals). Enter any domain (e.g. `spotify.com`, `stripe.com`, `linear.app`, `netflix.com`, `openai.com`) or click a pre-seeded target chip, and the terminal concurrently ingests 4 tactical data streams:

```text
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │  PRISM // OS  [v2.4-PROBE]                  11:42:09 UTC ZULU      ● REDIS: 5 ENTITIES │
 ├────────────────────────────────────────────────────────────────────────────────────────┤
 │  [ TARGET DOMAIN: stripe.com                        ]  [ SCAN TARGET ]                 │
 │  Quick Recon: [ Spotify ]  [ Stripe ]  [ Linear ]  [ Netflix ]  [ OpenAI ]             │
 ├───────────────────────────────────────────┬────────────────────────────────────────────┤
 │ 🪪 QUADRANT 1: BRAND IDENTITY             │ 🌐 QUADRANT 2: CLOUD & NETWORK TELEMETRY   │
 │   • High-Res Vector Brand Logo & Monogram │   • Cloud Provider Hero (AWS / Cloudflare) │
 │   • Corporate Bio & Verified Entity Badge │   • TTFB Latency Speedometer (42ms)        │
 │   • Interactive Click-to-Copy Hex Palette │   • Direct Copyable IPv4 & TLSv1.3 Edge    │
 │   • Verified Social Network Footprint     │   • SSL Certificate 90-Day Renewal Ring    │
 ├───────────────────────────────────────────┼────────────────────────────────────────────┤
 │ ⚡ QUADRANT 3: WEB VITALS & LIGHTHOUSE    │ 🧠 QUADRANT 4: AI STRATEGIC TEARDOWN       │
 │   • Animated SVG Radial Dial: Performance │   • Unfiltered Reality Truth Quote         │
 │   • Animated SVG Radial Dial: Access      │   • Competitive Moat vs Existential Threat │
 │   • Animated SVG Radial Dial: SEO Audit   │   • Interactive 1-Click Competitor Prober  │
 │   • First Contentful Paint & Speed Index  │   • Inferred Architecture Tech Stack Tags  │
 ├───────────────────────────────────────────┴────────────────────────────────────────────┤
 │  ● BUFFER: 0.4ms (CACHE HIT)  •  PROCESSING: 0.8ms  •  [ 📋 EXPORT EXECUTIVE DOSSIER ] │
 └────────────────────────────────────────────────────────────────────────────────────────┘
```

### 🦎 Dynamic Chameleon Theme Engine
The frontend features a reactive CSS token architecture with zero CSS framework overhead. When a company is evaluated, `applyBrandTheme()` dynamically recalculates primary and secondary RGB color channels and applies custom properties (`--brand-primary`, `--brand-glow`, `--brand-surface`) across a smooth `0.8s cubic-bezier(0.16, 1, 0.3, 1)` transition, adapting every card border, glowing aura, button, and radial dial in real time.

---

## 🎯 High-Value Engineering Skills Demonstrated

Built to demonstrate production-grade distributed backend architecture and modern reactive frontend design:

| Architectural Dimension | Traditional Web Stack | PRISM // OS Implementation |
| :--- | :--- | :--- |
| **Backend Language** | Node.js / PHP | **Python 3.12+ (Asynchronous IO)** |
| **API Framework** | Express / Next.js API Routes | **FastAPI** with Pydantic v2 strict schema contracts |
| **Data Ingestion** | Sequential blocking requests | **Parallel `asyncio.gather()`** with non-blocking timeouts |
| **Network Probing** | Generic HTTP GET | Direct **Socket SSL certificate parsing**, DNS resolution & TLS negotiation |
| **In-Memory Caching** | Direct DB / filesystem | **Redis** distributed cache (24h TTL) with sub-millisecond RAM fallback |
| **API Abuse Prevention**| Unprotected endpoints | **Token-bucket rate limiting** (`SlowAPI`, 30 req/min) |
| **Frontend Framework** | Generic React / Tailwind | **Vue 3 Composition API** + custom CSS design token system |
| **Containerization** | Manual local host | Multi-container **Docker Compose** orchestration |
| **Automated Testing** | Manual Postman checks | **Pytest + HTTPX** integration suite with 100% route coverage |

---

## 🏗️ Architecture & Data Pipeline

```mermaid
graph TD
    Client[Browser / Vue 3 Terminal] -->|GET /api/v1/intel/{domain}| Gateway[FastAPI Router]
    Gateway --> Limiter{SlowAPI 30/min}
    Limiter -->|Check Cache| Redis[(Redis Buffer / RAM Fallback)]
    
    Redis -->|Cache Hit (Sub-ms)| Client
    Redis -->|Cache Miss| Aggregator[Async Intelligence Service]
    
    subgraph Multi-Stream Ingestion [asyncio.gather]
        Aggregator --> Stream1[Brand & Vector Logo Stream]
        Aggregator --> Stream2[Socket SSL & Cloud Telemetry]
        Aggregator --> Stream3[PageSpeed & Lighthouse Vitals]
        Aggregator --> Stream4[LLM Strategic AI Analysis]
    end
    
    Stream1 --> Assembler[Unified Dossier Assembler]
    Stream2 --> Assembler
    Stream3 --> Assembler
    Stream4 --> Assembler
    
    Assembler -->|Store with 24h TTL| Redis
    Assembler -->|JSON Response| Client
```

---

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)
Make sure Docker Desktop is running, then run:

```bash
docker compose up --build
```

- **Frontend Terminal**: `http://localhost:5173` (or Vite dev port)
- **Backend API**: `http://localhost:8000`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **Redis Cache**: `localhost:6379`

---

### Option 2: Local Development Without Docker

#### 1. Backend (FastAPI):
```bash
cd backend

# Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend dev server
uvicorn app.main:app --reload --port 8000
```

#### 2. Frontend (Vue 3 + Vite):
```bash
cd frontend

# Install Node dependencies
npm install

# Start Vite dev server
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 🧪 Automated Test Suite

PRISM // OS includes automated tests covering health checks, Pydantic contracts, fallback resilience, live multi-stream aggregation, and Redis caching:

```bash
cd backend
pytest tests/ -v
```

### Test Output:
```text
tests/test_health.py::test_health_check_endpoint PASSED                  [ 10%]
tests/test_intel_endpoint.py::test_get_presets_endpoint PASSED           [ 20%]
tests/test_intel_endpoint.py::test_cache_telemetry_endpoint PASSED       [ 30%]
tests/test_intel_endpoint.py::test_intel_endpoint_cache_miss_and_hit PASSED [ 40%]
tests/test_intel_endpoint.py::test_intel_invalid_domain PASSED           [ 50%]
tests/test_intelligence_service.py::test_sanitize_domain PASSED          [ 60%]
tests/test_intelligence_service.py::test_aggregate_curated_company_dossier PASSED [ 70%]
tests/test_redis_client.py::test_set_and_get_cached_dossier PASSED       [ 80%]
tests/test_redis_client.py::test_cache_stats PASSED                      [ 90%]
tests/test_schemas.py::test_prism_dossier_contract_serialization PASSED  [100%]

============================= 10 passed in 5.20s ==============================
```

Frontend production build verification:
```bash
cd frontend
npm run build
# ✓ 1743 modules transformed, dist/ built in 1.33s
```

---

## 📁 Repository Structure

```text
├── backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   └── router.py                 # REST routes (/intel, /cache/stats, /presets)
│   │   ├── core/
│   │   │   ├── config.py                 # Pydantic BaseSettings environment config
│   │   │   └── redis_client.py           # Redis buffer pool with memory fallback & backoff
│   │   ├── schemas/
│   │   │   └── dossier.py                # Pydantic v2 data models for 4 pillars
│   │   ├── services/
│   │   │   ├── http_client.py            # Shared async HTTPX client & domain sanitizer
│   │   │   └── intelligence_service.py   # Multi-stream parallel aggregation pipeline
│   │   └── main.py                       # FastAPI entrypoint, CORS, SlowAPI rate limiter
│   ├── tests/                            # 10 integration & unit tests
│   ├── requirements.txt                  # Python dependencies
│   ├── Dockerfile                        # Backend container specification
│   └── .env.example                      # API key configuration template
├── frontend/
│   ├── src/
│   │   ├── assets/styles/
│   │   │   └── tokens.css                # Obsidian glassmorphic & chameleon token system
│   │   ├── components/
│   │   │   ├── HeaderBar.vue             # Zulu UTC clock, terminal badge, Redis telemetry
│   │   │   ├── SearchConsole.vue         # Radar sweep input bar & preset target chips
│   │   │   ├── BrandCard.vue             # Q1: Vector logo, bio, copyable hex swatches
│   │   │   ├── NetworkCard.vue           # Q2: Cloud hero, TTFB latency speedometer, SSL
│   │   │   ├── VitalsCard.vue            # Q3: SVG radial score rings (Perf, A11y, SEO)
│   │   │   ├── AiDossierCard.vue         # Q4: Brutal truth, moat/vulnerability, competitor recon
│   │   │   └── StatusBar.vue             # Buffer status & 1-click Markdown dossier export
│   │   ├── stores/
│   │   │   └── useIntelStore.js          # Centralized reactive store & brand theme mutator
│   │   ├── App.vue                       # Master viewport assembly & ambient glowing auras
│   │   └── main.js                       # Vue application mount
│   ├── package.json                      # Frontend scripts & dependencies
│   ├── vite.config.js                    # Vite build config with backend proxy
│   └── index.html                        # Google Fonts & terminal root
├── docker-compose.yml                    # Multi-container orchestration (FastAPI + Redis)
├── TECHNICAL_ANALYSIS.md                 # Living engineering logbook & architecture memory
└── README.md
```

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
