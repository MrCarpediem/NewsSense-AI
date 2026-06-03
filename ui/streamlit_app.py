import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import tempfile
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
st.set_page_config(
    page_title="NewsSense AI — Intelligent News Analysis",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CLEAN CSS (lightweight, no animations) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp {
    font-family: 'Inter', sans-serif !important;
    background: #0a0e1a !important;
    color: #e2e8f0;
}
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

.hero-title {
    text-align: center; font-size: 2.2rem; font-weight: 800;
    color: #818cf8; margin: 1rem 0 0.2rem;
}
.hero-sub {
    text-align: center; color: #64748b; font-size: 0.9rem; margin-bottom: 1.5rem;
}
.card {
    background: #111827; padding: 1.2rem; border-radius: 12px;
    border: 1px solid #1e293b; margin-bottom: 1rem;
}
.label { font-size: 0.7rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #6366f1; margin-bottom: 0.4rem; }
.summary-text { font-size: 0.92rem; line-height: 1.7; color: #cbd5e1; }
.metric-row { display: flex; gap: 0.8rem; margin: 0.8rem 0; }
.metric-box {
    flex: 1; background: #111827; border: 1px solid #1e293b;
    border-radius: 10px; padding: 1rem; text-align: center;
}
.metric-box .icon { font-size: 1.4rem; }
.metric-box .val { font-size: 1rem; font-weight: 700; color: #f1f5f9; margin-top: 0.2rem; }
.metric-box .lbl { font-size: 0.65rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.06em; }
.tag { display: inline-block; padding: 3px 10px; border-radius: 100px; font-size: 0.75rem; font-weight: 600; margin: 2px; }
.tag-topic { background: rgba(99,102,241,0.15); color: #a5b4fc; border: 1px solid rgba(99,102,241,0.25); }
.tag-entity { background: rgba(16,185,129,0.15); color: #6ee7b7; border: 1px solid rgba(16,185,129,0.25); }
.pos { color: #34d399; } .neg { color: #f87171; } .neu { color: #fbbf24; }
.comp-table { width: 100%; border-collapse: collapse; margin: 0.5rem 0; }
.comp-table th { background: #1e293b; color: #a5b4fc; padding: 0.5rem; font-size: 0.72rem; text-align: left; text-transform: uppercase; letter-spacing: 0.06em; }
.comp-table td { padding: 0.5rem; border-bottom: 1px solid #1e293b; font-size: 0.85rem; color: #cbd5e1; }
section[data-testid="stSidebar"] { background: #0a0e1a !important; border-right: 1px solid #1e293b !important; }
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #7c3aed) !important;
    color: white !important; border: none !important; border-radius: 10px !important;
    padding: 0.6rem 1.5rem !important; font-weight: 700 !important; width: 100% !important;
}
.stTextArea textarea {
    background: #111827 !important; border: 1px solid #1e293b !important;
    border-radius: 10px !important; color: #e2e8f0 !important;
}
.divider { height: 1px; background: #1e293b; margin: 1rem 0; }
.footer { text-align: center; color: #334155; font-size: 0.72rem; padding: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="hero-title">🧠 NewsSense AI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Intelligent News Analysis • NLP Engine v3.0</div>', unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🧠 NewsSense")
    st.caption("AI News Intelligence")
    st.divider()
    language = st.selectbox("🌐 Language", ["English", "Hindi"])
    mode = st.radio("🔬 Mode", ["Comparison", "Manual"], horizontal=True)
    if mode == "Manual":
        selected_model = st.selectbox("🤖 Model", ["Rule-Based", "Naive Bayes", "Logistic Reg.", "SVM (Linear)"])
    else:
        selected_model = "SVM (Linear)"
    st.divider()
    st.caption("NB · LR · SVM · Rule-Based")
    st.caption("Built with ❤️ by Prem")

# --- HELPERS ---
def sent_html(s):
    if s == "Positive": return '<span class="pos">▲ Positive</span>'
    if s == "Negative": return '<span class="neg">▼ Negative</span>'
    return '<span class="neu">● Neutral</span>'

def cat_icon(c):
    return {"Sports":"🏆","Politics":"🏛️","Technology":"💻","Crime":"🔒","Business":"📈","Healthcare":"🏥","Education":"🎓"}.get(c,"📰")

# --- TABS ---
t_run, t_log = st.tabs(["🔍 Analysis", "📂 History"])

with t_run:
    c1, c2 = st.columns([1, 1.2])

    with c1:
        st.markdown("**📥 Input**")
        src = st.radio("Method", ["📝 Text", "📷 Image (OCR)"], horizontal=True, label_visibility="collapsed")
        raw_text = ""
        if "📝" in src:
            raw_text = st.text_area("Paste news here...", height=250, label_visibility="collapsed")
        else:
            up = st.file_uploader("Upload image", type=["jpg","jpeg","png","webp"], label_visibility="collapsed")
            if up:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                    tmp.write(up.getbuffer())
                    tmp_path = tmp.name
                try:
                    raw_text = extract_text_from_image(tmp_path)
                    if raw_text:
                        st.success("✅ Text extracted!")
                    else:
                        st.warning("⚠️ No text found in image.")
                finally:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)

        if raw_text.strip():
            st.caption(f"📊 {len(raw_text.split())} words")
            analyze = st.button("🚀 Run Analysis")
        else:
            analyze = False

    with c2:
        st.markdown("**📊 Results**")
        if raw_text.strip() and analyze:
            with st.spinner("Analyzing..."):
                try:
                    results = classify_all(raw_text)
                    cat = results.get(selected_model, {"label": "Other"})["label"]
                    sent = analyze_sentiment(raw_text, cat)
                    summ = summarize(raw_text, language)
                    keywords = get_top_keywords(raw_text)
                    entities = get_entities(raw_text)
                    save_news(raw_text[:80], summ, cat, sent)

                    # Metrics
                    ic = cat_icon(cat)
                    si = "😊" if sent=="Positive" else "😠" if sent=="Negative" else "😐"
                    st.markdown(f"""
                    <div class="metric-row">
                        <div class="metric-box"><div class="icon">{ic}</div><div class="lbl">Category</div><div class="val">{cat}</div></div>
                        <div class="metric-box"><div class="icon">{si}</div><div class="lbl">Sentiment</div><div class="val">{sent_html(sent)}</div></div>
                    </div>""", unsafe_allow_html=True)

                    # Summary
                    st.markdown(f"""<div class="card">
                        <div class="label">📝 Summary ({language})</div>
                        <div class="summary-text">{summ}</div>
                    </div>""", unsafe_allow_html=True)

                    # Entities
                    if entities:
                        e_html = "".join([f'<span class="tag tag-entity">{e}</span>' for e in entities])
                        st.markdown(f'<div class="label">👤 Entities</div>{e_html}', unsafe_allow_html=True)

                    # Keywords
                    if keywords:
                        k_html = "".join([f'<span class="tag tag-topic">#{k}</span>' for k in keywords])
                        st.markdown(f'<div class="label" style="margin-top:0.8rem;">🏷️ Topics</div>{k_html}', unsafe_allow_html=True)

                    # Comparison table
                    if mode == "Comparison":
                        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                        rows = "".join([f'<tr><td>{"✦ " if k==selected_model else ""}{k}</td><td><b>{v["label"]}</b></td></tr>' for k,v in results.items()])
                        st.markdown(f'<div class="label">🔬 Model Comparison</div><table class="comp-table"><tr><th>Model</th><th>Prediction</th></tr>{rows}</table>', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"❌ Error: {e}")
        elif not raw_text.strip():
            st.markdown("""
            <div style="text-align:center;padding:2rem;color:#475569;">
                <div style="font-size:2.5rem;opacity:0.4;">🔍</div>
                <div style="margin-top:0.5rem;">Paste a news article to begin</div>
            </div>""", unsafe_allow_html=True)

with t_log:
    data = get_all_news()
    if data:
        df = pd.DataFrame(data, columns=["ID","Title","Summary","Category","Sentiment","Date"]).drop(columns=["ID"])
        st.markdown(f"**{len(df)}** articles analyzed")
        st.dataframe(df, width="stretch", hide_index=True)
    else:
        st.info("No history yet. Analyze some news first!")

st.markdown('<div class="footer">NewsSense AI v3.0 • NLP · ML · Sentiment · OCR • Built with Streamlit</div>', unsafe_allow_html=True)
