"""Token refresh utilities for EVE SSO."""

import base64
import json
import time

import requests

SSO_TOKEN = "https://login.eveonline.com/v2/oauth/token"
USER_AGENT = "EVE Getting Started Guide/1.0 (your@email.com)"


def is_token_expired(access_token: str, buffer_seconds: int = 60) -> bool:
    """Check if a JWT access token is expired or will expire soon."""
    payload = access_token.split(".")[1]
    payload += "=" * (-len(payload) % 4)  # Fix base64 padding
    claims = json.loads(base64.urlsafe_b64decode(payload))
    return time.time() >= (claims["exp"] - buffer_seconds)


def refresh_access_token(
    refresh_token: str, client_id: str, client_secret: str
) -> dict:
    """Exchange a refresh token for a new access token."""
    response = requests.post(
        SSO_TOKEN,
        data={"grant_type": "refresh_token", "refresh_token": refresh_token},
        auth=(client_id, client_secret),
        headers={"User-Agent": USER_AGENT},
    )
    response.raise_for_status()
    return response.json()  # {"access_token": "...", "refresh_token": "...", ...}


def ensure_valid_token(
    access_token: str,
    refresh_token: str,
    client_id: str,
    client_secret: str,
) -> tuple[str, str]:
    """Return a valid access token, refreshing if needed."""
    if not is_token_expired(access_token):
        return access_token, refresh_token
    tokens = refresh_access_token(refresh_token, client_id, client_secret)
    return tokens["access_token"], tokens["refresh_token"]
