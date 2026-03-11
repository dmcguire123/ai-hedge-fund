import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

load_dotenv()

from routes.auth_routes import router as auth_router
from routes.garmin_routes import router as garmin_router
from routes.googlefit_routes import router as googlefit_router
from routes.strava_routes import router as strava_router

app = FastAPI(title="Health Dashboard API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:4173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(garmin_router)
app.include_router(strava_router)
app.include_router(googlefit_router)


@app.get("/health")
def health():
    return {"status": "ok"}
