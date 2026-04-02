"""Structured logging configuration using loguru."""

import sys
from typing import TYPE_CHECKING

from loguru import logger

from fastapi_production_template.middleware.request_id import get_request_id

if TYPE_CHECKING:
    from loguru import Record


def _inject_request_id(record: "Record") -> None:
    record["extra"]["request_id"] = get_request_id()


def configure_logging(*, level: str) -> None:
    """Configure loguru for JSON output."""

    logger.remove()
    logger.configure(patcher=_inject_request_id)
    logger.add(
        sys.stdout,
        level=level.upper(),
        serialize=True,
        enqueue=False,
        backtrace=False,
        diagnose=False,
    )
