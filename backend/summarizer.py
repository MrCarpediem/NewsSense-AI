# backend/summarizer.py
# Lightweight extractive summarizer (NO API)
# Works for English + Hindi

import re
from collections import Counter
from .text_cleaner import clean_ocr_text


def summarize(text: str, language: str = "English") -> str:
    """
    Lightweight extractive summarization.
    No external API.
    Works for both English and Hindi text.
    """

    if not text or not text.strip():
        return "Summary not available."

    # Clean OCR noise (Hindi-safe)
    text = clean_ocr_text(text)

    # Split into sentences
    sentences = split_sentences(text)

    # If text is very short, return as-is
    if len(sentences) <= 2:
        return humanize(" ".join(sentences))

    # Build word frequency table
    word_freq = build_word_frequency(text)

    # Score each sentence
    sentence_scores = {}
    for sentence in sentences:
        score = 0
        for word in tokenize(sentence):
            score += word_freq.get(word, 0)
        sentence_scores[sentence] = score

    # Pick top 2 sentences
    top_sentences = sorted(
        sentence_scores,
        key=sentence_scores.get,
        reverse=True
    )[:2]

    # Hindi-aware / English-aware join
    joiner = "। " if contains_hindi(text) else ". "
    summary = joiner.join(top_sentences)

    return humanize(summary)


# ---------------- HELPERS ----------------

def split_sentences(text: str):
    """
    Splits sentences for both:
    - English: . ? !
    - Hindi: ।
    """
    sentences = re.split(r"[.!?।]", text)
    return [s.strip() for s in sentences if len(s.strip()) > 20]


def tokenize(sentence: str):
    """
    Tokenize words for scoring.
    Supports English + Hindi characters.
    """
    return re.findall(r"[\u0900-\u097F]+|[a-zA-Z]{3,}", sentence.lower())


def build_word_frequency(text: str):
    """
    Builds word frequency table.
    Simple & explainable.
    """

    words = tokenize(text)

    stopwords = {
        # English
        "the", "and", "that", "with", "from", "this", "were",
        "have", "been", "will", "their", "after", "before",
        "about", "into", "while", "there", "which", "would",
        "could", "should",
        # Hindi
        "है", "और", "था", "थे", "की", "का",
        "में", "से", "पर", "को", "लिए"
    }

    words = [w for w in words if w not in stopwords]
    return Counter(words)


def humanize(summary: str) -> str:
    """
    Makes summary readable without over-polishing.
    """

    summary = " ".join(summary.split())

    if not summary:
        return "Summary not available."

    # Ensure proper ending punctuation
    if not summary.endswith(("।", ".")):
        summary += "।" if contains_hindi(summary) else "."

    return summary


def contains_hindi(text: str) -> bool:
    """
    Checks if text contains Hindi characters.
    """
    return any("\u0900" <= ch <= "\u097F" for ch in text)
