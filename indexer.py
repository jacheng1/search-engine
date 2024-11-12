import os
import json
import zipfile
import string
import math
import nltk

nltk.download('punkt_tab')

from bs4 import BeautifulSoup
from collections import defaultdict
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

from tokenizers.remo.PartA import tokenize, compute_word_frequencies

# Tokens: all alphanumeric sequences in the dataset.
# Stop words: do not use stopping, i.e. use all words, even the frequently occurring ones.
# Stemming: use stemming for better textual matches. Suggestion: Porter stemming.
# Important words: Words in bold, in headings (h1, h2, h3), and in titles should be treated as more important than the other words.

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
        word = ps.stem(word)

        if word.isalnum():
            alnum_list.append(word)
    
    return alnum_list

# Indexing and file parsing
class Indexer:
    def __init__(self, num_of_docs):
        self.num_of_docs = 56000
        self.index = defaultdict(lambda: defaultdict(lambda: [0, 0]))
        self.doc_id = 0
        self.partial_dict = self.create_partial_files()
    
    def create_partial_files(self):
        partial_dict = {}
        index_range = string.ascii_lowercase + string.digits + "!"
        for i in index_range:
            path = f"partial-index/{i}.txt"
            with open(path, "w", encoding="UTF-8") as partial_file:
                partial_dict[i] = partial_file
        
        return partial_dict

    def process_zip(self, zip_path):
        # Process zip file and build index
        with open("doc_id.txt", "a", encoding="UTF-8") as lookup:
            with zipfile.ZipFile(zip_path, "r") as zippedFile:
                files = zippedFile.namelist()
                for file_name in files:
                    try:
                        if file_name.endswith('.json'):
                            self.process_json_file(zippedFile, file_name, lookup)
                    except Exception as e:
                        print(f"Error processing file {file_name}: {e}")

    def process_json_file(self, zippedFile, file_name, lookup):
        # Process JSON file and update the index
        with zippedFile.open(file_name) as json_file:
            try:
                json_content = json_file.read()
                json_dict = json.loads(json_content)
                page_soup = BeautifulSoup(json_dict['content'], 'html.parser')

                # Extract important text
                important_text_len = self.process_important_text(page_soup)

                # Process rest of text
                self.process_normal_text(page_soup)

                if important_text_len > 0:
                    self.doc_id += 1
                    lookup.write(f"{self.doc_id} {json_dict['url']}\n")
                
                self.offload_data_if_needed()
            
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError in file {file_name}: Skipping file.")
            except KeyError as e:
                print(f"KeyError: Missing expected key in '{file_name}' - {e}: Skipping file.")

    def process_important_text(self, page_soup):
        # Process important text (headings, title, etc).
        text = page_soup.find_all(['title', 'h1', 'h2', 'h3', 'b', 'strong'])
        













def offload(my_dict, p_dict)->defaultdict:
    index_list = sorted(my_dict.items(), key=lambda x: (x[0]))

    for elem in index_list:
        partial_file = p_dict.get(elem[0][0], p_dict["!"])
        partial_file.write("{} ".format(elem[0]))

        for doc, count in elem[1].items():
            partial_file.write("{}.{}.{}".format(doc, count[0], count[1]))

        
        partial_file.write("\n")

    return defaultdict(lambda: defaultdict(lambda: [0, 0]))  # Optional reset if necessary
    

def update_index(files, doc_nums):
    
    with open("vocab.txt", "w", encoding="UTF-8") as vocab_file:

        for letter in sorted(files.keys()):
            partial_index = defaultdict(lambda: defaultdict())
            files[letter].seek(0)

            for line in files[letter]:
                split_line = line.split()

                for posting in split_line[1:]:
                    split_posting = posting.split(".")

                    tf = 1 + int(split_posting[1]) + (int(split_posting[2]) * 2)

                    df = len(split_line[1:])

                    tf_idf = (1 + math.log10(tf)) * math.log(doc_nums / df)
                    
                    partial_index[split_line[0]][int(split_posting[0])] = tf_idf
                
                files[letter].seek(0)
                files[letter].truncate(0)

                for key, value in sorted(partial_index.items(), key = lambda x: x[0]):

                    vocab_file.write("{} {}\n".format(key, files[letter].tell()))

                    files[letter].write(f"{key}")

                    for document, score in sorted(value.items(), key = lambda x: x[0]):
                        files[letter].write(f"{document}/{score}")
                    
                    files[letter].write("\n")

if __name__ == "__main__":
