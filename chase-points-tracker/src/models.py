from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field, computed_field


class DealType(str, Enum):
    FLIGHT = "flight"
    HOTEL = "hotel"


class Deal(BaseModel):
    """A potential points redemption deal."""

    deal_type: DealType
    source: str = Field(description="Where the deal was found (e.g., 'google_flights', 'points_guy')")
    title: str = Field(description="Short description of the deal")
    origin: str | None = Field(default=None, description="Origin airport/city code (flights)")
    destination: str = Field(description="Destination airport/city or hotel name")
    travel_date: date | None = Field(default=None, description="Travel/check-in date")
    return_date: date | None = Field(default=None, description="Return/check-out date")
    cash_price: float = Field(description="Cash price in USD")
    points_price: int = Field(description="Points required for redemption")
    transfer_partner: str | None = Field(default=None, description="Transfer partner (e.g., 'Hyatt', 'United')")
    url: str | None = Field(default=None, description="Link to the deal")
    scraped_at: datetime = Field(default_factory=datetime.now)

    @computed_field
    @property
    def cents_per_point(self) -> float:
        """Calculate cents per point value."""
        if self.points_price <= 0:
            return 0.0
        return round(self.cash_price / self.points_price * 100, 2)


class DealAlert(BaseModel):
    """A flagged deal that meets the alert threshold."""

    deal: Deal
    reason: str = Field(description="Why this deal was flagged")
    portal_cpp: float = Field(default=1.5, description="Chase portal baseline cpp")
    alerted_at: datetime = Field(default_factory=datetime.now)

    @computed_field
    @property
    def savings_vs_portal(self) -> float:
        """Dollar savings compared to portal redemption at 1.5 cpp."""
        portal_cost_in_points = int(self.deal.cash_price / self.portal_cpp * 100)
        points_saved = portal_cost_in_points - self.deal.points_price
        return round(points_saved * self.portal_cpp / 100, 2)


class PointsConfig(BaseModel):
    """User configuration for points tracking."""

    points_balance: int = Field(default=100_000, description="Current UR points balance")
    cpp_threshold: float = Field(default=2.0, description="Minimum cpp to trigger an alert")
