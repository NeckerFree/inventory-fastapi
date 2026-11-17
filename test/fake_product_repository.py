from decimal import Decimal

from inventory_api.repositories.inmemory_product_repository import InMemoryProductRepository
from inventory_api.schemas.product import Product


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