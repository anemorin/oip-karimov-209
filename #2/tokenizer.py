import ssl
import os
from collections import defaultdict

# Fix SSL for macOS
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
    pass

from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR   = os.path.join(BASE_DIR, "..", "#1", "pages")
TOKENS_FILE = os.path.join(BASE_DIR, "tokens.txt")
LEMMAS_FILE = os.path.join(BASE_DIR, "lemmas.txt")

STOP_WORDS = set(stopwords.words("english"))

lemmatizer = WordNetLemmatizer()


def get_wordnet_pos(treebank_tag: str) -> str:
    """Map NLTK POS tag to WordNet POS for accurate lemmatization."""
    if treebank_tag.startswith("J"):
        return wordnet.ADJ
    elif treebank_tag.startswith("V"):
        return wordnet.VERB
    elif treebank_tag.startswith("N"):
        return wordnet.NOUN
    elif treebank_tag.startswith("R"):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def is_valid_token(word: str) -> bool:
    if not word.isalpha():
        return False

    if len(word) < 2:
        return False

    if word.lower() in STOP_WORDS:
        return False
    return True


def extract_text_from_html(filepath: str) -> str:
    """Extract visible text from an HTML file, stripping all tags."""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")

    for tag in soup(["script", "style", "link", "noscript", "iframe", "meta"]):
        tag.decompose()
    return soup.get_text(separator=" ")


def process_pages():
    page_files = sorted(
        f for f in os.listdir(PAGES_DIR) if f.endswith(".html")
    )
    print(f"Processing {len(page_files)} HTML files from {PAGES_DIR} …")

    all_tokens: set[str] = set()

    for fname in page_files:
        filepath = os.path.join(PAGES_DIR, fname)
        text = extract_text_from_html(filepath)
        words = word_tokenize(text)
        for w in words:
            w_lower = w.lower()
            if is_valid_token(w_lower):
                all_tokens.add(w_lower)

    print(f"Unique valid tokens (global): {len(all_tokens)}")

    token_list = sorted(all_tokens)
    tagged = nltk.pos_tag(token_list)

    lemma_map: dict[str, list[str]] = defaultdict(list)
    for token, pos in tagged:
        wn_pos = get_wordnet_pos(pos)
        lemma = lemmatizer.lemmatize(token, pos=wn_pos)
        lemma_map[lemma].append(token)

    with open(TOKENS_FILE, "w", encoding="utf-8") as f:
        for token in token_list:
            f.write(token + "\n")
    print(f"Saved tokens  → {TOKENS_FILE}  ({len(token_list)} lines)")

    with open(LEMMAS_FILE, "w", encoding="utf-8") as f:
        for lemma in sorted(lemma_map):
            tokens_str = " ".join(sorted(lemma_map[lemma]))
            f.write(f"{lemma} {tokens_str}\n")
    print(f"Saved lemmas  → {LEMMAS_FILE}  ({len(lemma_map)} lemmas)")


if __name__ == "__main__":
    process_pages()
