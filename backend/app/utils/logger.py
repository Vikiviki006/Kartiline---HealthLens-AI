"""
Centralized logger configuration using Loguru.

Usage anywhere in the codebase:
    from app.utils.logger import logger
    logger.info("Something happened")
    logger.bind(user_id=user_id).info("User action")
"""

import sys
from loguru import logger
from app.core.config import settings


def _configure_logger() -> None:
    logger.remove()  # remove default handler

    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
        "{extra}"
    )

    logger.add(
        sys.stdout,
        format=log_format,
        level=settings.LOG_LEVEL,
        colorize=True,
        backtrace=True,
        diagnose=not settings.is_production,
        enqueue=True,
    )

    if settings.is_production:
        logger.add(
            "logs/healthlens_{time:YYYY-MM-DD}.log",
            rotation="00:00",
            retention="30 days",
            compression="zip",
            format=log_format,
            level="INFO",
            enqueue=True,
            backtrace=False,
            diagnose=False,
        )


_configure_logger()

__all__ = ["logger"]
