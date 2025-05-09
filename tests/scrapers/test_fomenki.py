import datetime

import pytest

from src.scrapers.fomenki import FomenkiScraper


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def fomenki_scraper():
    return FomenkiScraper()


@pytest.mark.anyio
async def test_get_performances(fomenki_scraper, html_content, mocker):
    fonemki_html = html_content("fomenki")
    if not fonemki_html:
        pytest.skip(
            "No HTML content available for Fomenki. Use save_sample_html.py to fetch it."
        )

    # Mock db call
    mock_get_stage_id = mocker.patch(
        "src.services.stage_service.StageService.get_stage_id_by_name"
    )
    mock_get_stage_id.return_value = 1

    performances = await fomenki_scraper.parse_repertoire(fonemki_html)
    assert isinstance(performances, list), "Expected a list of performances"
    assert len(performances) > 0, "Expected at least one performance"
    assert performances[0].stage_id == 1
    assert performances[0].title == "Приречная страна"
    assert performances[0].datetime == datetime.datetime(
        year=2025, month=5, day=1, hour=14, minute=0
    )
