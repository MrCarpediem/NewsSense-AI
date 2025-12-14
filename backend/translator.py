import requests
from .config import HF_API_TOKEN, HF_TRANSLATE_EN, HF_TRANSLATE_HI

HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

def translate(text, language):
    if language == "English":
        model = HF_TRANSLATE_EN
    elif language == "Hindi":
        model = HF_TRANSLATE_HI
    else:
        return text

    url = f"https://api-inference.huggingface.co/models/{model}"
    payload = {"inputs": text[:2000]}

    r = requests.post(url, headers=HEADERS, json=payload)
    out = r.json()

    if isinstance(out, list) and "translation_text" in out[0]:
        return out[0]["translation_text"]

    return text
