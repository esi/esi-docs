# X-Pages Pagination

X-Pages pagination uses page numbers to navigate through datasets, with pages starting at 1.
This is a traditional pagination approach where you request specific page numbers to browse through the data.

## How pagination works

1. **Request a page**: Use the `page` request parameter to specify which page you want to retrieve.
2. **Check total pages**: The `X-Pages` response header tells you how many pages are available in total.
3. **Navigate through pages**: Request pages sequentially (1, 2, 3, etc.) until you've retrieved all available data.

### Request parameters

- `page`: The page number to retrieve. Pages start at 1.

### Response headers

- `X-Pages`: The total number of pages available in the dataset.

## Caching considerations

An important caveat with X-Pages pagination is caching behavior.
If the cache expires between fetching two different pages, you may see duplicated items in your results.

This happens because:

- Page 1 might be cached with data from time T.
- By the time you fetch page 2, the cache for page 1 has expired.
- The server generates new data for page 1, which may overlap with what you already retrieved from page 2.

### Solution: don't fetch close to expiry

Some implementations solve this by checking how close page 1 is to the cache expiration time.
If page 1 is within a few seconds of expiring, they first wait for the cache to refresh.
Only then do they fetch the entire set of pages.

## Example

--8<-- "snippets/examples/pagination-x-pages.md"
