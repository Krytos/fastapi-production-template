# FastAPI Production Template

[![CI](https://img.shields.io/github/actions/workflow/status/Krytos/fastapi-production-template/ci.yml?branch=main&label=ci-cd)](https://github.com/Krytos/fastapi-production-template/actions/workflows/ci.yml)
[![Tests](https://img.shields.io/github/actions/workflow/status/Krytos/fastapi-production-template/tests.yml?branch=main&label=tests)](https://github.com/Krytos/fastapi-production-template/actions/workflows/tests.yml)
[![PyPI version](https://img.shields.io/pypi/v/fastapi-production-template)](https://pypi.org/project/fastapi-production-template/)
[![Python](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fpypi.org%2Fpypi%2Ffastapi-production-template%2Fjson&query=%24.info.requires_python&label=python&color=3776AB)](https://pypi.org/project/fastapi-production-template/)
[![Coverage gate](https://img.shields.io/badge/coverage%20gate-100%25-brightgreen)](https://github.com/Krytos/fastapi-production-template/blob/main/pyproject.toml)
[![Code style: Ruff](https://img.shields.io/badge/lint-ruff-46a758)](https://github.com/astral-sh/ruff)
[![Type checking: Ty](https://img.shields.io/badge/types-ty-0f172a)](https://github.com/astral-sh/ty)
[![Publish: PyPI](https://img.shields.io/badge/publish-pypi-blue)](https://github.com/Krytos/fastapi-production-template/blob/main/.github/workflows/ci.yml)
[![Package manager: uv](https://img.shields.io/badge/package%20manager-uv-DE5FE9)](https://github.com/astral-sh/uv)
[![Framework: FastAPI](https://img.shields.io/badge/framework-fastapi-009688)](https://fastapi.tiangolo.com/)
[![ORM: SQLAlchemy](https://img.shields.io/badge/orm-sqlalchemy-d71f00)](https://www.sqlalchemy.org/)
[![Database: PostgreSQL](https://img.shields.io/badge/database-postgresql-336791)](https://www.postgresql.org/)
[![Infra: Terraform](https://img.shields.io/badge/infra-terraform-844FBA)](https://www.terraform.io/)
[![Container: Docker](https://img.shields.io/badge/container-docker-2496ED)](https://www.docker.com/)

[![Open for Freelance](https://img.shields.io/badge/open%20for-freelance%20projects-success)](mailto:kevin@meinon.de?subject=FastAPI%20Freelance%20Inquiry)
[![Hire Me](https://img.shields.io/badge/hire%20me-fastapi%20backend-0ea5e9)](mailto:kevin@meinon.de?subject=Backend%20Project%20Inquiry)
[![Contact](https://img.shields.io/badge/contact-kevin%40meinon.de-blue)](mailto:kevin@meinon.de)

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
