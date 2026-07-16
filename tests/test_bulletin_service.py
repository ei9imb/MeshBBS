"""
Tests for the MeshBBS bulletin service.
"""

from __future__ import annotations

from pathlib import Path

from bbs.database import Database
from bbs.services.bulletins import BulletinService


TEST_DATABASE = Path("data") / "test_meshbbs.db"


def test_post_read_list_delete() -> None:
    """Verify bulletin service operations."""

    if TEST_DATABASE.exists():
        TEST_DATABASE.unlink()

    database = Database(TEST_DATABASE)
    database.start()

    try:
        assert database.bulletins is not None

        service = BulletinService(database.bulletins)

        bulletin_id = service.post(
            author_node_id="!12345678",
            author_name="CMBB",
            subject="Welcome",
            body="Welcome to Cumann Muscraí BBS.",
        )

        bulletin = service.read(bulletin_id)

        assert bulletin is not None
        assert bulletin.author_node_id == "!12345678"
        assert bulletin.author_name == "CMBB"
        assert bulletin.subject == "Welcome"

        bulletins = service.list()

        assert len(bulletins) == 1

        service.delete(bulletin_id)

        assert service.read(bulletin_id) is None

    finally:
        database.stop()

        if TEST_DATABASE.exists():
            TEST_DATABASE.unlink()