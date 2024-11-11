import os
import json
import zipfile
import string

from bs4 import BeautifulSoup
from collections import defaultdict
from nltk.stem import PorterStemmer
from tokenizers.remo.PartA import * # change to your desired tokenizer

# Tokens: all alphanumeric sequences in the dataset.
# Stop words: do not use stopping, i.e. use all words, even the frequently occurring ones.
# Stemming: use stemming for better textual matches. Suggestion: Porter stemming.
# Important words: Words in bold, in headings (h1, h2, h3), and in titles should be treated as more important than the other words.

NUM_OF_DOCS = 56000

# Init Porter Stemmer
ps = PorterStemmer()

# Define inverted index
inverted_index = defaultdict(list)

def setup_partial_index():
    os.makedirs("partial-index", exist_ok=True)
    index_files = {}



def tokenize_text(text):
    with open(text, "w") as f:
        f.write(text)
    return tokenize(text)

def stem_tokens(tokens):
    return [ps.stem(token) for token in tokens]

def process_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

        important_text = ""
        body_text = ""

        if 'html' in data:
            soup = BeautifulSoup(data['html'], 'html.parser')

            important_text += " ".join(tag.get_next() for tag in soup.find_all(['title', 'h1', 'h2', 'h3', 'b']))

            body_text += soup.get_text()


def build_index(docs):
    # Build inverted index from JSON files
    doc_id = 0

    # I <- HashTable() == inverted_index = defaultdict(list)

    for doc in os.listdir(docs):
        doc_id += 1
        
        # Parse document into tokens
        file_path = os.path.join(docs, doc)

        important_text, body_text = process_json(file_path)

        important_tokens = stem_tokens(tokenize_text(important_text))
        body_tokens = stem_tokens(tokenize_text(body_text))

        for token in important_tokens:
            inverted_index[token].append((doc_id, "important"))
        for token in body_tokens:
            inverted_index[token].append((doc_id, "body"))


            












