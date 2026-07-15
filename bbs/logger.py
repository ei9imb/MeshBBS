"""
MeshBBS Logger

Provides a single application-wide logger.

All modules should import this logger rather than creating their own.

Example:
    from bbs.logger import get_logger

    logger = get_logger(__name__)
    logger.info("Application started")
"""

from __future__ import annotations

import logging
from pathlib import Path

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

LOG_DIRECTORY = Path("logs")
LOG_FILE = LOG_DIRECTORY / "meshbbs.log"

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ---------------------------------------------------------------------
# Internal state
# ---------------------------------------------------------------------

_INITIALISED = False


def initialise() -> None:
    """
    Configure the application logger.

    Safe to call multiple times.
    """

    global _INITIALISED

    if _INITIALISED:
        return

    LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # File output
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    # Console output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    _INITIALISED = True


def get_logger(name: str) -> logging.Logger:
    """
    Return a logger for the specified module.
    """

    initialise()
    return logging.getLogger(name)