import re
import unicodedata
from typing import List, Tuple

import spacy

_nlp = None


def _load_spacy():
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("pt_core_news_sm")
        except Exception as e:
            raise RuntimeError(
                "SpaCy Portuguese model not found. Please install it using 'python -m spacy download pt_core_news_sm'.") from e
    return _nlp


def normalize(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces/newlines with a single space
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)  # Remove URLs and email
    text = re.sub(r"<[^>]+>", " ", text)  # Remove HTML tags
    text = re.sub(r"\S+@\S+\.\S+", " ", text)
    text = re.sub(r"(?i)unsubscribe|cancelar inscrição|descadastrar", " ", text) # Remove common "unsubscribe" patterns / disclaimers (exemplos)
    # Normalize unicode and whitespace
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def remove_signatures(text: str) -> str:
    # Define common signature patterns in Portuguese, uses regex to identify them
    signature_patterns = re.compile(r'^\s*[-–—\*\s]*\b(atenciosamente|cordialmente|abraços|abçs|grato|obrigado|obrigada|melhores cumprimentos|saudações|att(?:\.|))\b', re.I)
    lines = text.splitlines()

    for i, line in enumerate(lines):
        # Check if the line matches any signature pattern
        if signature_patterns.search(line):
            # If a signature pattern is found, return text up to that line
            return "\n".join(lines[:i])
    return text


# Basic text cleaning: normalization and signature removal
def clean_text_basic(text: str) -> str:
    text = normalize(text)
    text = remove_signatures(text)
    return text

def clean_and_lemmatize(text: str, remove_stopwords: bool = True) -> str:
    nlp = _load_spacy()
    text = clean_text_basic(text)
    text = text.lower()
    doc = nlp(text)
    tokens: List[str] = []
    for token in doc:
        #remove punctuation, spaces, and optionally stopwords
        if token.is_punct or token.is_space:
            continue
        #remove stopwords if specified
        if remove_stopwords and token.is_stop:
            continue
        lemma = token.lemma_.strip()
        #if lemma is empty, skip it
        if lemma == "":
            continue
        #append the lemma to the tokens list
        tokens.append(lemma)
    return ' '.join(tokens)

# Simple tokenization without lemmatization or stopword removal
def simple_tokenize(text: str) -> List[str]:
    nlp = _load_spacy()
    doc = nlp(text)
    return [token.text for token in doc if not (token.is_space or token.is_punct)]

#Preprocess text for classification tasks
def preprocess_for_classification(text: str) -> tuple[str, list[str]]:
    clean_text = clean_and_lemmatize(text, remove_stopwords=True)
    tokens = simple_tokenize(text)

    return clean_text, tokens