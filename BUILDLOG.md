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

Phase 1 design is complete.

Implementation has not started yet.