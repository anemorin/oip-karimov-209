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

BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR       = os.path.join(BASE_DIR, "..", "#1", "pages")
TOKENS_FILE     = os.path.join(BASE_DIR, "tokens.txt")
LEMMAS_FILE     = os.path.join(BASE_DIR, "lemmas.txt")
TOKENS_PER_DOC  = os.path.join(BASE_DIR, "tokens_per_doc")
LEMMAS_PER_DOC  = os.path.join(BASE_DIR, "lemmas_per_doc")

STOP_WORDS = set(stopwords.words("english"))

lemmatizer = WordNetLemmatizer()


def get_wordnet_pos(treebank_tag: str) -> str:
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
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")

    for tag in soup(["script", "style", "link", "noscript", "iframe", "meta"]):
        tag.decompose()
    return soup.get_text(separator=" ")


def process_pages():
    os.makedirs(TOKENS_PER_DOC, exist_ok=True)
    os.makedirs(LEMMAS_PER_DOC, exist_ok=True)

    page_files = sorted(
        f for f in os.listdir(PAGES_DIR) if f.endswith(".html")
    )
    print(f"Processing {len(page_files)} HTML files from {PAGES_DIR} …")

    all_tokens: set[str] = set()
    doc_tokens: dict[str, list[str]] = {}

    for fname in page_files:
        filepath = os.path.join(PAGES_DIR, fname)
        text = extract_text_from_html(filepath)
        words = word_tokenize(text)
        doc_set: set[str] = set()
        for w in words:
            w_lower = w.lower()
            if is_valid_token(w_lower):
                doc_set.add(w_lower)
                all_tokens.add(w_lower)
        stem = os.path.splitext(fname)[0]
        doc_tokens[stem] = sorted(doc_set)

    print(f"Unique valid tokens (global): {len(all_tokens)}")

    token_list = sorted(all_tokens)
    tagged = nltk.pos_tag(token_list)

    token_to_lemma: dict[str, str] = {}
    lemma_map: dict[str, list[str]] = defaultdict(list)
    for token, pos in tagged:
        wn_pos = get_wordnet_pos(pos)
        lemma = lemmatizer.lemmatize(token, pos=wn_pos)
        token_to_lemma[token] = lemma
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

    for stem, tokens in doc_tokens.items():
        tok_path = os.path.join(TOKENS_PER_DOC, f"{stem}.txt")
        with open(tok_path, "w", encoding="utf-8") as f:
            for t in tokens:
                f.write(t + "\n")

        doc_lemma_map: dict[str, list[str]] = defaultdict(list)
        for t in tokens:
            lemma = token_to_lemma.get(t, t)
            doc_lemma_map[lemma].append(t)

        lem_path = os.path.join(LEMMAS_PER_DOC, f"{stem}.txt")
        with open(lem_path, "w", encoding="utf-8") as f:
            for lemma in sorted(doc_lemma_map):
                tokens_str = " ".join(sorted(doc_lemma_map[lemma]))
                f.write(f"{lemma} {tokens_str}\n")

    print(f"Saved per-doc tokens → {TOKENS_PER_DOC}/  ({len(doc_tokens)} files)")
    print(f"Saved per-doc lemmas → {LEMMAS_PER_DOC}/  ({len(doc_tokens)} files)")


if __name__ == "__main__":
    process_pages()
