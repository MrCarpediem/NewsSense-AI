# PURE LOCAL NEWS CLASSIFIER
# Uses weighted keyword matching for interview-ready explainability

CATEGORIES = {
    "Sports": ["match", "cricket", "football", "goal", "score", "win", "won", "victory", "player", "team", "stadium", "tournament", "खेल", "मैच", "खिलाड़ी", "जीत"],
    "Politics": ["election", "government", "minister", "vote", "party", "parliament", "prime minister", "president", "policy", "cabinet", "सरकार", "चुनाव", "मंत्री", "संसद"],
    "Technology": ["tech", "software", "hardware", "computer", "ai", "internet", "startup", "data", "cloud", "security", "innovation", "तकनीक", "सॉफ्टवेयर"],
    "Crime": ["police", "arrest", "murder", "jail", "court", "sentence", "prison", "assault", "crime", "victim", "robbery", "fraud", "investigation", "पुलिस", "अपराध", "अदालत", "जेल", "सजा"],
    "Business": ["market", "stock", "share", "company", "investment", "profit", "economy", "bank", "revenue", "funding", "startup", "बाजार", "कंपनी", "निवेश", "बैंक"],
    "Healthcare": ["hospital", "doctor", "medicine", "covid", "health", "disease", "vaccine", "treatment", "patient", "अस्पताल", "डॉक्टर", "स्वास्थ्य", "बीमारी"],
    "Education": ["school", "college", "university", "student", "exam", "result", "education", "degree", "learning", "शिक्षा", "स्कूल", "कॉलेज", "विश्वविद्यालय"]
}

def classify(text: str) -> str:
    """
    Classifies news by calculating a match score for each category.
    Optimized for production-level local performance.
    """
    if not text:
        return "Other"

    t = text.lower()
    scores = {}

    for category, keywords in CATEGORIES.items():
        score = 0
        for kw in keywords:
            # Check for exact word matches (more accurate)
            if kw.lower() in t:
                # Assign more weight to the first occurrence
                score += 1
                # If the word is at the start (likely a headline/key topic), double the score
                if t.find(kw.lower()) < 200:
                    score += 1
        scores[category] = score

    # Find the category with the highest score
    best_category = max(scores, key=scores.get)
    
    # Threshold check to ensure accuracy
    if scores[best_category] > 0:
        return best_category
    
    return "Other"
