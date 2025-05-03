from abc import ABC, abstractmethod
from typing import Any

import httpx


class Scraper(ABC):
    """Base scraper class for theater repertoire data."""

    # Default headers for HTTP requests
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    def __init__(
        self,
        repertoire_url: str,
        theater_name: str,
    ):
        """
        Initialize the scraper with configurable URL and theater name.

        Args:
            repertoire_url: URL to the theater's repertoire page
            theater_name: Name identifier for the theater
        """
        self.repertoire_url = repertoire_url
        self.theater_name = theater_name

    async def scrape_repertoire(self) -> str | None:
        """
        Fetches HTML content from theater repertoire page.

        Returns:
            HTML content as string if successful, None otherwise
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.repertoire_url, headers=self.HEADERS)
                response.raise_for_status()
                return response.text

        except httpx.HTTPError as e:
            print(f"Error fetching data from {self.theater_name} theater: {e}")
            return None

    @abstractmethod
    async def parse_repertoire(self, html_content: str) -> Any:
        """
        Parse the HTML content and extract performance information.

        Args:
            html_content: HTML content from the theater's repertoire page

        Returns:
            Parsed performance data in the format specific to each theater

        Raises:
            ValueError: If the HTML content cannot be parsed correctly
        """
        pass

    async def get_performances(self) -> Any:
        """
        Performs the full scraping workflow: fetch and parse.

        Returns:
            Parsed performance data or None if scraping failed
        """
        html_content = await self.scrape_repertoire()
        if html_content:
            try:
                return await self.parse_repertoire(html_content)
            except ValueError:
                return None
        return None
