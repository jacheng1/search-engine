import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from query import load_index_and_vocab, search_query

app = Flask(__name__)

# Load index, document URL map, vocab upon startup
index, doc_url_map, vocab = load_index_and_vocab()

def fetch_metadata(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string if soup.title else "No Title Available"
        description_meta = soup.find("meta", attrs={"name": "description"})
        description = description_meta["content"] if description_meta else "No Description Available"
        domain = requests.utils.urlparse(url).hostname

        return {
            "url": url,
            "domain": domain,
            "title": title,
            "description": description,
        }
    except Exception as e:
        return {
            "url": url,
            "domain": None,
            "title": "Error Fetching Title",
            "description": str(e),
        }

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    # Perform the query search
    results = search_query(query, index, doc_url_map)
    
    # Enrich results with metadata
    enriched_results = [fetch_metadata(url) for url in results]

    # Return results in JSON format
    return jsonify({"results": enriched_results})

if __name__ == '__main__':
    app.run(debug=True)