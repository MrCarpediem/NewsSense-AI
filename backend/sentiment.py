# backend/sentiment.py

# Generic positive & negative words
POS = [
    "success", "happy", "win", "won", "victory", "victorious",
    "growth", "benefit", "profit", "achievement", "celebrate",
    "celebrated", "excellent", "great", "historic", "thrilling",
    "dominated", "dominate", "record", "champion"
]

NEG = [
    "death", "loss", "lost", "injury", "attack", "crime",
    "defeat", "defeated", "fail", "failure", "violence",
    "damage", "collapse"
]


def analyze_sentiment(text: str, category: str) -> str:
    """
    Determines sentiment of the news article using
    rule-based logic with category awareness.
    """

    if not text:
        return "Neutral"

    t = text.lower()

    if category == "Crime":
        return "Negative"
    if category == "Sports":
        if any(w in t for w in [
            "win", "won", "victory", "champion", "celebrated",
            "dominated", "historic", "record"
        ]):
            return "Positive"

        if any(w in t for w in [
            "loss", "lost", "defeat", "defeated"
        ]):
            return "Negative"

    p = sum(1 for w in POS if w in t)
    n = sum(1 for w in NEG if w in t)

    if p > n:
        return "Positive"
    if n > p:
        return "Negative"

    return "Neutral"
