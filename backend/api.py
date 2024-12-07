import re
import time
import asyncio
import aiohttp

from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from tldextract import extract
from search import load_index_and_vocab, search_query

app = Flask(__name__)

# Load index, document URL map, vocab upon startup
index, doc_url_map, vocab = load_index_and_vocab()

ROOT_DOMAIN_MAPPING = {
    "uci.edu": "UC Irvine",
    "mit.edu": "MIT",
    "stanford.edu": "Stanford University",
}

async def fetch_metadata_async(url, session):
    try:
        async with session.get(url, ssl=False, timeout=5) as response:
            response.raise_for_status()
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")

            # Extract the title
            title = soup.title.string.strip() if soup.title else "No Title Available"

            # Extract the meta description
            description_meta = soup.find("meta", attrs={"name": "description"})
            description = description_meta["content"].strip() if description_meta else None

            # Fallback to richer content if there is no meta description, or contains irrelevant content
            if not description or re.match(r'^\s*\d{4}[-/]\d{1,2}[-/]\d{1,2}\s*$', description):
                paragraphs = soup.find_all("p", limit=3)
                description_candidates = [p.text.strip() for p in paragraphs if p.text.strip()]

                for candidate in description_candidates:
                    if not re.match(r'^\s*\d{4}[-/]\d{1,2}[-/]\d{1,2}\s*$', candidate):
                        description = candidate

                        break

                if not description:
                    description = "No Description Available"

            # Extract the root domain
            parsed_url = extract(url)
            root_domain = f"{parsed_url.domain}.{parsed_url.suffix}"
            organization_name = ROOT_DOMAIN_MAPPING.get(root_domain, root_domain)

            return {
                "url": url,
                "domain": organization_name,
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

async def enrich_results(search_results):
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_metadata_async(result[0], session)
            for result in search_results
        ]

        enriched_results = await asyncio.gather(*tasks)
        for enriched_result, score in zip(enriched_results, (r[1] for r in search_results)):
            enriched_result["score"] = score
            
        return enriched_results

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    # Perform the query search
    search_results, response_time = search_query(query, index, doc_url_map)

    # Enrich results with metadata (run asyncio loop)
    enriched_results = asyncio.run(enrich_results(search_results))

    return jsonify({
        "results": enriched_results,
        "response_time": round(response_time, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)