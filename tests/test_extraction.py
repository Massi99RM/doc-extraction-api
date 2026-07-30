import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.extraction import extract_invoice

@pytest.mark.asyncio
async def test_extract_invoice():
    mock_tool_input = {
        "vendor": "Acme Corp",
        "date": "2026-06-01",
        "amount": 150.00,
        "line_items": [
            {"description": "Widget A", "price": 150.00}
        ]
    }

    # Mock the response content block structure
    mock_content_block = MagicMock()
    mock_content_block.input = mock_tool_input

    mock_response = MagicMock()
    mock_response.content = [mock_content_block]

    # Setup the AsyncMock for client.messages.create
    mock_messages = AsyncMock()
    mock_messages.create.return_value = mock_response

    mock_client_instance = MagicMock()
    mock_client_instance.messages = mock_messages

    # Make AsyncAnthropic() act as an async context manager returning our mock client
    mock_client_context = AsyncMock()
    mock_client_context.__aenter__.return_value = mock_client_instance

    with patch("app.services.extraction.AsyncAnthropic", return_value=mock_client_context) as mock_anthropic_cls:
        ocr_sample = "Invoice from Acme Corp. Date: June 1, 2026. Widget A - $150.00. Total: $150.00"
        result = await extract_invoice(ocr_sample)

        mock_anthropic_cls.assert_called_once()
        mock_messages.create.assert_awaited_once()
        
        assert result == mock_tool_input
        assert result["vendor"] == "Acme Corp"
        assert result["amount"] == 150.00
        assert len(result["line_items"]) == 1