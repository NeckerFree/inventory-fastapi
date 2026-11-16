#file: src/inventory_api/routers/products.py
from fastapi import APIRouter, HTTPException, status

from inventory_api.schemas.product import (ProductCreate, ProductPatch, ProductUpdate, ProductResponse)

from inventory_api.services.product_service import ProductServiceDependency
router = APIRouter(prefix="/products", tags=["Products"])
def CreateProductResponse(product):
        return ProductResponse(
            id=product.id,
            name=product.name,
            price=product.price,
            quantity=product.quantity
        )
#get by id
@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int,
                      service: ProductServiceDependency) -> ProductResponse:
    product = service.get_product(product_id)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return CreateProductResponse(product=product)

@router.get("/", response_model=list[ProductResponse])
async def get_all_products(service: ProductServiceDependency) -> list[ProductResponse]:
    products = service.get_all_products()
    return [CreateProductResponse(product=product) for product in products] 


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product_create: ProductCreate,
                         service: ProductServiceDependency) -> ProductResponse:
    product = service.create_product(product_create.model_dump())
    return CreateProductResponse(product=product)

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int,
                         product_update: ProductUpdate,
                         service: ProductServiceDependency) -> ProductResponse:
    product = service.update_product(product_id, product_update.model_dump())
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    return CreateProductResponse(product=product)

@router.patch("/{product_id}", response_model=ProductResponse)
async def patch_product(product_id: int,
                        product_patch: ProductPatch,
                        service: ProductServiceDependency) -> ProductResponse:
    product = service.patch_product(
        product_id, product_patch.model_dump(exclude_unset=True)
    )
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    return CreateProductResponse(product=product)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int,
                         service: ProductServiceDependency) -> None:
    success = service.delete_product(product_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )