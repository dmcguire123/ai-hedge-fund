from datetime import datetime, timedelta

import httpx

from auth.strava_auth import get_valid_access_token

BASE_URL = "https://www.strava.com/api/v3"


async def get_activities(limit: int = 20) -> list[dict]:
    token = await get_valid_access_token()
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BASE_URL}/athlete/activities",
            headers={"Authorization": f"Bearer {token}"},
            params={"per_page": limit, "page": 1},
        )
        resp.raise_for_status()
        activities = resp.json()

    result = []
    for act in activities:
        result.append({
            "id": act["id"],
            "name": act["name"],
            "type": act["sport_type"],
            "start_date": act["start_date_local"],
            "distance_meters": act.get("distance", 0),
            "duration_seconds": act.get("moving_time", 0),
            "elevation_gain": act.get("total_elevation_gain", 0),
            "avg_speed_mps": act.get("average_speed", 0),
            "max_speed_mps": act.get("max_speed", 0),
            "avg_heart_rate": act.get("average_heartrate"),
            "max_heart_rate": act.get("max_heartrate"),
            "calories": act.get("calories"),
            "kudos": act.get("kudos_count", 0),
            "map_polyline": act.get("map", {}).get("summary_polyline"),
        })
    return result


async def get_athlete_stats() -> dict:
    token = await get_valid_access_token()
    async with httpx.AsyncClient() as client:
        # Get athlete ID first
        athlete_resp = await client.get(
            f"{BASE_URL}/athlete",
            headers={"Authorization": f"Bearer {token}"},
        )
        athlete_resp.raise_for_status()
        athlete_id = athlete_resp.json()["id"]

        stats_resp = await client.get(
            f"{BASE_URL}/athletes/{athlete_id}/stats",
            headers={"Authorization": f"Bearer {token}"},
        )
        stats_resp.raise_for_status()
        stats = stats_resp.json()

    return {
        "ytd_run_distance": stats.get("ytd_run_totals", {}).get("distance", 0),
        "ytd_ride_distance": stats.get("ytd_ride_totals", {}).get("distance", 0),
        "ytd_swim_distance": stats.get("ytd_swim_totals", {}).get("distance", 0),
        "all_run_distance": stats.get("all_run_totals", {}).get("distance", 0),
        "all_ride_distance": stats.get("all_ride_totals", {}).get("distance", 0),
        "recent_run_distance": stats.get("recent_run_totals", {}).get("distance", 0),
        "recent_ride_distance": stats.get("recent_ride_totals", {}).get("distance", 0),
    }


async def get_weekly_activity_summary(weeks: int = 8) -> list[dict]:
    """Group activities by week for chart display."""
    activities = await get_activities(limit=100)
    weeks_data: dict[str, dict] = {}

    for act in activities:
        dt = datetime.fromisoformat(act["start_date"].replace("Z", ""))
        monday = (dt - timedelta(days=dt.weekday())).date().isoformat()
        if monday not in weeks_data:
            weeks_data[monday] = {"week": monday, "distance_meters": 0, "count": 0, "duration_seconds": 0}
        weeks_data[monday]["distance_meters"] += act["distance_meters"]
        weeks_data[monday]["duration_seconds"] += act["duration_seconds"]
        weeks_data[monday]["count"] += 1

    sorted_weeks = sorted(weeks_data.values(), key=lambda x: x["week"])
    return sorted_weeks[-weeks:]
