from flask import Flask, request, jsonify
from query import load_index_and_vocab, search_query

app = Flask(__name__)

# Load index, document URL map, vocab upon startup
index, doc_url_map, vocab = load_index_and_vocab()

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    # Perform the query search
    results = search_query(query, index, doc_url_map)
    
    # Return results in JSON format
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True)