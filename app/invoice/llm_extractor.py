import json

from groq import Groq

from app.core.config import settings
from app.invoice.schemas import InvoiceData


client = Groq(
    api_key=settings.groq_api_key
)


def extract_invoice_data(invoice_text: str) -> InvoiceData:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are an invoice data extraction system. "
                    "Extract only information that exists in the invoice text. "
                    "Do not invent missing information. "
                    "If an optional field is missing, return null. "
                    "Return dates in YYYY-MM-DD format whenever possible. "
                    "Return monetary values as numbers without currency symbols "
                    "or thousands separators."
                    "Never calculate or infer missing line-item values. "
                    "Do not derive an item amount from subtotal differences. "
                    "If quantity, unit price, or amount is not explicitly visible "
                    "in the provided text, return null for that field."
                )
            },
            {
                "role": "user",
                "content": invoice_text
            }
        ],

        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "invoice_data",
                "strict": True,
                "schema": InvoiceData.model_json_schema()
            }
        }
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("Groq returned an empty response.")

    data = json.loads(content)

    return InvoiceData.model_validate(data)