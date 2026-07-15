"""
MeshBBS Component Base Class

Every subsystem in MeshBBS derives from Component.

The application controls the lifecycle of each component
through the start() and stop() methods.
"""

from __future__ import annotations

from abc import ABC


class Component(ABC):
    """
    Base class for all MeshBBS components.
    """

    def start(self) -> None:
        """Start the component."""
        return

    def stop(self) -> None:
        """Stop the component cleanly."""
        return