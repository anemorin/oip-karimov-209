import os
from collections import defaultdict

BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
LEMMAS_PER_DOC = os.path.join(BASE_DIR, "..", "#2", "lemmas_per_doc")
INDEX_FILE     = os.path.join(BASE_DIR, "inverted_index.txt")


def build_index() -> tuple[dict[str, set[int]], dict[int, str]]:
    files = sorted(f for f in os.listdir(LEMMAS_PER_DOC) if f.endswith(".txt"))

    if not files:
        raise FileNotFoundError(
            f"No lemma files found in {LEMMAS_PER_DOC}\n"
            "Run  python3 ../#2/tokenizer.py  first."
        )

    print(f"Building inverted index from {len(files)} lemma files …")

    index: dict[str, set[int]] = defaultdict(set)
    id_to_file: dict[int, str] = {}

    for doc_id, fname in enumerate(files):
        id_to_file[doc_id] = fname
        filepath = os.path.join(LEMMAS_PER_DOC, fname)
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.split()
                if parts:
                    lemma = parts[0]
                    index[lemma].add(doc_id)

    print(f"Index built. Unique lemmas: {len(index)}")
    return index, id_to_file


def save_index(index: dict[str, set[int]]) -> None:
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        for lemma in sorted(index):
            doc_ids = ", ".join(str(d) for d in sorted(index[lemma]))
            f.write(f"{lemma}: {doc_ids}\n")
    print(f"Saved inverted index → {INDEX_FILE}  ({len(index)} lemmas)")


if __name__ == "__main__":
    idx, _ = build_index()
    save_index(idx)
