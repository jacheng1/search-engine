import os
import json
import zipfile
import string
import math

from bs4 import BeautifulSoup
from collections import defaultdict
from nltk.stem import PorterStemmer

from tokenizers.remo.PartA import tokenize, compute_word_frequencies

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

def indexer():
    create_directory()

    index_range = string.ascii_lowercase + string.digits + "!"
    partial_dict = {}

    for i in index_range:
        path = f"partial-index/{i}.txt"
        partial_file = open(path, "w+", encoding="UTF-8")
        partial_dict[i] = partial_file

    # Iterates through .json files
    index = defaultdict(lambda: defaultdict(lambda: [0, 0]))

    offload_dict = True
    stemmer = PorterStemmer()

    with open("doc_id.txt", "a", encoding="UTF-8") as lookup:
        
        with zipfile.ZipFile("developer.zip", "r") as zippedFile:
            files = zippedFile.namelist()
            doc_id = 0

            for file_name in files:
                ext = os.path.splitext(file_name)[-1]

                if ext == '.json':
                    with zippedFile.open(file_name) as json_file:

                        json_content = json_file.read()
                        json_dict = json.loads(json_content)

                        page_soup = BeautifulSoup(json_dict['content'], 'html.parser')

                        text = page_soup.find_all(['title', 'h1', 'h2', 'h3', 'b', 'strong'])
                        important_text_len = len(text)
                        
                        for chunk in text:
                            word_list = tokenize(chunk.get_text())
                            word_list = [stemmer.stem(word) for word in word_list]
                            word_freq = compute_word_frequencies(word_list)
                            for key in word_freq:
                                index[key][doc_id][1] += word_freq[key]


                        skipped_tags = ['title', 'h1', 'h2', 'h3', 'b', 'strong']
                        for tag in skipped_tags:
                            [s.extract() for s in page_soup(tag)]

                        text = page_soup.find_all()
                        text_len = len(text)

                        for chunk in text:
                            word_list = tokenize(chunk.get_text())
                            word_list = [stemmer.stem(word) for word in word_list]
                            word_freq = compute_word_frequencies(word_list)
                            for key in word_freq:
                                index[key][doc_id][0] += word_freq[key]

                        if text_len + important_text_len > 0:
                            doc_id += 1
                            lookup.write("{} {}\n".format(doc_id, json_dict['url']))

                        if offload_dict is True:
                            if doc_id > (NUM_OF_DOCS / 5) * 4:
                                index = offload(index, partial_dict)
                                offload_dict = False
                            elif doc_id > (NUM_OF_DOCS / 5) * 3:
                                index = offload(index, partial_dict)
                            elif doc_id > (NUM_OF_DOCS / 5) * 2:
                                index = offload(index, partial_dict)
                            elif doc_id > (NUM_OF_DOCS / 5):
                                index = offload(index, partial_dict)
                    
    offload(index, partial_dict)
    update_index(partial_dict, doc_id)

    for key in partial_dict.keys():
        partial_dict[key].close()

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
    
    with open("vocab.txt", "a", encoding="UTF-8") as vocab_file:

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
    indexer()


