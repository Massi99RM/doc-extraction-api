import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock
from app.main import app

@pytest.fixture
def client():
    """Returns a TestClient wrapping the FastAPI app, managing the lifespan context."""
    with TestClient(app) as c:
        yield c

@pytest.fixture
def sample_invoice():
    """Returns a dictionary representing a clean, extracted invoice."""
    return {
        "vendor": "Acme Cloud Services, Inc.",
        "invoice_number": "INV-2026-0891",
        "date": "2026-07-15",
        "due_date": "2026-08-14",
        "currency": "USD",
        "subtotal": 1250.00,
        "tax": 100.00,
        "total": 1350.00,
        "line_items": [
            {
                "description": "Enterprise Cloud Hosting - July 2026",
                "quantity": 1,
                "unit_price": 1000.00,
                "amount": 1000.00
            },
            {
                "description": "Automated Backup Storage (500GB)",
                "quantity": 5,
                "unit_price": 50.00,
                "amount": 250.00
            }
        ],
        "billing_address": {
            "name": "Globex Corporation",
            "street": "123 Tech Way, Suite 400",
            "city": "San Francisco",
            "state": "CA",
            "zip_code": "94107"
        }
    }

@pytest.fixture
def mock_mongo():
    """Returns a MagicMock simulating a MongoDB collection (supporting async operations)."""
    mock = MagicMock()
    mock.find_one = AsyncMock()
    mock.insert_one = AsyncMock()
    return mock

@pytest.fixture
def mock_elastic():
    """Returns a MagicMock simulating an Elasticsearch client."""
    mock = MagicMock()
    mock.search = AsyncMock()
    mock.index = AsyncMock()
    return mock