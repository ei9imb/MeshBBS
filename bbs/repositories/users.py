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
        """
        Insert or update a user.

        Alias history is maintained automatically whenever the
        short name or long name changes.
        """

        existing = self.get(user.node_id)

        if existing is None:
            self._insert_user(user)
            self._insert_alias(user)
            self._connection.commit()
            return

        if (
            existing.short_name != user.short_name
            or existing.long_name != user.long_name
        ):
            self._close_current_alias(
                user.node_id,
                user.last_seen,
            )

            self._insert_alias(user)

        self._connection.execute(
            """
            UPDATE users
            SET
                short_name = ?,
                long_name = ?,
                last_seen = ?
            WHERE node_id = ?
            """,
            (
                user.short_name,
                user.long_name,
                user.last_seen,
                user.node_id,
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

    def find_by_short_name(
        self,
        short_name: str,
    ) -> User | None:
        """Return the current user with the given short name."""

        row = self._connection.execute(
            """
            SELECT
                node_id,
                short_name,
                long_name,
                first_seen,
                last_seen
            FROM users
            WHERE short_name = ?
            """,
            (short_name,),
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

    def get_display_name(
        self,
        node_id: str,
    ) -> str | None:
        """Return the current short name for a node."""

        row = self._connection.execute(
            """
            SELECT short_name
            FROM users
            WHERE node_id = ?
            """,
            (node_id,),
        ).fetchone()

        if row is None:
            return None

        return str(row["short_name"])

    def update_last_seen(
        self,
        node_id: str,
        timestamp: str,
    ) -> None:
        """Update the user's last seen timestamp."""

        self._connection.execute(
            """
            UPDATE users
            SET last_seen = ?
            WHERE node_id = ?
            """,
            (
                timestamp,
                node_id,
            ),
        )

        self._connection.commit()

    def _insert_user(self, user: User) -> None:
        """Insert a new user."""

        self._connection.execute(
            """
            INSERT INTO users (
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

    def _insert_alias(self, user: User) -> None:
        """Insert a new alias record."""

        self._connection.execute(
            """
            INSERT INTO user_aliases (
                node_id,
                short_name,
                long_name,
                first_seen,
                last_seen
            )
            VALUES (?, ?, ?, ?, NULL)
            """,
            (
                user.node_id,
                user.short_name,
                user.long_name,
                user.first_seen,
            ),
        )

    def _close_current_alias(
        self,
        node_id: str,
        retired: str,
    ) -> None:
        """Close the current alias record."""

        self._connection.execute(
            """
            UPDATE user_aliases
            SET last_seen = ?
            WHERE node_id = ?
              AND last_seen IS NULL
            """,
            (
                retired,
                node_id,
            ),
        )