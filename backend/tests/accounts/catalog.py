from pathlib import Path
from unittest.mock import MagicMock, patch


CATALOG_HTML = Path(__file__).parent / "PennCoursePrograms.html"


def mock_catalog(test):
    """Serve the saved catalog page to the scrapers for the rest of the test."""
    response = MagicMock(text=CATALOG_HTML.read_text())
    for module in ("accounts.update_majors", "accounts.update_schools"):
        patcher = patch(f"{module}.requests")
        patcher.start().get.return_value = response
        test.addCleanup(patcher.stop)
