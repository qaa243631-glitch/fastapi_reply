from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
import httpx

# In-memory storage
PRODUCTS = []
CATEGORIES = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load data on startup
    global PRODUCTS, CATEGORIES
    async with httpx.AsyncClient() as client:
        # Fetch all products (limit=0)
        try:
            print("Fetching products from dummyjson.com...")
            response = await client.get("https://dummyjson.com/products?limit=0")
            response.raise_for_status()
            data = response.json()
            PRODUCTS.clear()
            PRODUCTS.extend(data.get("products", []))
            print(f"Loaded {len(PRODUCTS)} products.")

            print("Fetching categories from dummyjson.com...")
            cat_response = await client.get("https://dummyjson.com/products/categories")
            cat_response.raise_for_status()
            CATEGORIES.clear()
            CATEGORIES.extend(cat_response.json())
            print(f"Loaded {len(CATEGORIES)} categories.")

        except Exception as e:
            print(f"Error fetching data: {e}")
            # We might want to re-raise or handle gracefully depending on requirements.
            # For this task, having data is crucial, so we print error.

    yield
    # Clean up on shutdown (not needed here)

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/debug/products-count")
def get_products_count():
    return {"count": len(PRODUCTS)}

@app.get("/debug/categories-count")
def get_categories_count():
    return {"count": len(CATEGORIES)}


@app.get("/products/categories")
def get_categories():
    """
    Get all product categories.
    """
    return CATEGORIES


@app.get("/products/category-list")
def get_category_list():
    """
    Get product category list (slugs).
    """
    # Assuming CATEGORIES is a list of objects with "slug"
    return [c["slug"] for c in CATEGORIES]


@app.get("/products/category/{category_name}")
def get_products_by_category(
    category_name: str, limit: int = 30, skip: int = 0
):
    """
    Get products by category.
    """
    # Filter products by category
    filtered_products = [
        p for p in PRODUCTS if p.get("category") == category_name
    ]

    paginated_products = filtered_products[skip : skip + limit]

    return {
        "products": paginated_products,
        "total": len(filtered_products),
        "skip": skip,
        "limit": limit,
    }


@app.get("/products/search")
def search_products(q: str, limit: int = 30, skip: int = 0):
    """
    Search products by title or description.
    """
    query = q.lower()
    filtered_products = [
        p
        for p in PRODUCTS
        if query in p.get("title", "").lower() or query in p.get("description", "").lower()
    ]

    paginated_products = filtered_products[skip : skip + limit]

    return {
        "products": paginated_products,
        "total": len(filtered_products),
        "skip": skip,
        "limit": limit,
    }


@app.get("/products")
def get_products(
    limit: int = 30,
    skip: int = 0,
    select: str | None = None,
    sortBy: str | None = None,
    order: str = "asc",
):
    """
    Get all products with pagination, sorting, and field selection.
    """
    filtered_products = list(PRODUCTS)

    # Sorting
    if sortBy:
        filtered_products.sort(
            key=lambda x: x.get(sortBy, ""), reverse=(order == "desc")
        )

    # Pagination
    paginated_products = filtered_products[skip : skip + limit]

    # Selection
    if select:
        fields = [f.strip() for f in select.split(",")]
        selected_products = []
        for product in paginated_products:
            selected_product = {k: v for k, v in product.items() if k in fields}
            if "id" not in fields:
                selected_product["id"] = product["id"]
            selected_products.append(selected_product)
        paginated_products = selected_products

    return {
        "products": paginated_products,
        "total": len(PRODUCTS),
        "skip": skip,
        "limit": limit,
    }


@app.get("/products/{product_id}")
def get_product(product_id: int):
    """
    Get a single product by ID.
    """
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")


@app.post("/products/add")
def add_product(product: dict):
    """
    Simulate adding a new product.
    Returns the input product with a new ID.
    Does NOT modify the server state.
    """
    # Generate new ID (max existing ID + 1)
    max_id = max(p["id"] for p in PRODUCTS) if PRODUCTS else 0
    new_product = product.copy()
    new_product["id"] = max_id + 1
    return new_product


@app.put("/products/{product_id}")
def update_product(product_id: int, product_update: dict):
    """
    Simulate updating a product.
    Returns the updated product (merged with existing).
    Does NOT modify the server state.
    """
    existing_product = None
    for p in PRODUCTS:
        if p["id"] == product_id:
            existing_product = p
            break

    if not existing_product:
        # Dummyjson behavior for update on non-existent: 404
        raise HTTPException(status_code=404, detail="Product not found")

    # Merge update into existing (simulate)
    updated_product = existing_product.copy()
    updated_product.update(product_update)
    return updated_product


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    """
    Simulate deleting a product.
    Returns the deleted product with isDeleted=True.
    Does NOT modify the server state.
    """
    existing_product = None
    for p in PRODUCTS:
        if p["id"] == product_id:
            existing_product = p
            break

    if not existing_product:
         raise HTTPException(status_code=404, detail="Product not found")

    deleted_product = existing_product.copy()
    deleted_product["isDeleted"] = True
    import datetime
    deleted_product["deletedOn"] = datetime.datetime.now().isoformat()
    return deleted_product
