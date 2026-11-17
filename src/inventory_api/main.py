#file: src/inventory_api/main.py
import time
import uuid

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from inventory_api.routers import products
from inventory_api.services.errors.product_not_found import ProductNotFoundError

app = FastAPI(
    title="Inventory API", description="Cloud Inventory Management API", version="1.0.0"
)

@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next)-> Response:
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    start_time = time.perf_counter()
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    elapsed=time.perf_counter()-start_time
    response.headers["X-Process-Time"]= str(elapsed)
    return response

@app.exception_handler(ProductNotFoundError)
async def product_not_found_handler( request: Request,   exc: ProductNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "type": "about:blank",
            "title": "Product not found",
            "status": 404,
            "detail": str(exc),
            "instance": str(request.url)
        }
    )

@app.get("/")
async def root():
    return {"message": "Inventory API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}

app.include_router(products.router)