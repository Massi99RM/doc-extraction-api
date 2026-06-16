from azure.ai.documentintelligence.aio import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from app.config import settings

async def extract_text(file_bytes: bytes):
    # create client, call begin_analyze_document, await the result
    async with DocumentIntelligenceClient(settings.azure_url, AzureKeyCredential(settings.azure_key)) as client:
        poller = await client.begin_analyze_document("prebuilt-invoice", file_bytes)
        result = await poller.result()
        return result