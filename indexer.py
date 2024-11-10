import os
import json
from bs4 import BeautifulSoup
from collections import defaultdict
from tokenizers.remo import *

# Tokens: all alphanumeric sequences in the dataset.
# Stop words: do not use stopping, i.e. use all words, even the frequently occurring ones.
# Stemming: use stemming for better textual matches. Suggestion: Porter stemming.
# Important words: Words in bold, in headings (h1, h2, h3), and in titles should be treated as more important than the other words.

def indexer():
    try:
        os.mkdir("directory.txt")
    except FileExistsError as e:
        print(e)
        return
    

def stem_tokens(self, tokens):
    return ""

def add_document(self, doc_id, text):
    return ""


def process_html(self, file_path):
    return ""


def build_index(self, html_dir):
    return ""





