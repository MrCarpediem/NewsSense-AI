# backend/text_cleaner.py
import re

def clean_ocr_text(text: str) -> str:
    """
    Clean OCR text WITHOUT breaking Hindi or English grammar.
    """

    if not text:
        return ""

    # Normalize line breaks and spaces
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    # Remove junk symbols but keep Hindi, English & punctuation
    text = re.sub(
        r"[^a-zA-Z0-9.,!?₹\u0900-\u097F\s]",
        "",
        text
    )

    return text.strip()
