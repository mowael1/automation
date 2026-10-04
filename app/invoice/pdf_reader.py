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
