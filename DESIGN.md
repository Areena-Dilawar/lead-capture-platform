# FlyRank Embeddable Widget & Lead-Capture Platform

## 1. Problem

Build a multi-tenant lead-capture platform that allows customers to create embeddable widgets and install them on external websites with a single script tag.

The platform must safely receive visitor submissions, validate them, protect the endpoint from abuse, enrich submissions with location data, persist them, and expose them through an authenticated owner dashboard.

## 2. Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker
- Pydantic

External services:
- **ip-api.com** — primary geo provider
- **ipapi.co** — fallback geo provider
- **Console / Mailpit** — notification side effect

## 3. Data Model

### Tenant
- `id`
- `name`
- `created_at`

### User
- `id`
- `tenant_id`
- `email`
- `password_hash`
- `created_at`

### Widget
- `id`
- `tenant_id`
- `type`
- `title`
- `description`
- `form_fields`
- `button_text`
- `display_options`
- `version`
- `is_active`
- `created_at`
- `updated_at`

### Submission
- `id`
- `tenant_id`
- `widget_id`
- `data`
- `ip_address`
- `country`
- `city`
- `user_agent`
- `is_spam`
- `created_at`

Important indexes:
- `widgets.tenant_id`
- `submissions.tenant_id`
- `submissions.widget_id`
- `submissions.created_at`

> Every tenant-owned query is scoped by `tenant_id`.

## 4. API Surface

### Authentication
```http
POST /auth/register
POST /auth/login
GET  /auth/me
```

### Widget Management
```http
POST   /api/widgets
GET    /api/widgets
GET    /api/widgets/{widget_id}
PATCH  /api/widgets/{widget_id}
DELETE /api/widgets/{widget_id}
GET    /api/widgets/{widget_id}/embed
```

### Public Widget Delivery
```http
GET /widget.js
GET /public/widgets/{widget_id}/config
```

### Public Submission
```http
OPTIONS /public/widgets/{widget_id}/submissions
POST    /public/widgets/{widget_id}/submissions
```

### Dashboard
```http
GET /api/submissions
GET /api/submissions/{submission_id}
GET /api/analytics/overview
GET /api/analytics/widgets/{widget_id}
GET /api/analytics/geo
```

## 5. Architecture

### Owner Workflow
```text
Authenticated owner
    ↓
Widget Management API
    ↓
Tenant-isolated database access
    ↓
Embed snippet
```

### Customer Website
```text
<script>
    ↓
Versioned widget JavaScript
    ↓
Public widget configuration
    ↓
Render widget
```

### Visitor Submission Flow
```text
Form submission
    ↓
CORS + validation
    ↓
Rate limiting
    ↓
Spam protection
    ↓
Geo enrichment
    ↓
PostgreSQL
    ↓
Background notification job
```

### Geo Enrichment Fallback
```text
Provider A
    ↓ failure
Provider B
    ↓ failure
Store submission without geo data
```

> **Note:** Notification failure never prevents a successful submission.

## 6. Layering

```text
Routes
    ↓
Services
    ↓
Repositories
    ↓
PostgreSQL
```

Supporting services handle:
- Rate limiting
- Spam detection
- Geo enrichment
- Notifications

## 7. Tenant Isolation

All authenticated access to widgets, submissions, and analytics is scoped to the authenticated user's `tenant_id`.

A tenant must never be able to read or modify another tenant's data.

## 8. Reliability

- The primary submission path stores the lead before triggering non-critical notification work.
- Geo providers use a fallback chain.
- Notification work runs separately and may retry after failure.
- Public submission requests support idempotency through an `Idempotency-Key` header.

## 9. Explicit Non-Goal

This project will not build a production-grade drag-and-drop form builder or full visual widget customization system.

The widget UI will remain intentionally minimal. The focus is the backend platform, cross-origin embedding, validation, abuse protection, enrichment, persistence, tenant isolation, and reliability.