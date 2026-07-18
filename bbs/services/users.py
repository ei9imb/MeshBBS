"""
User service.

Provides user administration for MeshBBS.
"""

from __future__ import annotations

from bbs.models import User
from bbs.repositories.users import UserRepository
from datetime import datetime, UTC


class UserService:
    """Provides user administration."""

    def __init__(
        self,
        users: UserRepository,
    ) -> None:
        self._users = users

    def is_admin(
        self,
        node_id: str,
    ) -> bool:
        """Return True if the user is an administrator."""

        user = self._users.get(node_id)

        if user is None:
            return False

        return user.is_admin
    
    def get(
        self,
        node_id: str,
    ) -> User | None:
        """Return a user by node ID."""

        return self._users.get(node_id)
    
    def ensure_user(
        self,
        node_id: str,
        short_name: str,
        long_name: str,
    ) -> User:
        """
        Return an existing user or register a new one.

        The user's names and last_seen timestamp are updated on
        every message.
        """

        user = self._users.get(
            node_id,
        )

        now = datetime.now(UTC).isoformat()

        if user is None:

            user = User(
                node_id=node_id,
                short_name=short_name,
                long_name=long_name,
                first_seen=now,
                last_seen=now,
            )

        else:

            user.short_name = short_name
            user.long_name = long_name
            user.last_seen = now

        self._users.add(
            user,
        )

        return user    

    def promote(
        self,
        node_id: str,
    ) -> bool:
        """Promote a user to administrator."""

        user = self._users.get(node_id)

        if user is None:
            return False

        if user.is_admin:
            return True

        user.is_admin = True
        self._users.add(user)

        return True

    def demote(
        self,
        node_id: str,
    ) -> bool:
        """Remove administrator rights."""

        user = self._users.get(node_id)

        if user is None:
            return False

        user.is_admin = False
        self._users.add(user)

        return True

    def list_admins(self) -> list[User]:
        """Return all administrators."""

        return self._users.list_admins()

    def list_users(self) -> list[User]:
        """Return all known users."""

        return self._users.list_users()