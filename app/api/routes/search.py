from fastapi import APIRouter
from app.services import storage, indexing

router = APIRouter()

@router.get("/invoices/search")
async def search_by_text(query: str):
    # Query Elasticsearch for invoices matching the search string
    match_list = await indexing.search_invoices(query)
    return match_list

@router.get("/invoices/{id}")
async def search_by_id(id: str):
    # Fetch a single invoice from MongoDB by its id
    invoice = await storage.get_invoice(id)
    return invoice