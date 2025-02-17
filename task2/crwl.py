from bs4 import BeautifulSoup  # For parsing and extracting data from HTML
from whoosh.index import open_dir, create_in  # For managing the Whoosh index
from whoosh.fields import Schema, TEXT, ID  # For defining the schema of the index
import requests  # For sending HTTP requests
import os  # For interacting with the file system


class Crawler:
    def __init__(self, start_url, prefix, index_dir="indexdir"):
        """
        Initialize the Crawler.

        :param start_url: The URL to start crawling from.
        :param prefix: The URL prefix to ensure we stay within a specific domain.
        :param index_dir: Directory to store or access the Whoosh index.
        """
        self.start_url = start_url
        self.prefix = prefix
        self.agenda = [start_url]  # List of URLs to crawl, starting with the seed URL
        self.visited = set()  # Set to track already visited URLs

        # Define or open the Whoosh index
        schema = Schema(
            title=TEXT(stored=True),  # The title of the document, stored for retrieval
            content=TEXT(stored=True),  # The main content of the document, searchable and retrievable
            url=ID(stored=True, unique=True)  # The URL of the document, stored and unique
        )
        if not os.path.exists(index_dir):
            # Create the directory and initialize a new Whoosh index
            os.mkdir(index_dir)
            self.index = create_in(index_dir, schema)
        else:
            # Open an existing Whoosh index
            self.index = open_dir(index_dir)

    def add_to_index(self, title, content, url):
        """
        Add a document to the Whoosh index.

        :param title: The title of the page.
        :param content: The main text content of the page.
        :param url: The URL of the page.
        """
        writer = self.index.writer()  # Open a writer to the index
        writer.add_document(title=title, content=content, url=url)  # Add the document
        writer.commit()  # Commit changes to the index
        print(f"Indexed: {title} ({url})")  # Debug message to confirm indexing

    def crawl(self):
        """
        Crawl the web starting from the seed URL.
        """
        while self.agenda:
            # Get the next URL to crawl
            url = self.agenda.pop(0)

            # Skip if the URL has already been visited
            if url in self.visited:
                continue

            print(f"Crawling: {url}")  # Debug message to indicate current URL being crawled

            try:
                # Fetch the content of the URL
                response = requests.get(url, timeout=5)

                # Skip non-HTML content
                if 'text/html' not in response.headers.get('Content-Type', ''):
                    continue

                # Parse the HTML content using BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                self.visited.add(url)  # Mark the URL as visited

                # Extract the title and text content
                title = soup.title.string if soup.title else "No Title"  # Use "No Title" if title is missing
                content = soup.get_text()  # Get all text content from the page

                # Add the extracted data to the index
                self.add_to_index(title, content, url)

                # Find all links on the page
                for link in soup.find_all('a', href=True):
                    absolute_url = self.prefix + link['href']  # Resolve relative links
                    # Add the link to the agenda if it's within the same domain and not visited
                    if absolute_url.startswith(self.prefix) and absolute_url not in self.visited:
                        self.agenda.append(absolute_url)

            except Exception as e:
                print(f"Failed to crawl {url}: {e}")  # Debug message for errors


if __name__ == "__main__":
    # Define the starting URL and the domain prefix
    start_url = "https://vm009.rz.uos.de/crawl/index.html"
    prefix = "https://vm009.rz.uos.de/crawl/"

    # Initialize and start the crawler
    crawler = Crawler(start_url, prefix)
    crawler.crawl()
    print("Crawling and indexing completed!")  # Final message after crawling is done
