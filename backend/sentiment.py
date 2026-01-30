# backend/sentiment.py

# Generic positive & negative words (English + Hindi)
POS = [
    # English (UNCHANGED)
    "success", "happy", "win", "won", "victory", "victorious",
    "growth", "benefit", "profit", "achievement", "celebrate",
    "celebrated", "excellent", "great", "historic", "thrilling",
    "dominated", "dominate", "record", "champion",

    # Hindi (ADDED)
    "जीत", "जीता", "विजय", "शानदार", "बेहतरीन",
    "उत्कृष्ट", "सफल", "दबदबा", "सराहना", "खुशी"
]

NEG = [
    # English (UNCHANGED)
    "death", "loss", "lost", "injury", "attack", "crime",
    "defeat", "defeated", "fail", "failure", "violence",
    "damage", "collapse",

    # Hindi (ADDED)
    "मौत", "हार", "अपराध", "हमला", "हिंसा", "नुकसान"
]


def analyze_sentiment(text: str, category: str) -> str:
    """
    Rule-based sentiment analysis.
    English logic preserved, Hindi support added.
    """

    if not text:
        return "Neutral"

    t = text.lower()

    # Crime always negative (UNCHANGED)
    if category == "Crime":
        return "Negative"

    # Sports-specific logic (EXTENDED, not reduced)
    if category == "Sports":
        if any(w in t for w in POS):
            return "Positive"
        if any(w in t for w in NEG):
            return "Negative"

    # Generic fallback (UNCHANGED)
    p = sum(1 for w in POS if w in t)
    n = sum(1 for w in NEG if w in t)

    if p > n:
        return "Positive"
    if n > p:
        return "Negative"

    return "Neutral"
