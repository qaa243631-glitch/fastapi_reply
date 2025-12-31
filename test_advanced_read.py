from fastapi.testclient import TestClient
from main import app, PRODUCTS

def test_advanced_read():
    with TestClient(app) as client:
        # Test Sorting (asc)
        response = client.get("/products?sortBy=title&order=asc")
        assert response.status_code == 200
        data = response.json()
        products = data["products"]
        titles = [p["title"] for p in products]
        # Check if sorted
        assert titles == sorted(titles)

        # Test Sorting (desc)
        response = client.get("/products?sortBy=price&order=desc")
        assert response.status_code == 200
        data = response.json()
        products = data["products"]
        prices = [p["price"] for p in products]
        # Check if sorted descending
        assert prices == sorted(prices, reverse=True)

        # Test Selection
        response = client.get("/products?select=title,price")
        assert response.status_code == 200
        data = response.json()
        first_product = data["products"][0]
        # Should contain id (implicit), title, price
        assert "title" in first_product
        assert "price" in first_product
        assert "id" in first_product
        assert "description" not in first_product # Should be filtered out

        # Test Search
        # Find a term that exists
        search_term = "phone"
        response = client.get(f"/products/search?q={search_term}")
        assert response.status_code == 200
        data = response.json()
        for p in data["products"]:
            # Check title or description
            in_title = search_term.lower() in p["title"].lower()
            in_desc = search_term.lower() in p["description"].lower()
            assert in_title or in_desc
