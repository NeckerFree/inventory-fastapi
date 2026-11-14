#file: src/inventory_api/main.py
from fastapi import FastAPI
from inventory_api.routers import products

app = FastAPI(
    title="Inventory API", description="Cloud Inventory Management API", version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Inventory API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}

app.include_router(products.router)