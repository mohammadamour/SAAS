# 🔮 Agent Guidelines: PRISM // OS

Welcome! You are working on **PRISM // OS** (Autonomous Corporate & Infrastructure Intelligence Terminal), a high-density, futuristic cybernetic intelligence terminal that analyzes any global company, domain, or product in real-time.

---

## 🎯 1. Project Overview & Architecture Context

- **Product Concept**: A Palantir/Cyberpunk-style intelligence command center that concurrently ingests 4 data streams for any entered domain:
  1. **Brand & Identity**: Vector logo, brand description, official social footprint, and primary/secondary hex color spectrum.
  2. **Global Cloud & Network Telemetry**: Cloud hosting provider (AWS, Cloudflare, GCP, Fastly), DNS IP, TTFB latency, SSL certificate validity & countdown.
  3. **Web Performance & Core Vitals**: Lighthouse audit dials (Performance, Accessibility, SEO) and speed metrics.
  4. **AI Strategic Intelligence**: Unfiltered 1-sentence truth, competitive moat, strategic vulnerabilities, top 3 competitors, and inferred tech stack.
- **Dynamic Chameleon Theming**: The entire frontend dynamically adapts its CSS custom properties (`--brand-primary`, `--brand-glow`, `--brand-surface`) to match the primary brand color of whatever company is searched.
- **Technology Stack**:
  - **Backend**: Python 3.12+ (FastAPI, Pydantic v2, HTTPX, SlowAPI rate limiting, Pytest).
  - **In-Memory Buffer / Caching**: Redis (24-hour TTL for full company dossiers, sub-millisecond cache hits).
  - **Frontend**: Vue 3 (Composition API, Vite, Lucide Icons, Pure CSS Tokens, zero Tailwind).
  - **Orchestration**: Docker & Docker Compose (`docker compose up --build`).

---

## 🧠 2. Core Operational Rules for Agents

### ⚡ Rule 1: Autonomous Git Commits After Every Feature
- **Always commit working code**: Whenever you complete a feature, bug fix, or master plan sub-step:
  - Run the test suite or verify correctness.
  - Automatically stage and commit the changes using conventional commit style (`git add .` + `git commit -m "feat(...): ..."`).
  - Provide a clean `git push origin main` command for the user to push whenever they choose.

### 🧩 Rule 2: Atomic Execution with "Proceed" Checkpoints
- Follow the master roadmap in `prism_os_master_plan.md`.
- Keep each step atomic, focused, and tested so execution never gets stuck in long loops.
- Update the master plan checkboxes after completing each milestone.

### 🎨 Rule 3: Rich, Futuristic Cybernetic Aesthetics
- This application is built for maximum visual impact and fun.
- Maintain the obsidian glassmorphism aesthetic (`#05070A` void, frosted card surfaces, hairline translucent borders, ambient glowing backdrops).
- Ensure smooth CSS transitions (`0.8s cubic-bezier(0.16, 1, 0.3, 1)`) when switching brand themes.

### 📖 Rule 4: Continuous Technical Analysis Maintenance
- **Keep `TECHNICAL_ANALYSIS.md` continuously updated**:
  - After completing any feature, step, or pipeline change, expand `TECHNICAL_ANALYSIS.md` to document what was built, architectural decisions, and any discovered quirks.
  - This file serves as the living technical memory and engineering backlog for the repository.

---

## 📁 Key File Locations

- `backend/app/main.py`: FastAPI entrypoint, CORS, rate limiting.
- `backend/app/schemas/dossier.py`: Pydantic data contracts for all 4 pillars.
- `backend/app/services/http_client.py`: Shared async HTTP client & domain sanitizer.
- `backend/app/services/intelligence_service.py`: Multi-stream async aggregator.
- `backend/app/core/redis_client.py`: Redis connection pool & caching layer.
- `frontend/src/assets/styles/tokens.css`: Chameleon CSS variables & cybernetic styles.
- `frontend/src/stores/useIntelStore.js`: Reactive company state & theme controller.
