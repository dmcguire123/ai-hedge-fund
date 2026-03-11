import json
import os
from pathlib import Path

import httpx

TOKENS_FILE = Path(__file__).parent.parent / "tokens" / "google.json"
TOKENS_FILE.parent.mkdir(exist_ok=True)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("OAUTH_REDIRECT_BASE", "http://localhost:8000") + "/auth/google/callback"

SCOPES = " ".join([
    "https://www.googleapis.com/auth/fitness.body.read",
    "https://www.googleapis.com/auth/fitness.activity.read",
])


def get_auth_url() -> str:
    return (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope={SCOPES}"
        f"&access_type=offline"
        f"&prompt=consent"
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
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "code": code,
                "redirect_uri": REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        resp.raise_for_status()
        tokens = resp.json()
        save_tokens(tokens)
        return tokens


async def refresh_tokens() -> dict:
    tokens = load_tokens()
    if not tokens or not tokens.get("refresh_token"):
        raise ValueError("No Google tokens found. Please authenticate first.")

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
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
        raise ValueError("Not authenticated with Google Fit. Visit /auth/google to connect.")

    expires_at = tokens.get("expires_at", 0)
    if not expires_at:
        import datetime
        expires_at = (datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp()

    if expires_at < time.time() + 60:
        tokens = await refresh_tokens()

    return tokens["access_token"]
