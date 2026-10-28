import sys
from pathlib import Path
from unittest.mock import patch

# Support running this test whether the FastAPI project is the repository root
# or is kept in the original ``Projcet_1`` subdirectory.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_DIRECTORY = PROJECT_ROOT / "Projcet_1"
if not APP_DIRECTORY.is_dir():
    APP_DIRECTORY = PROJECT_ROOT
sys.path.insert(0, str(APP_DIRECTORY))

from app import read_health


def test_health():
    """The health endpoint reports success when the database check succeeds."""
    with patch("app.database.check_connection") as check_connection:
        assert read_health() == {"status": "healthy", "database": "connected"}
        check_connection.assert_called_once_with()
