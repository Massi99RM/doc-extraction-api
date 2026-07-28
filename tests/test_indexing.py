import pytest
from unittest.mock import AsyncMock, patch
from app.db import elastic
from app.services.indexing import index_invoice, search_invoices

@pytest.mark.asyncio
async def test_index_invoice(sample_invoice):
    """Test indexing an invoice into Elasticsearch successfully."""
    invoice_id = "inv_12345"
    
    # Mock the return value of elastic.es.index
    mock_response = {
        "_id": invoice_id,
        "_index": "invoices",
        "result": "created",
        "_shards": {"total": 2, "successful": 1, "failed": 0}
    }
    
    with patch.object(elastic, "es") as mock_es:
        mock_es.index = AsyncMock(return_value=mock_response)
        
        result = await index_invoice(invoice_id, sample_invoice)
        
        # Verify Elasticsearch index method was called correctly
        mock_es.index.assert_awaited_once_with(
            index="invoices",
            id=invoice_id,
            document=sample_invoice
        )
        assert result == mock_response

@pytest.mark.asyncio
async def test_search_invoices(sample_invoice):
    """Test searching for invoices in Elasticsearch."""
    query_string = "Acme Cloud"
    
    # Mock the return value of elastic.es.search
    mock_search_response = {
        "hits": {
            "total": {"value": 1, "relation": "eq"},
            "hits": [
                {
                    "_index": "invoices",
                    "_id": "inv_12345",
                    "_score": 1.0,
                    "_source": sample_invoice
                }
            ]
        }
    }
    
    with patch.object(elastic, "es") as mock_es:
        mock_es.search = AsyncMock(return_value=mock_search_response)
        
        result = await search_invoices(query_string)
        
        # Verify Elasticsearch search method was called with the right query body
        mock_es.search.assert_awaited_once_with(
            index="invoices",
            body={"query": {"match": {"_all": query_string}}}
        )
        assert result == mock_search_response
        assert result["hits"]["total"]["value"] == 1