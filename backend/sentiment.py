from textblob import TextBlob

# PURE LOCAL SENTIMENT ANALYSIS
# Uses TextBlob for English and Keyword mapping for Hindi

def analyze_sentiment(text: str, category: str = "General") -> str:
    """
    Local sentiment analysis without APIs.
    """
    if not text:
        return "Neutral"

    # 1. Check for strong negative category override
    if category == "Crime":
        # Even if crime is reported neutrally, it's generally a negative news event
        return "Negative"

    # 2. TextBlob Analysis (Works great for English locally)
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"

    # 3. Keyword-based fallback (Good for Hindi or mixed text)
    t = text.lower()
    pos_keywords = ["win", "success", "growth", "शानदार", "बेहतरीन", "सफल", "जीत", "खुशी", "सराहना"]
    neg_keywords = ["death", "loss", "injury", "fail", "मौत", "हार", "अपराध", "नुकसान", "हिंसा"]
    
    p_score = sum(1 for w in pos_keywords if w in t)
    n_score = sum(1 for w in neg_keywords if w in t)

    if p_score > n_score:
        return "Positive"
    elif n_score > p_score:
        return "Negative"

    return "Neutral"
