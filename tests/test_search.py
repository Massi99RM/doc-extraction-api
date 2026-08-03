from unittest.mock import AsyncMock, patch
import pytest
from app.api.routes.search import indexing, storage

@pytest.mark.asyncio
async def test_search_by_text(client):
    with patch.object(indexing, "search_invoices", new_callable=AsyncMock) as mock:
        mock.return_value = [
            {"id": "inv_1", "total": 100.0},
            {"id": "inv_2", "total": 250.5}
        ]
        
        response = client.get("/invoices/search?query=test")
        
        assert response.status_code == 200
        assert response.json() == [
            {"id": "inv_1", "total": 100.0},
            {"id": "inv_2", "total": 250.5}
        ]
        mock.assert_awaited_once_with("test")


@pytest.mark.asyncio
async def test_search_by_id_success(client):
    with patch.object(storage, "get_invoice", new_callable=AsyncMock) as mock:
        mock.return_value = {"id": "12345", "vendor": "ACME Corp", "total": 500.0}
        
        response = client.get("/invoices/12345")
        
        assert response.status_code == 200
        assert response.json() == {"id": "12345", "vendor": "ACME Corp", "total": 500.0}
        mock.assert_awaited_once_with("12345")


@pytest.mark.asyncio
async def test_search_by_id_not_found(client):
    with patch.object(storage, "get_invoice", new_callable=AsyncMock) as mock:
        mock.return_value = None
        
        response = client.get("/invoices/nonexistent_id")
        
        assert response.status_code == 200
        assert response.json() is None
        mock.assert_awaited_once_with("nonexistent_id")