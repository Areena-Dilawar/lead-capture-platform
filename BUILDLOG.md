# Build Log

## Phase 1 - Design & Architecture

### Completed

- Created the project repository.
- Created the initial architecture and design document ([DESIGN.md](DESIGN.md)).
- Defined the multi-tenant data model.
- Defined the authenticated and public API surface.
- Defined the public visitor submission flow.
- Defined tenant isolation requirements.
- Defined geo-enrichment fallback behavior.
- Defined background notification behavior.
- Defined the explicit non-goal for the project.
- Created the initial [README.md](README.md).

### Architecture Decisions

- FastAPI will be used as the backend framework.
- PostgreSQL will be the primary database.
- SQLAlchemy will handle database access.
- Alembic will manage database migrations.
- Public submissions will be persisted before non-critical notification work.
- Geo enrichment will use a primary provider with a fallback provider.
- Tenant-owned resources will always be scoped by `tenant_id`.

### Current Status

- **Phase 1 (Design)**: Complete (Gate passed: `DESIGN.md` committed).
- **Phase 2 (The Hardened Submission Path)**: In Progress (Database foundation complete; API endpoints and submission pipeline next).

---

## Phase 2 — The Hardened Submission Path (In Progress)

### Completed (Database & Model Foundation)
- Configured PostgreSQL 16 using Docker Compose.
- Connected SQLAlchemy to PostgreSQL using environment-based configuration.
- Initialized Alembic for database migrations.
- Created and applied migrations for all four core models:
  - `Tenant`
  - `User`
  - `Widget`
  - `Submission`
- Verified that all four application tables and the `alembic_version` table exist in PostgreSQL.
- Added Git ignore rules to protect local environment variables and the Python virtual environment.

### Completed (Health API)
- Added a dedicated health route in `app/api/routes/health.py`.
- Registered the health router in `app/main.py`.
- Tested `GET /health` locally and confirmed it returns `{"status": "ok"}`.
- Confirmed the FastAPI application exposes its interactive documentation at `/docs`.

### In Progress / Next Steps
- Implement authentication and tenant-scoped access so each tenant can access only its own resources.
- Build tenant-scoped widget management CRUD APIs.
- Build the public submission endpoint (`POST /public/widgets/{id}/submissions`) with:
  - Cross-Origin Resource Sharing (CORS) & preflight handling.
  - Boundary payload validation (clean 4xx JSON errors, never 500).
  - Rate limiting & honeypot spam protection.
  - Geo-enrichment fallback chain (`ip-api.com` → `ipapi.co`).
  - Safe background side effect (notification/email).
- **Gate Objective**: Verify a cross-origin `curl` stores an enriched row.

---

## AI Collaboration & Debugging Log

### Where AI Helped
- Scaffolding the initial system architecture, design specification ([DESIGN.md](DESIGN.md)), and data flow sketches.
- Generating SQLAlchemy 2.0 declarative models with modern type annotations (`Mapped`, `mapped_column`) and Postgres-specific types (`JSONB`, `INET`).
- Structuring Alembic migrations and Docker Compose configuration.

### Where AI / Defaults Were Wrong & What Was Changed
- **Alembic Driver Resolution Error**:
  - *Issue*: Running `alembic current` threw `ModuleNotFoundError: No module named 'psycopg'` because SQLAlchemy 2.0 defaults `postgresql://` to `psycopg` (v3), whereas the project virtual environment uses `psycopg2-binary`.
  - *Fix*: Updated `migrations/env.py` to rewrite `postgresql://` to `postgresql+psycopg2://` before passing it to `engine_from_config`, aligning Alembic with the runtime configuration in `app/database.py`.
- **Phase Definition Alignment**:
  - *Issue*: Initially labeled the completed database setup as "Phase 2 Complete", which clashed with the official Capstone rubric where Phase 2 requires the full hardened submission path and a passing cross-origin submission gate.
  - *Fix*: Corrected the status in this log to accurately reflect Phase 2 as *In Progress*, clearly separating the database foundation from the upcoming submission pipeline.

### Engineering Ownership
- Manually inspected and verified the database tables (`tenants`, `users`, `widgets`, `submissions`, `alembic_version`) directly inside PostgreSQL via `psql` and SQLAlchemy inspector.
- Tested the `GET /health` endpoint locally and verified the successful JSON response.