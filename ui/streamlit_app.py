import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from backend.ocr_reader import extract_text_from_image
from backend.summarizer import summarize
from backend.classifier import classify
from backend.sentiment import analyze_sentiment
from backend.database import save_news, init_db

# Initialize database once
init_db()

st.set_page_config(
    page_title="NewsSense AI",
    layout="centered"
)

st.title("NewsSense AI")
st.caption("Multi-language News Summarizer (Image + Text)")
st.markdown("---")

# Warm-up model
with st.spinner("Initializing engine..."):
    try:
        summarize("Warmup text.", "English")
    except:
        pass

language = st.selectbox("Select summary language", ["English", "Hindi"])

mode = st.radio(
    "Choose input method",
    ["Upload Newspaper Image", "Paste Text Manually"]
)

text = ""

if mode == "Upload Newspaper Image":
    uploaded = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])
    if uploaded:
        with open("temp.jpg", "wb") as f:
            f.write(uploaded.getbuffer())
        text = extract_text_from_image("temp.jpg")
else:
    text = st.text_area("Paste news/article text", height=250)

if text.strip():
    st.subheader("Input Text")
    st.text_area("", text, height=200)

    if st.button("Generate Summary"):
        with st.spinner("Processing..."):
            category = classify(text)
            sentiment = analyze_sentiment(text, category)
            summary = summarize(text, language)

            # Save to database AFTER processing
            save_news(
                title=text[:80],
                summary=summary,
                category=category,
                sentiment=sentiment
            )

        st.subheader("Summary")
        st.success(summary)

        col1, col2 = st.columns(2)
        col1.metric("Category", category)
        col2.metric("Sentiment", sentiment)
