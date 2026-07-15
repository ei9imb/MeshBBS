"""
MeshBBS Application

Coordinates the lifecycle of all MeshBBS components.
"""

from __future__ import annotations

from bbs.config import Config
from bbs.database import Database
from bbs.logger import get_logger


class MeshBBS:
    """
    Main application class.
    """

    def __init__(self) -> None:
        self.config = Config()
        self.logger = get_logger(__name__)

        self.components = [
            Database(),
        ]

    def start(self) -> None:
        """Start the application."""

        self.logger.info("Starting MeshBBS")

        name = self.config.get("name")
        version = self.config.get("version")

        self.logger.info("%s v%s", name, version)

        for component in self.components:
            component.start()

    def stop(self) -> None:
        """Stop the application."""

        for component in reversed(self.components):
            component.stop()

        self.logger.info("Stopping MeshBBS")

    def run(self) -> None:
        """Run the application."""

        self.start()

        try:
            self.logger.info("MeshBBS is running")
        finally:
            self.stop()