import time
from datetime import datetime, timedelta

import httpx

from auth.google_auth import get_valid_access_token

BASE_URL = "https://www.googleapis.com/fitness/v1/users/me"

# Google Fit data type names
WEIGHT_TYPE = "com.google.weight"
BODY_FAT_TYPE = "com.google.body.fat.percentage"
BMI_TYPE = "com.google.body.mass.index"


def _ms(dt: datetime) -> int:
    return int(dt.timestamp() * 1000)


async def _aggregate(data_type_name: str, start: datetime, end: datetime) -> list[dict]:
    token = await get_valid_access_token()
    body = {
        "aggregateBy": [{"dataTypeName": data_type_name}],
        "bucketByTime": {"durationMillis": 86400000},  # 1 day buckets
        "startTimeMillis": _ms(start),
        "endTimeMillis": _ms(end),
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{BASE_URL}/dataset:aggregate",
            headers={"Authorization": f"Bearer {token}"},
            json=body,
        )
        resp.raise_for_status()
        return resp.json().get("bucket", [])


def _extract_fp_value(bucket: dict) -> float | None:
    """Extract a floating point value from a Google Fit bucket."""
    for dataset in bucket.get("dataset", []):
        for point in dataset.get("point", []):
            for val in point.get("value", []):
                fp = val.get("fpVal")
                if fp is not None:
                    return round(fp, 2)
    return None


async def get_weight_history(days: int = 90) -> list[dict]:
    end = datetime.now()
    start = end - timedelta(days=days)
    buckets = await _aggregate(WEIGHT_TYPE, start, end)

    results = []
    for bucket in buckets:
        value = _extract_fp_value(bucket)
        if value is not None:
            dt = datetime.fromtimestamp(int(bucket["startTimeMillis"]) / 1000)
            results.append({"date": dt.date().isoformat(), "weight_kg": value})
    return results


async def get_body_fat_history(days: int = 90) -> list[dict]:
    end = datetime.now()
    start = end - timedelta(days=days)
    buckets = await _aggregate(BODY_FAT_TYPE, start, end)

    results = []
    for bucket in buckets:
        value = _extract_fp_value(bucket)
        if value is not None:
            dt = datetime.fromtimestamp(int(bucket["startTimeMillis"]) / 1000)
            results.append({"date": dt.date().isoformat(), "body_fat_pct": value})
    return results


async def get_latest_body_metrics() -> dict:
    weights = await get_weight_history(days=30)
    body_fat = await get_body_fat_history(days=30)

    latest_weight = weights[-1] if weights else None
    latest_bf = body_fat[-1] if body_fat else None

    # Calculate BMI if we have weight (need height from user — we'll return raw weight)
    return {
        "weight_kg": latest_weight["weight_kg"] if latest_weight else None,
        "weight_date": latest_weight["date"] if latest_weight else None,
        "body_fat_pct": latest_bf["body_fat_pct"] if latest_bf else None,
        "body_fat_date": latest_bf["date"] if latest_bf else None,
    }
