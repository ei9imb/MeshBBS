"""
Domain models used by MeshBBS.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class User:
    """
    Represents a Meshtastic node known to MeshBBS.
    """

    node_id: str
    short_name: str
    long_name: str
    first_seen: str
    last_seen: str
    is_admin: bool = False


@dataclass(slots=True)
class Bulletin:
    """
    Represents a bulletin stored by MeshBBS.
    """

    id: int | None
    author_node_id: str
    author_name: str
    subject: str
    body: str
    created: str


@dataclass(slots=True)
class Mail:
    """
    Represents a private mail message.
    """

    id: int | None

    sender_node_id: str
    recipient_node_id: str

    subject: str
    body: str

    created: str

    read_at: str | None