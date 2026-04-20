import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "news.db")

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

# Models
HF_SUMMARY_MODEL = "facebook/bart-large-cnn"
HF_TRANSLATE_EN = "Helsinki-NLP/opus-mt-mul-en"
HF_TRANSLATE_HI = "Helsinki-NLP/opus-mt-mul-hi"
