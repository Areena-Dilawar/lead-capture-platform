# Embeddable Widget & Lead-Capture Platform

A multi-tenant backend platform for creating embeddable lead-capture widgets and collecting visitor submissions from external websites.

---

## Overview

Customers can create customizable widgets and embed them on their external websites using a lightweight JavaScript snippet tag.

The platform handles:
- **Widget Management**: CRUD operations for embeddable widgets with tenant isolation.
- **Cross-Origin Widget Delivery**: Serving versioned JavaScript snippets and dynamic widget configurations.
- **Visitor Submission Validation**: Strict payload validation against widget schema.
- **Abuse Prevention**: IP-based rate limiting and spam honeypot/content filtering.
- **Geo Enrichment**: IP-to-location resolution with automated fallback providers.
- **Persistence & Isolation**: Safe multi-tenant data storage in PostgreSQL.
- **Reliable Side Effects**: Asynchronous background notification dispatch.
- **Dashboard & Analytics**: Authenticated metrics, geo breakdown, and submission logs.

---

## Tech Stack

- **Language & Runtime**: Python 3.11+
- **Framework**: FastAPI
- **Database & ORM**: PostgreSQL, SQLAlchemy, Alembic
- **Validation & Serialization**: Pydantic v2
- **Containerization**: Docker & Docker Compose
- **External Services**:
  - `ip-api.com` (Primary Geo Provider)
  - `ipapi.co` (Fallback Geo Provider)
  - Console / Mailpit (Notification side effects)

---

## Core Architecture

### Owner Workflow

```text
Authenticated Owner
        │
        ▼
   FastAPI API
        │
        ▼
 Tenant Isolation (tenant_id scoping)
        │
        ▼
  Service Layer
        │
        ▼
Repository Layer
        │
        ▼
    PostgreSQL
```

### Visitor Submission Flow

```text
Visitor on External Site
        │
        ▼
  CORS + Schema Validation
        │
        ▼
    Rate Limiting
        │
        ▼
   Spam Protection
        │
        ▼
Geo Enrichment (Primary -> Fallback)
        │
        ▼
 PostgreSQL Persistence
        │
        ▼
Background Notification Job
```

---

## Reliability & Resilience

- **Persistence First**: Submissions are durably stored in PostgreSQL before triggering any external or non-critical side effects.
- **Geo-Enrichment Fallback**: Dual-provider chain (`ip-api.com` &rarr; `ipapi.co`). If both fail, submission proceeds without geo metadata rather than dropping lead data.
- **Fault-Tolerant Notifications**: Email / webhook notification failures never block or invalidate a successful lead capture.
- **Idempotency**: Public submission endpoints support idempotency keys to prevent duplicate leads from network retries.

---

## Project Status

- **Phase 1**: Design and architecture complete.
- **Phase 2+**: Incremental implementation following the backend capstone build phases.

---

## Explicit Non-Goals

- Building a drag-and-drop visual form builder or heavy UI customizer.
- Complex client-side rendering frameworks for the widget. The widget UI remains intentionally lightweight and vanilla.
- The primary focus is backend architecture, security, cross-origin embedding, tenant isolation, and high-reliability data capture.

---

## Documentation

For full architectural specifications, database schema, index definitions, and API route mappings, see [DESIGN.md](DESIGN.md).