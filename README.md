# Inventory API

A small FastAPI application for managing inventory products. It demonstrates request validation with Pydantic, a service layer, and a repository interface backed by an in-memory implementation.

## Features

- Create, list, retrieve, update, and delete products
- Validate product names, prices, quantities, and IDs
- Return `404 Not Found` when a requested product does not exist
- Replace the repository dependency during tests
- Interactive API documentation at `/docs`

## Requirements

- Python
- FastAPI and Uvicorn
- Pytest and `httpx2` to run the API tests

Install the packages in a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install fastapi uvicorn pytest httpx2
```

## Run the application

The source code uses the `src` layout. Set `PYTHONPATH` to `src` before starting Uvicorn:

```powershell
$env:PYTHONPATH = "src"
uvicorn inventory_api.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Open `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/` | API status message |
| `GET` | `/health` | Health check |
| `GET` | `/products/` | List products |
| `GET` | `/products/{product_id}` | Retrieve a product |
| `POST` | `/products/` | Create a product |
| `PUT` | `/products/{product_id}` | Update a product |
| `DELETE` | `/products/{product_id}` | Delete a product |

Product creation expects a JSON body such as:

```json
{
  "name": "Wireless Mouse",
  "price": 29.99,
  "quantity": 6
}
```

Names must be 3 to 100 characters, prices must be greater than zero, and quantities must be non-negative. Product IDs start at 1. A missing product returns `404`.

## Run tests

In PowerShell, set the source path and run:

```powershell
$env:PYTHONPATH = "src"
python -m pytest test/test.py
```

The tests cover repository dependency overrides and missing-product responses.

## Project layout

```text
src/inventory_api/
  dependencies.py            Repository protocol
  main.py                    FastAPI application
  routers/products.py        Product endpoints
  schemas/product.py         Product model and request/response schemas
  services/product_service.py Service and in-memory repository
test/
  test.py                    API tests
```

The in-memory repository retains data only while the application process is running. Restarting the server clears all products.
