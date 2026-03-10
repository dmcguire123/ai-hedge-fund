from datetime import date

from src.models import Deal, DealAlert, DealType, PointsConfig


def test_deal_cents_per_point():
    deal = Deal(
        deal_type=DealType.FLIGHT,
        source="test",
        title="Test flight",
        destination="NRT",
        cash_price=1800.00,
        points_price=70000,
    )
    assert deal.cents_per_point == 2.57


def test_deal_cents_per_point_zero_points():
    deal = Deal(
        deal_type=DealType.FLIGHT,
        source="test",
        title="Test",
        destination="NRT",
        cash_price=100.0,
        points_price=0,
    )
    assert deal.cents_per_point == 0.0


def test_deal_alert_savings_positive():
    deal = Deal(
        deal_type=DealType.FLIGHT,
        source="test",
        title="Good deal",
        destination="NRT",
        cash_price=1800.00,
        points_price=70000,
    )
    alert = DealAlert(deal=deal, reason="Great value")
    # Portal would cost 1800/1.5*100 = 120000 points
    # Savings: (120000 - 70000) * 1.5 / 100 = 750.0
    assert alert.savings_vs_portal == 750.0


def test_deal_alert_savings_negative():
    deal = Deal(
        deal_type=DealType.HOTEL,
        source="test",
        title="Bad deal",
        destination="Hotel",
        cash_price=100.00,
        points_price=100000,
    )
    alert = DealAlert(deal=deal, reason="Test")
    assert alert.savings_vs_portal < 0


def test_points_config_defaults():
    config = PointsConfig()
    assert config.points_balance == 100_000
    assert config.cpp_threshold == 2.0
