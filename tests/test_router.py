"""
Tests for the MeshBBS command router.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from bbs.commands.router import CommandRouter
from bbs.context import ExecutionContext
from bbs.database import Database
from bbs.services.bulletins import BulletinService
from bbs.services.mail import MailService


TEST_DATABASE = Path("data") / "test_meshbbs.db"


@pytest.fixture
def router() -> CommandRouter:
    """Create a command router backed by a temporary database."""

    if TEST_DATABASE.exists():
        TEST_DATABASE.unlink()

    database = Database(TEST_DATABASE)
    database.start()

    try:
        assert database.bulletins is not None
        assert database.mail is not None
        assert database.users is not None

        bulletin_service = BulletinService(
            database.bulletins,
        )

        mail_service = MailService(
            mail=database.mail,
            users=database.users,
        )

        context = ExecutionContext(
            node_id="!12345678",
            short_name="DMA",
            long_name="Domhnall",
            is_admin=True,
        )

        yield CommandRouter(
            bulletins=bulletin_service,
            mail=mail_service,
            context=context,
        )

    finally:
        database.stop()

        if TEST_DATABASE.exists():
            TEST_DATABASE.unlink()


def test_help_command(router: CommandRouter) -> None:
    """Verify HELP returns the command list."""

    response = router.execute("HELP")

    assert "LB" in response
    assert "PB" in response
    assert "LM" in response
    assert "SM" in response


def test_list_bulletins_empty(router: CommandRouter) -> None:
    """Verify LB reports an empty bulletin board."""

    response = router.execute("LB")

    assert response == "No bulletins."


def test_post_bulletin_uses_authenticated_user(
    router: CommandRouter,
) -> None:
    """Verify PB uses the authenticated user as the author."""

    response = router.execute(
        "PB.Welcome.Hello MeshBBS"
    )

    assert response == "Bulletin #1 posted."

    bulletin = router._bulletins.read(1)

    assert bulletin is not None
    assert bulletin.author_node_id == "!12345678"
    assert bulletin.author_name == "DMA"
    assert bulletin.subject == "Welcome"
    assert bulletin.body == "Hello MeshBBS"


def test_read_bulletin(router: CommandRouter) -> None:
    """Verify RB returns a bulletin."""

    router.execute(
        "PB.Welcome.Hello MeshBBS"
    )

    response = router.execute("RB.1")

    assert "Bulletin #1" in response
    assert "DMA" in response
    assert "Welcome" in response
    assert "Hello MeshBBS" in response