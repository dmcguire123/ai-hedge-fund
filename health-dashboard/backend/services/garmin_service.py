import os
from datetime import date, timedelta

from garminconnect import Garmin


def _client() -> Garmin:
    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")
    if not email or not password:
        raise ValueError("GARMIN_EMAIL and GARMIN_PASSWORD must be set in .env")
    client = Garmin(email, password)
    client.login()
    return client


def get_today_stats() -> dict:
    client = _client()
    today = date.today().isoformat()
    stats = client.get_stats(today)
    return {
        "steps": stats.get("totalSteps", 0),
        "calories": stats.get("totalKilocalories", 0),
        "active_calories": stats.get("activeKilocalories", 0),
        "distance_meters": stats.get("totalDistanceMeters", 0),
        "active_seconds": stats.get("highlyActiveSeconds", 0) + stats.get("activeSeconds", 0),
        "floors": stats.get("floorsAscended", 0),
        "resting_heart_rate": stats.get("restingHeartRate"),
        "stress_avg": stats.get("averageStressLevel"),
        "date": today,
    }


def get_sleep(days: int = 7) -> list[dict]:
    client = _client()
    results = []
    for i in range(days):
        day = (date.today() - timedelta(days=i)).isoformat()
        try:
            sleep = client.get_sleep_data(day)
            daily = sleep.get("dailySleepDTO", {})
            results.append({
                "date": day,
                "duration_seconds": daily.get("sleepTimeSeconds", 0),
                "deep_seconds": daily.get("deepSleepSeconds", 0),
                "light_seconds": daily.get("lightSleepSeconds", 0),
                "rem_seconds": daily.get("remSleepSeconds", 0),
                "awake_seconds": daily.get("awakeSleepSeconds", 0),
                "score": daily.get("sleepScores", {}).get("overall", {}).get("value"),
            })
        except Exception:
            results.append({"date": day, "duration_seconds": 0, "score": None})
    return list(reversed(results))


def get_heart_rate(days: int = 7) -> list[dict]:
    client = _client()
    results = []
    for i in range(days):
        day = (date.today() - timedelta(days=i)).isoformat()
        try:
            hr = client.get_rhr_day(day)
            results.append({
                "date": day,
                "resting_hr": hr.get("allMetrics", {}).get("metricsMap", {}).get("WELLNESS_RESTING_HEART_RATE", [{}])[0].get("value"),
            })
        except Exception:
            results.append({"date": day, "resting_hr": None})
    return list(reversed(results))


def get_activities(limit: int = 10) -> list[dict]:
    client = _client()
    activities = client.get_activities(0, limit)
    result = []
    for act in activities:
        result.append({
            "id": act.get("activityId"),
            "name": act.get("activityName"),
            "type": act.get("activityType", {}).get("typeKey", "unknown"),
            "start_time": act.get("startTimeLocal"),
            "duration_seconds": act.get("duration", 0),
            "distance_meters": act.get("distance", 0),
            "calories": act.get("calories", 0),
            "avg_hr": act.get("averageHR"),
            "elevation_gain": act.get("elevationGain"),
        })
    return result


def get_steps_history(days: int = 30) -> list[dict]:
    client = _client()
    results = []
    for i in range(days):
        day = (date.today() - timedelta(days=i)).isoformat()
        try:
            stats = client.get_stats(day)
            results.append({
                "date": day,
                "steps": stats.get("totalSteps", 0),
                "calories": stats.get("totalKilocalories", 0),
            })
        except Exception:
            results.append({"date": day, "steps": 0, "calories": 0})
    return list(reversed(results))
