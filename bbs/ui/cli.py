"""
Interactive command-line interface for MeshBBS.
"""

from __future__ import annotations

from bbs.commands.router import CommandRouter


class CommandLineInterface:
    """Interactive console interface."""

    def __init__(self, router: CommandRouter) -> None:
        self._router = router

    def run(self) -> None:
        """Run the interactive command loop."""

        self._display_banner()

        while True:
            command = input("> ").strip()

            if not command:
                continue

            if command.upper() in ("Q", "QUIT", "EXIT"):
                print("73!")
                break

            response = self._router.execute(command)

            print()
            print(response)
            print()

    def _display_banner(self) -> None:
        """Display the startup banner."""

        print("=" * 40)
        print("      Cumann Muscraí BBS")
        print("=" * 40)
        print()
        print("Type H for [H]elp.")
        print()