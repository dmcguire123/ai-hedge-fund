from fastapi import APIRouter, HTTPException

from services import strava_service

router = APIRouter(prefix="/strava", tags=["strava"])


@router.get("/activities")
async def activities(limit: int = 20):
    try:
        return await strava_service.get_activities(limit)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def athlete_stats():
    try:
        return await strava_service.get_athlete_stats()
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/weekly")
async def weekly_summary(weeks: int = 8):
    try:
        return await strava_service.get_weekly_activity_summary(weeks)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
