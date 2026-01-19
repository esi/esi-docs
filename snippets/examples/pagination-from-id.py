import requests
import time

def fetch_records(url, headers, from_id=None):
    params = {}
    if from_id is not None:
        params['from_id'] = from_id

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()

def collect_current_data(url, headers):
    all_records = []
    from_id = None

    while True:
        print(f"Fetching records from_id={from_id}...")
        records = fetch_records(url, headers, from_id=from_id)

        # If the response is empty, there are no records in the dataset.
        if not records:
            print("  Empty dataset")
            break

        # The response always contains the from_id record.
        # If it only contains that one record, we've reached the end.
        if from_id is not None and len(records) == 1:
            print("  No more records")
            break

        # Store all records.
        all_records.extend(records)
        print(f"  Found {len(records)} records; total {len(all_records)} records")

        # Use last record's ID for next request (go backwards in time).
        from_id = records[-1]['transaction_id']
        time.sleep(0.1) # Throttle requests to avoid rate limiting.

    print(f"Total: {len(all_records)} records")
    return all_records

if __name__ == "__main__":
    url = "https://esi.evetech.net/..." # ... (replace with actual route)
    headers = {
        "User-Agent": "ESI-Example/1.0",
        "X-Compatibility-Date": "2025-09-30",
        "Authorization": "Bearer <your-token>",
    }

    all_data = collect_current_data(url, headers)
    # ... (do something with all_data)

