# Inventory API

A small FastAPI application for managing inventory products. It demonstrates request validation with Pydantic, a service layer, and a repository interface backed by an in-memory implementation.

## Architecture

<img width="4032" height="2454" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/e2a25bc6-ac29-4c88-8d86-d5d1681fa149" />

## Features

- Create, list, retrieve, update, and delete products
- Validate product names, prices, quantities, and IDs
- Return a consistent `404 Not Found` response when a product does not exist
- Replace the repository dependency during tests
- Add `X-Request-ID` and `X-Process-Time` headers to responses
- Interactive API documentation at `/docs`

## Requirements

- Python
- FastAPI and Uvicorn
- Pytest and HTTPX to run the API tests

Install the packages in a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install fastapi uvicorn pytest httpx
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
| `PATCH` | `/products/{product_id}` | Partially update a product |
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

The missing-product response includes `type`, `title`, `status`, `detail`, and `instance` fields. The `X-Request-ID` response header echoes a supplied request ID or contains a generated ID.

## Run tests

Run the tests from the project root:

```powershell
python -m pytest test/test.py
```

The tests cover repository dependency overrides, product updates, validation, and missing-product responses.

## Project layout

```text
src/inventory_api/
  main.py                              FastAPI app, middleware, and error handler
  repositories/
    generic_repository.py              Generic repository protocol
    inmemory_product_repository.py     In-memory product repository
    product_repository.py              Product repository protocol
    repository_dependencies.py         Repository dependency provider
  routers/
    products.py                        Product endpoints
  schemas/
    product.py                         Product model and request/response schemas
  services/
    errors/
      product_not_found.py             Missing-product exception
    fake_database_session.py           Fake database session
    product_service.py                 Product service
    service_dependencies.py            Service dependency provider
test/
  fake_product_repository.py           Test repository
  test.py                               API tests
```

The in-memory repository retains data only while the application process is running. Restarting the server clears all products.
