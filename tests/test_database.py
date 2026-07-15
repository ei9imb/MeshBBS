"""
Tests for the MeshBBS database component.
"""

from __future__ import annotations

from pathlib import Path

from bbs.database import Database
from bbs.models import User


TEST_DATABASE = Path("data") / "test_meshbbs.db"


def test_add_and_get_user() -> None:
    """Verify a user can be stored and retrieved."""

    if TEST_DATABASE.exists():
        TEST_DATABASE.unlink()

    database = Database(TEST_DATABASE)
    database.start()

    assert database.users is not None

    user = User(
        node_id="!12345678",
        short_name="EI9IMB",
        long_name="Cumann Muscrai",
        first_seen="2026-07-15T18:30:00",
        last_seen="2026-07-15T18:30:00",
    )

    database.users.add(user)

    loaded = database.users.get(user.node_id)

    assert loaded is not None
    assert loaded.node_id == user.node_id
    assert loaded.short_name == user.short_name
    assert loaded.long_name == user.long_name

    database.stop()

    assert TEST_DATABASE.exists()

    TEST_DATABASE.unlink()