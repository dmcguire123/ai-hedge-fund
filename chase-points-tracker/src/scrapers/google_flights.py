from datetime import date

from src.models import Deal, DealType
from src.scrapers.base import BaseScraper


class GoogleFlightsScraper(BaseScraper):
    """Stub scraper for Google Flights award availability via transfer partners."""

    @property
    def name(self) -> str:
        return "Google Flights"

    def scrape(self) -> list[Deal]:
        # TODO: Implement real scraping logic.
        # For now, return sample deals to demonstrate the pipeline.
        return [
            Deal(
                deal_type=DealType.FLIGHT,
                source="google_flights",
                title="NYC to Tokyo round-trip (United MileagePlus)",
                origin="JFK",
                destination="NRT",
                travel_date=date(2026, 6, 15),
                return_date=date(2026, 6, 29),
                cash_price=1800.00,
                points_price=70000,
                transfer_partner="United",
            ),
            Deal(
                deal_type=DealType.FLIGHT,
                source="google_flights",
                title="SFO to London round-trip (Virgin Atlantic)",
                origin="SFO",
                destination="LHR",
                travel_date=date(2026, 7, 1),
                return_date=date(2026, 7, 14),
                cash_price=2400.00,
                points_price=90000,
                transfer_partner="Virgin Atlantic",
            ),
            Deal(
                deal_type=DealType.FLIGHT,
                source="google_flights",
                title="LAX to Cancun round-trip (Southwest via portal)",
                origin="LAX",
                destination="CUN",
                travel_date=date(2026, 5, 10),
                return_date=date(2026, 5, 17),
                cash_price=350.00,
                points_price=25000,
                transfer_partner=None,
            ),
        ]
