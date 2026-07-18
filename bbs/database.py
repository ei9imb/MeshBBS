"""
Database component for MeshBBS.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from bbs.component import Component
from bbs.logger import get_logger
from bbs.repositories.bulletins import BulletinRepository
from bbs.repositories.mail import MailRepository
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
        self.bulletins: BulletinRepository | None = None
        self.mail: MailRepository | None = None

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

        # Enable SQLite foreign key enforcement
        self.connection.execute("PRAGMA foreign_keys = ON")

        # Wait up to 5 seconds if the database is temporarily locked
        self.connection.execute("PRAGMA busy_timeout = 5000")

        self._initialise_schema()

        self._initialise_schema()

        self.users = UserRepository(self.connection)
        self.bulletins = BulletinRepository(self.connection)
        self.mail = MailRepository(self.connection)

        self.logger.info("Database ready.")

    def stop(self) -> None:
        """Stop the database component."""

        self.users = None
        self.bulletins = None
        self.mail = None

        if self._connection is not None:
            self._connection.close()
            self._connection = None

        self.logger.info("Database closed.")

    def _initialise_schema(self) -> None:
        """Create the database schema if required."""

        cursor = self.connection.cursor()

        cursor.executescript(
            """
            PRAGMA user_version = 5;

            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                node_id TEXT NOT NULL UNIQUE,
                short_name TEXT,
                long_name TEXT,
                first_seen TEXT,
                last_seen TEXT,
                is_admin INTEGER NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS user_aliases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                node_id TEXT NOT NULL,
                short_name TEXT,
                long_name TEXT,
                first_seen TEXT NOT NULL,
                last_seen TEXT
            );

            CREATE INDEX IF NOT EXISTS
                idx_user_aliases_node
            ON user_aliases(node_id);

            CREATE INDEX IF NOT EXISTS
                idx_user_aliases_short_name
            ON user_aliases(short_name);

            CREATE TABLE IF NOT EXISTS bulletins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author_node_id TEXT NOT NULL,
                author_name TEXT NOT NULL,
                subject TEXT NOT NULL,
                body TEXT NOT NULL,
                created TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS bulletin_reads (
                bulletin_id INTEGER NOT NULL,
                node_id TEXT NOT NULL,
                read_at TEXT NOT NULL,

                PRIMARY KEY (bulletin_id, node_id),

                FOREIGN KEY (bulletin_id)
                    REFERENCES bulletins(id)
                    ON DELETE CASCADE,

                FOREIGN KEY (node_id)
                    REFERENCES users(node_id)
                    ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS
            idx_bulletin_reads_node
        ON bulletin_reads(node_id);            

            CREATE TABLE IF NOT EXISTS mail (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_node_id TEXT NOT NULL,
                recipient_node_id TEXT NOT NULL,
                subject TEXT NOT NULL,
                body TEXT NOT NULL,
                created TEXT NOT NULL,
                read_at TEXT
            );

            CREATE INDEX IF NOT EXISTS
                idx_mail_recipient
            ON mail(recipient_node_id);

            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            """
        )

        self.connection.commit()
        
    def schema_version(self) -> int:
        """Return the database schema version."""

        row = self.connection.execute(
            "PRAGMA user_version"
        ).fetchone()

        return int(row[0])