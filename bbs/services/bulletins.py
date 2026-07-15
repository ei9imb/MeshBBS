"""
Bulletin service.

Implements the business logic for bulletin operations.
"""

from __future__ import annotations

from datetime import datetime, UTC

from bbs.models import Bulletin
from bbs.repositories.bulletins import BulletinRepository


class BulletinService:
    """Business logic for bulletin operations."""

    def __init__(self, repository: BulletinRepository) -> None:
        self._repository = repository

    def post(
        self,
        author: str,
        subject: str,
        body: str,
    ) -> int:
        """
        Post a new bulletin.

        Returns the bulletin ID.
        """

        bulletin = Bulletin(
            id=None,
            author=author,
            subject=subject.strip(),
            body=body.strip(),
            created=datetime.now(UTC).isoformat(timespec="seconds"),
        )

        return self._repository.add(bulletin)

    def read(self, bulletin_id: int) -> Bulletin | None:
        """Return a bulletin."""

        return self._repository.get(bulletin_id)

    def list(self) -> list[Bulletin]:
        """Return all bulletins."""

        return self._repository.get_all()

    def delete(self, bulletin_id: int) -> None:
        """Delete a bulletin."""

        self._repository.delete(bulletin_id)