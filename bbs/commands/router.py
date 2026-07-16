"""
MeshBBS command router.
"""

from __future__ import annotations

from bbs.context import ExecutionContext
from bbs.services.bulletins import BulletinService


class CommandRouter:
    """Routes MeshBBS commands to services."""

    def __init__(
        self,
        bulletins: BulletinService,
        context: ExecutionContext,
    ) -> None:
        self._bulletins = bulletins
        self._context = context

    def execute(self, command: str) -> str:
        """
        Execute a quick command.

        Returns a response string.
        """

        command = command.strip()

        if not command:
            return "No command entered."

        parts = command.split(".")

        opcode = parts[0].upper()
        arguments = parts[1:]

        if opcode == "HELP":
            return self._help()

        if opcode == "LB":
            return self._list_bulletins()

        if opcode == "PB":
            return self._post_bulletin(arguments)

        if opcode == "RB":
            return self._read_bulletin(arguments)

        if opcode == "DB":
            return self._delete_bulletin(arguments)

        return f"Unknown command: {opcode}"

    def _help(self) -> str:
        return (
            "MeshBBS Commands\n"
            "\n"
            "LB  List Bulletins\n"
            "PB  Post Bulletin\n"
            "RB  Read Bulletin\n"
            "DB  Delete Bulletin\n"
            "\n"
            "LM  List Mail\n"
            "SM  Send Mail\n"
            "RM  Read Mail\n"
            "DM  Delete Mail"
        )

    def _list_bulletins(self) -> str:
        bulletins = self._bulletins.list()

        if not bulletins:
            return "No bulletins."

        lines = []

        for bulletin in bulletins:
            lines.append(
                f"{bulletin.id:3} {bulletin.author_name:4} {bulletin.subject}"
            )

        return "\n".join(lines)

    def _post_bulletin(self, arguments: list[str]) -> str:
        """
        Post a bulletin.

        Format:
            PB.subject.body
        """

        if len(arguments) != 2:
            return "Usage: PB.subject.body"

        bulletin_id = self._bulletins.post(
            author_node_id=self._context.node_id,
            author_name=self._context.short_name,
            subject=arguments[0],
            body=arguments[1],
        )

        return f"Bulletin #{bulletin_id} posted."

    def _read_bulletin(self, arguments: list[str]) -> str:
        """
        Read a bulletin.

        Format:
            RB.id
        """

        if len(arguments) != 1:
            return "Usage: RB.id"

        try:
            bulletin_id = int(arguments[0])
        except ValueError:
            return "Bulletin ID must be a number."

        bulletin = self._bulletins.read(bulletin_id)

        if bulletin is None:
            return "Bulletin not found."

        return (
            f"Bulletin #{bulletin.id}\n"
            f"Author : {bulletin.author_name}\n"
            f"Subject: {bulletin.subject}\n"
            "\n"
            f"{bulletin.body}"
        )

    def _delete_bulletin(self, arguments: list[str]) -> str:
        """
        Delete a bulletin.

        Format:
            DB.id
        """

        return "Not yet implemented."