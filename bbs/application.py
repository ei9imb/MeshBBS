"""
MeshBBS Application

Coordinates the lifecycle of all MeshBBS components.
"""

from __future__ import annotations

from bbs.config import Config
from bbs.logger import get_logger


class MeshBBS:
    """
    Main application class.
    """

    def __init__(self) -> None:
        self.config = Config()
        self.logger = get_logger(__name__)

    def start(self) -> None:
        """Start the application."""

        self.logger.info("Starting MeshBBS")

        name = self.config.get("name")
        version = self.config.get("version")

        self.logger.info("%s v%s", name, version)

    def stop(self) -> None:
        """Stop the application."""

        self.logger.info("Stopping MeshBBS")

    def run(self) -> None:
        """
        Main application loop.
        """

        self.start()

        try:
            self.logger.info("MeshBBS is running")

        finally:
            self.stop()