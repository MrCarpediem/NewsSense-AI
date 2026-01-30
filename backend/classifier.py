# backend/classifier.py

CATEGORIES = {
    "Crime": [
        "crime", "criminal", "murder", "murderer", "kill", "killing",
        "death", "dead", "arrest", "police", "custody", "investigation",
        "attack", "assault", "rape", "robbery", "theft", "fraud",
        "gun", "shooting", "stab", "stabbing", "violence", "case",
        "court", "trial", "lawyer", "judge", "prison", "jail"
    ],

    "Politics": [
        "election", "government", "minister", "prime minister",
        "president", "parliament", "policy", "bill", "law",
        "vote", "voting", "party", "bjp", "congress", "democracy",
        "speech", "campaign", "opposition", "cabinet", "constitution"
    ],

    "Sports": [
        "sport", "match", "game", "tournament", "league",
        "cricket", "football", "soccer", "tennis", "badminton",
        "goal", "score", "win", "lose", "victory", "defeat",
        "player", "team", "coach", "captain", "final", "world cup"
    ],

    "Entertainment": [
        "movie", "film", "cinema", "actor", "actress", "director",
        "music", "song", "album", "concert", "show", "trailer",
        "bollywood", "hollywood", "celebrity", "star", "award",
        "festival", "netflix", "amazon prime", "ott"
    ],

    "Business": [
        "business", "company", "market", "stock", "share",
        "investment", "investor", "profit", "loss", "revenue",
        "startup", "funding", "ipo", "economy", "economic",
        "bank", "loan", "interest", "finance", "trade"
    ],

    "Technology": [
        "technology", "tech", "software", "hardware", "computer",
        "ai", "artificial intelligence", "machine learning",
        "data", "cloud", "cyber", "security", "hacking",
        "internet", "app", "application", "startup", "innovation"
    ],

    "Healthcare": [
        "health", "hospital", "doctor", "nurse", "patient",
        "medicine", "medical", "treatment", "disease",
        "covid", "virus", "infection", "vaccine", "surgery",
        "mental health", "clinic", "healthcare"
    ],

    "Education": [
        "education", "school", "college", "university",
        "student", "teacher", "exam", "examination",
        "result", "admission", "syllabus", "degree",
        "placement", "campus", "classroom", "learning"
    ]
}


def classify(text: str) -> str:
    """
    Classifies news text into predefined categories
    using keyword-based scoring.
    """

    if not text:
        return "Other"

    t = text.lower()
    scores = {}

    for category, keywords in CATEGORIES.items():
        scores[category] = sum(1 for word in keywords if word in t)

    best_category = max(scores, key=scores.get)

    return best_category if scores[best_category] > 0 else "Other"
