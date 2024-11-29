import math
import time
import os

from collections import defaultdict
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

def tokenize_query(query):
    """
    Tokenizes and stems the query terms.
    """
    ps = PorterStemmer()
    tokens = word_tokenize(query.lower())

    return [ps.stem(word) for word in tokens if word.isalnum()]

def count_documents(doc_id_file):
    """
    Counts the total number of documents listed in the doc_id.txt file.
    """
    try:
        with open(doc_id_file, "r", encoding="UTF-8") as file:
            total_docs = sum(1 for _ in file)

        return total_docs
    except FileNotFoundError:
        print(f"Error: {doc_id_file} not found.")

        return 0

def load_index_and_vocab():
    """
    Loads the partial index and vocabulary into memory.
    """
    index = defaultdict(lambda: defaultdict(float))
    doc_url_map = {}
    vocab = {}

    # Count number of documents in doc_id.txt
    num_docs = count_documents("doc_id.txt")

    # Load doc_id to URL mapping
    with open("doc_id.txt", "r", encoding="UTF-8") as lookup:
        for line in lookup:
            doc_id, url = line.strip().split(" ", 1)

            doc_url_map[int(doc_id)] = url

    # Load vocabulary
    with open("vocab.txt", "r", encoding="UTF-8") as vocab_file:
        for line in vocab_file:
            term, offset = line.strip().split(" ")

            vocab[term] = int(offset)

    # Load partial index
    for file_name in os.listdir("partial-index"):
        with open(f"partial-index/{file_name}", "r", encoding="UTF-8") as file:
            for line in file:
                parts = line.strip().split(" ")
                term = parts[0]

                for doc_data in parts[1:]:
                    # Parse format `doc_id.freq1.freq2` for each line in partial-index/ .txt files
                    doc_id, freq1, freq2 = map(float, doc_data.split("."))

                    # Compute term/document frequencies
                    tf = 1 + freq1 + (freq2 * 2)
                    df = len(parts) - 1

                    tf_idf = (1 + math.log10(tf)) * math.log10(num_docs / df)

                    # Update the index
                    index[term][int(doc_id)] = tf_idf

    return index, doc_url_map, vocab

def search_query(query, index, doc_url_map):
    """
    Process the search query and retrieve ranked documents.
    """
    query_terms = tokenize_query(query)

    document_scores = defaultdict(float)

    # Retrieve documents containing all query terms
    relevant_docs = None
    for term in query_terms:
        if term in index:
            term_docs = set(index[term].keys())

            if relevant_docs is None:
                relevant_docs = term_docs
            else:
                relevant_docs &= term_docs
        else:
            # No match; contains no result
            relevant_docs = set()

    if not relevant_docs:
        return []

    # Calculate the cumulative score for each document
    for term in query_terms:
        for doc_id in relevant_docs:
            if doc_id in index[term]:
                document_scores[doc_id] += index[term][doc_id]

    # Rank documents by score
    ranked_docs = sorted(document_scores.items(), key=lambda x: x[1], reverse=True)

    # Map doc_ids to URLs and return
    return [(doc_url_map[doc_id], score) for doc_id, score in ranked_docs]

def main():
    # Load the index and vocab
    index, doc_url_map, vocab = load_index_and_vocab()

    # Prompt the user for a query
    while True:
        query = input("Search for a query (Type 'exit' to quit): ").strip()
        if query.lower() == "exit":
            break

        start_time = time.perf_counter()
        results = search_query(query, index, doc_url_map)
        end_time = time.perf_counter()
        response_time = (end_time - start_time) * 1000

        # Search and display results
        results = search_query(query, index, doc_url_map)
        if results:
            result_num = 1

            print("\nTop results:")
            for url, score in results:
                print(f"{result_num}. {url} (Score: {score:.4f})")

                result_num += 1
        else:
            print("No results found for your query.\n")

        print(f"\nResponse time: {response_time:.2f} ms\n")

if __name__ == "__main__":
    main()