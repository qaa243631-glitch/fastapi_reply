from fastapi.testclient import TestClient
from main import app, PRODUCTS

def test_write_simulations():
    with TestClient(app) as client:
        # Test Add
        new_product_data = {"title": "New Product", "price": 100}
        response = client.post("/products/add", json=new_product_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Product"
        assert "id" in data
        new_id = data["id"]
        # Verify it wasn't added to store
        assert not any(p["id"] == new_id for p in PRODUCTS)

        # Test Update
        # Pick existing ID
        existing_id = PRODUCTS[0]["id"]
        original_title = PRODUCTS[0]["title"]
        update_data = {"title": "Updated Title"}

        response = client.put(f"/products/{existing_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["id"] == existing_id
        # Verify store is unchanged
        assert PRODUCTS[0]["title"] == original_title

        # Test Delete
        response = client.delete(f"/products/{existing_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["isDeleted"] is True
        assert "deletedOn" in data
        assert data["id"] == existing_id
        # Verify store is unchanged
        assert any(p["id"] == existing_id for p in PRODUCTS)
