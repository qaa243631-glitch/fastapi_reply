from fastapi.testclient import TestClient
from main import app

def test_categories():
    with TestClient(app) as client:
        # Test /products/categories
        response = client.get("/products/categories")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert "slug" in data[0]
        assert "name" in data[0]

        # Test /products/category-list
        response = client.get("/products/category-list")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert isinstance(data[0], str)

        # Test /products/category/{category_name}
        # Pick a category
        category_slug = data[0]
        response = client.get(f"/products/category/{category_slug}")
        assert response.status_code == 200
        data = response.json()
        products = data["products"]
        assert len(products) > 0
        for p in products:
            # dummyjson usually returns category slug in product
            # but sometimes it might be just "category" field
            assert p["category"] == category_slug
