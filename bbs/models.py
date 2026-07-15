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


@dataclass(slots=True)
class Bulletin:
    """
    Represents a bulletin stored by MeshBBS.
    """

    id: int | None
    author: str
    subject: str
    body: str
    created: str