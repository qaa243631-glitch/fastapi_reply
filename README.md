# CRUD FastAPI Proxy

This is a CRUD API implemented using FastAPI that acts as a **proxy/relay** for `https://dummyjson.com/products`.

It forwards requests to `dummyjson.com` and returns the response to the client. No data is stored locally.

## Requirements

- Python 3.12
- FastAPI
- Uvicorn
- HTTPX

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the API

Run the application using `uvicorn`:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## Endpoints

All endpoints mirror the behavior of `dummyjson.com`.

### Products

- **Get all products**: `GET /products`
  - Query Params: `limit`, `skip`, `select`, `sortBy`, `order` are forwarded.
- **Get a single product**: `GET /products/{id}`
- **Search products**: `GET /products/search?q=...`

### Categories

- **Get all categories**: `GET /products/categories`
- **Get category list**: `GET /products/category-list`
- **Get products by category**: `GET /products/category/{category_name}`

### Write Operations

These operations are forwarded to `dummyjson.com`, which simulates the write (returns the modified object without changing the actual database).

- **Add a product**: `POST /products/add`
- **Update a product**: `PUT /products/{id}`
- **Delete a product**: `DELETE /products/{id}`
