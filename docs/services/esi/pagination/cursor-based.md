# Cursor-based Pagination

Cursor-based pagination uses tokens to navigate through datasets, unlike traditional offset-based pagination that uses page numbers.
Instead of requesting "page 1, page 2, page 3", you use tokens that represent specific positions in the data.

Cursor-based pagination is available on a select few routes, and is slowly being added to others.

## What are tokens?

Tokens are encoded strings that contain information about a specific position in the dataset.
They are designed to be used as-is without any interpretation or parsing by your application.
Think of them as "bookmarks" that the server creates to remember exactly where you are in the data.

- **Don't try to decode them** - The internal structure and encoding of tokens is not meant to be understood by clients.
- **Treat them as black boxes** - Just pass them back to the server exactly as you received them.
- **They're position markers** - Each token represents a specific point in the ordered dataset.
- **They're server-generated** - Only the server knows how to create and interpret these tokens.

## How pagination works

1. **Initial request**: Make a request without pagination parameters to get the first batch of records.
2. **Token-based navigation**: Use the returned tokens to move forward (`after`) or backward (`before`) through the dataset.
3. **Change detection**: The `after` token can be used later to detect new or modified records.

### Request parameters

- `limit`: The maximum amount of records to retrieve. This is a limit: you might receive fewer records.
- `before`: Retrieve records that come just before the position specified by this token.
- `after`: Retrieve records that come just after the position specified by this token.

When you omit both `before` and `after` parameters, you get the most recent records (up to the specified `limit`).

For each route supporting cursor-based pagination, the API specification will mention how to set these request parameters.

### Data ordering

Records returned by these listing routes are always ordered by the date they were last modified or created.
A record cannot change without the last modified being updated.

The most recent modified records are always last in the dataset.
This means that using `before` returns older records, and using `after` returns newer records.

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
4. Go back to step 2 until you retrieve an empty list (no more records). You now have retrieved all data available in the dataset.

## Monitor for new data

After your initial scan, monitor for changes using the `after` token.

1. Make a new request with the `after` token.
2. Store the data you retrieved.
3. Go back to step 1 until you retrieve an empty list (no more records). You are now up-to-date with the latest changes.
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
When using `after` it could happen because the record was updated.
When using `before` it can happen because you received a (partially) cached page.

To handle duplicates correctly:

- If you were using the `before` token, the record is older than what you have already stored. Keep your existing stored record.
- If you were using the `after` token, the record is newer than what you have already stored. Replace your stored record with the retrieved record.

## Example

--8<-- "snippets/examples/pagination-cursor.md"
