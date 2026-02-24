import urllib.request
import urllib.error
import ssl
import os
import time

ssl_ctx = ssl._create_unverified_context()

URLS = [
    "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "https://en.wikipedia.org/wiki/Java_(programming_language)",
    "https://en.wikipedia.org/wiki/C%2B%2B",
    "https://en.wikipedia.org/wiki/JavaScript",
    "https://en.wikipedia.org/wiki/Rust_(programming_language)",
    "https://en.wikipedia.org/wiki/Go_(programming_language)",
    "https://en.wikipedia.org/wiki/TypeScript",
    "https://en.wikipedia.org/wiki/Kotlin_(programming_language)",
    "https://en.wikipedia.org/wiki/Swift_(programming_language)",
    "https://en.wikipedia.org/wiki/R_(programming_language)",
    "https://en.wikipedia.org/wiki/Machine_learning",
    "https://en.wikipedia.org/wiki/Deep_learning",
    "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "https://en.wikipedia.org/wiki/Neural_network_(machine_learning)",
    "https://en.wikipedia.org/wiki/Natural_language_processing",
    "https://en.wikipedia.org/wiki/Computer_vision",
    "https://en.wikipedia.org/wiki/Reinforcement_learning",
    "https://en.wikipedia.org/wiki/Supervised_learning",
    "https://en.wikipedia.org/wiki/Unsupervised_learning",
    "https://en.wikipedia.org/wiki/Decision_tree",
    "https://en.wikipedia.org/wiki/Random_forest",
    "https://en.wikipedia.org/wiki/Support_vector_machine",
    "https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm",
    "https://en.wikipedia.org/wiki/Naive_Bayes_classifier",
    "https://en.wikipedia.org/wiki/Logistic_regression",
    "https://en.wikipedia.org/wiki/Linear_regression",
    "https://en.wikipedia.org/wiki/Gradient_descent",
    "https://en.wikipedia.org/wiki/Backpropagation",
    "https://en.wikipedia.org/wiki/Convolutional_neural_network",
    "https://en.wikipedia.org/wiki/Recurrent_neural_network",
    "https://en.wikipedia.org/wiki/Transformer_(machine_learning_model)",
    "https://en.wikipedia.org/wiki/Generative_adversarial_network",
    "https://en.wikipedia.org/wiki/Autoencoder",
    "https://en.wikipedia.org/wiki/Long_short-term_memory",
    "https://en.wikipedia.org/wiki/Attention_(machine_learning)",
    "https://en.wikipedia.org/wiki/Data_science",
    "https://en.wikipedia.org/wiki/Big_data",
    "https://en.wikipedia.org/wiki/Database",
    "https://en.wikipedia.org/wiki/SQL",
    "https://en.wikipedia.org/wiki/NoSQL",
    "https://en.wikipedia.org/wiki/PostgreSQL",
    "https://en.wikipedia.org/wiki/MySQL",
    "https://en.wikipedia.org/wiki/MongoDB",
    "https://en.wikipedia.org/wiki/Redis",
    "https://en.wikipedia.org/wiki/Apache_Kafka",
    "https://en.wikipedia.org/wiki/Apache_Hadoop",
    "https://en.wikipedia.org/wiki/Apache_Spark",
    "https://en.wikipedia.org/wiki/Elasticsearch",
    "https://en.wikipedia.org/wiki/Graph_database",
    "https://en.wikipedia.org/wiki/Data_structure",
    "https://en.wikipedia.org/wiki/Algorithm",
    "https://en.wikipedia.org/wiki/Sorting_algorithm",
    "https://en.wikipedia.org/wiki/Search_algorithm",
    "https://en.wikipedia.org/wiki/Binary_search_algorithm",
    "https://en.wikipedia.org/wiki/Hash_table",
    "https://en.wikipedia.org/wiki/Linked_list",
    "https://en.wikipedia.org/wiki/Stack_(abstract_data_type)",
    "https://en.wikipedia.org/wiki/Queue_(abstract_data_type)",
    "https://en.wikipedia.org/wiki/Binary_tree",
    "https://en.wikipedia.org/wiki/Graph_(abstract_data_type)",
    "https://en.wikipedia.org/wiki/Heap_(data_structure)",
    "https://en.wikipedia.org/wiki/Trie",
    "https://en.wikipedia.org/wiki/Dynamic_programming",
    "https://en.wikipedia.org/wiki/Greedy_algorithm",
    "https://en.wikipedia.org/wiki/Divide-and-conquer_algorithm",
    "https://en.wikipedia.org/wiki/Operating_system",
    "https://en.wikipedia.org/wiki/Linux",
    "https://en.wikipedia.org/wiki/Unix",
    "https://en.wikipedia.org/wiki/Microsoft_Windows",
    "https://en.wikipedia.org/wiki/MacOS",
    "https://en.wikipedia.org/wiki/Android_(operating_system)",
    "https://en.wikipedia.org/wiki/IOS",
    "https://en.wikipedia.org/wiki/Computer_network",
    "https://en.wikipedia.org/wiki/Internet",
    "https://en.wikipedia.org/wiki/World_Wide_Web",
    "https://en.wikipedia.org/wiki/HTTP",
    "https://en.wikipedia.org/wiki/HTTPS",
    "https://en.wikipedia.org/wiki/TCP/IP",
    "https://en.wikipedia.org/wiki/DNS",
    "https://en.wikipedia.org/wiki/IP_address",
    "https://en.wikipedia.org/wiki/Firewall_(computing)",
    "https://en.wikipedia.org/wiki/Virtual_private_network",
    "https://en.wikipedia.org/wiki/Cloud_computing",
    "https://en.wikipedia.org/wiki/Amazon_Web_Services",
    "https://en.wikipedia.org/wiki/Microsoft_Azure",
    "https://en.wikipedia.org/wiki/Google_Cloud_Platform",
    "https://en.wikipedia.org/wiki/Docker_(software)",
    "https://en.wikipedia.org/wiki/Kubernetes",
    "https://en.wikipedia.org/wiki/Microservices",
    "https://en.wikipedia.org/wiki/DevOps",
    "https://en.wikipedia.org/wiki/Continuous_integration",
    "https://en.wikipedia.org/wiki/Software_testing",
    "https://en.wikipedia.org/wiki/Agile_software_development",
    "https://en.wikipedia.org/wiki/Scrum_(software_development)",
    "https://en.wikipedia.org/wiki/Version_control",
    "https://en.wikipedia.org/wiki/Git",
    "https://en.wikipedia.org/wiki/GitHub",
    "https://en.wikipedia.org/wiki/Software_engineering",
    "https://en.wikipedia.org/wiki/Object-oriented_programming",
    "https://en.wikipedia.org/wiki/Functional_programming",
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "pages")
INDEX_FILE = os.path.join(BASE_DIR, "index.txt")

os.makedirs(OUTPUT_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; educational-crawler/1.0)"
}

successful = []
failed = []

for i, url in enumerate(URLS, start=1):
    filename = os.path.join(OUTPUT_DIR, f"{i:03d}.html")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15, context=ssl_ctx) as response:
            content = response.read()
        with open(filename, "wb") as f:
            f.write(content)
        successful.append((i, url))
        print(f"[{i:3d}/{len(URLS)}] OK  -> {filename}")
    except Exception as e:
        failed.append((i, url, str(e)))
        print(f"[{i:3d}/{len(URLS)}] FAIL: {url} — {e}")
    time.sleep(0.3)

with open(INDEX_FILE, "w", encoding="utf-8") as idx:
    for num, url in successful:
        idx.write(f"{url}\n")

print(f"\nDone! Downloaded {len(successful)} pages, {len(failed)} failed.")
print(f"Pages saved in: ./{OUTPUT_DIR}/")
print(f"Index saved in: ./{INDEX_FILE}")

if failed:
    print("\nFailed URLs:")
    for num, url, err in failed:
        print(f"  [{num:03d}] {url} — {err}")
