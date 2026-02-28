"""Complete OAuth2 flow — authenticate and read your character's location."""

import base64
import http.server
import json
import threading
import urllib.parse
import webbrowser

import requests

# --- Configuration -----------------------------------------------------------
CLIENT_ID = "your-client-id"  # From developers.eveonline.com
CLIENT_SECRET = "your-client-secret"  # Keep this secret!
CALLBACK_URL = "http://localhost:8089/callback"
SCOPES = "esi-location.read_location.v1"

BASE_URL = "https://esi.evetech.net"
SSO_AUTH = "https://login.eveonline.com/v2/oauth/authorize"
SSO_TOKEN = "https://login.eveonline.com/v2/oauth/token"
USER_AGENT = "EVE Getting Started Guide/1.0 (your@email.com)"


# --- Step 1: Start a local server to capture the callback -------------------
auth_code = None


class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        auth_code = params.get("code", [None])[0]
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(
            b"<h1>Login successful!</h1><p>You can close this tab.</p>"
        )

    def log_message(self, format, *args):
        pass  # Suppress server logs


server = http.server.HTTPServer(("localhost", 8089), CallbackHandler)
thread = threading.Thread(target=server.handle_request, daemon=True)
thread.start()


# --- Step 2: Open the browser for SSO login ---------------------------------
auth_params = urllib.parse.urlencode(
    {
        "response_type": "code",
        "redirect_uri": CALLBACK_URL,
        "client_id": CLIENT_ID,
        "scope": SCOPES,
        "state": "getting-started",
    }
)

print("Opening browser for EVE SSO login...")
webbrowser.open(f"{SSO_AUTH}?{auth_params}")
thread.join(timeout=120)

if not auth_code:
    raise SystemExit("No authorization code received. Did you log in?")


# --- Step 3: Exchange the code for tokens -----------------------------------
token_response = requests.post(
    SSO_TOKEN,
    data={"grant_type": "authorization_code", "code": auth_code},
    auth=(CLIENT_ID, CLIENT_SECRET),
    headers={"User-Agent": USER_AGENT},
)
token_response.raise_for_status()
tokens = token_response.json()
access_token = tokens["access_token"]


# --- Step 4: Extract character ID from the JWT ------------------------------
# The JWT payload is the second base64url-encoded segment
payload = access_token.split(".")[1]
payload += "=" * (-len(payload) % 4)  # Fix base64 padding
claims = json.loads(base64.urlsafe_b64decode(payload))
character_id = int(claims["sub"].split(":")[-1])
character_name = claims["name"]


# --- Step 5: Call an authenticated endpoint ---------------------------------
location = requests.get(
    f"{BASE_URL}/v1/characters/{character_id}/location/",
    headers={
        "Authorization": f"Bearer {access_token}",
        "User-Agent": USER_AGENT,
    },
)
location.raise_for_status()
loc = location.json()

print(f"\n{character_name} is in solar system {loc['solar_system_id']}")
