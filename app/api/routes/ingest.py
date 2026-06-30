from fastapi import APIRouter, UploadFile
from app.services import ocr, extraction, storage, indexing

router = APIRouter()

@router.post("/invoices/upload")
async def upload_invoice(file: UploadFile):
    file_bytes = await file.read()

    # Azure OCR returns structured layout data, the flat text is for Claude
    ocr_result = await ocr.extract_text(file_bytes)
    ocr_text = ocr_result.content

    # Claude interprets the raw OCR text into structured invoice fields
    invoice_data = await extraction.extract_invoice(ocr_text)
    
    # MongoDB is the source: save first so there is an id to index against
    invoice_id = await storage.save_invoice(invoice_data)
    
    # Elasticsearch indexes the extracted fields for search
    await indexing.index_invoice(invoice_id, invoice_data)
    
    # ObjectId isn't JSON-serializable, better convert it to a string type
    return {"invoice_id": str(invoice_id), "invoice_data": invoice_data}
