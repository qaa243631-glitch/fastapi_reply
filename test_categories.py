from fastapi.testclient import TestClient
from main import app, PRODUCTS, CATEGORIES

def test_categories():
    with TestClient(app) as client:
        # Test /products/categories
        response = client.get("/products/categories")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == len(CATEGORIES)
        assert "slug" in data[0]
        assert "name" in data[0]

        # Test /products/category-list
        response = client.get("/products/category-list")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert isinstance(data[0], str)
        assert data[0] == CATEGORIES[0]["slug"]

        # Test /products/category/{category_name}
        # Pick a category from loaded categories
        category_slug = CATEGORIES[0]["slug"]
        response = client.get(f"/products/category/{category_slug}")
        assert response.status_code == 200
        data = response.json()
        products = data["products"]
        assert len(products) > 0
        for p in products:
            assert p["category"] == category_slug
