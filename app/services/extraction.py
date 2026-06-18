from anthropic import AsyncAnthropic
from app.config import settings

INVOICE_TOOL = {
    "name": "extract_invoice_data",
    "description": "given an OCR extracted invoice text having products with descriptions and a price, extract the vendor, date and the total amount on the invoice",
    "input_schema": {
        "type": "object",
        "properties": {
            "vendor": {"type": "string"},
            "date": {"type": "string"},
            "amount": {"type": "number"},
            "line_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "price": {"type": "number"},

                    },
                },
            
            },

        },
        "required": ["vendor", "date", "amount", "line_items"]
    }
}

async def extract_invoice(ocr_text: str):
    async with AsyncAnthropic(api_key=settings.claude_api_key) as client:
    # extract the tool_use block's input and return it
        answer = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1000,
            messages=[{"role": "user", "content": ocr_text}],
            tools=[INVOICE_TOOL],
            tool_choice={"type": "tool", "name": "extract_invoice_data"}
        )

        return answer.content[0].input