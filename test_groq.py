# from pathlib import Path

# from app.invoice.pdf_reader import extract_text_with_ocr_fallback
# from app.invoice.llm_extractor import extract_invoice_data
# from app.invoice.validator import validate_invoice
# pdf_bytes = Path(
#     "sample_invoices/test_invoice.pdf"
# ).read_bytes()


# text, ocr_pages = extract_text_with_ocr_fallback(
#     pdf_bytes
# )


# print("\n========== RAW EXTRACTED TEXT ==========")
# print(text)

# print("\n========== OCR PAGES ==========")
# print(ocr_pages)

# invoice = extract_invoice_data(text)

# validation = validate_invoice(invoice)

# print("Extracted Invoice:")
# print(
#     invoice.model_dump_json(
#         indent=2
#     )
# )

# print("\nValidation Result:")
# print(
#     validation.model_dump_json(
#         indent=2
#     )
# )

# print(
#     invoice.model_dump_json(
#         indent=2
#     )
# )


from pathlib import Path

from app.invoice.pipeline import (
    run_invoice_pipeline
)


pdf_bytes = Path(
    "sample_invoices/test_invoice.pdf"
).read_bytes()


result = run_invoice_pipeline(
    pdf_bytes
)


print(
    result.model_dump_json(
        indent=2
    )
)