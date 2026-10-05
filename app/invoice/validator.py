from decimal import Decimal

from app.invoice.schemas import (
    InvoiceData,
    InvoiceValidationResult,
)


def to_decimal(value: float | None) -> Decimal | None:
    if value is None:
        return None

    return Decimal(str(value))


def amounts_equal(
    first: Decimal,
    second: Decimal,
    tolerance: Decimal = Decimal("0.01"),
) -> bool:
    return abs(first - second) <= tolerance


def validate_invoice(
    invoice: InvoiceData
) -> InvoiceValidationResult:

    errors = []
    warnings = []

    # ---------------------------------
    # 1. Validate individual line items
    # ---------------------------------

    for index, item in enumerate(invoice.items, start=1):

        quantity = to_decimal(item.quantity)
        unit_price = to_decimal(item.unit_price)
        amount = to_decimal(item.amount)

        # We cannot validate the calculation
        # if OCR/LLM could not extract all values.
        if (
            quantity is None
            or unit_price is None
            or amount is None
        ):
            warnings.append(
                f"Item {index} ({item.description}) has missing "
                "values and could not be fully validated."
            )
            continue

        expected_amount = quantity * unit_price

        if not amounts_equal(
            expected_amount,
            amount
        ):
            errors.append(
                f"Item {index} ({item.description}): "
                "quantity × unit_price does not equal amount."
            )

    # ---------------------------------
    # 2. Validate subtotal
    # ---------------------------------

    if invoice.subtotal is not None:

        subtotal = to_decimal(invoice.subtotal)

        item_amounts = [
            to_decimal(item.amount)
            for item in invoice.items
        ]

        # Only verify subtotal if every item amount
        # was successfully extracted.
        if all(
            amount is not None
            for amount in item_amounts
        ):

            calculated_subtotal = sum(
                item_amounts,
                Decimal("0")
            )

            if not amounts_equal(
                calculated_subtotal,
                subtotal
            ):
                errors.append(
                    "Sum of line item amounts "
                    "does not equal subtotal."
                )

        else:
            warnings.append(
                "Subtotal could not be fully validated "
                "because one or more line item amounts are missing."
            )

    # ---------------------------------
    # 3. Validate final total
    # ---------------------------------

    if (
        invoice.subtotal is not None
        and invoice.tax_amount is not None
    ):

        subtotal = to_decimal(invoice.subtotal)
        tax = to_decimal(invoice.tax_amount)
        total = to_decimal(invoice.total_amount)

        adjustments_total = Decimal("0")

        for adjustment in invoice.adjustments:
            adjustments_total += Decimal(
                str(adjustment.amount)
            )

        expected_total = (
            subtotal
            + adjustments_total
            + tax
        )

        if not amounts_equal(
            expected_total,
            total
        ):
            errors.append(
                "Subtotal + adjustments + tax "
                "does not equal total."
            )

    return InvoiceValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
    )