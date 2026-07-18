"""
MeshBBS Entry Point
"""

from __future__ import annotations

from bbs.application import MeshBBS
from bbs.logger import configure_logging
from bbs.meshtastic import MeshtasticInterface


def main() -> None:
    configure_logging()

    app = MeshBBS()

    app.start()

    transport = MeshtasticInterface(
        app,
    )

    try:

        transport.connect()

        transport.run()

    finally:

        app.stop()


if __name__ == "__main__":
    main()