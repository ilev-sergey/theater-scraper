import datetime
import re

from bs4 import BeautifulSoup
from bs4.element import Tag

from models import Performance

from .scraper import Scraper


class FomenkiScraper(Scraper):
    """
    Scraper for Fomenko Theater (Мастерская Петра Фоменко).
    Extracts performance names and datetimes from the timetable page.
    """

    def __init__(self):
        super().__init__(
            repertoire_url="https://fomenki.ru/timetable/",
            theater_name="fomenki",
        )

    async def _parse_month_year(self) -> tuple[int, int]:
        """
        Extract the current month and year from the HTML content.

        Returns:
            Tuple of (month, year) as integers
        """
        title_text = self.soup.head.find("title").text
        match = re.search(r"\s+(\w+)\s+(\d{4})", title_text)

        if not match:
            raise ValueError("Could not find month and year in the title")

        month_name = match.group(1)
        year = match.group(2)

        # Russian month names to numbers mapping
        ru_months = {
            "январь": 1,
            "февраль": 2,
            "март": 3,
            "апрель": 4,
            "май": 5,
            "июнь": 6,
            "июль": 7,
            "август": 8,
            "сентябрь": 9,
            "октябрь": 10,
            "ноябрь": 11,
            "декабрь": 12,
        }

        month_number = ru_months.get(month_name.lower(), None)

        return int(month_number), int(year)

    async def _parse_performance_day(self, event: Tag) -> int:
        """
        Extract performance info from a single event tag.

        Args:
            event: BeautifulSoup Tag object representing a single event

        Returns:
            Day as an integer
        """
        date_text = event.find("div", class_="date").text
        day = "".join(filter(str.isdigit, date_text))  # keep only number
        return int(day)

    async def _parse_performance_time(self, event: Tag) -> tuple[int, int]:
        """
        Extract performance time from a single event tag.

        Args:
            event: BeautifulSoup Tag object representing a single event

        Returns:
            Time as a tuple (hour, minute)
        """
        time_text = event.find("p", class_="time").text.replace("Премьера", "")

        hour, minute = time_text.split(":")
        return int(hour), int(minute)

    async def _parse_performance_name(self, event: Tag) -> str:
        """
        Extract performance name from a single event tag.

        Args:
            event: BeautifulSoup Tag object representing a single event

        Returns:
            Performance name as a string
        """
        return event.find("a").get("title")

    async def parse_repertoire(self, html_content: str) -> list[Performance]:
        """
        Parse the HTML content from Fomenki theater website and extract performance information.

        Args:
            html_content: HTML content from the theater's timetable page

        Returns:
            List of Performance objects with basic info (name and datetime)

        Raises:
            ValueError: If the HTML content cannot be parsed correctly
        """
        if not html_content:
            raise ValueError("Empty HTML content provided")

        self.soup = BeautifulSoup(html_content, "html.parser")

        month, year = await self._parse_month_year()

        performances = []

        events_container = self.soup.find("div", class_="events")
        events = events_container.find_all("div", class_="event")

        for event in events:
            day = await self._parse_performance_day(event)
            hour, minute = await self._parse_performance_time(event)
            datetime_obj = datetime.datetime(
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
            )
            performance_name = await self._parse_performance_name(event)
            performance = Performance(
                stage_id=1,
                title=performance_name,
                datetime=datetime_obj,
            )
            performances.append(performance)

        return performances
