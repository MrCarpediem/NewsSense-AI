import joblib
import os
import re
from collections import Counter

CATEGORIES_RULES = {
    "Sports": ["match", "cricket", "football", "goal", "score", "win"],
    "Politics": ["election", "government", "minister", "vote", "party"],
    "Technology": ["tech", "software", "hardware", "computer", "ai"],
    "Crime": ["police", "arrest", "murder", "jail", "court", "prison"],
    "Business": ["market", "stock", "share", "company", "investment"],
    "Healthcare": ["hospital", "doctor", "medicine", "health", "disease"],
    "Education": ["school", "college", "university", "student", "exam"]
}

class MLResourceLoader:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MLResourceLoader, cls).__new__(cls)
            cls._instance.loaded = False
            cls._instance.vectorizer = None
            cls._instance.models = {}
            cls._instance.load()
        return cls._instance

    def load(self):
        try:
            if os.path.exists('models/vectorizer.pkl'):
                self.vectorizer = joblib.load('models/vectorizer.pkl')
                self.models['Naive Bayes'] = joblib.load('models/model_nb.pkl')
                self.models['Logistic Reg.'] = joblib.load('models/model_lr.pkl')
                self.models['SVM (Linear)'] = joblib.load('models/model_svm.pkl')
                self.loaded = True
        except: pass

def classify_all(text: str):
    results = {}
    t = text.lower()
    rule_scores = {cat: sum(1 for kw in kws if kw in t) for cat, kws in CATEGORIES_RULES.items()}
    best_rule = max(rule_scores, key=rule_scores.get)
    results['Rule-Based'] = {"label": best_rule if rule_scores[best_rule] > 0 else "Other", "conf": 100}

    loader = MLResourceLoader()
    if loader.loaded:
        X = loader.vectorizer.transform([text])
        for name, model in loader.models.items():
            results[name] = {"label": model.predict(X)[0], "conf": 90}
    return results

def get_entities(text: str):
    """
    Improved NER: Filters out numbers and noisy OCR artifacts.
    """
    # Find words starting with Capital letter
    words = re.findall(r'(?<!\. )(?<!^)([A-Z][a-z]+)', text)
    
    # Noise Filter: No numbers, length > 3, not in common exclusion list
    excluded = {"The", "This", "That", "There", "When", "What", "With", "From", "India", "News"}
    
    clean_entities = []
    for w in words:
        # Check if word contains any digit or is a common stopword
        if not any(char.isdigit() for char in w) and w not in excluded and len(w) > 3:
            clean_entities.append(w)
            
    # Return top 5 unique entities by frequency
    counts = Counter(clean_entities)
    return [k for k, v in counts.most_common(5)]

def get_top_keywords(text: str, n=5):
    """
    Improved Keywords: Only alphabetic words, length > 4.
    """
    # Extract only alphabetic words
    words = re.findall(r'\b[a-zA-Z]{5,}\b', text.lower())
    
    stopwords = {"about", "there", "their", "would", "could", "should", "after", "before", "under", "which"}
    filtered = [w for w in words if w not in stopwords]
    
    return [k for k, v in Counter(filtered).most_common(n)]
