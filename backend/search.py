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
    tokens = word_tokenize(query)
    return [ps.stem(word, True) for word in tokens if word.isalnum()]


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
        for term_line in lookup:
            doc_id, url = term_line.strip().split(" ", 1)
            doc_url_map[int(doc_id)] = url

    # Load vocabulary
    with open("vocab.txt", "r", encoding="UTF-8") as vocab_file:
        for term_line in vocab_file:
            term, offset = term_line.strip().split(" ")
            vocab[term] = int(offset)

    # Load partial index
    for letter in os.listdir("partial-index"):
        with open(f"partial-index/{letter}", "r", encoding="UTF-8") as letter_file:
            for term_line in letter_file:
                postings = term_line.strip().split(" ")
                term = postings[0]

                for posting in postings[1:]:
                    if "/" in posting:
                        doc_id, tf_idf = map(float, posting.split("/"))
                        index[term][int(doc_id)] = tf_idf
                    elif "." in posting:
                        doc_id, reg_freq, imp_freq = map(float, posting.split("."))
                        tf = reg_freq + (imp_freq * 2)
                        df = len(postings) - 1
                        tf_idf = (1 + math.log10(tf)) * math.log10(num_docs / df)
                        index[term][int(doc_id)] = tf_idf
                    else:
                        print(f"Unexpected format: {posting}")

    return index, doc_url_map, vocab


def search_query(query, index, doc_url_map):
    """
    Process the search query and retrieve ranked documents.
    """

    query_terms = tokenize_query(query)
    document_scores = defaultdict(float)
    relevant_docs = set()

    for term in query_terms:
        if term in index:
            relevant_docs.update(index[term].keys())

    if not relevant_docs:
        return [], 0

    start_time = time.perf_counter()

    # Calculate the cumulative score for each document
    for term in query_terms:
        for doc_id in relevant_docs:
            if doc_id in index[term]:
                document_scores[doc_id] += index[term][doc_id]

    # Normalize scores by the number of query terms
    num_query_terms = len(query_terms)
    for doc_id in document_scores:
        document_scores[doc_id] /= num_query_terms

    # Rank documents by combined score
    ranked_docs = sorted(document_scores.items(), key=lambda x: x[1], reverse=True)

    end_time = time.perf_counter()
    response_time = (end_time - start_time) * 1000

    # Map doc_ids to URLs
    results = [(doc_url_map[doc_id], score) for doc_id, score in ranked_docs]

    return results, response_time


def main():
    # Load the index and vocab
    index, doc_url_map, vocab = load_index_and_vocab()

    # Prompt the user for a query
    while True:
        query = input("Search for a query (Type 'exit' to quit): ").strip()
        if query.lower() == "exit":
            break

        results, response_time = search_query(query, index, doc_url_map)

        # Search and display results
        if results:
            print("\nTop results:")
            
            for i, (url, score) in enumerate(results, start=1):
                print(f"{i}. {url} (Score: {score:.4f})")
        else:
            print("No results found for your query.\n")

        print(f"\nResponse time: {response_time:.2f} ms\n")


if __name__ == "__main__":
    main()
