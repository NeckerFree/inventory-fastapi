#file: src/inventory_api/services/product_service.py
from decimal import Decimal
from fastapi.params import Depends
from typing_extensions import Annotated

from inventory_api.dependencies import IProductRepository
from inventory_api.schemas.product import Product

# In-memory implementation of the Product repository
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

#returning None is appropriate
    def delete(self, product_id: int) -> bool:
        if product_id in self.products:
            del self.products[product_id]
            return True
        return False

# Service layer for Product operations
class ProductService:
    def __init__(self, repository: IProductRepository):
        self.repository = repository

    def get_product(self, product_id: int) -> Product|None:
        return self.repository.get_by_id(product_id)

    def get_all_products(self) -> list[Product]:
        return self.repository.get_all()
    
    def create_product(self, product_data: dict) -> Product:
        return self.repository.create(product_data)

    def update_product(self, product_id: int, product_data: dict) -> Product | None:
        return self.repository.update(product_id, product_data)
    
    def patch_product(self, product_id: int, product_data: dict) -> Product | None:
        return self.repository.patch(product_id, product_data)

    def delete_product(self, product_id: int) -> bool:
        return self.repository.delete(product_id)

_product_repository = InMemoryProductRepository()


def get_product_repository() -> IProductRepository:
    return _product_repository


ProductRepositoryDependency = Annotated[
    IProductRepository,
    Depends(get_product_repository),
]


def get_product_service(repository: ProductRepositoryDependency) -> ProductService:
    return ProductService(repository=repository)


ProductServiceDependency = Annotated[
    ProductService,
    Depends(get_product_service),
]



