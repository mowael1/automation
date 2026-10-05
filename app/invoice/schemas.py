from pydantic import BaseModel, ConfigDict


class InvoiceItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    description: str
    quantity: float | None
    unit_price: float | None
    amount: float | None


class InvoiceAdjustment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: str
    amount: float

class InvoiceData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    invoice_number: str
    invoice_date: str
    due_date: str | None

    supplier_name: str
    customer_name: str | None

    currency: str

    items: list[InvoiceItem]

    subtotal: float | None
    tax_amount: float | None
    total_amount: float

    payment_status: str | None
    
    adjustments: list[InvoiceAdjustment]
    
class InvoiceValidationResult(BaseModel):
    is_valid: bool
    errors: list[str]
    warnings: list[str]
    

class InvoiceProcessingResult(BaseModel):
    ocr_used: bool
    ocr_pages: list[int]

    extracted_text: str

    invoice: InvoiceData
    validation: InvoiceValidationResult