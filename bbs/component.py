"""
MeshBBS Component Base Class

Every subsystem in MeshBBS derives from Component.

The application controls the lifecycle of each component
through the start() and stop() methods.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Component(ABC):
    """
    Base class for all MeshBBS components.
    """

    @abstractmethod
    def start(self) -> None:
        """Start the component."""

    @abstractmethod
    def stop(self) -> None:
        """Stop the component cleanly."""