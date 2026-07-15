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

    assert database.bulletins is not None

    service = BulletinService(database.bulletins)

    bulletin_id = service.post(
        author="CMBB",
        subject="Welcome",
        body="Welcome to Cumann Muscraí BBS.",
    )

    bulletin = service.read(bulletin_id)

    assert bulletin is not None
    assert bulletin.author == "CMBB"
    assert bulletin.subject == "Welcome"

    bulletins = service.list()

    assert len(bulletins) == 1

    service.delete(bulletin_id)

    assert service.read(bulletin_id) is None

    database.stop()

    if TEST_DATABASE.exists():
        TEST_DATABASE.unlink()