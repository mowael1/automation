import pymupdf

from app.invoice.ocr import extract_text_from_page_with_ocr


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text from all pages of a PDF file.
    """

    pages_text = []

    with pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf"
    ) as document:

        for page in document:
            text = page.get_text("text")
            pages_text.append(text)

    return "\n".join(pages_text).strip()




def needs_ocr(
    text: str,
    min_chars: int = 50,
    min_readable_ratio: float = 0.60
) -> bool:

    # 1. Empty text
    if not text or not text.strip():
        return True

    # 2. Remove whitespace
    clean_chars = [
        char for char in text
        if not char.isspace()
    ]

    # 3. Count letters and numbers
    readable_chars = sum(
        char.isalnum()
        for char in clean_chars
    )

    # 4. Check minimum text length
    if readable_chars < min_chars:
        return True

    # 5. Calculate readable characters ratio
    readable_ratio = readable_chars / len(clean_chars)

    if readable_ratio < min_readable_ratio:
        return True

    return False


def extract_text_with_ocr_fallback(
    pdf_bytes: bytes
) -> tuple[str, list[int]]:
    """
    Extract text page by page.

    Use PyMuPDF when enough text is available.
    Fall back to OCR when the extracted text is insufficient.

    Returns:
        tuple:
            - Full extracted text
            - List of page numbers that required OCR
    """

    pages_text = []
    ocr_pages = []

    with pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf"
    ) as document:

        for page_number, page in enumerate(document, start=1):

            # Try normal PDF text extraction first
            text = page.get_text("text").strip()

            # If text quality is poor, use OCR
            if needs_ocr(text):

                text = extract_text_from_page_with_ocr(page)

                ocr_pages.append(page_number)

            pages_text.append(text)

    full_text = "\n\n".join(pages_text).strip()

    return full_text, ocr_pages