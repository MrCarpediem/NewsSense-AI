from PIL import Image
import pytesseract
import os


def extract_text_from_image(image_path: str) -> str:
    """
    Extracts text from an image using Tesseract OCR.
    Supports English + Hindi.
    """

    if not os.path.exists(image_path):
        return ""

    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang="eng+hin")
        return text.strip()
    except Exception as e:
        print("OCR Error:", e)
        return ""
