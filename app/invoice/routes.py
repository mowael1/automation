import pymupdf

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
)

from app.invoice.pdf_reader import (
    extract_text_with_ocr_fallback,
)

from app.invoice.pipeline import (
    run_invoice_pipeline,
)

from app.invoice.schemas import (
    InvoiceProcessingResult,
)

router = APIRouter(
    prefix="/api/v1/invoices",
    tags=["Invoices"]
)


@router.post("/extract-text")
async def extract_invoice_text(
    file: UploadFile = File(...)
):

    # Check file extension
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # Read uploaded file
    pdf_bytes = await file.read()

    if not pdf_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty."
        )

    try:

        extracted_text, ocr_pages = (
            extract_text_with_ocr_fallback(pdf_bytes)
        )

    except (pymupdf.FileDataError, pymupdf.EmptyFileError):

        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted PDF file."
        )

    # Determine extraction method
    if not ocr_pages:
        extraction_method = "pymupdf"

    else:
        extraction_method = "hybrid"

    return {
        "filename": file.filename,
        "extraction_method": extraction_method,
        "ocr_used": bool(ocr_pages),
        "ocr_pages": ocr_pages,
        "extracted_text": extracted_text
    }
    
@router.post(
    "/process",
    response_model=InvoiceProcessingResult
)
async def process_invoice(
    file: UploadFile = File(...)
):

    # 1. Validate file extension
    if (
        not file.filename
        or not file.filename.lower().endswith(".pdf")
    ):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # 2. Read uploaded PDF
    pdf_bytes = await file.read()

    # 3. Check empty file
    if not pdf_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty."
        )

    # 4. Run complete invoice pipeline
    try:
        result = run_invoice_pipeline(
            pdf_bytes
        )

    except (
        pymupdf.FileDataError,
        pymupdf.EmptyFileError
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted PDF file."
        )

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error)
        )

    # 5. Return structured result
    return result