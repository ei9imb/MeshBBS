"""
User service.

Provides user administration for MeshBBS.
"""

from __future__ import annotations

from bbs.models import User
from bbs.repositories.users import UserRepository


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