from unittest.mock import AsyncMock, MagicMock, patch
from bson import ObjectId
import pytest


@pytest.fixture
def mock_services(sample_invoice):
    """Fixture to mock all external asynchronous services using the provided fixtures and sample data."""
    with patch("app.api.routes.ingest.ocr") as mock_ocr, patch(
        "app.api.routes.ingest.extraction"
    ) as mock_extraction, patch("app.api.routes.ingest.storage") as mock_storage, patch(
        "app.api.routes.ingest.indexing"
    ) as mock_indexing:

        # Configure return values using the detailed sample_invoice data
        mock_ocr.extract_text = AsyncMock(
            return_value=MagicMock(content="Sample OCR text for Acme Cloud Services invoice")
        )
        mock_extraction.extract_invoice = AsyncMock(
            return_value=sample_invoice
        )

        # Generate a dummy ObjectId for storage
        dummy_invoice_id = ObjectId()
        mock_storage.save_invoice = AsyncMock(return_value=dummy_invoice_id)

        mock_indexing.index_invoice = AsyncMock(return_value=None)

        yield {
            "ocr": mock_ocr,
            "extraction": mock_extraction,
            "storage": mock_storage,
            "indexing": mock_indexing,
            "invoice_id": dummy_invoice_id,
        }


@pytest.mark.asyncio
async def test_upload_invoice_success(client, sample_invoice, mock_services):
    """Test the /invoices/upload endpoint successfully processes a file with realistic invoice data."""
    # Arrange
    file_content = b"%PDF-1.4 enterprise cloud hosting invoice PDF bytes..."
    files = {"file": ("acme_invoice.pdf", file_content, "application/pdf")}

    # Act
    response = client.post("/invoices/upload", files=files)

    # Assert
    assert response.status_code == 200
    data = response.json()

    # Verify response structure and serialization
    assert data["invoice_id"] == str(mock_services["invoice_id"])
    assert data["invoice_data"] == sample_invoice
    assert data["invoice_data"]["vendor"] == "Acme Cloud Services, Inc."
    assert data["invoice_data"]["total"] == 1350.00

    # Verify service interactions and proper data piping
    mock_services["ocr"].extract_text.assert_awaited_once_with(file_content)
    mock_services["extraction"].extract_invoice.assert_awaited_once_with(
        "Sample OCR text for Acme Cloud Services invoice"
    )
    mock_services["storage"].save_invoice.assert_awaited_once_with(sample_invoice)
    mock_services["indexing"].index_invoice.assert_awaited_once_with(
        mock_services["invoice_id"], sample_invoice
    )