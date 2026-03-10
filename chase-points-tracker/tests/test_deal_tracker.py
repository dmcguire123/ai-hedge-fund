from src.deal_tracker import evaluate_deals
from src.models import Deal, DealType, PointsConfig


def _make_deal(cash_price: float, points_price: int, **kwargs) -> Deal:
    defaults = dict(
        deal_type=DealType.FLIGHT,
        source="test",
        title="Test deal",
        destination="TEST",
    )
    defaults.update(kwargs)
    return Deal(cash_price=cash_price, points_price=points_price, **defaults)


def test_evaluate_deals_filters_below_threshold():
    config = PointsConfig(cpp_threshold=2.0, points_balance=200000)
    deals = [
        _make_deal(cash_price=150.0, points_price=10000),   # 1.5 cpp — below
        _make_deal(cash_price=300.0, points_price=10000),   # 3.0 cpp — above
    ]
    alerts = evaluate_deals(deals, config)
    assert len(alerts) == 1
    assert alerts[0].deal.cents_per_point == 3.0


def test_evaluate_deals_sorted_by_cpp_descending():
    config = PointsConfig(cpp_threshold=2.0, points_balance=500000)
    deals = [
        _make_deal(cash_price=200.0, points_price=8000),    # 2.5 cpp
        _make_deal(cash_price=500.0, points_price=10000),   # 5.0 cpp
        _make_deal(cash_price=250.0, points_price=10000),   # 2.5 cpp
    ]
    alerts = evaluate_deals(deals, config)
    assert len(alerts) == 3
    cpps = [a.deal.cents_per_point for a in alerts]
    assert cpps == sorted(cpps, reverse=True)


def test_evaluate_deals_empty():
    config = PointsConfig()
    alerts = evaluate_deals([], config)
    assert alerts == []


def test_evaluate_deals_notes_insufficient_points():
    config = PointsConfig(cpp_threshold=2.0, points_balance=5000)
    deals = [
        _make_deal(cash_price=500.0, points_price=10000),   # 5.0 cpp, but needs 10k points
    ]
    alerts = evaluate_deals(deals, config)
    assert len(alerts) == 1
    assert "insufficient points" in alerts[0].reason


def test_evaluate_deals_exceptional_reason():
    config = PointsConfig(cpp_threshold=2.0, points_balance=200000)
    deals = [
        _make_deal(cash_price=500.0, points_price=10000, transfer_partner="United"),
    ]
    alerts = evaluate_deals(deals, config)
    assert "Exceptional" in alerts[0].reason
    assert "United" in alerts[0].reason
