"""
MeshBBS command router.
"""

from __future__ import annotations
from bbs.context import ExecutionContext
from bbs.services import bulletins
from bbs.services.bulletins import BulletinService, DeleteResult
from bbs.services.mail import MailService
from bbs.services.statistics import StatisticsService


class CommandRouter:
    """Routes MeshBBS commands to services."""

    def __init__(
        self,
        bulletins: BulletinService,
        mail: MailService,
        statistics: StatisticsService,
        context: ExecutionContext,
    ) -> None:
        self._bulletins = bulletins
        self._mail = mail
        self._statistics = statistics
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
           return self._help(arguments)

        if opcode == "LB":
            return self._list_bulletins()

        if opcode == "PB":
            return self._post_bulletin(arguments)

        if opcode == "RB":
            return self._read_bulletin(arguments)
        
        if opcode == "LDB":
            return self._list_deletable_bulletins()

        if opcode == "DB":
            return self._delete_bulletin(arguments)

        if opcode == "LM":
            return self._list_mail()

        if opcode == "SM":
            return self._send_mail(arguments)

        if opcode == "RM":
            return self._read_mail(arguments)

        if opcode == "DM":
            return self._delete_mail(arguments)
        
        if opcode == "ST":
            return self._statistics_summary()

        return f"Unknown command: {opcode}"

    def _help(
        self,
        arguments: list[str],
    ) -> str:
        """Return one of the help pages."""

        if not arguments:
            return (
                "Cumann Mhúscraí BBS\n"
                "\n"
                "Most users navigate using the menus.\n"
                "Quick Commands provide faster access.\n"
                "\n"
                "Bulletins\n"
                "----------\n"
                "LB  List Bulletins\n"
                "\n"
                "PB  Post Bulletin\n"
                "PB.[subject].[body]\n"
                "e.g. PB.Storm.Warning in effect.\n"
                "\n"
                "RB  Read Bulletin\n"
                "RB.[id]\n"
                "e.g. RB.12\n"
                "\n"
                "[N]ext for page 2"
            )

        if arguments == ["2"]:
            return (
                "Bulletins (cont.)\n"
                "\n"
                "DB  Delete Bulletin\n"
                "DB.[id]\n"
                "e.g. DB.12\n"
                "\n"
                "Mail\n"
                "----\n"
                "LM  List Mail\n"
                "\n"
                "SM  Send Mail\n"
                "SM.[recipient].[subject].[body]\n"
                "e.g. SM.MBBS.Hello.Great BBS!\n"
                "\n"
                "RM  Read Mail\n"
                "RM.[id]\n"
                "e.g. RM.3\n"
                "\n"
                "DM  Delete Mail\n"
                "DM.[id]\n"
                "e.g. DM.3"
            )

        return "Usage: HELP or HELP.2"

    # ------------------------------------------------------------------
    # Bulletin Commands
    # ------------------------------------------------------------------

    def _list_bulletins(self) -> str:
        bulletins, read_ids = self._bulletins.list(
            self._context,
        )

        if not bulletins:
            return "Bulletins\n----------\n\nNo bulletins."

        lines = [
            "Bulletins",
            "----------",
            "",
        ]

        for bulletin in bulletins:
            marker = " " if bulletin.id in read_ids else "*"

            lines.append(
                f"{marker} {bulletin.id:>3} {bulletin.author_name:<8} {bulletin.subject}"
            )

        return "\n".join(lines)
    
    def _list_deletable_bulletins(self) -> str:
        """
        List bulletins that the current user may delete.

        Normal users:
            Only their own bulletins.

        Administrators:
            All bulletins.
        """

        bulletins, _ = self._bulletins.list(self._context)

        if self._context.is_admin:
            deletable = bulletins
        else:
            deletable = [
                bulletin
                for bulletin in bulletins
                if bulletin.author_node_id == self._context.node_id
            ]

        if not deletable:
            return (
                "Delete Bulletins\n"
                "-----------------\n\n"
                "You have no bulletins that can be deleted."
            )

        lines = [
            "Delete Bulletins",
            "-----------------",
            "",
        ]

        for bulletin in deletable:

            if self._context.is_admin:
                lines.append(
                    f"{bulletin.id:>3} {bulletin.author_name:<8} {bulletin.subject}"
                )
            else:
                lines.append(
                    f"{bulletin.id:>3} {bulletin.subject}"
                )

        return "\n".join(lines)

    def _post_bulletin(
        self,
        arguments: list[str],
    ) -> str:
        """
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

    def _read_bulletin(
        self,
        arguments: list[str],
    ) -> str:
        """
        Format:

            RB.id
        """

        if len(arguments) != 1:
            return "Usage: RB.id"

        try:
            bulletin_id = int(arguments[0])
        except ValueError:
            return "Bulletin ID must be a number."

        bulletin = self._bulletins.read(bulletin_id, 
                                        self._context,
        )
        

        if bulletin is None:
            return "Bulletin not found."

        return (
            f"Bulletin #{bulletin.id}\n"
            f"Author : {bulletin.author_name}\n"
            f"Subject: {bulletin.subject}\n"
            "\n"
            f"{bulletin.body}"
        )

    def _delete_bulletin(
        self,
        arguments: list[str],
    ) -> str:
        """
        Format:

            DB.id
        """

        if len(arguments) != 1:
            return "Usage: DB.id"

        try:
            bulletin_id = int(arguments[0])
        except ValueError:
            return "Bulletin ID must be a number."

        result = self._bulletins.delete(
            bulletin_id,
            self._context,
        )

        if result is DeleteResult.NOT_FOUND:
            return "Bulletin not found."

        if result is DeleteResult.PERMISSION_DENIED:
            return "Permission denied."

        return "Bulletin deleted."

    # ------------------------------------------------------------------
    # Mail Commands
    # ------------------------------------------------------------------
    def _list_mail(self) -> str:
        """
        List the authenticated user's inbox.
        """

        messages = self._mail.list(self._context)

        if not messages:
            return "No mail."

        lines = []

        for message in messages:
            status = " " if message.read_at else "*"

            lines.append(
                f"{status}{message.id:3} "
                f"{message.sender_node_id:12} "
                f"{message.subject}"
            )

        return "\n".join(lines)

    def _send_mail(
        self,
        arguments: list[str],
    ) -> str:
        """
        Format:

            SM.recipient.subject.body
        """

        if len(arguments) != 3:
            return "Usage: SM.recipient.subject.body"

        try:
            mail_id = self._mail.send(
                context=self._context,
                recipient_short_name=arguments[0],
                subject=arguments[1],
                body=arguments[2],
            )
        except ValueError as error:
            return str(error)

        return f"Mail #{mail_id} sent."

    def _read_mail(
        self,
        arguments: list[str],
    ) -> str:
        """
        Format:

            RM.id
        """

        if len(arguments) != 1:
            return "Usage: RM.id"

        try:
            mail_id = int(arguments[0])
        except ValueError:
            return "Mail ID must be a number."

        mail = self._mail.read(mail_id)

        if mail is None:
            return "Mail not found."

        return (
            f"Mail #{mail.id}\n"
            f"From   : {mail.sender_node_id}\n"
            f"Subject: {mail.subject}\n"
            "\n"
            f"{mail.body}"
        )

    def _delete_mail(
        self,
        arguments: list[str],
    ) -> str:
        """
        Format:

            DM.id
        """

        if len(arguments) != 1:
            return "Usage: DM.id"

        try:
            mail_id = int(arguments[0])
        except ValueError:
            return "Mail ID must be a number."

        try:
            self._mail.delete(
                mail_id,
                self._context,
            )
        except PermissionError as error:
            return str(error)

        return "Mail deleted."
    
    def _statistics_summary(self) -> str:
        """Return MeshBBS statistics."""

        stats = self._statistics.summary()

        return (
            "MeshBBS Statistics\n"
            "\n"
            f"Users......{stats['users']}\n"
            f"Bulletins..{stats['bulletins']}\n"
            f"Mail.......{stats['mail']}\n"
            f"Uptime.....{stats['uptime']}"
        )