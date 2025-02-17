# **Search Engine Project**
## Overview

This project implements a functional search engine with the following components:

**Crawler**: A script (crwl.py) to crawl a specified website and extract HTML content for indexing.
**Indexing**: Uses the Whoosh library to create and manage an inverted index of the website's content.
**Search Functionality**: A script (search.py) to handle user queries and retrieve relevant results.
**Web Frontend**: A Flask-based application (myapp2.py) to provide a user interface for searching and viewing results.

---

## Features

- Crawler:
    - Extracts content from HTML pages starting from a given URL.
    - Indexes titles, content, and URLs into a Whoosh index.
- Web Search Application:
  - Provides a search form for user queries.
  - Displays results with titles, URLs, and highlighted snippets.

---

## Setup and installation
### Prerequisites

Ensure the following tools and libraries are installed:

- Python 3.8+
- pip (Python package manager)

### Installation Steps

**Clone the Repository:**

    git clone <repository_url>
    cd task2/week2

**Set Up a Virtual Environment:**

    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

**Install Dependencies:**

    pip install -r requirements.txt

**Run the Crawler**: Update the "start_url" and "prefix" in "crwl.py", then execute:

    python crwl.py

This will crawl the website and store the index in the indexdir directory.

**Run the Web Application**: Start the Flask app by running:

    python myapp2.py

**Access the Application**: Open your web browser and go to:

    http://127.0.0.1:5000

---

## Project structure
````
task2/
└── week2/
    ├── indexdir/             # Directory to store Whoosh index
    ├── templates/            # HTML templates for the web app
    │   └── results.html      # Search results template
    ├── crwl.py               # Web crawler and indexing script
    ├── myapp2.py             # Flask app for search functionality
    ├── search.py             # Search query handler
    ├── wooshdemo.py          # Demo script for testing Whoosh
    ├── requirements.txt      # Python dependencies
````

--- 

## Usage
### Crawling and Indexing

- Update start_url and prefix in crwl.py to specify the website to crawl.
- Run crwl.py to crawl the website and index its content.

### Searching

1. Start the Flask app by running myapp2.py.
2. Enter a search query in the form on the web interface.
3. Results will display:
   - Page titles (as clickable links)
   - URLs
   - Snippets showing the queried keywords in context. 