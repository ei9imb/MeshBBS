"""
MeshBBS Application

Coordinates the lifecycle of all MeshBBS components.
"""

from __future__ import annotations

from bbs.commands.router import CommandRouter
from bbs.config import Config
from bbs.context import ExecutionContext
from bbs.database import Database
from bbs.logger import get_logger
from bbs.models import User
from bbs.services.bulletins import BulletinService
from bbs.services.mail import MailService
from bbs.ui.cli import CommandLineInterface
from bbs.services.statistics import StatisticsService
from bbs.services.users import UserService
from bbs.session import SessionManager


class MeshBBS:
    """
    Main application class.
    """

    def __init__(self) -> None:
        self.config = Config()
        self.logger = get_logger(__name__)

        self.database = Database()

        self.sessions = SessionManager()

        self.components = [
            self.database,
        ]

    def start(self) -> None:
        """Start the application."""

        self.logger.info("Starting MeshBBS")

        name = self.config.get("name")
        version = self.config.get("version")

        self.logger.info("%s v%s", name, version)

        for component in self.components:
            component.start()

    def stop(self) -> None:
        """Stop the application."""

        for component in reversed(self.components):
            component.stop()

        self.logger.info("Stopping MeshBBS")

    def _build_router(
        self,
        context: ExecutionContext,
        users: UserService,
    ) -> CommandRouter:
        """
        Build a command router for the supplied execution
        context.
        """

        if self.database.users is None:
            raise RuntimeError(
                "User repository not initialised"
            )

        assert self.database.bulletins is not None
        assert self.database.mail is not None

        bulletin_service = BulletinService(
            self.database.bulletins,
        )

        mail_service = MailService(
            mail=self.database.mail,
            users=self.database.users,
        )

        statistics_service = StatisticsService(
            users=self.database.users,
            bulletins=self.database.bulletins,
            mail=self.database.mail,
        )

        return CommandRouter(
            bulletins=bulletin_service,
            mail=mail_service,
            users=users,
            statistics=statistics_service,
            context=context,
        )
    
    def handle_message(
        self,
        node_id: str,
        short_name: str,
        long_name: str,
        message: str,
    ) -> str:
        """
        Process a message received from a transport and
        return the reply.
        """

        if self.database.users is None:
            raise RuntimeError(
                "User repository not initialised"
            )

        users = UserService(
            self.database.users,
        )

        user = users.ensure_user(
            node_id=node_id,
            short_name=short_name,
            long_name=long_name,
        )

        self.sessions.get_or_create(
            node_id,
        )

        context = ExecutionContext(
            node_id=user.node_id,
            short_name=user.short_name,
            long_name=user.long_name,
            is_admin=user.is_admin,
        )

        router = self._build_router(
            context,
            users,
        )

        return router.execute(
            message,
        )    


    def run(self) -> None:
        """Run the application."""

        self.start()

        try:
            if self.database.users is None:
                raise RuntimeError("User repository not initialised")
            assert self.database.bulletins is not None
            assert self.database.mail is not None

            if self.database.users.get("!LOCALDEV") is None:
                self.database.users.add(
                    User(
                        node_id="!LOCALDEV",
                        short_name="MBBS",
                        long_name="Cumann Mhúscraí BBS",
                        first_seen="2026-07-16T00:00:00",
                        last_seen="2026-07-16T00:00:00",
                    )
                )

            self.database.users.add(
                User(
                    node_id="!TEST001",
                    short_name="TUSER1",
                    long_name="Test User 1",
                    first_seen="2026-07-16T00:00:00",
                    last_seen="2026-07-16T00:00:00",
                )
            )

            context = ExecutionContext(
                node_id="!LOCALDEV",
                short_name="MBBS",
                long_name="Cumann Mhúscraí BBS",
                is_admin=True,
            )

            router = self._build_router(
                context,
                UserService(
                    self.database.users,
                ),
            )

            cli = CommandLineInterface(router)

            self.logger.info("MeshBBS is running")

            cli.run()

        except Exception:
            self.logger.exception("Unhandled exception")
            raise
        finally:
            self.stop()