# 🧠 NewsSense AI

> **Intelligent News Analysis Powered by Machine Learning**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

NewsSense AI is a production-grade NLP application that summarizes, classifies, and extracts insights from news articles using multiple Machine Learning models — all running **100% locally** with zero API dependencies.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📰 **Text Summarization** | Extractive summarization using TF scoring |
| 🏷️ **Multi-Model Classification** | Naive Bayes, Logistic Regression, SVM + Rule-Based |
| 🔬 **Model Comparison** | Side-by-side prediction comparison across all models |
| 😊 **Sentiment Analysis** | TextBlob + keyword-based hybrid sentiment detection |
| 👤 **Entity Extraction** | Named Entity Recognition for people and places |
| 📷 **OCR Support** | Extract text from news images (Tesseract) |
| 🌐 **Bilingual** | English and Hindi support |
| 📂 **History Tracking** | SQLite-backed analysis log with stats |

---

## 🏗️ Architecture

```
NewsSense-AI/
├── .streamlit/           # Streamlit configuration & theme
│   └── config.toml
├── backend/              # Core NLP engine
│   ├── classifier.py     # ML classification (NB, LR, SVM) + rule-based
│   ├── summarizer.py     # Extractive text summarization
│   ├── sentiment.py      # Hybrid sentiment analysis
│   ├── ocr_reader.py     # Tesseract OCR integration
│   ├── text_cleaner.py   # Text preprocessing pipeline
│   ├── database.py       # SQLite persistence layer
│   └── config.py         # Environment & path configuration
├── models/               # Trained ML model artifacts (.pkl)
├── data/                 # SQLite database
├── ui/
│   └── streamlit_app.py  # Premium Streamlit dashboard
├── train_models.py       # Model training script
├── packages.txt          # System dependencies (Streamlit Cloud)
├── requirements.txt      # Python dependencies
└── README.md
```

---

## 🚀 Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/MrCarpediem/NewsSense-AI.git
cd NewsSense-AI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Train ML models (first time only)
python train_models.py

# Launch the app
streamlit run ui/streamlit_app.py
```

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Set **Main file path** to `ui/streamlit_app.py`
5. Click **Deploy** — the `packages.txt` will auto-install Tesseract

---

## 🤖 ML Models

| Model | Type | Strength |
|-------|------|----------|
| **Naive Bayes** | Probabilistic | Fast, good baseline |
| **Logistic Regression** | Linear | Balanced accuracy |
| **SVM (LinearSVC)** | Max-margin | Best for small datasets |
| **Rule-Based** | Keyword matching | Interpretable fallback |

All models are trained on a curated multi-category news dataset and serialized with `joblib`.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit with custom glassmorphism UI
- **NLP**: NLTK, TextBlob, scikit-learn
- **ML**: TF-IDF + MultinomialNB / LogisticRegression / LinearSVC
- **OCR**: Tesseract (pytesseract)
- **Database**: SQLite3
- **Deployment**: Streamlit Cloud

---

## 📄 License

This project is licensed under the MIT License.

---

<p align="center">
  Built with ❤️ by <a href="https://github.com/MrCarpediem">Prem</a>
</p>
