# FastAPI Production Template

Production-ready FastAPI starter focused on clean architecture, strict quality gates, and cloud-ready infrastructure baselines.

## Tech stack

- Python 3.14
- FastAPI + Pydantic v2
- SQLAlchemy async + asyncpg
- UV package management
- Ruff + Ty + Pytest
- Docker + Docker Compose
- Terraform (AWS, Azure, GCP)
- GitHub Actions CI

## What is included

- App factory setup with versioned API routes (`/api/v1`)
- Typed request/response models and domain layer separation
- SQLAlchemy async ORM + repository-backed document workflows
- PoC-mode DB lifecycle wiring with dependency injection and startup schema creation
- API key auth (`X-API-Key`) for document endpoints
- Structured JSON logging + request ID middleware (`X-Request-ID`)
- Lightweight Prometheus-style metrics endpoint
- Quality checks wired for linting, typing, tests, and coverage gate
- Terraform starter modules for container registry setup:
  - AWS ECR
  - Azure Container Registry
  - GCP Artifact Registry

## API endpoints

- `GET /api/v1/health`
- `GET /api/v1/metrics`
- `POST /api/v1/documents/analyze`
- `POST /api/v1/documents`
- `GET /api/v1/documents`
- `GET /api/v1/documents/{document_id}`
- `PUT /api/v1/documents/{document_id}`
- `DELETE /api/v1/documents/{document_id}`

`/health` and `/metrics` are public. All `/documents*` routes require `X-API-Key`.

## Local development

```bash
uv sync --all-groups
uv run uvicorn fastapi_production_template.main:app --reload
```

Example authenticated request:

```bash
curl -H "X-API-Key: dev-api-key" http://localhost:8000/api/v1/documents
```

## Tests and quality gates

```bash
uv run pytest
uv run ruff check .
uv run ty check .
uv run tox
```

Pre-commit hooks (Ruff, unit tests, Terraform fmt check):

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

## Docker

Standard compose setup:

```bash
docker compose up --build
```

Dev profile with file watching (`src`, `tests`, `pyproject.toml`):

```bash
docker compose --profile dev up --build --watch api-dev postgres
```

## Terraform validation

```bash
terraform -chdir=infra/terraform-aws init
terraform -chdir=infra/terraform-aws validate
terraform -chdir=infra/terraform-azure init
terraform -chdir=infra/terraform-azure validate
terraform -chdir=infra/terraform-gcp init
terraform -chdir=infra/terraform-gcp validate
```

## Freelance work

I am Kevin Meinon, a freelance backend developer focused on Python/FastAPI, API architecture, and production hardening.

If your team needs support with:
- backend feature delivery
- API performance and reliability
- test strategy and CI quality gates
- cloud deployment foundations

Reach out at `kevin@meinon.de`.
