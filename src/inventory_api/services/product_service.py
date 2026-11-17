# Service layer for Product operations
from inventory_api.repositories.product_repository import IProductRepository
from inventory_api.schemas.product import Product
from inventory_api.services.fake_database_session import FakeDatabaseSession
from inventory_api.services.errors.product_not_found import ProductNotFoundError


class ProductService:
    def __init__(
        self,
        repository: IProductRepository,
        session: FakeDatabaseSession | None = None,
    ):
        self.repository = repository
        self.session = session

    def get_product(self, product_id: int) -> Product:
        product= self.repository.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundError(product_id)
        return product

    def get_all_products(self) -> list[Product]:
        return self.repository.get_all()
    
    def create_product(self, product_data: dict) -> Product:
        return self.repository.create(product_data)

    def update_product(self, product_id: int, product_data: dict) -> Product:
        product = self.repository.update(product_id, product_data)
        if product is None:
            raise ProductNotFoundError(product_id)
        return product
    
    def patch_product(self, product_id: int, product_data: dict) -> Product:
        product = self.repository.patch(product_id, product_data)
        if product is None:
            raise ProductNotFoundError(product_id)
        return product

    def delete_product(self, product_id: int) -> bool:
         product= self.repository.get_by_id(product_id)
         if product is None:
            raise ProductNotFoundError(product_id)
         return self.repository.delete(product_id)

    