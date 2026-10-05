from app.invoice.pdf_reader import (
    extract_text_with_ocr_fallback
)

from app.invoice.llm_extractor import (
    extract_invoice_data
)

from app.invoice.validator import (
    validate_invoice
)

from app.invoice.schemas import (
    InvoiceProcessingResult
)


def run_invoice_pipeline(
    pdf_bytes: bytes
) -> InvoiceProcessingResult:

    # Step 1: Extract text from PDF
    extracted_text, ocr_pages = (
        extract_text_with_ocr_fallback(pdf_bytes)
    )

    if not extracted_text:
        raise ValueError(
            "No text could be extracted from the PDF."
        )

    # Step 2: Extract structured invoice data using Groq
    invoice_data = extract_invoice_data(
        extracted_text
    )

    # Step 3: Validate extracted invoice data
    validation_result = validate_invoice(
        invoice_data
    )

    # Step 4: Return complete processing result
    return InvoiceProcessingResult(
        ocr_used=bool(ocr_pages),
        ocr_pages=ocr_pages,
        extracted_text=extracted_text,
        invoice=invoice_data,
        validation=validation_result
    )