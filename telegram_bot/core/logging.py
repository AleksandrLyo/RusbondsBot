"""Настройки логирования для бота."""
import logging

import structlog

logging.basicConfig(level=logging.INFO)

structlog.configure(
    processors=[
        structlog.processors.UnicodeDecoder(),
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
        structlog.processors.JSONRenderer(ensure_ascii=False),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()