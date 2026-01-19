import requests
import time

def fetch_records(url, headers, limit=100, before=None, after=None):
    params = {'limit': limit}
    if before:
        params['before'] = before
    if after:
        params['after'] = after

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()

def collect_current_data(url, headers):
    all_records = {}

    after_token = None
    before_token = None
    while True:
        print(f"Collecting data from before {before_token}...")

        data = fetch_records(url, headers, before=before_token)
        records = data.get('records', [])
        cursor = data.get('cursor', {})

        if not records:
            break

        for record in records:
            # As this is from a "before", the records in the data are always older than the ones already stored.
            if record['id'] in all_records:
                continue
            all_records[record['id']] = record

        before_token = cursor['before']
        # Remember the after-token of the first request.
        if after_token is None:
            after_token = cursor['after']

        print(f"  Found {len(records)} records")

    print(f"  End of record; found {len(all_records)} records")
    return all_records, after_token

def monitor_new_data(url, headers, after_token):
    print(f"Checking for new data from after {after_token}...")

    new_records = {}

    current_after = after_token
    while True:
        data = fetch_records(url, headers, after=current_after)
        records = data.get('records', [])
        cursor = data.get('cursor', {})

        if not records:
            break

        for record in records:
            # As this is from an "after", the records in the data are always newer than the ones already stored.
            new_records[record['id']] = record

        current_after = cursor['after']
        print(f"  Found {len(records)} new records")

    print(f"  End of record; found {len(new_records)} new records")
    return new_records

if __name__ == "__main__":
    url = "https://esi.evetech.net/..." # ... (replace with actual route)
    headers = {
        "User-Agent": "ESI-Example/1.0",
        "X-Compatibility-Date": "2025-09-30",
        "Authorization": "Bearer <your-token>",
    }

    all_data, last_after_token = collect_current_data(url, headers)
    # ... (do something with all_data)
    while True:
        new_data = monitor_new_data(url, headers, last_after_token)
        # ... (do something with new_data)

        time.sleep(30) # ... (throttle before checking for new data again)
