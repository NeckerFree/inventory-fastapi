# In-memory implementation of the Product repository
from decimal import Decimal

from inventory_api.repositories.product_repository import IProductRepository
from inventory_api.schemas.product import Product

class InMemoryProductRepository(IProductRepository):
    def __init__(self):
        self.products: dict[int, Product] = {}
        self.next_id: int = 1

    def get_by_id(self, product_id: int) -> Product|None:
        return self.products.get(product_id)

    def get_all(self) -> list[Product]:
        return list(self.products.values())

    def create(self, product_data: dict) -> Product:
        product = Product(
            id=self.next_id,
            name=product_data["name"],
            price=Decimal(product_data["price"]),
            quantity=product_data["quantity"],
        )
        self.products[self.next_id] = product
        self.next_id += 1
        return product
    
    def patch(self, product_id: int, product_data: dict) -> Product|None:
        product = self.products.get(product_id)
        if product is None:
            return None
        
        if "name" in product_data:
            product.name = product_data["name"]
        if "price" in product_data:
            product.price = Decimal(product_data["price"])
        if "quantity" in product_data:
            product.quantity = product_data["quantity"]

        return product
    
    def update(self, product_id: int, product_data: dict) -> Product|None:
        product= self.products.get(product_id)
        if product is None:
            return None
        
        product.name = product_data["name"]
        product.price = product_data["price"]
        product.quantity = product_data["quantity"]

        return product

    def delete(self, product_id: int) -> bool:
        if product_id in self.products:
            del self.products[product_id]
            return True
        return False
