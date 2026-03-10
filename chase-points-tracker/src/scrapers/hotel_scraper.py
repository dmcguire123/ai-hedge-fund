from datetime import date

from src.models import Deal, DealType
from src.scrapers.base import BaseScraper


class HotelScraper(BaseScraper):
    """Stub scraper for hotel transfer partner deals (Hyatt, IHG, Marriott)."""

    @property
    def name(self) -> str:
        return "Hotel Deals"

    def scrape(self) -> list[Deal]:
        # TODO: Implement real scraping logic.
        return [
            Deal(
                deal_type=DealType.HOTEL,
                source="hotel_scraper",
                title="Park Hyatt Maldives - 4 nights",
                destination="Maldives (Park Hyatt)",
                travel_date=date(2026, 8, 1),
                return_date=date(2026, 8, 5),
                cash_price=3200.00,
                points_price=100000,
                transfer_partner="Hyatt",
            ),
            Deal(
                deal_type=DealType.HOTEL,
                source="hotel_scraper",
                title="Hyatt Regency Maui - 3 nights",
                destination="Maui (Hyatt Regency)",
                travel_date=date(2026, 6, 20),
                return_date=date(2026, 6, 23),
                cash_price=1050.00,
                points_price=60000,
                transfer_partner="Hyatt",
            ),
            Deal(
                deal_type=DealType.HOTEL,
                source="hotel_scraper",
                title="IHG Intercontinental Bora Bora - 2 nights",
                destination="Bora Bora (Intercontinental)",
                travel_date=date(2026, 9, 10),
                return_date=date(2026, 9, 12),
                cash_price=1400.00,
                points_price=140000,
                transfer_partner="IHG",
            ),
        ]
