from typing import Protocol

from inventory_api.repositories.generic_repository import Repository
from inventory_api.schemas.product import Product


class IProductRepository(Repository[Product], Protocol):
    ...
