import logging
from datetime import datetime

from sqlmodel import Session, select

from ..db import engine
from ..models import Performance
from .fomenki import FomenkiScraper

logger = logging.getLogger(__name__)


class ScraperManager:
    """Manages the execution of theater scrapers"""

    @staticmethod
    async def run_all_scrapers():
        """Run all theater scrapers and store their results"""
        logger.info(f"Starting scheduled scraping job at {datetime.now()}")

        try:
            scrapers = [FomenkiScraper()]
            results = []

            # Run all scrapers concurrently
            for scraper in scrapers:
                logger.info(f"Running scraper: {scraper.__class__.__name__}")
                try:
                    performances = await scraper.get_performances()
                    results.extend(performances)
                    logger.info(
                        f"Scraper {scraper.__class__.__name__} found {len(performances)} performances"
                    )
                except Exception as e:
                    logger.error(
                        f"Error in scraper {scraper.__class__.__name__}: {str(e)}"
                    )

            # Store results in database
            with Session(engine) as session:
                await ScraperManager.store_performances(session, results)

            logger.info(
                f"Scraping job completed. Total performances found: {len(results)}"
            )
            return len(results)

        except Exception as e:
            logger.error(f"Scraping job failed: {str(e)}")
            return 0

    @staticmethod
    async def store_performances(session: Session, performances: list[Performance]):
        """Store performances in database, avoiding duplicates"""
        for performance in performances:
            try:
                # Check if performance already exists
                query = select(Performance).where(
                    (Performance.title == performance.title)
                    & (Performance.stage_id == performance.stage_id)
                    & (Performance.datetime == performance.datetime)
                )
                existing_performance = session.exec(query).first()

                if not existing_performance:
                    session.add(performance)

            except Exception as e:
                logger.error(f"Error storing performance {performance.title}: {str(e)}")

        session.commit()
