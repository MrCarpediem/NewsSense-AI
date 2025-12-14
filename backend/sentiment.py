POS = ["success", "happy", "win", "growth", "benefit"]
NEG = ["death", "loss", "injury", "attack", "crime"]

def analyze_sentiment(text, category):
    if category == "Crime":
        return "Negative"

    t = text.lower()
    p = sum(w in t for w in POS)
    n = sum(w in t for w in NEG)

    if p - n >= 2:
        return "Positive"
    if n - p >= 2:
        return "Negative"
    return "Neutral"
