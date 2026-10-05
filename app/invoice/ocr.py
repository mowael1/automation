from io import BytesIO

import cv2
import numpy as np
import pymupdf
import pytesseract

from PIL import Image


def preprocess_image_for_ocr(
    image: Image.Image
) -> Image.Image:

    # PIL Image -> NumPy array
    image_array = np.array(
        image.convert("RGB")
    )

    # Convert to grayscale
    gray = cv2.cvtColor(
        image_array,
        cv2.COLOR_RGB2GRAY
    )

    # Convert image to binary
    binary = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )[1]

    # Detect horizontal table lines
    horizontal_kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (40, 1)
    )

    horizontal_lines = cv2.morphologyEx(
        binary,
        cv2.MORPH_OPEN,
        horizontal_kernel
    )

    # Detect vertical table lines
    vertical_kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (1, 40)
    )

    vertical_lines = cv2.morphologyEx(
        binary,
        cv2.MORPH_OPEN,
        vertical_kernel
    )

    # Combine table lines
    table_lines = cv2.bitwise_or(
        horizontal_lines,
        vertical_lines
    )

    # Remove table lines from image
    cleaned = cv2.bitwise_and(
        binary,
        cv2.bitwise_not(table_lines)
    )

    # Tesseract expects black text on white background
    cleaned = cv2.bitwise_not(cleaned)

    return Image.fromarray(cleaned)


def extract_text_from_page_with_ocr(
    page: pymupdf.Page,
    languages: str = "eng"
) -> str:

    pixmap = page.get_pixmap(
        dpi=400,
        alpha=False
    )

    image_bytes = pixmap.tobytes("png")

    image = Image.open(
        BytesIO(image_bytes)
    )

    image = preprocess_image_for_ocr(
        image
    )

    custom_config = (
        "--oem 3 "
        "--psm 6 "
        "-c preserve_interword_spaces=1"
    )

    text = pytesseract.image_to_string(
        image,
        lang=languages,
        config=custom_config
    )

    return text.strip()