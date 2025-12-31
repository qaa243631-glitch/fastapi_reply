from fastapi.testclient import TestClient
from main import app

def test_get_products_pagination():
    with TestClient(app) as client:
        # Test default pagination
        response = client.get("/products")
        assert response.status_code == 200
        data = response.json()
        assert "products" in data
        assert len(data["products"]) == 30
        assert data["limit"] == 30
        assert data["skip"] == 0
        assert data["total"] > 0

        # Test custom pagination
        limit = 10
        skip = 5
        response = client.get(f"/products?limit={limit}&skip={skip}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["products"]) == limit
        assert data["limit"] == limit
        assert data["skip"] == skip

def test_get_product_by_id():
    with TestClient(app) as client:
        # Get first product ID (assuming 1 exists)
        first_product_id = 1

        response = client.get(f"/products/{first_product_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == first_product_id

        # Test non-existent ID (dummyjson usually returns 404 for large IDs)
        response = client.get("/products/1000000")
        assert response.status_code == 404
