"""
Mail repository.

Handles all database operations related to private mail.
"""

from __future__ import annotations

import sqlite3

from bbs.models import Mail


class MailRepository:
    """Repository for private mail."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def add(self, mail: Mail) -> int:
        """Store a mail message."""

        cursor = self._connection.execute(
            """
            INSERT INTO mail (
                sender_node_id,
                recipient_node_id,
                subject,
                body,
                created,
                read_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                mail.sender_node_id,
                mail.recipient_node_id,
                mail.subject,
                mail.body,
                mail.created,
                mail.read_at,
            ),
        )

        self._connection.commit()

        return int(cursor.lastrowid)

    def get(self, mail_id: int) -> Mail | None:
        """Return a mail message by ID."""

        row = self._connection.execute(
            """
            SELECT
                id,
                sender_node_id,
                recipient_node_id,
                subject,
                body,
                created,
                read_at
            FROM mail
            WHERE id = ?
            """,
            (mail_id,),
        ).fetchone()

        if row is None:
            return None

        return Mail(
            id=row["id"],
            sender_node_id=row["sender_node_id"],
            recipient_node_id=row["recipient_node_id"],
            subject=row["subject"],
            body=row["body"],
            created=row["created"],
            read_at=row["read_at"],
        )

    def get_for_recipient(
        self,
        recipient_node_id: str,
    ) -> list[Mail]:
        """Return all mail for a recipient."""

        rows = self._connection.execute(
            """
            SELECT
                id,
                sender_node_id,
                recipient_node_id,
                subject,
                body,
                created,
                read_at
            FROM mail
            WHERE recipient_node_id = ?
            ORDER BY id DESC
            """,
            (recipient_node_id,),
        ).fetchall()

        return [
            Mail(
                id=row["id"],
                sender_node_id=row["sender_node_id"],
                recipient_node_id=row["recipient_node_id"],
                subject=row["subject"],
                body=row["body"],
                created=row["created"],
                read_at=row["read_at"],
            )
            for row in rows
        ]

    def mark_read(
        self,
        mail_id: int,
        timestamp: str,
    ) -> None:
        """Mark a message as read."""

        self._connection.execute(
            """
            UPDATE mail
            SET read_at = ?
            WHERE id = ?
              AND read_at IS NULL
            """,
            (
                timestamp,
                mail_id,
            ),
        )

        self._connection.commit()

    def delete(self, mail_id: int) -> None:
        """Delete a mail message."""

        self._connection.execute(
            """
            DELETE FROM mail
            WHERE id = ?
            """,
            (mail_id,),
        )

        self._connection.commit()