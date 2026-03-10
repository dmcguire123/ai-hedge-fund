from src.models import Deal, DealAlert, PointsConfig
from src.scrapers import ALL_SCRAPERS


def evaluate_deals(deals: list[Deal], config: PointsConfig) -> list[DealAlert]:
    """Evaluate deals and return alerts for those above the cpp threshold."""
    alerts: list[DealAlert] = []

    for deal in deals:
        cpp = deal.cents_per_point
        if cpp < config.cpp_threshold:
            continue

        # Check if user has enough points
        affordable = deal.points_price <= config.points_balance
        affordability_note = "" if affordable else " (insufficient points)"

        if cpp >= 3.0:
            reason = f"Exceptional value: {cpp} cpp via {deal.transfer_partner or 'portal'}{affordability_note}"
        elif cpp >= 2.5:
            reason = f"Great value: {cpp} cpp via {deal.transfer_partner or 'portal'}{affordability_note}"
        else:
            reason = f"Good value: {cpp} cpp via {deal.transfer_partner or 'portal'}{affordability_note}"

        alerts.append(DealAlert(deal=deal, reason=reason))

    # Sort by cpp descending — best deals first
    alerts.sort(key=lambda a: a.deal.cents_per_point, reverse=True)
    return alerts


def scan_for_deals(config: PointsConfig) -> tuple[list[Deal], list[DealAlert]]:
    """Run all scrapers and evaluate the results."""
    all_deals: list[Deal] = []
    for scraper_cls in ALL_SCRAPERS:
        scraper = scraper_cls()
        deals = scraper.scrape()
        all_deals.extend(deals)

    alerts = evaluate_deals(all_deals, config)
    return all_deals, alerts
