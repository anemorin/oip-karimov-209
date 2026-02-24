import ssl
import os
from collections import defaultdict

try:
    ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
    pass

from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR  = os.path.join(BASE_DIR, "..", "#1", "pages")
INDEX_FILE = os.path.join(BASE_DIR, "inverted_index.txt")

STOP_WORDS = set(stopwords.words("english"))


def is_valid_token(word: str) -> bool:
    return word.isalpha() and len(word) >= 2 and word not in STOP_WORDS


def extract_text(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")
    for tag in soup(["script", "style", "link", "noscript", "iframe", "meta"]):
        tag.decompose()
    return soup.get_text(separator=" ")


def build_index() -> tuple[dict[str, set[int]], dict[int, str]]:
    page_files = sorted(f for f in os.listdir(PAGES_DIR) if f.endswith(".html"))
    print(f"Building inverted index from {len(page_files)} HTML files …")

    index: dict[str, set[int]] = defaultdict(set)
    id_to_file: dict[int, str] = {}

    for doc_id, fname in enumerate(page_files):
        id_to_file[doc_id] = fname
        text = extract_text(os.path.join(PAGES_DIR, fname))
        for w in word_tokenize(text):
            w = w.lower()
            if is_valid_token(w):
                index[w].add(doc_id)

    print(f"Index built. Unique terms: {len(index)}")
    return index, id_to_file


def save_index(index: dict[str, set[int]]) -> None:
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        for token in sorted(index):
            doc_ids = ", ".join(str(d) for d in sorted(index[token]))
            f.write(f"{token}: {doc_ids}\n")
    print(f"Saved inverted index → {INDEX_FILE}  ({len(index)} terms)")


if __name__ == "__main__":
    idx, _ = build_index()
    save_index(idx)
