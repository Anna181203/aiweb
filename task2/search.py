from whoosh.index import open_dir
from whoosh.qparser import QueryParser

def search_index(query_string, index_dir="indexdir"):
    """Search the Whoosh index for a given query string."""
    # Open the index directory
    ix = open_dir(index_dir)

    # Open a searcher
    with ix.searcher() as searcher:
        # Parse the query string
        query = QueryParser("content", ix.schema).parse(query_string)

        # Execute the search
        results = searcher.search(query)

        # Display the results
        print(f"Results for query '{query_string}':")
        for result in results:
            print(f"Title: {result['title']}")
            print(f"URL: {result['url']}")
            print(f"Snippet: {result.highlights('content')}")
            print("-" * 40)

# Example usage
if __name__ == "__main__":
    query = input("Enter your search query: ")
    search_index(query)

        