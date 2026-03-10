from abc import ABC, abstractmethod

from src.models import Deal


class BaseScraper(ABC):
    """Abstract base class for deal scrapers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of the scraper."""
        ...

    @abstractmethod
    def scrape(self) -> list[Deal]:
        """Scrape deals from the source. Returns a list of Deal objects."""
        ...
