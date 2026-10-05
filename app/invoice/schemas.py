from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class InvoiceItem(BaseModel):
    description: str = Field(
        description="Description or name of the invoice item"
    )

    quantity: Decimal = Field(
        description="Quantity of the item"
    )

    unit_price: Decimal = Field(
        description="Price per unit"
    )

    amount: Decimal = Field(
        description="Total amount for this line item"
    )


class InvoiceData(BaseModel):
    invoice_number: str = Field(
        description="Invoice number or invoice identifier"
    )

    invoice_date: date = Field(
        description="Invoice issue date"
    )

    due_date: date | None = Field(
        default=None,
        description="Invoice due date if available"
    )

    supplier_name: str = Field(
        description="Name of the company or person issuing the invoice"
    )

    customer_name: str | None = Field(
        default=None,
        description="Name of the customer receiving the invoice"
    )

    currency: str = Field(
        description="Invoice currency such as EGP, USD, EUR"
    )

    items: list[InvoiceItem] = Field(
        default_factory=list,
        description="List of invoice line items"
    )

    subtotal: Decimal | None = Field(
        default=None,
        description="Subtotal before taxes"
    )

    tax_amount: Decimal | None = Field(
        default=None,
        description="Total tax amount"
    )

    total_amount: Decimal = Field(
        description="Final invoice total"
    )

    payment_status: str | None = Field(
        default=None,
        description="Payment status if available"
    )