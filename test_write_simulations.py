from fastapi.testclient import TestClient
from main import app

def test_write_simulations():
    with TestClient(app) as client:
        # Test Add
        new_product_data = {"title": "New Product Proxy", "price": 100}
        response = client.post("/products/add", json=new_product_data)
        assert response.status_code == 200 or response.status_code == 201
        data = response.json()
        assert data["title"] == "New Product Proxy"
        assert "id" in data

        # Test Update
        # Pick existing ID
        existing_id = 1
        update_data = {"title": "Updated Title Proxy"}

        response = client.put(f"/products/{existing_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title Proxy"
        assert data["id"] == existing_id

        # Test Delete
        response = client.delete(f"/products/{existing_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["isDeleted"] is True
        assert "deletedOn" in data
        assert data["id"] == existing_id
