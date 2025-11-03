# FastAPI CRUD Service

A simple FastAPI service demonstrating CRUD operations with automated testing via GitHub Actions.

## Features

- Simple item management (Create, Read, Update, Delete)
- In-memory storage
- 17 comprehensive tests
- CI/CD with GitHub Actions

## Project Structure

```
Github_Lab/
├── src/
│   └── main.py          # FastAPI application
├── tests/
│   └── test_main.py     # Test suite
└── requirements.txt     # Dependencies
├── results              #Output screenshots
```

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_main.py::test_create_item -v
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| POST | `/items` | Create new item |
| GET | `/items` | Get all items |
| GET | `/items/{id}` | Get single item |
| PUT | `/items/{id}` | Update item |
| DELETE | `/items/{id}` | Delete item |

## Example Usage

```bash
# Create an item
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Item", "description": "A test item"}'

# Get all items
curl http://localhost:8000/items

# Update an item
curl -X PUT http://localhost:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated", "description": "Updated description"}'

# Delete an item
curl -X DELETE http://localhost:8000/items/1
```

## CI/CD

GitHub Actions automatically runs tests on every push and pull request.