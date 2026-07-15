"""
MeshBBS Entry Point
"""

from __future__ import annotations

from bbs.application import MeshBBS


def main() -> None:
    app = MeshBBS()
    app.run()


if __name__ == "__main__":
    main()