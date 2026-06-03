import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import tempfile
import time
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

# --- PREMIUM CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* === GLOBAL === */
*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background: #06080f !important;
    color: #e2e8f0;
}
.stApp { background: linear-gradient(170deg, #06080f 0%, #0c1222 40%, #0a0e1a 100%) !important; }

/* Hide Streamlit defaults */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* === HERO HEADER === */
.hero-header {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    position: relative;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -60px; left: 50%; transform: translateX(-50%);
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}
.hero-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #818cf8, #6366f1, #a78bfa, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.03em;
    margin-bottom: 0.3rem;
    position: relative;
    z-index: 1;
}
.hero-subtitle {
    font-size: 1rem;
    color: #64748b;
    font-weight: 400;
    letter-spacing: 0.04em;
    position: relative;
    z-index: 1;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(168,85,247,0.2));
    border: 1px solid rgba(99,102,241,0.3);
    color: #a5b4fc;
    padding: 4px 14px;
    border-radius: 100px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-top: 0.6rem;
    position: relative;
    z-index: 1;
}

/* === GLASS CARDS === */
.glass-card {
    background: rgba(17, 24, 39, 0.6);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(99, 102, 241, 0.12);
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #6366f1, #a78bfa, transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}
.glass-card:hover { border-color: rgba(99, 102, 241, 0.3); transform: translateY(-2px); }
.glass-card:hover::before { opacity: 1; }

.card-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* === RESULT CARDS === */
.result-summary {
    background: rgba(17, 24, 39, 0.8);
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 14px;
    padding: 1.5rem;
    margin: 1rem 0;
}
.summary-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6366f1;
    margin-bottom: 0.5rem;
}
.summary-text {
    font-size: 0.95rem;
    line-height: 1.7;
    color: #cbd5e1;
}

/* === METRIC CARDS === */
.metric-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.8rem; margin: 1rem 0; }
.metric-card {
    background: rgba(17, 24, 39, 0.7);
    border: 1px solid rgba(99,102,241,0.1);
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    transition: all 0.3s ease;
}
.metric-card:hover { border-color: rgba(99,102,241,0.3); }
.metric-icon { font-size: 1.5rem; margin-bottom: 0.3rem; }
.metric-label { font-size: 0.65rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #64748b; }
.metric-value { font-size: 1.1rem; font-weight: 700; color: #f1f5f9; margin-top: 0.2rem; }

/* === TAGS === */
.tag-container { display: flex; flex-wrap: wrap; gap: 0.4rem; margin: 0.5rem 0; }
.topic-tag {
    background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(99,102,241,0.1));
    border: 1px solid rgba(99,102,241,0.25);
    color: #a5b4fc;
    padding: 4px 12px;
    border-radius: 100px;
    font-size: 0.75rem;
    font-weight: 600;
    transition: all 0.2s ease;
}
.topic-tag:hover { background: rgba(99,102,241,0.3); }
.entity-tag {
    background: linear-gradient(135deg, rgba(16,185,129,0.2), rgba(16,185,129,0.1));
    border: 1px solid rgba(16,185,129,0.25);
    color: #6ee7b7;
    padding: 4px 12px;
    border-radius: 100px;
    font-size: 0.75rem;
    font-weight: 600;
}

/* === SENTIMENT BADGES === */
.sentiment-positive { color: #34d399; }
.sentiment-negative { color: #f87171; }
.sentiment-neutral { color: #fbbf24; }

/* === SIDEBAR === */
section[data-testid="stSidebar"] {
    background: rgba(10, 14, 26, 0.95) !important;
    border-right: 1px solid rgba(99,102,241,0.1) !important;
}
section[data-testid="stSidebar"] .stMarkdown h1 {
    background: linear-gradient(135deg, #818cf8, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 1.4rem;
}

/* === BUTTONS === */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.7rem 2rem !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.3) !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(99,102,241,0.4) !important;
}

/* === TABS === */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: rgba(17,24,39,0.5);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid rgba(99,102,241,0.1);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    padding: 0.6rem 1.5rem !important;
    font-weight: 600 !important;
    color: #64748b !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(99,102,241,0.2) !important;
    color: #a5b4fc !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none; }
.stTabs [data-baseweb="tab-border"] { display: none; }

/* === TEXT AREA === */
.stTextArea textarea {
    background: rgba(17,24,39,0.7) !important;
    border: 1px solid rgba(99,102,241,0.15) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
}
.stTextArea textarea:focus { border-color: rgba(99,102,241,0.5) !important; box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important; }

/* === SELECT / RADIO === */
.stSelectbox > div > div, .stRadio > div { color: #e2e8f0; }

/* === DATAFRAME === */
.stDataFrame { border-radius: 12px; overflow: hidden; }

/* === DIVIDER === */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.3), transparent);
    margin: 1.2rem 0;
    border: none;
}

/* === COMPARISON TABLE === */
.comparison-table { width: 100%; border-collapse: separate; border-spacing: 0; margin: 0.8rem 0; }
.comparison-table th {
    background: rgba(99,102,241,0.15);
    color: #a5b4fc;
    padding: 0.6rem 1rem;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    text-align: left;
}
.comparison-table th:first-child { border-radius: 10px 0 0 0; }
.comparison-table th:last-child { border-radius: 0 10px 0 0; }
.comparison-table td {
    padding: 0.6rem 1rem;
    border-bottom: 1px solid rgba(99,102,241,0.08);
    font-size: 0.85rem;
    color: #cbd5e1;
}
.comparison-table tr:last-child td:first-child { border-radius: 0 0 0 10px; }
.comparison-table tr:last-child td:last-child { border-radius: 0 0 10px 0; }
.comparison-table tr:hover td { background: rgba(99,102,241,0.05); }

/* === PULSE ANIMATION === */
@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 15px rgba(99,102,241,0.2); }
    50% { box-shadow: 0 0 30px rgba(99,102,241,0.4); }
}
.pulse-active { animation: pulse-glow 2s ease-in-out infinite; }

/* === FOOTER === */
.app-footer {
    text-align: center;
    padding: 2rem 0 1rem;
    color: #334155;
    font-size: 0.75rem;
    letter-spacing: 0.04em;
}
</style>
""", unsafe_allow_html=True)

# --- HERO HEADER ---
st.markdown("""
<div class="hero-header">
    <div class="hero-title">🧠 NewsSense AI</div>
    <div class="hero-subtitle">Intelligent News Analysis Powered by Machine Learning</div>
    <div class="hero-badge">✦ NLP Engine v3.0 — Production</div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("# 🧠 NewsSense")
    st.caption("AI-Powered News Intelligence")
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    st.markdown("##### ⚙️ Configuration")
    language = st.selectbox("🌐 Output Language", ["English", "Hindi"], help="Choose summary language")
    mode = st.radio("🔬 Prediction Mode", ["Comparison", "Manual"], horizontal=True)

    if mode == "Manual":
        selected_model = st.selectbox("🤖 ML Model", ["Rule-Based", "Naive Bayes", "Logistic Reg.", "SVM (Linear)"])
    else:
        selected_model = "SVM (Linear)"

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("##### 📊 Model Info")
    st.markdown("""
    <div style="font-size:0.78rem; color:#64748b; line-height:1.7;">
    <b style="color:#a5b4fc;">Naive Bayes</b> — Probabilistic classifier<br>
    <b style="color:#a5b4fc;">Logistic Reg.</b> — Linear boundary model<br>
    <b style="color:#a5b4fc;">SVM</b> — Max-margin classifier<br>
    <b style="color:#a5b4fc;">Rule-Based</b> — Keyword matching
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="text-align:center;color:#334155;font-size:0.7rem;margin-top:1rem;">'
        'Built with ❤️ by Prem<br>© 2026 NewsSense AI</div>',
        unsafe_allow_html=True
    )


# --- HELPER FUNCTIONS ---
def get_sentiment_html(sent):
    colors = {"Positive": ("#34d399", "▲"), "Negative": ("#f87171", "▼"), "Neutral": ("#fbbf24", "●")}
    c, icon = colors.get(sent, ("#fbbf24", "●"))
    return f'<span style="color:{c};font-weight:700;">{icon} {sent}</span>'

def get_category_icon(cat):
    icons = {
        "Sports": "🏆", "Politics": "🏛️", "Technology": "💻",
        "Crime": "🔒", "Business": "📈", "Healthcare": "🏥",
        "Education": "🎓", "Other": "📰"
    }
    return icons.get(cat, "📰")


# --- MAIN TABS ---
t_run, t_log = st.tabs(["🔍 Analysis Engine", "📂 Analysis History"])

with t_run:
    col_input, col_spacer, col_result = st.columns([1, 0.05, 1.2])

    with col_input:
        st.markdown(
            '<div class="card-title">📥 Source Input</div>',
            unsafe_allow_html=True
        )

        src = st.radio("Input Method", ["📝 Text Input", "📷 Image (OCR)"], horizontal=True, label_visibility="collapsed")
        raw_text = ""

        if "📝" in src:
            raw_text = st.text_area(
                "Paste your news article here...",
                height=280,
                placeholder="Paste any news article in English or Hindi to analyze...",
                label_visibility="collapsed"
            )
        else:
            up = st.file_uploader("Upload a news image", type=["jpg", "jpeg", "png", "webp"], label_visibility="collapsed")
            if up:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                    tmp.write(up.getbuffer())
                    tmp_path = tmp.name
                try:
                    raw_text = extract_text_from_image(tmp_path)
                    if raw_text:
                        st.success("✅ Text extracted successfully!")
                        with st.expander("👁️ Preview extracted text"):
                            st.text(raw_text[:500])
                    else:
                        st.warning("⚠️ No text could be extracted from the image.")
                finally:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)

        if raw_text.strip():
            word_count = len(raw_text.split())
            st.markdown(
                f'<div style="font-size:0.75rem;color:#64748b;margin-top:0.5rem;">'
                f'📊 {word_count} words detected</div>',
                unsafe_allow_html=True
            )
            analyze_btn = st.button("🚀 Run Analysis", use_container_width=True)
        else:
            analyze_btn = False

    with col_result:
        st.markdown(
            '<div class="card-title">📊 NLP Intelligence Report</div>',
            unsafe_allow_html=True
        )

        if raw_text.strip() and analyze_btn:
            progress = st.progress(0, text="Initializing NLP pipeline...")
            time.sleep(0.3)
            progress.progress(20, text="Classifying article...")

            try:
                results = classify_all(raw_text)
                progress.progress(40, text="Analyzing sentiment...")

                cat = results.get(selected_model, {"label": "Other"})["label"]
                sent = analyze_sentiment(raw_text, cat)
                progress.progress(60, text="Generating summary...")

                summ = summarize(raw_text, language)
                progress.progress(80, text="Extracting entities & keywords...")

                keywords = get_top_keywords(raw_text)
                entities = get_entities(raw_text)
                progress.progress(100, text="Analysis complete!")
                time.sleep(0.3)
                progress.empty()

                save_news(raw_text[:80], summ, cat, sent)

                # --- METRICS ---
                cat_icon = get_category_icon(cat)
                sent_html = get_sentiment_html(sent)
                st.markdown(f"""
                <div class="metric-grid">
                    <div class="metric-card">
                        <div class="metric-icon">{cat_icon}</div>
                        <div class="metric-label">Category</div>
                        <div class="metric-value">{cat}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon">{'😊' if sent == 'Positive' else '😠' if sent == 'Negative' else '😐'}</div>
                        <div class="metric-label">Sentiment</div>
                        <div class="metric-value">{sent_html}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # --- SUMMARY ---
                st.markdown(f"""
                <div class="result-summary">
                    <div class="summary-label">📝 Summary ({language})</div>
                    <div class="summary-text">{summ}</div>
                </div>
                """, unsafe_allow_html=True)

                # --- ENTITIES ---
                if entities:
                    st.markdown('<div class="summary-label" style="margin-top:1rem;">👤 Key Entities</div>', unsafe_allow_html=True)
                    entity_html = "".join([f'<span class="entity-tag">{e}</span>' for e in entities])
                    st.markdown(f'<div class="tag-container">{entity_html}</div>', unsafe_allow_html=True)

                # --- KEYWORDS ---
                if keywords:
                    st.markdown('<div class="summary-label" style="margin-top:1rem;">🏷️ Topics</div>', unsafe_allow_html=True)
                    kw_html = "".join([f'<span class="topic-tag">#{k}</span>' for k in keywords])
                    st.markdown(f'<div class="tag-container">{kw_html}</div>', unsafe_allow_html=True)

                # --- MODEL COMPARISON ---
                if mode == "Comparison":
                    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
                    st.markdown('<div class="summary-label">🔬 Model Comparison</div>', unsafe_allow_html=True)
                    rows_html = ""
                    for k, v in results.items():
                        is_selected = "✦ " if k == selected_model else ""
                        rows_html += f'<tr><td>{is_selected}{k}</td><td><b>{v["label"]}</b></td></tr>'
                    st.markdown(f"""
                    <table class="comparison-table">
                        <thead><tr><th>Model</th><th>Prediction</th></tr></thead>
                        <tbody>{rows_html}</tbody>
                    </table>
                    """, unsafe_allow_html=True)

            except Exception as e:
                progress.empty()
                st.error(f"❌ Analysis failed: {str(e)}")

        elif not raw_text.strip():
            st.markdown("""
            <div style="text-align:center; padding:3rem 1rem; color:#475569;">
                <div style="font-size:3rem; margin-bottom:1rem; opacity:0.5;">🔍</div>
                <div style="font-size:1rem; font-weight:600; color:#64748b;">Ready for Analysis</div>
                <div style="font-size:0.85rem; margin-top:0.5rem; color:#475569;">
                    Paste a news article or upload an image to begin
                </div>
            </div>
            """, unsafe_allow_html=True)


with t_log:
    data = get_all_news()
    if data:
        df = pd.DataFrame(data, columns=["ID", "Title", "Summary", "Category", "Sentiment", "Date"])
        df = df.drop(columns=["ID"])

        # Stats bar
        total = len(df)
        cats = df["Category"].nunique()
        st.markdown(f"""
        <div class="metric-grid" style="grid-template-columns: repeat(3, 1fr);">
            <div class="metric-card">
                <div class="metric-icon">📊</div>
                <div class="metric-label">Total Analyzed</div>
                <div class="metric-value">{total}</div>
            </div>
            <div class="metric-card">
                <div class="metric-icon">🏷️</div>
                <div class="metric-label">Categories</div>
                <div class="metric-value">{cats}</div>
            </div>
            <div class="metric-card">
                <div class="metric-icon">🕐</div>
                <div class="metric-label">Latest</div>
                <div class="metric-value" style="font-size:0.8rem;">{df['Date'].iloc[0][:10] if total > 0 else 'N/A'}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Title": st.column_config.TextColumn("Title", width="medium"),
                "Summary": st.column_config.TextColumn("Summary", width="large"),
                "Category": st.column_config.TextColumn("Category", width="small"),
                "Sentiment": st.column_config.TextColumn("Sentiment", width="small"),
                "Date": st.column_config.TextColumn("Date", width="small"),
            }
        )
    else:
        st.markdown("""
        <div style="text-align:center; padding:3rem; color:#475569;">
            <div style="font-size:3rem; margin-bottom:1rem; opacity:0.4;">📂</div>
            <div style="font-size:1rem; font-weight:600; color:#64748b;">No Analysis History</div>
            <div style="font-size:0.85rem; margin-top:0.5rem;">Analyzed articles will appear here</div>
        </div>
        """, unsafe_allow_html=True)


# --- FOOTER ---
st.markdown("""
<div class="app-footer">
    NewsSense AI v3.0 — Production Release &nbsp;|&nbsp;
    NLP · ML Classification · Sentiment Analysis · OCR &nbsp;|&nbsp;
    Built with Streamlit
</div>
""", unsafe_allow_html=True)
