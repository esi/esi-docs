import requests

def get_esi_route(origin_id, destination_id, route_type="Shorter", security_penalty=50):
    url = f"https://esi.evetech.net/route/{origin_id}/{destination_id}"
    params = {
        "preference": route_type,
        "security_penalty": security_penalty
    }

    response = requests.post(
        url,
        headers={
            "X-Compatibility-Date": "2025-09-30",
            "User-Agent": "esi-docs-example",
        },
        json=params,
    )

    if response.status_code == 200:
        return response.json()  # List of system IDs
    else:
        raise Exception(f"ESI route calculation failed: {response.status_code}: {response.json()}")
