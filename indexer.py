import os
import json
from bs4 import BeautifulSoup
from collections import defaultdict

# Tokens: all alphanumeric sequences in the dataset.
# Stop words: do not use stopping, i.e. use all words, even the frequently occurring ones.
# Stemming: use stemming for better textual matches. Suggestion: Porter stemming.
# Important words: Words in bold, in headings (h1, h2, h3), and in titles should be treated as more important than the other words.

class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(list)
        self.doc_id = 0
    
    def tokenize(self, text):


    def stem_tokens(self, tokens):

    def add_document(self, doc_id, text):


    def process_html(self, file_path):

    
    def build_index(self, html_dir):

    

    
