from fastapi import APIRouter, HTTPException

from services import garmin_service

router = APIRouter(prefix="/garmin", tags=["garmin"])


@router.get("/today")
def today_stats():
    try:
        return garmin_service.get_today_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sleep")
def sleep(days: int = 7):
    try:
        return garmin_service.get_sleep(days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/heart-rate")
def heart_rate(days: int = 7):
    try:
        return garmin_service.get_heart_rate(days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/activities")
def activities(limit: int = 10):
    try:
        return garmin_service.get_activities(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/steps")
def steps(days: int = 30):
    try:
        return garmin_service.get_steps_history(days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
