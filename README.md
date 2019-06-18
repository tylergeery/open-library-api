# Open Library API Search

## Overview
This provides a Django API on top of the [OpenLibrary](https://openlibrary.org/dev/docs/api/search). It uses Postgres as a database and provides wishlist functionality for saving "wish" requests for books.

## API
### Endpoints
Method | Endpoint | Example | Param | Meaning
--- | --- | --- | --- | ---
GET | /books/?q={query} | [example](#get-booksqquery) | |
 | | | | *query* | Query for book titles
GET | /books/{book_id}/ | [example](#get-booksbook_id) | |
 | | | | *book_id* | Book ID to view details of
POST | /wishlist/ | [example](#post-wishlist) | |
 | | | | *library_user_id* | User ID for creating "wish"
 | | | | *book_id* | Book ID from OpenLibraryAPI
DELETE | /wishlist/{wish_id}/ | [example](#delete-wishlistwish_id) | |
 | | | | *wish_id* | Wish ID to delete
GET | /wishlist/user/{library_user_id}/ | [example](#get-wishlistuserlibrary_user_id) | |
 | | | | *library_user_id* | User ID to view wishlist of

### Example Requests
#### GET /books/?q={query}
```
curl -X GET \
  'http://localhost:3000/books?q=harry' \
  -H 'Content-Type: application/json'
```

#### GET /books/{book_id}/
```
curl -X GET \
  'http://localhost:3000/books/1/' \
  -H 'Content-Type: application/json'
```

#### POST /wishlist/
```
curl -X POST \
  http://localhost:3000/wishlist/ \
  -H 'Content-Type: application/json' \
  -d '{
    "library_user_id": 1,
    "book_id": "OL7603924W"
  }'
```

#### DELETE /wishlist/{wish_id}/
```
curl -X DELETE \
  http://localhost:3000/wishlist/1/ \
  -H 'Content-Type: application/json'
```

#### GET /wishlist/user/{library_user_id}/
```
curl -X GET \
  'http://localhost:3000/wishlist/user/1/' \
  -H 'Content-Type: application/json'
```

## Installation
### Dependencies
- Make
- Docker

### Instructions
```bash
make dev-images
make dev
```

### Cleanup
```bash
make dev-clean
make dev-clean-images
```

### Test
```bash
make test
```

### Help
```bash
make
```
