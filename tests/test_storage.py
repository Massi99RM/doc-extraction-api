import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from bson import ObjectId

from app.services.storage import save_invoice, get_invoice

@pytest.mark.asyncio
async def test_save_invoice(sample_invoice):
    with patch("app.services.storage.mongo") as mock_mongo_module:
        # Setup the mock database and collection behavior
        mock_collection = MagicMock() 
        mock_collection.insert_one = AsyncMock() 
        fake_inserted_id = ObjectId() 
        mock_collection.insert_one.return_value.inserted_id = fake_inserted_id
        
        # Configure mongo.db to return the mock collection
        mock_mongo_module.db = {
            "invoice_collection": mock_collection
        }

        # Call save_invoice
        result_id = await save_invoice(sample_invoice)

        mock_collection.insert_one.assert_awaited_once_with(sample_invoice)
        assert result_id == fake_inserted_id

@pytest.mark.asyncio
async def test_get_invoice(sample_invoice):
    with patch("app.services.storage.mongo") as mock_mongo_module:
        # Setup the mock database and collection behavior
        mock_collection = MagicMock()
        mock_collection.find_one = AsyncMock(return_value=sample_invoice)
        valid_object_id = ObjectId()
        
        # Configure mongo.db to return the mock collection
        mock_mongo_module.db = {
            "invoice_collection": mock_collection
        }

        # Call get_invoice with a valid ObjectId string
        result = await get_invoice(str(valid_object_id))

        mock_collection.find_one.assert_awaited_once_with({"_id": valid_object_id})
        assert result == sample_invoice