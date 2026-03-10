from datetime import date

from src.models import Deal, DealType
from src.scrapers.base import BaseScraper


class PointsGuyScraper(BaseScraper):
    """Stub scraper for The Points Guy deal alerts."""

    @property
    def name(self) -> str:
        return "The Points Guy"

    def scrape(self) -> list[Deal]:
        # TODO: Implement real scraping of TPG deal posts.
        return [
            Deal(
                deal_type=DealType.FLIGHT,
                source="points_guy",
                title="FLASH: Business class to Paris via Air France (Flying Blue)",
                origin="JFK",
                destination="CDG",
                travel_date=date(2026, 5, 20),
                return_date=date(2026, 5, 30),
                cash_price=4500.00,
                points_price=120000,
                transfer_partner="Air France (Flying Blue)",
            ),
            Deal(
                deal_type=DealType.HOTEL,
                source="points_guy",
                title="Hyatt all-inclusive Cancun - 5 nights",
                destination="Cancun (Hyatt Ziva)",
                travel_date=date(2026, 7, 5),
                return_date=date(2026, 7, 10),
                cash_price=2800.00,
                points_price=125000,
                transfer_partner="Hyatt",
            ),
        ]
