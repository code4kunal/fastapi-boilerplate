# Siteops Platform

Lean FastAPI service using layered architecture: **api** → **application** → **domain** → **infrastructure**, with **core** shared utilities.

## Quick start

```bash
cp .env.example .env
uv sync --all-extras
make migrate   # after DB is up
make dev
```

- OpenAPI: http://localhost:8000/docs
- Health: http://localhost:8000/api/v1/health/live
- Readiness: http://localhost:8000/api/v1/health/ready
- Metrics: http://localhost:8000/metrics

## Layout

- `src/siteops_platform/api` — routers, schemas, versioning
- `src/siteops_platform/application` — use cases, DTOs
- `src/siteops_platform/domain` — entities, repository protocols
- `src/siteops_platform/infrastructure` — ORM, repositories, UoW
- `src/siteops_platform/core` — config, logging, errors, middleware
- `src/siteops_platform/modules` — feature plugins (`service_cli add-module …`)

## Tests

```bash
make test        # unit + API (fast)
make test-cov    # full with coverage threshold
```

## Roadmap (enterprise evolution)

- Tenant-aware session factory and routing in `infrastructure.persistence`
- Optional Celery/RQ via `modules/jobs`
- Secrets manager adapter in `core.config`
- Grafana dashboards from `/metrics`
- Stricter auth (OAuth2 providers, token revocation store)