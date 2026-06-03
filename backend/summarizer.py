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

# Common abbreviations that should NOT trigger sentence splits
_ABBREVIATIONS = {
    "mr", "mrs", "ms", "dr", "prof", "sr", "jr", "vs", "etc", "approx",
    "dept", "est", "govt", "inc", "ltd", "corp", "jan", "feb", "mar",
    "apr", "jun", "jul", "aug", "sep", "oct", "nov", "dec",
    "st", "ave", "blvd", "gen", "col", "sgt", "lt", "capt",
    "u.s", "u.k", "u.n", "e.u", "a.m", "p.m", "i.e", "e.g",
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


def _split_sentences(text: str) -> list:
    """
    Smart sentence splitter that handles abbreviations, decimal numbers,
    and other tricky cases where a period does NOT end a sentence.
    """
    # Protect abbreviations by replacing their dots temporarily
    protected = text
    for abbr in _ABBREVIATIONS:
        # Match abbreviation followed by a period (case-insensitive)
        pattern = re.compile(rf'\b({re.escape(abbr)})\.\s', flags=re.IGNORECASE)
        protected = pattern.sub(rf'\1<DOT> ', protected)
    
    # Protect decimal numbers (e.g., "3.5", "Rs. 500")
    protected = re.sub(r'(\d)\.(\d)', r'\1<DOT>\2', protected)
    
    # Protect single-letter initials (e.g., "A. B. Vajpayee", "U.S.A.")
    protected = re.sub(r'\b([A-Z])\.\s*(?=[A-Z])', r'\1<DOT> ', protected)
    
    # Now split on actual sentence-ending punctuation
    # Split on . ! ? । followed by a space and a capital letter or end of string
    raw_parts = re.split(r'(?<=[.!?।])\s+(?=[A-Z\u0900-\u097F])', protected)
    
    # If the above didn't split well (e.g., no capital letters after periods), fallback
    if len(raw_parts) <= 1:
        raw_parts = re.split(r'[.!?।]\s+', protected)
    
    # Restore protected dots
    sentences = []
    for part in raw_parts:
        restored = part.replace('<DOT>', '.').strip()
        if len(restored) > 20:  # Ignore tiny fragments
            sentences.append(restored)
    
    return sentences


def summarize(text: str, language: str = "English") -> str:
    """
    100% Local Extractive Summarizer.
    Uses TF scoring with position weighting to find the most important sentences.
    Supports English and Hindi output.
    """
    if not text or len(text) < 100:
        if language == "Hindi" and text:
            return _translate_to_hindi(text)
        return text if text else ""

    text = clean_ocr_text(text)
    
    # 1. Smart sentence tokenization (handles abbreviations, decimals, etc.)
    sentences = _split_sentences(text)
    
    if len(sentences) <= 3:
        summary = ". ".join(sentences)
        if not summary.endswith("."):
            summary += "."
        if language == "Hindi":
            return _translate_to_hindi(summary)
        return summary

    # 2. Build word frequency (Term Frequency)
    words = re.findall(r"[\u0900-\u097F]+|[a-zA-Z]{3,}", text.lower())
    stopwords = {
        "the", "and", "this", "that", "with", "from", "were", "have", "been", "will",
        "was", "are", "for", "not", "but", "had", "has", "its", "his", "her",
        "they", "them", "than", "then", "also", "into", "over", "such", "can",
        "more", "some", "very", "just", "about", "being", "would", "could", "should",
        "did", "does", "these", "those", "each", "which", "their", "there", "other",
        "said", "says", "told",
        "है", "और", "था", "थे", "की", "का", "में", "से", "पर", "को", "लिए",
        "एक", "यह", "वह", "ने", "हैं", "जो", "तो", "भी", "या", "कि",
    }
    
    word_freq = Counter([w for w in words if w not in stopwords])
    if not word_freq:
        summary = ". ".join(sentences[:3])
        if not summary.endswith("."):
            summary += "."
        if language == "Hindi":
            return _translate_to_hindi(summary)
        return summary
    
    # Normalize frequency
    max_freq = max(word_freq.values())
    for word in word_freq:
        word_freq[word] /= max_freq

    # 3. Score sentences: TF importance + position bonus + length normalization
    sentence_scores = {}
    total_sentences = len(sentences)
    
    for idx, sent in enumerate(sentences):
        sent_words = re.findall(r"[\u0900-\u097F]+|[a-zA-Z]{3,}", sent.lower())
        if not sent_words:
            continue
        
        # TF score: sum of word importance, normalized by sentence length
        tf_score = sum(word_freq.get(w, 0) for w in sent_words)
        length_norm = len(sent_words) ** 0.5  # Square root normalization (not too harsh)
        normalized_score = tf_score / length_norm if length_norm > 0 else 0
        
        # Position bonus: first sentences in news articles carry the most info
        # First sentence gets 1.5x boost, second gets 1.3x, third gets 1.15x, rest get 1.0x
        if idx == 0:
            position_weight = 1.5
        elif idx == 1:
            position_weight = 1.3
        elif idx == 2:
            position_weight = 1.15
        elif idx >= total_sentences - 2:
            # Last 2 sentences often have conclusions — slight boost
            position_weight = 1.1
        else:
            position_weight = 1.0
        
        sentence_scores[sent] = normalized_score * position_weight

    if not sentence_scores:
        summary = ". ".join(sentences[:3])
        if not summary.endswith("."):
            summary += "."
        if language == "Hindi":
            return _translate_to_hindi(summary)
        return summary

    # 4. Pick top sentences — adaptive count based on article length
    if len(sentences) <= 5:
        pick_count = 2
    elif len(sentences) <= 10:
        pick_count = 3
    else:
        pick_count = 4  # Longer articles get 4-sentence summaries
    
    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:pick_count]
    
    # Sort top sentences back to their original appearance order for better flow
    final_summary = sorted(top_sentences, key=lambda x: sentences.index(x))
    
    # Strip trailing punctuation from each sentence before joining (avoids ".." artifacts)
    cleaned_sentences = [re.sub(r'[.!?।]+$', '', s).strip() for s in final_summary]
    
    is_hindi_text = any("\u0900" <= ch <= "\u097F" for ch in text)
    joiner = "। " if is_hindi_text else ". "
    summary = joiner.join(cleaned_sentences)
    
    # Add final punctuation
    summary += "।" if is_hindi_text else "."

    # Translate to Hindi if requested and text is in English
    if language == "Hindi" and not is_hindi_text:
        summary = _translate_to_hindi(summary)
    
    return summary
