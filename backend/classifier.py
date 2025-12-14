CATEGORIES = {
    "Crime": ["police", "arrest", "crime", "murder", "stabbed", "theft"],
    "Entertainment": ["movie", "film", "actor", "music", "cinema"],
    "Sports": ["match", "cricket", "football", "tournament", "goal"],
    "Healthcare": ["hospital", "doctor", "health", "covid", "medicine"]
}

def classify(text):
    t = text.lower()
    scores = {}

    for cat, words in CATEGORIES.items():
        scores[cat] = sum(1 for w in words if w in t)

    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "Other"
