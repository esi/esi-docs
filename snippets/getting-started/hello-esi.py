"""Your first ESI call — check the EVE server status."""

import requests

BASE_URL = "https://esi.evetech.net"
USER_AGENT = "EVE Getting Started Guide/1.0 (your@email.com)"

response = requests.get(
    f"{BASE_URL}/v2/status/",
    headers={"User-Agent": USER_AGENT},
)
response.raise_for_status()

status = response.json()
print(f"Players online: {status['players']}")
print(f"Server version: {status['server_version']}")
print(f"Started at:     {status['start_time']}")
