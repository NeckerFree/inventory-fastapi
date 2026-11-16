from decimal import Decimal

from fastapi.testclient import TestClient

from inventory_api.main import app
from inventory_api.schemas.product import Product
from inventory_api.services.product_service import (
    InMemoryProductRepository,
    get_product_repository,
)


class FakeProductRepository(InMemoryProductRepository):
    def __init__(self) -> None:
        super().__init__()
        self.products[1] = Product(
            id=1,
            name="Fake Product",
            price=Decimal("9.99"),
            quantity=1,
        )
        self.next_id = 2


def test_product_repository_provider_reuses_repository() -> None:
    assert get_product_repository() is get_product_repository()


def test_get_product_uses_fake_repository() -> None:
    app.dependency_overrides[get_product_repository] = lambda: FakeProductRepository()

    try:
        with TestClient(app) as client:
            response = client.get("/products/1")

        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "name": "Fake Product",
            "price": "9.99",
            "quantity": 1,
        }
    finally:
        app.dependency_overrides.pop(get_product_repository, None)


def test_patch_product_changes_only_provided_fields() -> None:
    app.dependency_overrides[get_product_repository] = lambda: FakeProductRepository()

    try:
        with TestClient(app) as client:
            response = client.patch("/products/1", json={"name": "Updated Product"})

        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "name": "Updated Product",
            "price": "9.99",
            "quantity": 1,
        }
    finally:
        app.dependency_overrides.pop(get_product_repository, None)


def test_patch_product_rejects_null_values() -> None:
    app.dependency_overrides[get_product_repository] = lambda: FakeProductRepository()

    try:
        with TestClient(app) as client:
            response = client.patch("/products/1", json={"name": None})

        assert response.status_code == 422
    finally:
        app.dependency_overrides.pop(get_product_repository, None)


def test_missing_products_return_404() -> None:
    app.dependency_overrides[get_product_repository] = lambda: FakeProductRepository()

    try:
        with TestClient(app) as client:
            get_response = client.get("/products/999")
            update_response = client.put(
                "/products/999",
                json={"name": "Missing Product", "price": "9.99", "quantity": 1},
            )
            delete_response = client.delete("/products/999")

        assert get_response.status_code == 404
        assert update_response.status_code == 404
        assert delete_response.status_code == 404
    finally:
        app.dependency_overrides.pop(get_product_repository, None)
