from fastapi import FastAPI, HTTPException, Request, Response
import httpx

app = FastAPI()

BASE_URL = "https://dummyjson.com"

async def proxy_request(method: str, path: str, params: dict = None, json_body: dict = None):
    async with httpx.AsyncClient() as client:
        try:
            url = f"{BASE_URL}{path}"
            response = await client.request(method, url, params=params, json=json_body)
            # We return the JSON content and status code
            # We could also return a Response object directly, but let's parse it to ensure it's valid JSON if expected
            # OR just forward the raw response?
            # The requirement says "check the result ... and report it back".
            # Parsing as JSON is safer to ensure we are sending back valid JSON.
            # However, dummyjson always returns JSON.

            # If upstream returns error, we forward it.
            return response.json(), response.status_code
        except httpx.RequestError as exc:
            raise HTTPException(status_code=502, detail=f"An error occurred while requesting {exc.request.url!r}.")

@app.get("/products")
async def get_products(request: Request):
    # Forward all query params
    params = dict(request.query_params)
    data, status = await proxy_request("GET", "/products", params=params)
    # We can use Response to set status code explicitly
    # But FastAPI returns 200 by default. If status is different, we need to handle it.
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data

@app.get("/products/search")
async def search_products(request: Request):
    params = dict(request.query_params)
    data, status = await proxy_request("GET", "/products/search", params=params)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data

@app.get("/products/categories")
async def get_categories():
    data, status = await proxy_request("GET", "/products/categories")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data

@app.get("/products/category-list")
async def get_category_list():
    data, status = await proxy_request("GET", "/products/category-list")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data

@app.get("/products/category/{category_name}")
async def get_products_by_category(category_name: str, request: Request):
    params = dict(request.query_params)
    data, status = await proxy_request("GET", f"/products/category/{category_name}", params=params)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    data, status = await proxy_request("GET", f"/products/{product_id}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data

@app.post("/products/add")
async def add_product(product: dict):
    data, status = await proxy_request("POST", "/products/add", json_body=product)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data

@app.put("/products/{product_id}")
async def update_product(product_id: int, product_update: dict):
    data, status = await proxy_request("PUT", f"/products/{product_id}", json_body=product_update)
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    data, status = await proxy_request("DELETE", f"/products/{product_id}")
    if status >= 400:
        raise HTTPException(status_code=status, detail=data)
    return data
