"""
User repository.

Handles all database operations related to Meshtastic users.
"""

from __future__ import annotations

import sqlite3

from bbs.models import User


class UserRepository:
    """Repository for user records."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def add(self, user: User) -> None:
        """Insert or update a user."""

        self._connection.execute(
            """
            INSERT OR REPLACE INTO users (
                node_id,
                short_name,
                long_name,
                first_seen,
                last_seen
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user.node_id,
                user.short_name,
                user.long_name,
                user.first_seen,
                user.last_seen,
            ),
        )

        self._connection.commit()

    def get(self, node_id: str) -> User | None:
        """Return a user by node ID."""

        row = self._connection.execute(
            """
            SELECT
                node_id,
                short_name,
                long_name,
                first_seen,
                last_seen
            FROM users
            WHERE node_id = ?
            """,
            (node_id,),
        ).fetchone()

        if row is None:
            return None

        return User(
            node_id=row["node_id"],
            short_name=row["short_name"],
            long_name=row["long_name"],
            first_seen=row["first_seen"],
            last_seen=row["last_seen"],
        )