import re

def clean_ocr_text(text):
    # Remove junk symbols
    text = re.sub(r"[^a-zA-Z0-9.,!?₹₹\u0900-\u097F\s]", " ", text)

    # Remove very short words (OCR garbage)
    words = text.split()
    words = [w for w in words if len(w) > 2]

    cleaned = " ".join(words)

    return cleaned.strip()
