from app.db import elastic

async def index_invoice(invoice_id: str, invoice_data: dict):
    # index the invoice in Elasticsearch
    index_document = await elastic.es.index(index="invoices", id=invoice_id, document=invoice_data)
    return index_document

async def search_invoices(query: str):
    # search invoices by query string
    results = await elastic.es.search(index="invoices", body={"query": {"match": {"_all": query}}})
    return results