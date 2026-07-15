"""
MeshBBS execution context.

Carries authenticated user information from the transport layer
into the application.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ExecutionContext:
    """
    Represents the authenticated identity executing a command.
    """

    node_id: str
    short_name: str
    long_name: str
    is_admin: bool = False