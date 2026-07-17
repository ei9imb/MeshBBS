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
            """
            DELETE FROM bulletins
            WHERE id = ?
            """,
            (bulletin_id,),
        )

        self._connection.commit()

    def count(self) -> int:
        """Return the number of bulletins."""

        row = self._connection.execute(
            """
            SELECT COUNT(*)
            FROM bulletins
            """
        ).fetchone()

        return int(row[0])
    
    def mark_read(
        self,
        bulletin_id: int,
        node_id: str,
        timestamp: str,
    ) -> None:
        """Record that a user has read a bulletin."""

        self._connection.execute(
            """
            INSERT OR IGNORE INTO bulletin_reads (
                bulletin_id,
                node_id,
                read_at
            )
            VALUES (?, ?, ?)
            """,
            (
                bulletin_id,
                node_id,
                timestamp,
            ),
        )

        self._connection.commit()

    def has_read(
        self,
        bulletin_id: int,
        node_id: str,
    ) -> bool:
        """Return True if the user has read the bulletin."""

        row = self._connection.execute(
            """
            SELECT 1
            FROM bulletin_reads
            WHERE bulletin_id = ?
              AND node_id = ?
            """,
            (
                bulletin_id,
                node_id,
            ),
        ).fetchone()

        return row is not None
    
    def read_ids(
        self,
        node_id: str,
    ) -> set[int]:
        """Return the IDs of bulletins read by a user."""

        rows = self._connection.execute(
            """
            SELECT bulletin_id
            FROM bulletin_reads
            WHERE node_id = ?
            """,
            (node_id,),
        ).fetchall()

        return {
            int(row["bulletin_id"])
            for row in rows
        }