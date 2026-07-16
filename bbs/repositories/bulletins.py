"""
Bulletin repository.

Handles all database operations related to bulletins.
"""

from __future__ import annotations

import sqlite3

from bbs.models import Bulletin


class BulletinRepository:
    """Repository for bulletin records."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def add(self, bulletin: Bulletin) -> int:
        """Insert a bulletin and return its database ID."""

        cursor = self._connection.execute(
            """
            INSERT INTO bulletins (
                author_node_id,
                author_name,
                subject,
                body,
                created
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                bulletin.author_node_id,
                bulletin.author_name,
                bulletin.subject,
                bulletin.body,
                bulletin.created,
            ),
        )

        self._connection.commit()

        return int(cursor.lastrowid)

    def get(self, bulletin_id: int) -> Bulletin | None:
        """Return a bulletin by ID."""

        row = self._connection.execute(
            """
            SELECT
                id,
                author_node_id,
                author_name,
                subject,
                body,
                created
            FROM bulletins
            WHERE id = ?
            """,
            (bulletin_id,),
        ).fetchone()

        if row is None:
            return None

        return Bulletin(
            id=row["id"],
            author_node_id=row["author_node_id"],
            author_name=row["author_name"],
            subject=row["subject"],
            body=row["body"],
            created=row["created"],
        )

    def get_all(self) -> list[Bulletin]:
        """Return all bulletins."""

        rows = self._connection.execute(
            """
            SELECT
                id,
                author_node_id,
                author_name,
                subject,
                body,
                created
            FROM bulletins
            ORDER BY id
            """
        ).fetchall()

        return [
            Bulletin(
                id=row["id"],
                author_node_id=row["author_node_id"],
                author_name=row["author_name"],
                subject=row["subject"],
                body=row["body"],
                created=row["created"],
            )
            for row in rows
        ]

    def delete(self, bulletin_id: int) -> None:
        """Delete a bulletin."""

        self._connection.execute(
            "DELETE FROM bulletins WHERE id = ?",
            (bulletin_id,),
        )

        self._connection.commit()