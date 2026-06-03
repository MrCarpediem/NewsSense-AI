from PIL import Image
import pytesseract
import os


def extract_text_from_image(image_path: str) -> str:
    """
    Extracts text from an image using Tesseract OCR.
    Supports English + Hindi.
    Resizes large images for faster processing.
    """

    if not os.path.exists(image_path):
        return ""

    try:
        img = Image.open(image_path)
        
        # Resize large images for speed (max 1500px on longest side)
        max_dim = 1500
        if max(img.size) > max_dim:
            ratio = max_dim / max(img.size)
            new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
            img = img.resize(new_size, Image.LANCZOS)
        
        # Convert to grayscale for better OCR accuracy and speed
        img = img.convert('L')
        
        text = pytesseract.image_to_string(img, lang="eng")
        return text.strip()
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""
