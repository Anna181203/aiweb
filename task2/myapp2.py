from flask import Flask, request, render_template
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
import os
import subprocess

app = Flask(__name__)

# Directory for the Whoosh index
index_dir = "indexdir"

# Check if the index directory exists
if not os.path.exists(index_dir):
    print(f"Index directory '{index_dir}' not found. Running crwl.py to create it...")
    try:
        # Run crwl.py to create the index
        subprocess.run(["python", "crwl.py"], check=True)
        print("Crawling and indexing completed.")
    except subprocess.CalledProcessError as e:
        print(f"Error running crwl.py: {e}")
        exit(1)

# Open the Whoosh index
ix = open_dir(index_dir)

@app.route("/")
def home():
    """Render the search form."""
    return render_template('start.html')

@app.route("/search")
def search():
    """Handle the search query and display results."""
    query_string = request.args.get("q", "")
    results = []

    if query_string:
        # Query the Whoosh index
        with ix.searcher() as searcher:
            query = QueryParser("content", ix.schema).parse(query_string)
            whoosh_results = searcher.search(query)

            # Collect results
            for result in whoosh_results:
                results.append({
                    "title": result["title"],
                    "url": result["url"],
                    "snippet": result.highlights("content")
                })

    return render_template('results.html', query=query_string, results=results)

if __name__ == "__main__":
    app.run(debug=True)

import traceback
@app.errorhandler(500)
def internal_error(exception):
   return "<pre>"+traceback.format_exc()+"</pre>"