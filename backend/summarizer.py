import re
from collections import Counter
from .text_cleaner import clean_ocr_text

# Basic English-to-Hindi translation map for common news terms
_EN_TO_HI = {
    "government": "सरकार", "election": "चुनाव", "minister": "मंत्री",
    "police": "पुलिस", "court": "अदालत", "market": "बाजार",
    "company": "कंपनी", "hospital": "अस्पताल", "school": "स्कूल",
    "match": "मैच", "team": "टीम", "player": "खिलाड़ी",
    "country": "देश", "world": "दुनिया", "people": "लोग",
    "said": "कहा", "new": "नया", "first": "पहला",
    "year": "साल", "report": "रिपोर्ट", "according": "अनुसार",
    "today": "आज", "announced": "घोषणा की", "arrested": "गिरफ्तार",
    "death": "मौत", "killed": "मारे गए", "injured": "घायल",
    "money": "पैसा", "crore": "करोड़", "lakh": "लाख",
    "cricket": "क्रिकेट", "football": "फुटबॉल",
    "president": "राष्ट्रपति", "prime minister": "प्रधानमंत्री",
    "technology": "तकनीक", "software": "सॉफ्टवेयर",
    "positive": "सकारात्मक", "negative": "नकारात्मक",
    "increase": "बढ़ोतरी", "decrease": "कमी",
    "important": "महत्वपूर्ण", "breaking": "ब्रेकिंग",
}

def _translate_to_hindi(text: str) -> str:
    """
    Basic keyword-based English-to-Hindi translation.
    Not a full translator — provides a Hindi-flavored summary for local use.
    """
    result = text
    for en, hi in _EN_TO_HI.items():
        result = re.sub(rf'\b{en}\b', hi, result, flags=re.IGNORECASE)
    return result


def summarize(text: str, language: str = "English") -> str:
    """
    100% Local Extractive Summarizer.
    Uses TF (Term Frequency) scoring to find the most important sentences.
    Supports English and Hindi output.
    """
    if not text or len(text) < 100:
        if language == "Hindi" and text:
            return _translate_to_hindi(text)
        return text if text else ""

    text = clean_ocr_text(text)
    
    # 1. Tokenize into sentences
    sentences = re.split(r"[.!?।]", text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 30]
    
    if len(sentences) <= 3:
        summary = " ".join(sentences)
        if language == "Hindi":
            return _translate_to_hindi(summary)
        return summary

    # 2. Build word frequency (Term Frequency)
    words = re.findall(r"[\u0900-\u097F]+|[a-zA-Z]{3,}", text.lower())
    stopwords = {"the", "and", "this", "that", "with", "from", "were", "have", "been", "will", 
                 "है", "और", "था", "थे", "की", "का", "में", "से", "पर", "को", "लिए"}
    
    word_freq = Counter([w for w in words if w not in stopwords])
    if not word_freq:
        summary = " ".join(sentences[:2])
        if language == "Hindi":
            return _translate_to_hindi(summary)
        return summary
    
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

    if not sentence_scores:
        summary = " ".join(sentences[:2])
        if language == "Hindi":
            return _translate_to_hindi(summary)
        return summary

    # 4. Pick top 2-3 sentences and keep them in original order
    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:2]
    
    # Sort top sentences back to their original appearance order for better flow
    final_summary = sorted(top_sentences, key=lambda x: sentences.index(x))
    
    is_hindi_text = any("\u0900" <= ch <= "\u097F" for ch in text)
    joiner = "। " if is_hindi_text else ". "
    summary = joiner.join(final_summary) + joiner.strip()

    # Translate to Hindi if requested and text is in English
    if language == "Hindi" and not is_hindi_text:
        summary = _translate_to_hindi(summary)
    
    return summary
