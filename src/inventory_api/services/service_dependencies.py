#file: src/inventory_api/services/product_service.py
from decimal import Decimal
from fastapi.params import Depends
from typing_extensions import Annotated
from inventory_api.repositories.product_repository import IProductRepository
from inventory_api.repositories.repository_dependencies import ProductRepositoryDependency
from inventory_api.schemas.product import Product

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


def get_product_service(repository: ProductRepositoryDependency) -> ProductService:
    return ProductService(repository=repository)

ProductServiceDependency = Annotated[
    ProductService,
    Depends(get_product_service),
]



