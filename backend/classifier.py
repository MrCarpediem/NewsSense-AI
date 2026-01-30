# backend/classifier.py
# English + Hindi keyword based classifier (balanced & explainable)

CATEGORIES = {
    "Crime": [
        # English
        "crime", "criminal", "murder", "murderer", "kill", "killing",
        "death", "dead", "arrest", "police", "custody", "investigation",
        "attack", "assault", "rape", "robbery", "theft", "fraud",
        "gun", "shooting", "stab", "stabbing", "violence", "case",
        "court", "trial", "lawyer", "judge", "prison", "jail",
        # Hindi
        "हत्या", "अपराध", "पुलिस", "गिरफ्तार", "मौत", "हमला",
        "डकैती", "चोरी", "हिंसा", "अदालत", "मुकदमा", "जेल"
    ],

    "Sports": [
        # English
        "sport", "match", "game", "tournament", "league",
        "cricket", "football", "soccer", "tennis", "badminton",
        "goal", "score", "win", "won", "lose", "lost",
        "victory", "defeat", "player", "team", "coach",
        "captain", "final", "world cup",
        # Hindi
        "खेल", "मैच", "जीत", "जीता", "हार", "विजय",
        "खिलाड़ी", "टीम", "कप्तान", "फाइनल", "विश्व कप",
        "टूर्नामेंट"
    ],

    "Politics": [
        # English
        "election", "government", "minister", "prime minister",
        "president", "parliament", "policy", "bill", "law",
        "vote", "voting", "party", "democracy", "speech",
        "campaign", "opposition", "cabinet", "constitution",
        # Hindi
        "सरकार", "चुनाव", "मंत्री", "प्रधानमंत्री",
        "राष्ट्रपति", "संसद", "नीति", "कानून",
        "वोट", "दल", "लोकतंत्र", "संविधान"
    ],

    "Business": [
        # English
        "business", "company", "market", "stock", "share",
        "investment", "investor", "profit", "loss", "revenue",
        "startup", "funding", "ipo", "economy", "bank",
        "loan", "interest", "finance", "trade",
        # Hindi
        "व्यापार", "कंपनी", "बाजार", "निवेश",
        "मुनाफा", "नुकसान", "अर्थव्यवस्था",
        "बैंक", "ऋण", "स्टार्टअप"
    ],

    "Technology": [
        # English
        "technology", "tech", "software", "hardware", "computer",
        "ai", "artificial intelligence", "machine learning",
        "data", "cloud", "cyber", "security", "hacking",
        "internet", "app", "application", "innovation",
        # Hindi
        "तकनीक", "प्रौद्योगिकी", "सॉफ्टवेयर",
        "हार्डवेयर", "कंप्यूटर", "एआई",
        "डेटा", "साइबर", "इंटरनेट"
    ],

    "Healthcare": [
        # English
        "health", "hospital", "doctor", "nurse", "patient",
        "medicine", "medical", "treatment", "disease",
        "covid", "virus", "infection", "vaccine", "surgery",
        # Hindi
        "स्वास्थ्य", "अस्पताल", "डॉक्टर",
        "मरीज", "दवा", "इलाज",
        "बीमारी", "टीका", "संक्रमण"
    ],

    "Education": [
        # English
        "education", "school", "college", "university",
        "student", "teacher", "exam", "examination",
        "result", "admission", "syllabus", "degree",
        "placement", "campus", "learning",
        # Hindi
        "शिक्षा", "स्कूल", "कॉलेज",
        "विश्वविद्यालय", "छात्र", "शिक्षक",
        "परीक्षा", "परिणाम", "प्रवेश",
        "पाठ्यक्रम", "डिग्री", "प्लेसमेंट"
    ]
}


def classify(text: str) -> str:
    """
    Classify news text using keyword scoring.
    Supports English + Hindi.
    """

    if not text:
        return "Other"

    t = text.lower()
    scores = {}

    for category, keywords in CATEGORIES.items():
        scores[category] = sum(1 for kw in keywords if kw.lower() in t)

    best_category = max(scores, key=scores.get)
    return best_category if scores[best_category] > 0 else "Other"
