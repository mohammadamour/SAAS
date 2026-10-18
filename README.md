# PulseEngine — Full-Stack Telemetry & Microservices SaaS

A modern, high-performance SaaS architecture built with **Python (FastAPI)**, **Redis**, and a reactive **Vue 3** frontend, orchestrated with **Docker Compose**.

Designed as a low-pressure "vibe coded" portfolio piece that demonstrates production-grade systems architecture, distributed in-memory caching, rate limiting, and edge-ready API design.

---

## 🎯 Background & Motivation

As a developer with experience in **Node.js, React, Next.js, Laravel, PostgreSQL, MySQL, and TypeScript**, the goal of this project is to branch into high-demand, enterprise-standard technologies that immediately stand out to senior technical recruiters and engineering leads:

| Dimension | Previous Stack | New Marketable Skills Demonstrated |
| :--- | :--- | :--- |
| **Backend Language** | Node.js / PHP (Laravel) | **Python 3.12+ (Async)** |
| **API Framework** | Express / Next API Routes | **FastAPI** (Pydantic v2 data validation, OpenAPI/Swagger docs) |
| **In-Memory & Caching** | Direct DB queries | **Redis** (distributed caching with TTL, token-bucket rate limiting) |
| **Frontend Framework** | React / Next.js | **Vue 3** (Composition API, Vite, modern reactive primitives) |
| **Infrastructure** | Manual local servers | **Docker & Docker Compose** (multi-container orchestration) |
| **API Testing** | Manual / Jest | **Pytest + HTTPX** (Async integration testing) |

---

## 🏗️ Architecture Overview

```text
[ Browser / Vue 3 Landing Page ]
         |
         |  (Interactive Widget: e.g. "Live Endpoint Inspection")
         v
[ FastAPI REST Gateway ]  <---> [ SlowAPI (Redis Rate Limiter) ]
         |
    +----+----+
    |         |
    v         v
[ Redis Cache ]  [ Async HTTPX Prober ]
(TTL: 60s cache)       (Measures DNS/TTFB & SSL Telemetry)
```

### Key Engineering Features:
1. **Interactive Real-Time Telemetry Engine**: Live URL probe measuring status, latency (TTFB), SSL status, and server headers.
2. **Distributed Redis Caching**: Sub-millisecond response for repeated requests with automatic 60-second TTL invalidation.
3. **Token-Bucket Rate Limiting**: Built with `SlowAPI` backed by Redis to safeguard endpoints against abuse.
4. **Interactive Swagger & OpenAPI Documentation**: Live schema testing at `/docs` and `/redoc`.
5. **Containerized from Day 1**: Spin up the entire infrastructure with a single `docker compose up` command.

---

## 🚀 Quick Start

### Option 1: Running with Docker (Recommended)
Make sure Docker Desktop is running, then run:

```bash
docker compose up --build
```
* **Backend API**: `http://localhost:8000`
* **Interactive Swagger Docs**: `http://localhost:8000/docs`
* **Redis**: `localhost:6379`

### Option 2: Running Locally Without Docker

#### Backend:
```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### Frontend:
```bash
cd frontend
npm install
npm run dev
```

---

## 🧪 Running Automated Tests

```bash
cd backend
pytest -v
```

---

## 📁 Repository Layout

```text
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py         # Pydantic BaseSettings environment config
│   │   │   └── redis_client.py   # Async Redis connection pool manager
│   │   └── main.py               # FastAPI app, SlowAPI limiter, telemetry routes
│   ├── tests/
│   │   └── test_health.py        # Async API tests with Pytest + HTTPX
│   ├── requirements.txt          # Python dependencies
│   ├── Dockerfile                # Production-ready Python container image
│   └── .env.example              # Environment variables template
├── frontend/                     # Vue 3 + Vite frontend application
├── docker-compose.yml            # Multi-container orchestration (FastAPI + Redis)
├── .gitignore
└── README.md
```
