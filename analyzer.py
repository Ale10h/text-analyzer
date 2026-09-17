# analyzer.py
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from collections import Counter
import string
import re


STOPWORDS = set(stopwords.words('spanish')) 

def clean_text(text: str) -> str:
    """Normaliza el texto: minusculas, elimina exceso de espacios."""
    text = text.lower().strip()
    # reemplazar saltos de linea por espacio
    text = re.sub(r'\s+', ' ', text)
    return text

def tokenize_words(text: str):
    """Tokeniza palabras básicas (remueve puntuación)."""
    # quitar puntuación
    translator = str.maketrans('', '', string.punctuation)
    no_punct = text.translate(translator)
    words = nltk.word_tokenize(no_punct)
    return words

def count_characters(text: str) -> int:
    return len(text)

def count_words(text: str) -> int:
    words = tokenize_words(text)
    return len(words)

def count_sentences(text: str) -> int:
    blob = TextBlob(text)
    return len(blob.sentences)

def top_n_words(text: str, n: int = 10, remove_stopwords: bool = True):
    words = tokenize_words(text)
    if remove_stopwords:
        words = [w for w in words if w not in STOPWORDS]
    words = [w for w in words if w.isalpha()]  # quitar tokens numéricos
    counter = Counter(words)
    return counter.most_common(n)

def sentiment_analysis(text: str):
    """Usa TextBlob para obtener polarity y subjectivity.
    polarity: -1 (neg) a 1 (pos)
    subjectivity: 0 (objetivo) a 1 (subjetivo)
    """
    blob = TextBlob(text)
    polarity = round(blob.sentiment.polarity, 4)
    subjectivity = round(blob.sentiment.subjectivity, 4)

    # Clasificación simple basada en polarity
    if polarity > 0:
        label = "Positivo"
    elif polarity < 0:
        label = "Negativo"
    else:
        label = "Neutral"

    return {"polarity": polarity, "subjectivity": subjectivity, "label": label}

def analyze_text(text: str, top_n: int = 10, remove_stopwords: bool = True) -> dict:
    text_clean = clean_text(text)
    chars = count_characters(text_clean)
    words_count = count_words(text_clean)
    sentences = count_sentences(text_clean)
    top_words = top_n_words(text_clean, n=top_n, remove_stopwords=remove_stopwords)
    sentiment = sentiment_analysis(text_clean)

    return {
        "characters": chars,
        "words": words_count,
        "sentences": sentences,
        "top_words": top_words,
        "sentiment": sentiment
    }
