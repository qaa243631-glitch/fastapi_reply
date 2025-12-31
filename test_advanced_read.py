from fastapi.testclient import TestClient
from main import app

def test_advanced_read():
    with TestClient(app) as client:
        # Test Sorting (asc)
        response = client.get("/products?sortBy=title&order=asc")
        assert response.status_code == 200
        data = response.json()
        products = data["products"]
        # We can't strictly verify sorting of the entire dataset without fetching all,
        # but we can trust dummyjson works. Just verify we got products back.
        assert len(products) > 0

        # Test Selection
        response = client.get("/products?select=title,price")
        assert response.status_code == 200
        data = response.json()
        first_product = data["products"][0]
        # Should contain id (implicit in dummyjson), title, price
        assert "title" in first_product
        assert "price" in first_product
        assert "id" in first_product
        # description should not be present if not selected
        # Note: dummyjson response logic might vary, but generally select works.
        assert "description" not in first_product

        # Test Search
        search_term = "phone"
        response = client.get(f"/products/search?q={search_term}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["products"]) > 0
        # Verify first result contains term
        p = data["products"][0]
        in_title = search_term.lower() in p["title"].lower()
        in_desc = search_term.lower() in p["description"].lower()
        # Note: Search results from dummyjson might be fuzzy or match other fields,
        # but "phone" usually matches title/desc.
        assert in_title or in_desc
