import os
import json
import string
import math
import nltk

nltk.download('punkt_tab')

from bs4 import BeautifulSoup
from collections import defaultdict
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# Tokens: all alphanumeric sequences in the dataset.
# Stop words: do not use stopping, i.e. use all words, even the frequently occurring ones.
# Stemming: use stemming for better textual matches. Suggestion: Porter stemming.
# Important words: Words in bold, in headings (h1, h2, h3), and in titles should be treated as more important than the other words.

NUM_OF_DOCS = 56000


def create_directory():
    try:
        os.makedirs("partial-index", exist_ok=True) 

        print("Directory 'partial-index' is ready.")

    except FileExistsError as e:
        print(f"Error creating directory: {e}")


def tokenize_text(text:str)->list:
    ps = PorterStemmer()

    alnum_list = []
    word_list = word_tokenize(text)

    for word in word_list:
        word = ps.stem(word, True)
        if word.isalnum():
            alnum_list.append(word)
    
    return alnum_list


# Indexing and file parsing
class Indexer:
    def __init__(self, num_of_docs):
        self.num_of_docs = num_of_docs
        self.index = defaultdict(lambda: defaultdict(lambda: [0, 0]))
        self.doc_id = 0
        self.partial_dict = self.create_partial_files()
    
    
    def create_partial_files(self):
        """
        Creates and keeps open all partial index files.
        """

        partial_dict = {}
        index_range = string.ascii_lowercase + string.digits + "!" # ! for non english symbols
        for i in index_range:
            path = f"partial-index/{i}.txt"
            partial_dict[i] = open(path, "a", encoding="UTF-8")

        return partial_dict


    def close_partial_files(self):
        """"
        Closes all partial index files
        """

        for file in self.partial_dict.values():
            file.close()


    def process_json(self, path, lookup):
        """
        Process JSON file and update the index
        """

        with open(path) as json_file:
            try:
                json_content = json_file.read()
                json_dict = json.loads(json_content)
                page_soup = BeautifulSoup(json_dict['content'], 'html.parser')

                # Extract important text
                important_text_len = self.process_important_text(page_soup)

                # Process rest of text
                self.process_normal_text(page_soup)

                # Add to doc_ids
                self.doc_id += 1
                lookup.write(f"{self.doc_id} {json_dict['url']}\n")

                self.offload_data_if_needed()

            except json.JSONDecodeError as e:
                print(f"JSONDecodeError in file {path}: Skipping file.")
            except KeyError as e:
                print(f"KeyError: Missing expected key in '{path}' - {e}: Skipping file.")


    def process_directory(self, directory):
        """
        Process process_directory and build index
        """

        with open("doc_id.txt", "a", encoding="UTF-8") as lookup:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    path = os.path.join(root, file)
                    try:
                        if path.endswith('.json'):
                            self.process_json(path, lookup)
                    except Exception as e:
                        print(f"Error processing file {path}: {e}")


    def process_important_text(self, page_soup):
        """
        Process important text (headings, title, etc).
        Frequencies are saved in the second position in index entry
        """

        text = page_soup.find_all(['title', 'h1', 'h2', 'h3', 'b', 'strong'])
        important_text_len = len(text)

        for word_chunk in text:
            word_list = tokenize_text(word_chunk.get_text())

            word_freq = self.compute_word_frequencies(word_list)
            for key in word_freq:
                self.index[key][self.doc_id][1] += word_freq[key]
        
        return important_text_len


    def process_normal_text(self, page_soup):
        """
        Process rest of text
        Frequencies are saved in the first position in index entry
        """

        skipped_tags = ['title', 'h1', 'h2', 'h3', 'b', 'strong']
        for tag in skipped_tags:
            [s.extract() for s in page_soup(tag)]
        
        text = page_soup.find_all()
        for word_chunk in text:
            word_list = tokenize_text(word_chunk.get_text())

            word_freq = self.compute_word_frequencies(word_list)
            for key in word_freq:
                self.index[key][self.doc_id][0] += word_freq[key]


    def compute_word_frequencies(self, token_list: list[str]) -> dict[str, int]:
        """
        Count the number of occurrences of each token in the token list.
        """

        token_dict = {}
        for token in token_list:
            if token in token_dict:
                token_dict[token] += 1
            else:
                token_dict[token] = 1

        return token_dict


    def offload_data_if_needed(self):
        """
        Offload data to partial index 
        Checks if doc_id exceeds any threshold and triggers offload to save current index to partial index files 
        """

        offload_thresholds = [
            (self.num_of_docs // 5),
            (self.num_of_docs // 5) * 2,
            (self.num_of_docs // 5) * 3,
            (self.num_of_docs // 5) * 4
        ]

        for threshold in offload_thresholds:
            if self.doc_id == threshold:
                self.index = offload(self.index, self.partial_dict)
                break

    # End of class


def offload(index, partial_dict) -> defaultdict:
    """
    Offload data into partial index file
    Writes current in-memory index to appropriate partial index file in p_dict
    """

    index_list = sorted(index.items(), key=lambda x: (x[0]))

    for elem in index_list:
        partial_file = partial_dict.get(elem[0][0], partial_dict["!"])
        partial_file.write(f"{elem[0]} ")

        for doc, count in elem[1].items():
            partial_file.write(f"{doc}.{count[0]}.{count[1]}")

        partial_file.write("\n")

    return defaultdict(lambda: defaultdict(lambda: [0, 0]))  # Resets the index


def update_index(files, doc_nums):
    """
    Updates the vocabulary and final index
    Uses tf-idf for each term-document pair
    Final index data back to partial index files and records vocabulary in vocab.txt
    """

    with open("vocab.txt", "a", encoding="UTF-8") as vocab:
        # Format: "term doc_id/tf_idf"
        for letter in sorted(files.keys()): # iterate over each partial index file

            with open(f"partial-index/{letter}.txt", "r+", encoding="UTF-8") as letter_file:
                partial_index = defaultdict(lambda: defaultdict())

                letter_file.seek(0)
                term_lines = letter_file.readlines()

                # For each term:
                for term_line in term_lines:
                    postings = term_line.split()
                    term = postings[0]

                    # For each doc:
                    for posting in postings[1:]:
                        split_posting = posting.split(".")
                        doc_id = split_posting[0]
                        reg_freq = split_posting[1]
                        imp_freq = split_posting[2]

                        # Calculate tf_idf
                        tf = int(reg_freq) + (int(imp_freq) * 2)
                        df = len(postings[1:])
                        tf_idf = (1 + math.log10(tf)) * math.log10(doc_nums / df)
                        
                        # Update tf_idf in partial index
                        partial_index[term][int(doc_id)] = tf_idf

                # Clear letter file
                letter_file.seek(0)
                letter_file.truncate(0)

                # Write term offsets to vocab
                for key, value in sorted(partial_index.items(), key = lambda x: x[0]):
                    try:
                        vocab.write(f"{key} {letter_file.tell()}\n")
                    except Exception as e:
                        print(f"Error writing to vocab file: {e}")

                    # Write term postings to partial index file
                    letter_file.write(f"{key}")
                    for document, score in sorted(value.items(), key = lambda x: x[0]):
                        letter_file.write(f" {document}/{score}")
                    letter_file.write("\n")


if __name__ == "__main__":
    create_directory()
    indexer = Indexer(NUM_OF_DOCS)
    indexer.process_directory("./developer")

    # Offload and update the final index after all files are processed
    offload(indexer.index, indexer.partial_dict)
    update_index(indexer.partial_dict, indexer.doc_id)

    indexer.close_partial_files()
