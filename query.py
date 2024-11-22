class Query:
    def __init__(self, vocab_path, partial_index_dir, doc_id_path):
        self.vocab = self.load_vocab(vocab_path)
        self.partial_index_dir = partial_index_dir
        self.doc_lookup = self.load_doc_lookup(doc_id_path)

    # vocab.txt
    def load_vocab(self, vocab_path):
        with open(vocab_path, "r", encoding="UTF-8") as file:
            vocab = {}
            for line in file:
                term, position = line.strip().split()
                vocab[term] = int(position)
        return vocab

    # doc_id.txt
    def load_doc_lookup(self, doc_id_path):
        doc_lookup = {}
        with open(doc_id_path, "r", encoding="UTF-8") as file:
            for line in file:
                doc_id, url = line.strip().split(maxsplit=1)
                doc_lookup[int(doc_id)] = url
        return doc_lookup
    


    
if __name__ == "__main__":
    search = Query("vocab.txt", "partial-index", "doc_id.txt")
    queries = ["cristina lopes", "machine learning", "ACM", "master of software engineering"]
    