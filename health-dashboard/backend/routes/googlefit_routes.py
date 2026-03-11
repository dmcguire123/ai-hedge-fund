from fastapi import APIRouter, HTTPException

from services import googlefit_service

router = APIRouter(prefix="/googlefit", tags=["googlefit"])


@router.get("/weight")
async def weight_history(days: int = 90):
    try:
        return await googlefit_service.get_weight_history(days)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bodyfat")
async def body_fat_history(days: int = 90):
    try:
        return await googlefit_service.get_body_fat_history(days)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/latest")
async def latest_metrics():
    try:
        return await googlefit_service.get_latest_body_metrics()
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
