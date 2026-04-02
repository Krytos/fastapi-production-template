"""Request id middleware and context utilities."""

from contextvars import ContextVar
from time import perf_counter
from uuid import uuid4

from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response as StarletteResponse
from starlette.types import ASGIApp

from fastapi_production_template.observability.metrics import MetricsStore

_request_id_ctx: ContextVar[str | None] = ContextVar("request_id", default=None)


def get_request_id() -> str | None:
    """Read request id from context."""

    return _request_id_ctx.get()


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Attach request id to context, response, logs, and metrics."""

    def __init__(self, app: ASGIApp, *, metrics: MetricsStore) -> None:
        super().__init__(app)
        self._metrics = metrics

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID") or str(uuid4())
        token = _request_id_ctx.set(request_id)

        start = perf_counter()
        self._metrics.increment_in_flight()
        response: StarletteResponse
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
        finally:
            duration = perf_counter() - start
            self._metrics.observe(
                method=request.method,
                path=request.url.path,
                status_code=status_code,
                duration_seconds=duration,
            )
            self._metrics.decrement_in_flight()
            _request_id_ctx.reset(token)

        response.headers["X-Request-ID"] = request_id
        logger.info("{} {} {}", request.method, request.url.path, response.status_code)
        return response
