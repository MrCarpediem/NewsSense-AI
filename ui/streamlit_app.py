import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from backend.ocr_reader import extract_text_from_image
from backend.summarizer import summarize
from backend.classifier import classify
from backend.sentiment import analyze_sentiment
from backend.database import save_news, init_db

# ---------------- INITIAL SETUP ----------------

# Initialize database once
init_db()

st.set_page_config(
    page_title="NewsSense AI",
    layout="wide"   # ✅ FIX 1: wide layout for smooth scrolling
)

# Small UI padding polish
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("NewsSense AI")
st.caption("Multi-language News Summarizer (Image + Text)")
st.markdown("---")

# ---------------- CACHING (BIG SPEED BOOST) ----------------

@st.cache_data(show_spinner=False)
def cached_summary(text, language):
    return summarize(text, language)

@st.cache_data(show_spinner=False)
def cached_classify(text):
    return classify(text)

@st.cache_data(show_spinner=False)
def cached_sentiment(text, category):
    return analyze_sentiment(text, category)

# ---------------- UI CONTROLS ----------------

language = st.selectbox("Select summary language", ["English", "Hindi"])

mode = st.radio(
    "Choose input method",
    ["Upload Newspaper Image", "Paste Text Manually"]
)

text = ""

# ---------------- INPUT HANDLING ----------------

if mode == "Upload Newspaper Image":
    uploaded = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])
    if uploaded:
        with open("temp.jpg", "wb") as f:
            f.write(uploaded.getbuffer())
        text = extract_text_from_image("temp.jpg")
else:
    text = st.text_area("Paste news/article text", height=250)

# ---------------- PROCESSING ----------------

if text.strip():
    st.subheader("Input Text")

    # ✅ FIX 2: Scrollable input preview
    with st.container(height=220):
        st.write(text)

    if st.button("Generate Summary"):
        with st.spinner("Processing..."):
            category = cached_classify(text)
            sentiment = cached_sentiment(text, category)
            summary = cached_summary(text, language)

            # Save to database AFTER processing
            save_news(
                title=text[:80],
                summary=summary,
                category=category,
                sentiment=sentiment
            )

        st.subheader("Summary")

        # ✅ FIX 3: Scrollable summary output
        with st.container(height=180):
            st.success(summary)

        col1, col2 = st.columns(2)
        col1.metric("Category", category)
        col2.metric("Sentiment", sentiment)
