"""
MeshBBS Entry Point
"""

from __future__ import annotations

from bbs.application import MeshBBS
from bbs.logger import configure_logging


def main() -> None:
    configure_logging()
    app = MeshBBS()
    app.run()


if __name__ == "__main__":
    main()