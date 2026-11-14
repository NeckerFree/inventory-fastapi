#file: src/inventory_api/schemas/product.py
from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal

@dataclass
class Product:
    id: int
    name: str
    price: Decimal
    quantity: int

    def __post_init__(self) -> None:
        if self.id <= 0:
            raise ValueError("Product ID must be positive")
        if self.price <= Decimal("0"):
            raise ValueError("Product price cannot be zero or negative")
        if not self.name.strip():
            raise ValueError("Product name cannot be empty")
        if self.quantity < 0:
            raise ValueError("Product quantity cannot be negative")

class ProductCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(min_length=3, max_length=100)
    price: Decimal = Field(gt=0)
    quantity: int = Field(ge=0)


class ProductUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(min_length=3, max_length=100)
    price: Decimal = Field(gt=0)
    quantity: int = Field(ge=0)


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: Decimal
    quantity: int
