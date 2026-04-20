import re
from collections import Counter
from .text_cleaner import clean_ocr_text

def summarize(text: str, language: str = "English") -> str:
    """
    100% Local Extractive Summarizer.
    Uses TF (Term Frequency) scoring to find the most important sentences.
    """
    if not text or len(text) < 100:
        return text

    text = clean_ocr_text(text)
    
    # 1. Tokenize into sentences
    sentences = re.split(r"[.!?।]", text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 30]
    
    if len(sentences) <= 3:
        return " ".join(sentences)

    # 2. Build word frequency (Term Frequency)
    words = re.findall(r"[\u0900-\u097F]+|[a-zA-Z]{3,}", text.lower())
    stopwords = {"the", "and", "this", "that", "with", "from", "were", "have", "been", "will", 
                 "है", "और", "था", "थे", "की", "का", "में", "से", "पर", "को", "लिए"}
    
    word_freq = Counter([w for w in words if w not in stopwords])
    if not word_freq:
        return " ".join(sentences[:2])
    
    # Normalize frequency
    max_freq = max(word_freq.values())
    for word in word_freq:
        word_freq[word] /= max_freq

    # 3. Score sentences based on word importance
    sentence_scores = {}
    for sent in sentences:
        for word in re.findall(r"[\u0900-\u097F]+|[a-zA-Z]{3,}", sent.lower()):
            if word in word_freq:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + word_freq[word]

    # 4. Pick top 2-3 sentences and keep them in original order
    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:2]
    
    # Sort top sentences back to their original appearance order for better flow
    final_summary = sorted(top_sentences, key=lambda x: sentences.index(x))
    
    joiner = "। " if any("\u0900" <= ch <= "\u097F" for ch in text) else ". "
    return joiner.join(final_summary) + (joiner.strip())
