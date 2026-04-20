import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from backend.ocr_reader import extract_text_from_image
from backend.summarizer import summarize
from backend.classifier import classify
from backend.sentiment import analyze_sentiment
from backend.database import save_news, init_db, get_all_news

# ---------------- INITIAL SETUP ----------------
init_db()

st.set_page_config(
    page_title="NewsSense AI | Pure Logic",
    page_icon="📰",
    layout="wide"
)

# ---------------- CUSTOM CSS (PREMIUM LOOK) ----------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #0e1117;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #ff4b2b 0%, #ff416c 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2540/2540832.png", width=80)
    st.title("NewsSense AI")
    st.info("Pure NLP Edition (No External APIs)")
    st.markdown("---")
    st.markdown("### Settings")
    language = st.selectbox("Display Language", ["English", "Hindi"])
    st.success("✅ Pure Local Logic Active")
    
# ---------------- MAIN UI ----------------
tab1, tab2 = st.tabs(["🔍 Analyze News", "📂 History Explorer"])

with tab1:
    col_input, col_output = st.columns([1, 1], gap="large")
    
    with col_input:
        st.subheader("Input Source")
        mode = st.radio("Select Method", ["Upload Image (OCR)", "Paste Text"], horizontal=True)
        
        text = ""
        if mode == "Upload Image (OCR)":
            uploaded = st.file_uploader("Upload newspaper snippet", type=["png", "jpg", "jpeg"])
            if uploaded:
                with open("uploaded.jpg", "wb") as f:
                    f.write(uploaded.getbuffer())
                with st.spinner("Extracting text with OCR..."):
                    text = extract_text_from_image("uploaded.jpg")
                    if text:
                        st.success("Text extracted successfully!")
                    else:
                        st.error("Failed to extract text. Check image quality.")
        else:
            text = st.text_area("Paste news article content", height=300, placeholder="Enter text here...")
            
    with col_output:
        st.subheader("NLP Analysis Results")
        if text.strip():
            if st.button("🚀 Run Analysis"):
                with st.spinner("Processing locally..."):
                    try:
                        # 100% Local Processing
                        category = classify(text)
                        sentiment = analyze_sentiment(text, category)
                        summary = summarize(text, language)
                        
                        # Save to Database
                        save_news(
                            title=text[:100].replace("\n", " ") + "...",
                            summary=summary,
                            category=category,
                            sentiment=sentiment
                        )
                        
                        # Display results
                        st.markdown(f"### Summary ({language})")
                        st.write(summary)
                        
                        st.markdown("---")
                        m_col1, m_col2 = st.columns(2)
                        
                        with m_col1:
                            st.metric("Category", category)
                        with m_col2:
                            sentiment_icon = "🟢" if sentiment == "Positive" else "🔴" if sentiment == "Negative" else "⚪"
                            st.metric("Sentiment", f"{sentiment_icon} {sentiment}")
                            
                    except Exception as e:
                        st.error(f"Local analysis failed: {str(e)}")
        else:
            st.info("Enter or upload news content to begin analysis.")

with tab2:
    st.subheader("Saved News History")
    history = get_all_news()
    
    if history:
        df = pd.DataFrame(history, columns=["ID", "Title", "Summary", "Category", "Sentiment", "Timestamp"])
        
        search_query = st.text_input("🔍 Search history by title or category")
        if search_query:
            df = df[df['Title'].str.contains(search_query, case=False) | df['Category'].str.contains(search_query, case=False)]
            
        for _, row in df.iterrows():
            with st.expander(f"{row['Timestamp']} | {row['Category']} | {row['Title'][:60]}..."):
                st.markdown(f"**Full Summary:**\n{row['Summary']}")
                st.markdown(f"**Sentiment:** {row['Sentiment']}")
    else:
        st.info("No news history found yet.")
