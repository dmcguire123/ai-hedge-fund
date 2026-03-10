import json
from datetime import datetime
from pathlib import Path

from src.config import DATA_DIR
from src.models import Deal, DealAlert


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _deals_path() -> Path:
    return DATA_DIR / "deals.json"


def _alerts_path() -> Path:
    return DATA_DIR / "alerts.json"


def _load_json(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path) as f:
        return json.load(f)


def _save_json(path: Path, data: list[dict]) -> None:
    _ensure_data_dir()
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)


def save_deals(deals: list[Deal]) -> None:
    """Append new deals to the store, deduplicating by key fields."""
    existing = _load_json(_deals_path())
    existing_keys = {
        (d["destination"], d["points_price"], d["source"])
        for d in existing
    }
    new_deals = [
        d.model_dump()
        for d in deals
        if (d.destination, d.points_price, d.source) not in existing_keys
    ]
    _save_json(_deals_path(), existing + new_deals)


def load_deals() -> list[Deal]:
    """Load all stored deals."""
    raw = _load_json(_deals_path())
    return [Deal(**d) for d in raw]


def save_alerts(alerts: list[DealAlert]) -> None:
    """Append new alerts to the store."""
    existing = _load_json(_alerts_path())
    new_alerts = [a.model_dump() for a in alerts]
    _save_json(_alerts_path(), existing + new_alerts)


def load_alerts() -> list[DealAlert]:
    """Load all stored alerts."""
    raw = _load_json(_alerts_path())
    return [DealAlert(**a) for a in raw]
