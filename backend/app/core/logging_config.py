"""
Centralized logging configuration with structured logging support.
"""
import logging
import logging.config
import sys
from typing import Any, Dict
from app.core.config import settings


def setup_logging() -> None:
    """
    Configure application-wide logging with structured output.

    Configures:
    - Log levels based on environment
    - JSON formatting for production
    - Console output for development
    - Request ID correlation
    """
    log_level = getattr(
        logging,
        settings.ENV.upper() if hasattr(settings, "LOG_LEVEL") else "INFO",
        logging.INFO,
    )

    # Use different formatters based on environment
    if settings.ENV == "production":
        # JSON format for production (easier to parse by log aggregators)
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d"
    else:
        # Human-readable format for development
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging_config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": log_format,
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(pathname)s:%(lineno)d]",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "default" if settings.ENV != "production" else "detailed",
                "stream": sys.stdout,
            },
        },
        "root": {
            "level": log_level,
            "handlers": ["console"],
        },
        "loggers": {
            # App loggers
            "app": {
                "level": log_level,
                "handlers": ["console"],
                "propagate": False,
            },
            # Quiet down some noisy libraries in development
            "uvicorn.access": {
                "level": logging.WARNING if settings.DEBUG else logging.INFO,
                "handlers": ["console"],
                "propagate": False,
            },
            "sqlalchemy.engine": {
                "level": logging.WARNING,
                "handlers": ["console"],
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(logging_config)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)
