"""
MeshBBS Session Management

Maintains active user sessions.

A session represents a temporary conversation with a registered user.
Sessions automatically expire after a period of inactivity.

Author: MeshBBS
"""

from __future__ import annotations

import logging

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any


logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Session
# ---------------------------------------------------------------------------

@dataclass
class Session:
    """
    Represents one active user session.

    Sessions are temporary and exist only while the user is actively
    interacting with the BBS.
    """

    node_id: str

    created: datetime = field(default_factory=datetime.utcnow)
    last_activity: datetime = field(default_factory=datetime.utcnow)

    state: str = "idle"

    data: dict[str, Any] = field(default_factory=dict)

    def touch(self) -> None:
        """
        Update the activity timestamp.
        """
        self.last_activity = datetime.utcnow()


# ---------------------------------------------------------------------------
# Session Manager
# ---------------------------------------------------------------------------

class SessionManager:
    """
    Stores and manages active sessions.
    """

    DEFAULT_TIMEOUT = timedelta(minutes=20)

    def __init__(self, timeout: timedelta | None = None):

        self.timeout = timeout or self.DEFAULT_TIMEOUT

        self._sessions: dict[str, Session] = {}

        logger.info(
            "SessionManager initialised (timeout=%s)",
            self.timeout,
        )

    # ------------------------------------------------------------------

    def get(self, node_id: str) -> Session | None:
        """
        Return an existing session.

        Returns None if no active session exists.
        """

        session = self._sessions.get(node_id)

        if session is None:
            return None

        if self._is_expired(session):

            logger.info(
                "Session expired for node %s",
                node_id,
            )

            self.remove(node_id)

            return None

        session.touch()

        return session

    # ------------------------------------------------------------------

    def create(self, node_id: str) -> Session:
        """
        Create a new session.

        Existing sessions are replaced.
        """

        session = Session(node_id=node_id)

        self._sessions[node_id] = session

        logger.info(
            "Created session for node %s",
            node_id,
        )

        return session

    # ------------------------------------------------------------------

    def get_or_create(self, node_id: str) -> Session:
        """
        Return an active session or create one.
        """

        session = self.get(node_id)

        if session is not None:
            return session

        return self.create(node_id)

    # ------------------------------------------------------------------

    def remove(self, node_id: str) -> None:
        """
        Remove a session.
        """

        if node_id in self._sessions:

            del self._sessions[node_id]

            logger.info(
                "Removed session for node %s",
                node_id,
            )

    # ------------------------------------------------------------------

    def exists(self, node_id: str) -> bool:
        """
        True if an active session exists.
        """

        return self.get(node_id) is not None
    
        # ------------------------------------------------------------------

    def cleanup_expired(self) -> int:
        """
        Remove all expired sessions.

        Returns
        -------
        int
            Number of sessions removed.
        """

        expired = [
            node_id
            for node_id, session in self._sessions.items()
            if self._is_expired(session)
        ]

        for node_id in expired:
            logger.info(
                "Cleaning up expired session for node %s",
                node_id,
            )
            del self._sessions[node_id]

        return len(expired)

    # ------------------------------------------------------------------

    def active_count(self) -> int:
        """
        Return the number of active sessions.

        Expired sessions are removed first.
        """

        self.cleanup_expired()

        return len(self._sessions)

    # ------------------------------------------------------------------

    def all_sessions(self) -> list[Session]:
        """
        Return all active sessions.
        """

        self.cleanup_expired()

        return list(self._sessions.values())

    # ------------------------------------------------------------------

    def session_ids(self) -> list[str]:
        """
        Return a list of active node IDs.
        """

        self.cleanup_expired()

        return list(self._sessions.keys())

    # ------------------------------------------------------------------

    def clear(self) -> None:
        """
        Remove every active session.
        """

        count = len(self._sessions)

        self._sessions.clear()

        logger.info(
            "Cleared %d active session(s)",
            count,
        )

    # ------------------------------------------------------------------

    def _is_expired(self, session: Session) -> bool:
        """
        Determine whether a session has expired.
        """

        return (
            datetime.utcnow() - session.last_activity
        ) > self.timeout

    # ------------------------------------------------------------------

    def __len__(self) -> int:
        """
        Return the number of active sessions.
        """

        return self.active_count()

    # ------------------------------------------------------------------

    def __contains__(self, node_id: str) -> bool:
        """
        Support:

            if node_id in session_manager:
        """

        return self.exists(node_id)

    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"SessionManager("
            f"active={self.active_count()}, "
            f"timeout={self.timeout})"
        )