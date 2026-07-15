"""
Tests for the MeshBBS bulletin repository.
"""

from __future__ import annotations

from pathlib import Path

from bbs.database import Database
from bbs.models import Bulletin


TEST_DATABASE = Path("data") / "test_meshbbs.db"


def test_bulletin_repository() -> None:
    """Verify bulletin CRUD operations."""

    if TEST_DATABASE.exists():
        TEST_DATABASE.unlink()

    database = Database(TEST_DATABASE)
    database.start()

    assert database.bulletins is not None

    bulletin = Bulletin(
        id=None,
        author="EI9IMB",
        subject="Welcome",
        body="Welcome to Cumann Muscraí BBS.",
        created="2026-07-15T21:00:00",
    )

    bulletin_id = database.bulletins.add(bulletin)

    loaded = database.bulletins.get(bulletin_id)

    assert loaded is not None
    assert loaded.id == bulletin_id
    assert loaded.author == bulletin.author
    assert loaded.subject == bulletin.subject
    assert loaded.body == bulletin.body

    bulletins = database.bulletins.get_all()

    assert len(bulletins) == 1
    assert bulletins[0].id == bulletin_id

    database.bulletins.delete(bulletin_id)

    assert database.bulletins.get(bulletin_id) is None

    database.stop()

    if TEST_DATABASE.exists():
        TEST_DATABASE.unlink()