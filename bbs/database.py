"""
Database component for MeshBBS.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from bbs.component import Component
from bbs.logger import get_logger
from bbs.repositories.users import UserRepository


class Database(Component):
    """SQLite database component."""

    def __init__(self, database_path: Path | None = None) -> None:
        project_root = Path(__file__).resolve().parent.parent

        if database_path is None:
            database_path = project_root / "data" / "meshbbs.db"

        self._db_path = database_path
        self._connection: sqlite3.Connection | None = None

        self.logger = get_logger(__name__)

        self.users: UserRepository | None = None

    @property
    def connection(self) -> sqlite3.Connection:
        """Return the active database connection."""
        if self._connection is None:
            raise RuntimeError("Database is not connected.")
        return self._connection

    def start(self) -> None:
        """Start the database component."""

        self.logger.info("Opening database: %s", self._db_path)

        self._db_path.parent.mkdir(parents=True, exist_ok=True)

        self._connection = sqlite3.connect(self._db_path)
        self._connection.row_factory = sqlite3.Row

        self._initialise_schema()

        self.users = UserRepository(self.connection)

        self.logger.info("Database ready.")

    def stop(self) -> None:
        """Stop the database component."""

        self.users = None

        if self._connection is not None:
            self._connection.close()
            self._connection = None

        self.logger.info("Database closed.")

    def _initialise_schema(self) -> None:
        """Create the database schema if required."""

        cursor = self.connection.cursor()

        cursor.executescript(
            """
            PRAGMA user_version = 1;

            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                node_id TEXT NOT NULL UNIQUE,
                short_name TEXT,
                long_name TEXT,
                first_seen TEXT,
                last_seen TEXT
            );

            CREATE TABLE IF NOT EXISTS bulletins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author TEXT NOT NULL,
                subject TEXT NOT NULL,
                body TEXT NOT NULL,
                created TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS mail (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                recipient TEXT NOT NULL,
                subject TEXT NOT NULL,
                body TEXT NOT NULL,
                created TEXT NOT NULL,
                delivered INTEGER NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            """
        )

        self.connection.commit()