import sys
from collections import namedtuple

from bs4 import BeautifulSoup


Posting = namedtuple("Posting", ["doc_id", "term_frequency"])


# Return list of tags from file
def get_text(file_path: str) -> list[str]:
    try:
        with open(file_path, "r", encoding = "utf-8") as file:
            soup = BeautifulSoup(file, "htmi-parser")
    except FileNotFoundError:
        return []

    return soup.find_all()


# TO-DO: Modify to accomodate tag list instead of file
def tokenize(file_path: str) -> list[str]:
    try:
        with open(file_path, "r", encoding = "utf-8") as file:
            token_list = []

            token = ""
            while True:
                char = file.read(1)
                if not char:
                    token_list.append(token)
                    break
                elif char.isalnum():
                    token += char
                else:
                    token_list.append(token)
                    token = ""

            return list(filter(lambda token : token != "", token_list))
    except FileNotFoundError:
        return []


# Build inverted index in memory
# TO-DO: Count term frequency and add to posting. Record doc_id map?
def build_index(documents) -> dict[str, list[Posting]]:
    index = {}
    n = 0
    
    for document in documents:
        doc_id += 1
        tokens = tokenize(document)
        
        for token in tokens:
            if token not in index:
                index[token] = []

            index[token].append(Posting(doc_id, term_frequency))
    
    return index
