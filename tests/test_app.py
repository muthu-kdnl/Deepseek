from unittest.mock import patch

from app import read_health


def test_health():
    """The health endpoint reports success when the database check succeeds."""
    with patch("app.database.check_connection") as check_connection:
        assert read_health() == {"status": "healthy", "database": "connected"}
        check_connection.assert_called_once_with()
