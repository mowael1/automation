import pymupdf


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
