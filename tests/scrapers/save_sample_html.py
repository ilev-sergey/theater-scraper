# save_sample_html.py
import asyncio
import logging
import os
from pathlib import Path

# explicitly import scrapers for subclasses to be recognized
from scrapers.fomenki import FomenkiScraper
from scrapers.scraper import Scraper

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def save_html():
    fixtures_dir = Path(__file__).parent / "fixtures"
    os.makedirs(fixtures_dir, exist_ok=True)

    results = []

    for scraper_class in Scraper.__subclasses__():
        scraper = scraper_class()
        class_name = scraper_class.__name__.lower().replace("scraper", "")
        filename = f"{class_name}_sample.html"
        file_path = fixtures_dir / filename

        html = await scraper.scrape_repertoire()

        if not html:
            logger.error(f"Failed to fetch HTML for {class_name}")
            continue

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

        logger.info(f"HTML saved to {file_path}")
        results.append(f"Saved {class_name} HTML")

    return results


if __name__ == "__main__":
    results = asyncio.run(save_html())
    for result in results:
        logger.info(result)
