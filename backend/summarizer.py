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

    text = clean_ocr_text(text)

    sentences = split_sentences(text)

    if len(sentences) <= 2:
        return humanize(" ".join(sentences))

    word_freq = build_word_frequency(text)

    sentence_scores = {}
    for sentence in sentences:
        score = 0
        for word in tokenize(sentence):
            score += word_freq.get(word, 0)
        sentence_scores[sentence] = score

    top_sentences = sorted(
        sentence_scores,
        key=sentence_scores.get,
        reverse=True
    )[:2]

    summary = " ".join(top_sentences)
    return humanize(summary)



def split_sentences(text: str):
    """
    Splits sentences for both English (., ?, !)
    and Hindi (।)
    """
    sentences = re.split(r"[.!?।]", text)
    return [s.strip() for s in sentences if len(s.strip()) > 20]


def tokenize(sentence: str):
    """
    Tokenize words for scoring.
    Works for English and Hindi characters.
    """
    return re.findall(r"[\u0900-\u097F]+|[a-zA-Z]{3,}", sentence.lower())


def build_word_frequency(text: str):
    """
    Builds word frequency table.
    Keeps logic simple & explainable.
    """

    words = tokenize(text)

    stopwords = {
        "the", "and", "that", "with", "from", "this", "were",
        "have", "been", "will", "their", "after", "before",
        "about", "into", "while", "there", "which", "would",
        "could", "should", "है", "और", "था", "थे", "की", "का",
        "में", "से", "पर", "को", "लिए"
    }

    words = [w for w in words if w not in stopwords]
    return Counter(words)


def humanize(summary: str) -> str:
    """
    Makes summary readable without over-polishing.
    """
    summary = summary.strip()
    summary = summary.replace("  ", " ")

    if summary and not summary.endswith(("।", ".")):
        summary += "।" if contains_hindi(summary) else "."

    return summary[0].upper() + summary[1:] if summary else "Summary not available."


def contains_hindi(text: str) -> bool:
    return any("\u0900" <= ch <= "\u097F" for ch in text)
