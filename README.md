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
- Service layer with seeded example document workflows
- Async database engine/session module
- Quality checks wired for linting, typing, tests, and coverage gate
- Terraform starter modules for container registry setup:
  - AWS ECR
  - Azure Container Registry
  - GCP Artifact Registry

## API endpoints

- `GET /api/v1/health`
- `POST /api/v1/documents/analyze`
- `GET /api/v1/documents/{document_id}`

## Local development

```bash
uv sync --all-groups
uv run uvicorn fastapi_production_template.main:app --reload
```

## Tests and quality gates

```bash
uv run pytest
uv run ruff check .
uv run ty check .
uv run tox
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
