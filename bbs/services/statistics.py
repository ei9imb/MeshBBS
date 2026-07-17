"""
Statistics service.

Provides system statistics for MeshBBS.
"""

from __future__ import annotations

from datetime import UTC, datetime
from bbs.repositories.bulletins import BulletinRepository
from bbs.repositories.mail import MailRepository
from bbs.repositories.users import UserRepository


class StatisticsService:
    """Provides MeshBBS statistics."""

    def __init__(
        self,
        users: UserRepository,
        bulletins: BulletinRepository,
        mail: MailRepository,
    ) -> None:
        self._users = users
        self._bulletins = bulletins
        self._mail = mail
        self._started = datetime.now(UTC)

    def summary(self) -> dict[str, int]:
        """Return the current system statistics."""

        return {
            "users": self._users.count(),
            "bulletins": self._bulletins.count(),
            "mail": self._mail.count(),
            "uptime": self.uptime(),
        }
    def uptime(self) -> str:
        """Return the application uptime."""

        elapsed = datetime.now(UTC) - self._started

        total_seconds = int(elapsed.total_seconds())

        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        return f"{hours:02}:{minutes:02}:{seconds:02}"