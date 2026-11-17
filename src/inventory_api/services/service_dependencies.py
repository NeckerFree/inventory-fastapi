#file: src/inventory_api/services/product_service.py
from fastapi.params import Depends
from typing_extensions import Annotated

from inventory_api.repositories.repository_dependencies import ProductRepositoryDependency
from inventory_api.services.fake_database_session import FakeDatabaseSession
from inventory_api.services.product_service import ProductService


def get_product_service(repository: ProductRepositoryDependency) -> ProductService:
    return ProductService(repository=repository)

ProductServiceDependency = Annotated[
    ProductService,
    Depends(get_product_service),
]

def get_db_session():
    session = FakeDatabaseSession()

    try:
        yield session
    finally:
        session.close()

Annotated[FakeDatabaseSession, Depends(get_db_session)]
