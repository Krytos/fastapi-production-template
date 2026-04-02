FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src

RUN uv sync

EXPOSE 8000

CMD ["uvicorn", "fastapi_production_template.main:app", "--host", "0.0.0.0", "--port", "8000"]
