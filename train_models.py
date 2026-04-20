import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
import joblib
import os

# --- 1. Dataset Taiyar Karna (Sample Data for Training) ---
# Interview ke liye aap bata sakte ho ki humne ye data categorize kiya hai
data = {
    'text': [
        # Sports
        "The football match ended in a draw after a thrilling final minute goal.",
        "Cricket world cup is scheduled to happen next year with ten teams.",
        "The athlete broke the world record in the 100m sprint yesterday.",
        "Tennis legend wins his 20th grand slam title in Paris.",
        "Badminton championship sees a new rising star from Asia.",
        
        # Politics
        "The government announced a new policy for urban development and housing.",
        "Election results are out and the opposition party has gained majority.",
        "Prime minister met with world leaders to discuss global trade and peace.",
        "The parliament passed a new bill regarding climate change and carbon taxes.",
        "Voting percentage was at an all-time high in the recent state elections.",
        
        # Technology
        "New AI model released that can generate realistic images from text.",
        "Software update fixes critical security vulnerabilities in the operating system.",
        "The startup raised $50 million to develop next-gen cloud computing hardware.",
        "Cybersecurity experts warn about a new type of ransomware attacking businesses.",
        "The tech giant announced a new smartphone with foldable screen technology.",
        
        # Business
        "Stock market reached a new high as investor confidence improved.",
        "The company reported a 20% increase in quarterly revenue and profits.",
        "Startups are struggling to find funding in the current economic climate.",
        "Interest rates were hiked by the central bank to control rising inflation.",
        "The merger between the two tech giants was approved by regulators.",
        
        # Crime
        "Police arrested three suspects in connection with the bank robbery.",
        "The court sentenced the murderer to life imprisonment after a long trial.",
        "Investigation is ongoing into the mysterious death of the businessman.",
        "Crime rates have dropped significantly due to increased police patrolling.",
        "The fraud suspect was caught at the airport trying to flee the country.",
        
        # Healthcare
        "New vaccine shows high effectiveness against the seasonal virus.",
        "Hospitals are overwhelmed with patients during the winter season.",
        "A breakthrough treatment for the disease was announced by doctors.",
        "Doctors recommend regular exercise and a balanced diet for good health.",
        "The medical researchers found a link between lifestyle and chronic illnesses."
    ],
    'category': [
        'Sports', 'Sports', 'Sports', 'Sports', 'Sports',
        'Politics', 'Politics', 'Politics', 'Politics', 'Politics',
        'Technology', 'Technology', 'Technology', 'Technology', 'Technology',
        'Business', 'Business', 'Business', 'Business', 'Business',
        'Crime', 'Crime', 'Crime', 'Crime', 'Crime',
        'Healthcare', 'Healthcare', 'Healthcare', 'Healthcare', 'Healthcare'
    ]
}

df = pd.DataFrame(data)

# --- 2. Preprocessing (TF-IDF) ---
# Isse text numbers mein convert hota hai
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(df['text'])
y = df['category']

# --- 3. Model Training ---
print("Training models...")

# Model A: Naive Bayes
model_nb = MultinomialNB()
model_nb.fit(X, y)

# Model B: Logistic Regression
model_lr = LogisticRegression()
model_lr.fit(X, y)

# Model C: SVM
model_svm = LinearSVC()
model_svm.fit(X, y)

# --- 4. Models Save Karna ---
os.makedirs('models', exist_ok=True)

joblib.dump(vectorizer, 'models/vectorizer.pkl')
joblib.dump(model_nb, 'models/model_nb.pkl')
joblib.dump(model_lr, 'models/model_lr.pkl')
joblib.dump(model_svm, 'models/model_svm.pkl')

print("Success! All models saved in the 'models/' directory.")
