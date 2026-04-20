import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from backend.ocr_reader import extract_text_from_image
from backend.summarizer import summarize
from backend.classifier import classify_all, get_top_keywords, get_entities
from backend.sentiment import analyze_sentiment
from backend.database import save_news, init_db, get_all_news

# --- SYSTEM INIT ---
@st.cache_resource
def setup():
    init_db()
    return True

setup()
st.set_page_config(page_title="NewsSense v2.5", layout="wide")

# --- UI STYLE ---
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #f1f5f9; }
    .card { background: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155; margin-bottom: 20px; }
    .tag { background: #3b82f6; color: white; padding: 3px 10px; border-radius: 15px; font-size: 0.8rem; margin-right: 5px; }
    .entity-tag { background: #10b981; color: white; padding: 3px 10px; border-radius: 15px; font-size: 0.8rem; margin-right: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🗞️ NewsSense")
    st.write("v2.5 | NLP Pro")
    st.markdown("---")
    language = st.selectbox("Output Language", ["English", "Hindi"])
    mode = st.radio("Prediction Mode", ["Comparison 🔬", "Manual 🎯"])
    if mode == "Manual 🎯":
        selected_model = st.selectbox("Model", ["Rule-Based", "Naive Bayes", "Logistic Reg.", "SVM (Linear)"])
    else:
        selected_model = "SVM (Linear)"

# --- MAIN ---
t_run, t_log = st.tabs(["🔍 Analysis Engine", "📂 History"])

with t_run:
    c1, c2 = st.columns([1, 1.2], gap="large")
    
    with c1:
        st.subheader("Source Input")
        src = st.radio("Method", ["Text", "Image (OCR)"], horizontal=True)
        raw_text = ""
        if src == "Text":
            raw_text = st.text_area("Paste News Here", height=250)
        else:
            up = st.file_uploader("Upload Image", type=["jpg", "png"])
            if up:
                with open("temp.jpg", "wb") as f: f.write(up.getbuffer())
                raw_text = extract_text_from_image("temp.jpg")
                if raw_text: st.success("Text Extracted!")

    with c2:
        st.subheader("NLP Insights")
        if raw_text.strip():
            if st.button("🚀 EXECUTE ANALYSIS"):
                with st.spinner("Processing NLP Pipeline..."):
                    results = classify_all(raw_text)
                    cat = results.get(selected_model, {"label": "Other"})["label"]
                    sent = analyze_sentiment(raw_text, cat)
                    summ = summarize(raw_text, language)
                    keywords = get_top_keywords(raw_text)
                    entities = get_entities(raw_text) # NEW FEATURE
                    
                    save_news(raw_text[:50], summ, cat, sent)
                    
                    # Display Result Card
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.markdown(f"### Summary ({language})")
                    st.write(summ)
                    
                    st.markdown("---")
                    st.write("**Key Entities (People/Places):**")
                    if entities:
                        st.markdown(" ".join([f"<span class='entity-tag'>{e}</span>" for e in entities]), unsafe_allow_html=True)
                    else:
                        st.write("No major entities found.")
                    
                    st.write("**Topics:**")
                    st.markdown(" ".join([f"<span class='tag'>#{k}</span>" for k in keywords]), unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    if mode == "Comparison 🔬":
                        st.table(pd.DataFrame([{"Model": k, "Result": v["label"]} for k, v in results.items()]))
                    
                    col1, col2 = st.columns(2)
                    col1.metric("Category", cat)
                    col2.metric("Sentiment", sent)
        else:
            st.info("Input news to start the analysis pipeline.")

with t_log:
    data = get_all_news()
    if data:
        st.dataframe(pd.DataFrame(data, columns=["ID", "Title", "Summary", "Cat", "Sent", "Date"]).drop(columns=["ID"]), width=1000)
