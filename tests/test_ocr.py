from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from app.services import ocr

@pytest.mark.asyncio
async def test_extract_text_success():
    # Arrange mock data and expected results
    fake_file_bytes = b"fake-pdf-content"
    expected_result = {"status": "succeeded", "content": "Extracted invoice text"}

    # Mock the poller object returned by begin_analyze_document
    mock_poller = AsyncMock()
    mock_poller.result.return_value = expected_result

    # Mock the DocumentIntelligenceClient instance
    mock_client = AsyncMock()
    mock_client.begin_analyze_document.return_value = mock_poller

    # Configure the client to act as an async context manager
    mock_client_instance = MagicMock()
    mock_client_instance.__aenter__.return_value = mock_client
    mock_client_instance.__aexit__.return_value = None

    # Patch the DocumentIntelligenceClient class constructor
    with patch(
        "app.services.ocr.DocumentIntelligenceClient",
        return_value=mock_client_instance,
    ) as mock_client_cls:
        
        result = await ocr.extract_text(fake_file_bytes)

        assert result == expected_result
        
        # Verify settings were passed correctly to the client
        mock_client_cls.assert_called_once()
        
        # Verify `begin_analyze_document` was called with the correct model and payload
        mock_client.begin_analyze_document.assert_awaited_once_with(
            "prebuilt-invoice", fake_file_bytes
        )
        
        # Verify `result()` was awaited on the poller
        mock_poller.result.assert_awaited_once()