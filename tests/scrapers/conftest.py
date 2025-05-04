from pathlib import Path

import pytest


@pytest.fixture
def html_content(request):
    def _get_content(theater_name):
        filename = f"{theater_name}_sample.html"
        current_file = Path(__file__)
        file_path = current_file.parent / "fixtures" / filename
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    return _get_content
