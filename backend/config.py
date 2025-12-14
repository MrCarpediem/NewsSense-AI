import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "news.db")

HF_API_TOKEN = os.getenv("HF_API_TOKEN", "hf_YOUR_TOKEN_HERE")

HF_SUMMARY_MODEL = "facebook/bart-large-cnn"
HF_TRANSLATE_EN = "Helsinki-NLP/opus-mt-mul-en"
HF_TRANSLATE_HI = "Helsinki-NLP/opus-mt-mul-hi"
