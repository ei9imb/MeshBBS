"""
MeshBBS - Meshtastic Connection Test

Purpose:
    Verify that the Raspberry Pi can communicate with a Meshtastic node.

This is not the final client implementation.
It is only a hardware communication test.
"""

from __future__ import annotations

import sys
import meshtastic.serial_interface


def main() -> int:
    print("======================================")
    print(" MeshBBS - Meshtastic Connection Test ")
    print("======================================")
    print()

    try:
        print("Searching for Meshtastic node...")

        interface = meshtastic.serial_interface.SerialInterface()

        node = interface.getMyNodeInfo()

        print()
        print("Connection successful!")
        print()

        print(f"Node ID      : {node.get('user', {}).get('id', 'Unknown')}")
        print(f"Long Name    : {node.get('user', {}).get('longName', 'Unknown')}")
        print(f"Short Name   : {node.get('user', {}).get('shortName', 'Unknown')}")
        print(f"Hardware     : {node.get('user', {}).get('hwModel', 'Unknown')}")

        interface.close()
        return 0

    except Exception as exc:
        print()
        print("Connection failed")
        print(exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())