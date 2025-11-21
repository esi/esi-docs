# From-id Pagination

From-id pagination uses record IDs to navigate backwards through datasets in chronological order.
This pagination method only allows you to move backwards in time, making it ideal for collecting historical data.

## How pagination works

1. **Initial request**: Make a request without the `from_id` parameter to get the most recent records.
2. **Backward navigation**: Use the `transaction_id` of the last record as `from_id` in your next request. The response will always include that `from_id` record.
3. **Stop condition**: If the response contains more than just the `from_id` record, continue. If it only contains that one record, stop.

### Request parameters

- `from_id`: The ID of a record. The response will contain this record and records that are older.

When you omit the `from_id` parameter, you get the most recent records.

### Data ordering

Records returned by these listing routes are ordered by time, with the most recent records first.
Using `from_id` returns that record and records that are older.

## Initial Data Collection

Start by making your first request without the `from_id` parameter:

```http
GET /<listing-route>
```

You'll receive a response like this:

```json
[
  {"id": 100, "name": "A", "created": "2024-01-15T09:15:00Z"},
  {"id": 99, "name": "B", "created": "2024-01-15T08:30:00Z"},
  {"id": 98, "name": "C", "created": "2024-01-15T07:45:00Z"}
]
```

**What to do:**

1. Store all the records you retrieved.
2. If you find a record you already know, stop.
3. If you are at the end of the record set, use the last `transaction_id` as `from_id` in your next request.
4. The response will always contain that `from_id` record (98). If it only contains that one record, stop. Otherwise continue at step 1.

## Example

--8<-- "snippets/examples/pagination-from-id.md"