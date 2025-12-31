# CRUD FastAPI

This is a CRUD API implemented using FastAPI, which mirrors specific endpoints from `https://dummyjson.com/products`.

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

### Products

- **Get all products**: `GET /products`
  - Query Params:
    - `limit` (default: 30)
    - `skip` (default: 0)
    - `select` (comma-separated fields)
    - `sortBy` (field name)
    - `order` (`asc` or `desc`)

- **Get a single product**: `GET /products/{id}`

- **Search products**: `GET /products/search`
  - Query Params: `q` (search query)

### Categories

- **Get all categories**: `GET /products/categories`
- **Get category list**: `GET /products/category-list`
- **Get products by category**: `GET /products/category/{category_name}`

### Write Operations (Simulated)

These endpoints simulate write operations but **do not** modify the server state.

- **Add a product**: `POST /products/add`
- **Update a product**: `PUT /products/{id}`
- **Delete a product**: `DELETE /products/{id}`
