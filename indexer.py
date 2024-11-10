import os
import json
from bs4 import BeautifulSoup
from collections import defaultdict
from nltk.stem import PorterStemmer
from tokenizers.remo.PartA import * # change to your desired tokenizer

# Tokens: all alphanumeric sequences in the dataset.
# Stop words: do not use stopping, i.e. use all words, even the frequently occurring ones.
# Stemming: use stemming for better textual matches. Suggestion: Porter stemming.
# Important words: Words in bold, in headings (h1, h2, h3), and in titles should be treated as more important than the other words.

ps = PorterStemmer()

inverted_index = defaultdict(list)


def build_index(html_dir):
    doc_id = 0

    


def indexer(html_dir):
    try:
        os.mkdirs("directory.txt", exists_ok=True)

    except FileExistsError as e:
        print(e)
        return


def tokenize_text(text):
    return tokenize(text)


def stem_tokens(tokens):
    return [ps.stem(token) for token in tokens]








