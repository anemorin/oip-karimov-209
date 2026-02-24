import os
import sys
from typing import Optional

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
INDEX_FILE = os.path.join(BASE_DIR, "inverted_index.txt")

def load_index(path: str) -> tuple[dict[str, set[int]], set[int], dict[int, str]]:
    index: dict[str, set[int]] = {}
    all_docs: set[int] = set()

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            token, _, rest = line.partition(": ")
            doc_ids = {int(d.strip()) for d in rest.split(",") if d.strip().isdigit()}
            index[token.lower()] = doc_ids
            all_docs |= doc_ids

    pages_dir = os.path.join(BASE_DIR, "..", "#1", "pages")
    id_to_file: dict[int, str] = {}
    if os.path.isdir(pages_dir):
        files = sorted(f for f in os.listdir(pages_dir) if f.endswith(".html"))
        for doc_id, fname in enumerate(files):
            id_to_file[doc_id] = fname

    return index, all_docs, id_to_file

def tokenize_query(query: str) -> list[str]:
    query = query.replace("(", " ( ").replace(")", " ) ")
    return [t for t in query.split() if t]

class BooleanQueryParser:
    OPERATORS = {"and", "or", "not"}

    def __init__(self, tokens: list[str],
                 index: dict[str, set[int]],
                 all_docs: set[int]) -> None:
        self.tokens   = tokens
        self.pos      = 0
        self.index    = index
        self.all_docs = all_docs

    def peek(self) -> Optional[str]:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos].lower()
        return None

    def consume(self, expected: Optional[str] = None) -> str:
        tok = self.tokens[self.pos]
        if expected and tok.lower() != expected:
            raise SyntaxError(f"Expected '{expected}', got '{tok}'")
        self.pos += 1
        return tok

    def parse_expr(self) -> set[int]:
        result = self.parse_term()
        while self.peek() == "or":
            self.consume("or")
            result = result | self.parse_term()
        return result

    def parse_term(self) -> set[int]:
        result = self.parse_factor()
        while self.peek() == "and":
            self.consume("and")
            result = result & self.parse_factor()
        return result

    def parse_factor(self) -> set[int]:
        tok = self.peek()
        if tok == "not":
            self.consume("not")
            return self.all_docs - self.parse_factor()
        if tok == "(":
            self.consume("(")
            result = self.parse_expr()
            self.consume(")")
            return result
        if tok is None:
            raise SyntaxError("Unexpected end of query")
        if tok in self.OPERATORS:
            raise SyntaxError(f"Unexpected operator '{tok}'")
        word = self.consume().lower()
        return self.index.get(word, set())

    def parse(self) -> set[int]:
        result = self.parse_expr()
        if self.pos != len(self.tokens):
            raise SyntaxError(f"Unexpected token '{self.tokens[self.pos]}'")
        return result

def search(query: str,
           index: dict[str, set[int]],
           all_docs: set[int]) -> list[int]:
    tokens = tokenize_query(query)
    if not tokens:
        return []
    return sorted(BooleanQueryParser(tokens, index, all_docs).parse())


def print_results(doc_ids: list[int], id_to_file: dict[int, str]) -> None:
    if not doc_ids:
        print("  Ничего не найдено.")
        return
    print(f"  Найдено документов: {len(doc_ids)}")
    for doc_id in doc_ids:
        print(f"  [{doc_id}] {id_to_file.get(doc_id, 'unknown')}")


def main() -> None:
    if not os.path.exists(INDEX_FILE):
        print(f"[ERROR] Index file not found: {INDEX_FILE}")
        print("Run  python3 index.py  first.")
        sys.exit(1)

    print("Loading inverted index …", end=" ", flush=True)
    index, all_docs, id_to_file = load_index(INDEX_FILE)
    print(f"{len(index)} terms, {len(all_docs)} documents loaded.\n")

    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        print("Введите запрос (AND, OR, NOT, скобки).")
        print("Пример: (html AND markup) OR css\n")
        query = input("Запрос > ").strip()

    if not query:
        print("Запрос пуст.")
        return

    print(f"\nЗапрос: {query}")
    try:
        print_results(search(query, index, all_docs), id_to_file)
    except SyntaxError as e:
        print(f"  [Ошибка разбора] {e}")


if __name__ == "__main__":
    main()
