# file: src/inventory_api/repositories/repository_dependencies.py
from inventory_api.repositories.inmemory_product_repository import (
    InMemoryProductRepository,
)
from inventory_api.repositories.product_repository import IProductRepository
from fastapi.params import Depends
from typing_extensions import Annotated


_product_repository = InMemoryProductRepository()


def get_product_repository() -> IProductRepository:
    return _product_repository


ProductRepositoryDependency = Annotated[
    IProductRepository, Depends(get_product_repository)
]
