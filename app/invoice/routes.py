
from fastapi import APIRouter, UploadFile, File, HTTPException
import pymupdf

from app.invoice.pdf_reader import (
    extract_text_from_pdf,
    needs_ocr
)


router = APIRouter(
    prefix="/api/v1/invoices",
    tags=["Invoices"]
)


@router.post("/extract-text")
async def extract_invoice_text(file: UploadFile = File(...)):

    # 1. Check file extension
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # 2. Read uploaded PDF
    pdf_bytes = await file.read()

    # 3. Check if file is empty
    if not pdf_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty."
        )

    # 4. Extract text
    try:
        extracted_text = extract_text_from_pdf(pdf_bytes)

    except (pymupdf.FileDataError, pymupdf.EmptyFileError):
        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted PDF file."
        )

    # 5. Return result
    requires_ocr = needs_ocr(extracted_text)

    return {
        "filename": file.filename,
        "extracted_text": extracted_text,
        "requires_ocr": requires_ocr
    }
