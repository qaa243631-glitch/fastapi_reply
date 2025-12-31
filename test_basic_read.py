from fastapi.testclient import TestClient
from main import app, PRODUCTS

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
        assert data["total"] == len(PRODUCTS)

        # Test custom pagination
        limit = 10
        skip = 5
        response = client.get(f"/products?limit={limit}&skip={skip}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["products"]) == limit
        assert data["limit"] == limit
        assert data["skip"] == skip

        # Verify content matches loaded data
        expected_product_id = PRODUCTS[skip]["id"]
        assert data["products"][0]["id"] == expected_product_id

def test_get_product_by_id():
    with TestClient(app) as client:
        # Get first product ID
        first_product_id = PRODUCTS[0]["id"]

        response = client.get(f"/products/{first_product_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == first_product_id

        # Test non-existent ID
        response = client.get("/products/9999999")
        assert response.status_code == 404
