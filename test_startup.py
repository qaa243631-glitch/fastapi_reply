from fastapi.testclient import TestClient
from main import app, PRODUCTS

client = TestClient(app)

def test_startup_data_loading():
    # Trigger lifespan events
    with TestClient(app) as c:
        response = c.get("/debug/products-count")
        assert response.status_code == 200
        count = response.json()["count"]
        assert count > 0

        response_cat = c.get("/debug/categories-count")
        assert response_cat.status_code == 200
        cat_count = response_cat.json()["count"]
        assert cat_count > 0
