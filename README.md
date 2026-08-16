# Insurance Recommendation Agent (README)

> Portfolio adaptation: This fork preserves the original production-style architecture and broadens the insurance demo to include modern, digital-first recommendation flows for home, auto, and pet insurance. It keeps the Google ADK → MCP Toolbox → SQL/RAG → FastAPI design while adding UI and evaluation improvements for a portfolio demo.

This repository provides a working example of an insurance recommendation AI Agent built on top of Google ADK. The system integrates FastAPI, Next.js, MCP Toolbox (controlled tools), PostgreSQL with pgvector, and Geminic/Vertex AI models. It demonstrates product search, FAQ semantic retrieval, session-aware memory, audit logging, PII protection, and optional multimodal live interactions.

Primary goals of this README:

1. Explain what the project does and the problems it solves.
2. Show how to run the system locally (quickstart).
3. Point to documentation for testing, evaluation, and deployment.

## Key Features

- Google ADK based Agent: understands user needs, asks clarifying questions, queries tools, and produces recommendation responses.
- MCP Toolbox: controlled SQL tools for querying products, recommendation rules, and FAQ knowledge.
- FastAPI backend: REST endpoints, SSE streaming for agent responses, and WebSocket support for live/multimodal sessions.
- Next.js frontend: customer-facing recommendation UI, live mode, and agent state visualization.
- PostgreSQL + pgvector: stores products, recommendation rules, FAQ embeddings, sessions, and audit logs.
- Multimodal Live Agent: optional real-time voice/video and interactive session support via WebSocket.
- Security & compliance: JWT authentication, PII redaction, public-state filtering, and audit hash chains to support traceability.
- Evaluation-driven development: ADK evalsets verify recommendation quality, safety, and session-aware behavior.
- Cloud-ready deployment: Docker Compose examples plus Cloud Run / Terraform configuration for dev/staging/prod.

## System Architecture

```
Browser / Next.js
    |
    | REST / SSE / WebSocket
    v
FastAPI Backend
    |
    +-- Google ADK Runner
    |      +-- Insurance Agent
    |      +-- Session tools
    |      +-- MCP Toolbox tools
    |
    +-- Services: Session, User, Audit Log, Live Agent
    |
    v
PostgreSQL + pgvector (products, rules, FAQ embeddings, sessions, audits)
```

## Technology Stack

| Area                | Technology                                  |
|---------------------|---------------------------------------------|
| Agent framework     | Google ADK                                  |
| Models              | Gemini / Vertex AI                           |
| Backend API         | FastAPI, Uvicorn                             |
| Frontend            | Next.js 15, React 19, NextAuth.js            |
| Database            | PostgreSQL, pgvector                         |
| Tooling             | MCP Toolbox (controlled DB tools)           |
| Auth                | JWT, NextAuth                                |
| Infra               | Docker Compose, Cloud Run, Terraform         |
| Testing & Eval      | pytest, ADK eval, Locust                     |

## Repository Layout

```
.
├── app/               # Backend agent, FastAPI app, tools and services
├── db/                # Schema, seeds, and MCP Toolbox tool definitions
├── frontend/          # Next.js application and UI components
├── docs/              # Architecture and design docs
├── deployment/        # Terraform and deployment manifests
├── scripts/           # Setup, ingestion and helper scripts
├── tests/             # Unit, integration, eval and load tests
├── docker-compose.yml
├── Makefile
├── pyproject.toml
└── .env.example
```

## Prerequisites

Local development requires:

- Python 3.12
- Node.js 20+ and npm
- Docker & Docker Compose (for the full local demo)
- Google Cloud credentials when using Vertex AI, embeddings, or cloud Toolbox

Copy the environment template and update values before running:

```bash
cp .env.example .env
# Edit .env to add credentials and overrides
```

## Quick Start

There are two main ways to run the project locally: the full Docker Compose demo (recommended for a complete environment), or running services independently for development.

### Option A — Full demo with Docker Compose

This brings up PostgreSQL, Toolbox, backend, and frontend together:

```bash
cp .env.example .env
# Fill required credentials in .env
make up-build
```

Open in your browser:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8080
- Health check: http://localhost:8080/healthz

Stop services:

```bash
make down
```

View logs:

```bash
make logs
```

### Option B — Run services separately (development)

Install dependencies and start database and toolbox when you only develop one component:

```bash
cp .env.example .env
make install-all
make db-up
make db-seed
make db-ingest
```

Start backend:

```bash
make run-fastapi
```

In another terminal, start the frontend:

```bash
make ui-install
make ui-dev
```

Then access the UI at http://localhost:3000 and the API at http://localhost:8080.

## Environment Variables

The application reads configuration from environment variables. Use `.env.example` as a template. Key variables include:

| Variable                      | Purpose / Notes |
|-------------------------------|-----------------|
| GOOGLE_GENAI_USE_VERTEXAI     | Set `1` to use Vertex AI. |
| GOOGLE_CLOUD_PROJECT          | Google Cloud project id. |
| GOOGLE_CLOUD_LOCATION         | Google Cloud region, e.g. `us-central1`. |
| GOOGLE_API_KEY                | GenAI API key for local API-key usage. |
| GOOGLE_APPLICATION_CREDENTIALS| Path to service account JSON for Vertex AI. |
| ADK_APP_NAME                  | ADK app name (default: `app`). |
| DATABASE_URL                  | Main database URL (used by services). |
| ADK_SESSION_DB_URI            | Session DB URL for ADK session store. |
| ADK_MEMORY_MODE               | Set `in_memory` to use non-persistent sessions. |
| MODEL_NAME                    | Default text model, e.g. `gemini-2.5-flash`. |
| LIVE_MODEL_NAME               | Multimodal model used by Live mode. |
| TOOLBOX_SERVER_URL            | MCP Toolbox server base URL. |
| JWT_SECRET                    | Backend JWT signing secret (use strong secret in prod). |
| NEXTAUTH_SECRET               | Frontend NextAuth secret (use strong secret in prod). |
| AUDIT_LOG_ENABLED             | Set `1` to enable audit logging. |
| AUDIT_DB_PATH                 | Audit log DB URL. |
| AUDIT_HASH_SALT               | Salt used for audit hashing. |
| PII_REDACTION_ENABLED         | Set `1` to enable PII redaction. |
| ENABLE_CLOUD_TRACING          | Enable Cloud Trace export. |
| ENABLE_CLOUD_LOGGING          | Enable Cloud Logging export. |

## Common Development Commands

Most development tasks are available via the repository Makefile:

| Command | Description |
|---------|-------------|
| `make help` | Show available make targets. |
| `make install` | Create a Python 3.12 venv and install core dependencies. |
| `make install-all` | Install core, dev, eval and GCP deps. |
| `make db-up` | Start local PostgreSQL and MCP Toolbox containers. |
| `make db-setup` | Setup DB, create test users and import FAQ embeddings. |
| `make run-fastapi` | Run the backend on port 8080. |
| `make ui-install` | Install frontend dependencies. |
| `make ui-dev` | Run Next.js dev server on port 3000. |
| `make up` | Start all services with Docker Compose. |
| `make up-build` | Rebuild images and start all services. |
| `make down` | Stop Docker Compose services. |
| `make logs` | Follow Docker Compose logs. |
| `make clean` | Clear Python and pytest caches. |

## API Overview

The backend exposes health, auth, session management, agent run (SSE streaming), and live WebSocket endpoints. Examples:

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/healthz` | Basic health check. |
| GET | `/readyz` | Readiness checks for DB, Toolbox, etc. |
| POST | `/auth/token` | Obtain JWT access token. |
| POST | `/api/agent/run` | Run an agent request; returns SSE-streamed responses. |
| WS | `/api/agent/live/ws/{session_id}` | Start a multimodal live session via WebSocket. |

All user/session/agent endpoints require authentication. The frontend gets a token from `/auth/token` and forwards it on subsequent requests.

## Frontend

The frontend app lives in `frontend/` and is built with Next.js and NextAuth. Typical commands:

```bash
make ui-install
make ui-dev
make ui-build
```

Important directories:

- `frontend/app/` — page routes and API proxy routes
- `frontend/components/` — UI components and views
- `frontend/hooks/` — audio/camera/screen capture and Live Agent hooks
- `frontend/lib/` — proxy, markdown helpers, mock data and session helpers

## Database and MCP Toolbox

Database files are in `db/`:

| File | Purpose |
|------|---------|
| `db/schema.sql` | Schema for products, recommendation rules, FAQ, and vectors. |
| `db/audit_schema.sql` | Audit log schema. |
| `db/seed.sql` | Local development seed data. |
| `db/tools.local.yaml` | MCP Toolbox tool definitions for local dev. |
| `db/tools.cloud.yaml` | Tool definitions for cloud deployment. |

Controlled tools include product search and FAQ search helpers used by the Agent:

- `get_product_detail`, `get_recommendation_rules`, `search_faq`, and domain-specific search tools.

Ingest FAQ embeddings locally with:

```bash
make db-ingest
```

## Security and Compliance

Security features included:

- JWT authentication for API access.
- Ownership checks on protected endpoints.
- PII redaction logic (`app/security/pii.py`).
- Public-state filtering to avoid leaking sensitive session data to the frontend.
- Audit logging via `app/services/audit_log_service.py` with optional audit hash chains.

Important: replace example development secrets before deploying to production. Do not commit `.env` or service account keys.

## Testing

Run the full Python test suite:

```bash
make check
```

Run specific test groups:

```bash
make test-api
make test-security
make test-audit
```

Tests cover unit, integration, API, security, load and evaluation suites under `tests/`.

## Evaluation

ADK evalsets live under `tests/eval/evalsets/`.

Run evaluations:

```bash
make eval
make eval-all
```

Targeted evals:

```bash
make eval-core
make eval-safety
make eval-session-aware
```

## Deployment

Deployment manifests and docs are under `deployment/`.

Common deployment commands:

```bash
make tf-gen-config
make tf-plan ENV_NAME=dev
make tf-apply ENV_NAME=dev
make build-push
make gcp-deploy ENV_NAME=dev
```

Before deploying, ensure the following environment variables are set in your deployment environment:

- `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, `ARTIFACT_REPOSITORY`, `ENV_NAME`, `GITHUB_OWNER`, `GITHUB_REPO_NAME`.

## Troubleshooting / FAQ

- Missing `.env`:

```bash
cp .env.example .env
```

- Backend readiness failures: check `http://localhost:8080/readyz`. Make sure PostgreSQL and MCP Toolbox are running:

```bash
make db-up
make toolbox-logs
```

- Frontend cannot reach backend: verify `NEXT_PUBLIC_API_URL`, `FASTAPI_BASE_URL`, and `NEXTAUTH_URL` in `.env`. Local backend URL: `http://localhost:8080`.

- Authentication failures: ensure test users exist and secrets match between frontend and backend:

```bash
make db-seed
```

- FAQ semantic search not returning results: confirm Google credentials and that FAQ embeddings were ingested (`make db-ingest`).

- Ports used by services (defaults):

```text
Frontend: 3000
Backend: 8080
Toolbox: 5001
PostgreSQL: 5432
```

## Documentation Index

- Backend architecture: `docs/features/backend-agent-design.md`
- Frontend design: `docs/features/frontend.md`
- Live streaming architecture: `docs/features/live-streaming-architecture.md`
- MCP Toolbox & DB tools: `docs/features/mcp-toolboxs.md`
- Observability: `docs/features/obs.md`
- Evaluation: `docs/features/evaluation.md`
- Testing: `docs/features/testing.md`
- Deployment docs: `deployment/docs/README.md`

## Contributing

Before opening a PR, run the checks and tests:

```bash
make check
make test-security
make eval
make lint
```

If you modify Agent behavior, update or add corresponding evalsets under `tests/eval/evalsets/` so recommendation quality and safety rules remain validated.

## License

This project is available for use, modification and redistribution. If you share the repository publicly, please attribute the source.

## Disclaimer

This repository is intended for prototype demonstration, research, and architecture examples only. Recommendation outputs, rules, product descriptions, and premium calculations are fictional or illustrative and must not be used directly for real financial or insurance advice. Actual insurance purchases must rely on official insurer documentation and underwriting results.

## Portfolio Demo Dashboard

The repository contains a production-style Next.js application used as the primary customer-facing demo. A self-contained resume-friendly demo is also included.

Run the full local demo with Docker Compose:

```bash
cp .env.example .env
# Fill in credentials
docker compose up --build
```

Available endpoints:

- Customer dashboard: http://localhost:3000/dashboard
- Main web app: http://localhost:3000
- FastAPI health: http://localhost:8080/healthz

Local seeded demo credentials (development only):

```text
username: testuser
password: password123
```

## Resume-friendly demo (Gradio)

A lightweight one-file demo is available as `portfolio_demo.py`. It is intentionally separate from the Next.js app so it is easy to run and host for a portfolio link.

```bash
pip install gradio
python portfolio_demo.py
```

Open `http://localhost:7860`. To create a temporary public share URL while the process runs:

```bash
GRADIO_SHARE=true python portfolio_demo.py
```

---

If you want, I can also:

- Run a quick spell/format check of this README and commit the change.
- Generate a shorter README for GitHub project landing page.

Updated file: [README.md](README.md)
