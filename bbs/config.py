"""
MeshBBS Configuration

Loads the application configuration from config/config.toml.
"""

from __future__ import annotations

from pathlib import Path
import tomllib


CONFIG_FILE = Path("config/config.toml")


class Config:
    """
    Loads and provides access to the application configuration.
    """

    def __init__(self) -> None:
        with CONFIG_FILE.open("rb") as file:
            self._config = tomllib.load(file)

    def get(self, *keys, default=None):
        """
        Retrieve a configuration value.

        Example:
            config.get("logging", "level")
        """

        value = self._config

        for key in keys:
            if not isinstance(value, dict):
                return default

            value = value.get(key)

            if value is None:
                return default

        return value