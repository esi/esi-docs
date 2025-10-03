# Cursor-based Pagination

Cursor-based pagination uses opaque tokens to navigate through datasets, unlike traditional offset-based pagination that uses page numbers.
Instead of requesting "page 1, page 2, page 3", you use tokens that represent specific positions in the data.

Cursor-based pagination is available on selective few routes, and is slowly being added to others.

## How it works

1. **Initial request**: Make a request without pagination parameters to get the first batch of records.
2. **Token-based navigation**: Use the returned tokens to move forward (`after`) or backward (`before`) through the dataset.
3. **Change detection**: The `after` token can be used later to detect new or modified records.

### Request parameters

- `limit`: The maximum amount of records to fetch.
- `before`: Fetch records that come before a specific position using a token.
- `after`: Fetch records that come after a specific position using a token.

### Data ordering

Records returned by these listing routes are always ordered by the date they were last modified / created.
A record cannot change without the last modified being updated.

The most recent modified records are always last in the data.
This means that using `before` returns records with older last modified dates, and using `after` returns newer.

## Initial Data Collection

Start by making your first request without any pagination parameters:

```http
GET /<listing-route>
```

You'll receive a response like this:

```json
{
  "...": [
    {"id": 1, "name": "A", "modified": "2024-01-15T08:30:00Z"},
    {"id": 2, "name": "B", "modified": "2024-01-15T09:15:00Z"}
  ],
  "cursor": {
    "before": "MjAyNC0wMS0xNVQwODozMDowMFo=",
    "after": "MjAyNC0wMS0xNVQwOToxNTowMFo="
  }
}
```

**What to do:**

1. Remember the `after` token for later.
2. Store the data you retrieved.
3. Make a new request with the `before` token.
4. Go back to step 2 until you retrieve an empty list. You now retrieved all data available in the dataset.

## Monitor for new data

After your initial scan, monitor for changes using the `after` token.

1. Make a new request with the `after` token.
2. Store the data you retrieved.
3. Go back to step 1 until you retrieve an empty list. You are now up-to-date with the latest changes.
4. Come back any time to check for new / modified records. Make sure to use the latest `after` token you retrieved.

!!! note "Token lifetime"

    Tokens remain valid for a long time.
    Feel free to come back 24 hours later or a week later, and use the `after` token to check on what information you have missed.

!!! note "Fear of missing out"

    With this system you don't have to fear missing out on data.
    As long as you remember the `after` token you used last time, you always get the records that were updated since your last request.

    Remember: records are sorted by last modified, and `after` returns anything updated after your last request.

## Handling of Duplicates

Records may appear multiple times across different requests.
This is normal and indicates the record was modified between those requests.

- If you were using the `before` token, the record is older than what you have already stored. Use the stored record.
- If you were using the `after` token, the record is newer than what you have already stored. Use the retrieved record.

## Example

--8<-- "snippets/examples/pagination-cursor.md"

## Common Pitfalls to Avoid

1. **Don't parse tokens** - Treat them as opaque strings.
2. **Don't assume record count** - Pages may contain fewer records than requested. The limit is just that: a limit.
3. **Don't ignore empty responses** - They indicate no records were modified.
4. **Don't lose tokens** - Store them for future requests.
