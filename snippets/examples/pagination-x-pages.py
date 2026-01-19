import requests
import time

def fetch_page(url, headers, page=1):
    params = {
        'page': page,
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json(), response.headers

def collect_current_data(url, headers):
    all_records = []

    # Fetch page 1 to get total pages.
    records, page1_headers = fetch_page(url, headers, page=1)
    total_pages = int(page1_headers.get('X-Pages', 1))
    all_records.extend(records)

    # Fetch remaining pages.
    for page in range(2, total_pages + 1):
        print(f"Fetching page {page}/{total_pages}...")
        records, _ = fetch_page(url, headers, page=page)

        all_records.extend(records)

        print(f"  Found {len(records)} records; total {len(all_records)} records")
        time.sleep(0.1) # Throttle requests to avoid rate limiting.

    print(f"Total: {len(all_records)} records across {total_pages} pages")
    return all_records

if __name__ == "__main__":
    url = "https://esi.evetech.net/..." # ... (replace with actual route)
    headers = {
        "User-Agent": "ESI-Example/1.0",
        "X-Compatibility-Date": "2025-09-30",
    }

    all_data = collect_current_data(url, headers)
    # ... (do something with all_data)
