"""
Bulletin service.

Implements the business logic for bulletin operations.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum

from bbs.context import ExecutionContext
from bbs.models import Bulletin
from bbs.repositories import bulletins
from bbs.repositories.bulletins import BulletinRepository


class DeleteResult(Enum):
    """Result of attempting to delete a bulletin."""

    SUCCESS = "success"
    NOT_FOUND = "not_found"
    PERMISSION_DENIED = "permission_denied"


class BulletinService:
    """Business logic for bulletin operations."""

    def __init__(self, repository: BulletinRepository) -> None:
        self._repository = repository

    def post(
        self,
        author_node_id: str,
        author_name: str,
        subject: str,
        body: str,
    ) -> int:
        """
        Post a new bulletin.

        Returns the bulletin ID.
        """

        bulletin = Bulletin(
            id=None,
            author_node_id=author_node_id,
            author_name=author_name,
            subject=subject.strip(),
            body=body.strip(),
            created=datetime.now(UTC).isoformat(timespec="seconds"),
        )

        return self._repository.add(bulletin)

    def read(
            self,
            bulletin_id: int,
            context: ExecutionContext,
        ) -> Bulletin | None:
        """Return a bulletin and record that it has been read."""

        bulletin = self._repository.get(bulletin_id)

        if bulletin is None:
            return None

        self._repository.mark_read(
            bulletin_id=bulletin_id,
            node_id=context.node_id,
            timestamp=datetime.now(UTC).isoformat(timespec="seconds"),
        )

        return bulletin

    def list(
        self,
        context: ExecutionContext,
    ) -> tuple[list[Bulletin], set[int]]:
        """Return all bulletins and the user's read history."""

        bulletins = self._repository.get_all()

        read_ids = self._repository.read_ids(
        context.node_id,
        )

        return bulletins, read_ids

    def delete(
        self,
        bulletin_id: int,
        context: ExecutionContext,
    ) -> DeleteResult:
        """
        Delete a bulletin.

        Only the original author or an administrator may delete
        a bulletin.
        """

        bulletin = self._repository.get(bulletin_id)

        if bulletin is None:
            return DeleteResult.NOT_FOUND

        if (
            bulletin.author_node_id != context.node_id
            and not context.is_admin
        ):
            return DeleteResult.PERMISSION_DENIED

        self._repository.delete(bulletin_id)

        return DeleteResult.SUCCESS