from fastapi import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse

from auth import google_auth, strava_auth

router = APIRouter(prefix="/auth", tags=["auth"])


# ── Strava ────────────────────────────────────────────────────────────────────

@router.get("/strava")
def strava_login():
    return RedirectResponse(strava_auth.get_auth_url())


@router.get("/strava/callback")
async def strava_callback(code: str):
    await strava_auth.exchange_code(code)
    return HTMLResponse(_success_html("Strava", "/auth/strava/status"))


@router.get("/strava/status")
def strava_status():
    tokens = strava_auth.load_tokens()
    connected = tokens is not None
    return {"connected": connected, "athlete": tokens.get("athlete", {}) if tokens else None}


# ── Google Fit ────────────────────────────────────────────────────────────────

@router.get("/google")
def google_login():
    return RedirectResponse(google_auth.get_auth_url())


@router.get("/google/callback")
async def google_callback(code: str):
    await google_auth.exchange_code(code)
    return HTMLResponse(_success_html("Google Fit", "/auth/google/status"))


@router.get("/google/status")
def google_status():
    tokens = google_auth.load_tokens()
    connected = tokens is not None
    return {"connected": connected}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _success_html(service: str, status_url: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>{service} Connected</title>
    <style>body{{font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;background:#0f172a;color:#e2e8f0}}.box{{text-align:center;padding:2rem}}.tick{{font-size:4rem}}</style>
    </head>
    <body><div class="box">
      <div class="tick">✅</div>
      <h2>{service} connected successfully!</h2>
      <p>You can close this tab and return to the dashboard.</p>
    </div></body>
    </html>
    """
