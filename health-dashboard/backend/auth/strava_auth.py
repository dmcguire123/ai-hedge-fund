import json
import os
from pathlib import Path

import httpx

TOKENS_FILE = Path(__file__).parent.parent / "tokens" / "strava.json"
TOKENS_FILE.parent.mkdir(exist_ok=True)

STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID", "")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("OAUTH_REDIRECT_BASE", "http://localhost:8000") + "/auth/strava/callback"

SCOPES = "activity:read_all"


def get_auth_url() -> str:
    return (
        f"https://www.strava.com/oauth/authorize"
        f"?client_id={STRAVA_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope={SCOPES}"
    )


def load_tokens() -> dict | None:
    if TOKENS_FILE.exists():
        return json.loads(TOKENS_FILE.read_text())
    return None


def save_tokens(tokens: dict) -> None:
    TOKENS_FILE.write_text(json.dumps(tokens, indent=2))


async def exchange_code(code: str) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://www.strava.com/oauth/token",
            data={
                "client_id": STRAVA_CLIENT_ID,
                "client_secret": STRAVA_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
            },
        )
        resp.raise_for_status()
        tokens = resp.json()
        save_tokens(tokens)
        return tokens


async def refresh_tokens() -> dict:
    tokens = load_tokens()
    if not tokens:
        raise ValueError("No Strava tokens found. Please authenticate first.")

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://www.strava.com/oauth/token",
            data={
                "client_id": STRAVA_CLIENT_ID,
                "client_secret": STRAVA_CLIENT_SECRET,
                "refresh_token": tokens["refresh_token"],
                "grant_type": "refresh_token",
            },
        )
        resp.raise_for_status()
        new_tokens = {**tokens, **resp.json()}
        save_tokens(new_tokens)
        return new_tokens


async def get_valid_access_token() -> str:
    import time

    tokens = load_tokens()
    if not tokens:
        raise ValueError("Not authenticated with Strava. Visit /auth/strava to connect.")

    if tokens.get("expires_at", 0) < time.time() + 60:
        tokens = await refresh_tokens()

    return tokens["access_token"]
