import requests, time
from .config import HF_API_TOKEN, HF_SUMMARY_MODEL
from .translator import translate
from .text_cleaner import clean_ocr_text

HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}
URL = f"https://api-inference.huggingface.co/models/{HF_SUMMARY_MODEL}"

def summarize(text, language):
    # CLEAN OCR TEXT
    text = clean_ocr_text(text)

    if len(text) < 100:
        return fallback_summary(text, language)

    # Translate input to English for better summarization
    base_text = translate(text, "English")

    payload = {"inputs": base_text[:2000]}

    for _ in range(4):
        r = requests.post(URL, headers=HEADERS, json=payload)
        out = r.json()

        if isinstance(out, list) and "summary_text" in out[0]:
            summary = out[0]["summary_text"]

            # Translate final summary to user language
            if language != "English":
                summary = translate(summary, language)

            return summary

        time.sleep(3)

    return fallback_summary(text, language)


# 🔁 FALLBACK (NEVER FAILS)
def fallback_summary(text, language):
    lines = text.split(".")
    summary = ". ".join(lines[:3])

    if language != "English":
        summary = translate(summary, language)

    return summary if summary else "Summary not available."
