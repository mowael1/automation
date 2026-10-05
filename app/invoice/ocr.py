from io import BytesIO

import pymupdf
import pytesseract
from PIL import Image


def extract_text_from_page_with_ocr(
    page: pymupdf.Page,
    languages: str = "eng+ara"
) -> str:
    """
    Convert a PDF page to an image and extract text using Tesseract OCR.
    """

    pixmap = page.get_pixmap(
        dpi=300,
        alpha=False
    )

    image_bytes = pixmap.tobytes("png")

    image = Image.open(
        BytesIO(image_bytes)
    )

    text = pytesseract.image_to_string(
        image,
        lang=languages
    )

    return text.strip()