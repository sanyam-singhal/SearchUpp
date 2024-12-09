# Searchupp Modules Documentation

## Search Modules (`search_modules.py`)

### `extract_urls_from_json(file_path)`

URL Extraction Function

This function is designed to parse and extract URLs from a JSON file containing search results. 
It provides a robust method for retrieving web URLs along with their corresponding titles.

**Key Features:**
- Handles JSON file reading with UTF-8 encoding
- Extracts URLs from nested 'web' and 'results' dictionary structure
- Supports error handling and logging
- Returns a list of dictionaries with 'title' and 'url' keys

**Parameters:**
- `file_path` (str): The absolute or relative path to the JSON file containing search results

**Returns:**
- List or None: A list of dictionaries containing extracted URLs and titles
- Returns None if an error occurs during extraction

**Example Usage:**
```python
urls = extract_urls_from_json('search_results.json')
# Might return: [{'title': 'Example Page', 'url': 'https://example.com'}]
```

### `web_search(query, key, num_searches=5)`

Web Search Function using Brave Search API

This function conducts a web search by leveraging the Brave Search API, providing 
a robust and flexible method for retrieving web search results. It also reranks the results
based on their relevance to the provided query.

**Key Features:**
- Dynamically creates search result storage directories
- Utilizes Brave Search API for web searches
- Configurable number of search results
- Saves search results to a JSON file for further processing
- Extracts, reranks, and returns URLs from the search results

**Parameters:**
- `query` (str): The search query to be executed.
- `key` (str): A unique identifier for organizing search results.
- `num_searches` (int, optional): Number of search results to retrieve after reranking (default is 5).

**Returns:**
- List or None: A list of dictionaries containing URLs and titles from search results,
Returns None if an error occurs during the search process.

**Example Usage:**
```python
results = web_search('Python programming', 'python_search')
# Might return: [{'title': 'Python Tutorial', 'url': 'https://example.com/python'}]
```

### `scrape_page(driver, url, key_dir)`

Web Page Scraping Function using Selenium WebDriver

This function performs an in-depth web page scraping process, extracting structured 
content from a given URL using Selenium and BeautifulSoup.

**Key Features:**
- Utilizes Selenium WebDriver for dynamic web page interaction
- Employs BeautifulSoup for HTML parsing and content extraction
- Creates organized markdown files for scraped content
- Handles various HTML elements with structured extraction
- Supports error handling and logging

**Parameters:**
- `driver` (selenium.webdriver): An active Selenium WebDriver instance for browser automation
- `url` (str): The complete URL of the webpage to be scraped
- `key_dir` (str): Directory path for storing scraped content

**Example Usage:**
```python
scrape_page(selenium_driver, 'https://example.com', '/path/to/output')
# Creates a markdown file with structured page content
```

### `scrape_url(url, chrome_options, key_dir)`

URL Scraping Wrapper Function with Selenium WebDriver

This function serves as a convenient wrapper for web page scraping, 
managing the lifecycle of a Selenium WebDriver for a single URL.

**Key Features:**
- Initializes a new Chrome WebDriver instance
- Calls the main scraping function for a specific URL
- Ensures proper WebDriver resource management
- Provides a clean, abstracted interface for URL scraping

**Parameters:**
- `url` (str): The complete URL to be scraped
- `chrome_options` (selenium.webdriver.chrome.options.Options): Pre-configured Chrome WebDriver options
- `key_dir` (str): Directory path for storing scraped content

**Example Usage:**
```python
scrape_url('https://example.com', chrome_options, '/output/directory')
# Scrapes the URL and saves content in the specified directory
```

### `orchestrate_scraping(urls, key, key_dir)`

Web Scraping Orchestration Function

This function manages the parallel scraping of multiple URLs using 
ThreadPoolExecutor and Selenium WebDriver, providing an efficient 
and scalable web content extraction mechanism.

**Key Features:**
- Utilizes concurrent threading for parallel URL scraping
- Configures Selenium WebDriver with randomized user agents
- Manages multiple browser instances safely
- Supports flexible scraping of multiple web pages

**Parameters:**
- `urls` (list): A list of URLs to be scraped
- `key` (str): A unique identifier for the scraping session
- `key_dir` (str): Directory path for storing scraped content

**Example Usage:**
```python
orchestrate_scraping(['https://example1.com', 'https://example2.com'], 'search_key', '/output/dir')
# Scrapes multiple URLs concurrently and saves content
```

### `rerank_urls(query, urls, num_searches=5)`

Reranks a list of URLs based on their relevance to a given query.

This function takes a list of URLs and a search query, analyzing the content of each URL 
to determine its relevance to the query. It employs a scoring mechanism using the Google embedding model 
and the Euclidean norm to rank the URLs, returning the top results based on the specified number of searches.

**Key Features:**
- Analyzes the content of each URL to evaluate relevance
- Utilizes the Google embedding model for scoring based on embedding similarity
- Uses the Euclidean norm as the scoring mechanism
- Returns a list of the top-ranked URLs based on relevance

**Parameters:**
- `query` (str): The search query used to evaluate URL relevance.
- `urls` (list): A list of URLs to be reranked, where each URL is represented as a dictionary with a 'title' key.
- `num_searches` (int, optional): The number of top-ranked URLs to return (default is 5).

**Returns:**
- List: A list of the top-ranked URLs based on relevance to the query.

**Example Usage:**
```python
ranked_urls = rerank_urls('Python programming', urls)
# Might return the top 5 URLs relevant to 'Python programming'
```

### `smart_search(query, key, urls, model)`

Smart Search Orchestration Function

This function provides an end-to-end intelligent search solution, 
integrating web search, content scraping, and AI-powered summarization 
to deliver comprehensive and contextualized search results.

**Key Features:**
- Combines multiple search and content extraction techniques
- Leverages web search, web scraping, and AI summarization
- Provides a unified interface for complex search operations
- Supports flexible configuration and model selection

**Parameters:**
- `query` (str): The search query to be processed
- `key` (str): A unique identifier for the search session
- `urls` (list, optional): Pre-existing list of URLs to process (if not provided by web search)
- `model` (str, optional): AI model version for summarization

**Search Workflow:**
1. Perform web search if no URLs are provided
2. Create search result storage directory
3. Orchestrate web page scraping
4. Generate AI-powered summaries
5. Organize and store search results

**Flexibility and Extensibility:**
- Supports manual URL list or automatic web search
- Configurable AI model selection
- Modular design allows easy integration of new search techniques

**Error Handling and Resilience:**
- Gracefully handles failures in individual search stages
- Provides comprehensive logging
- Ensures partial results are preserved even if some steps fail

**Performance Considerations:**
- Uses concurrent processing for web scraping
- Manages system resources efficiently
- Implements rate limiting and error recovery mechanisms

**Example Usage:**
```python
smart_search('Machine Learning trends', 'ml_search')
# Performs a complete intelligent search and summarization process
```

## AI Modules (`ai_modules.py`)

### `ollama_model(query, urls, key, key_dir, model="llama3.2:1b")`

Generates a summary based on the user's query and scraped web content using the Ollama package.

The Ollama package provides an interface to interact with open-source models, allowing for 
the generation of summaries based on the content extracted from the specified URLs. This function 
reads the content from markdown files corresponding to the provided URLs, aggregates the content, 
and generates a summary using the specified Ollama model. It handles potential errors in reading files 
and generating summaries, providing feedback when issues arise.

**Key Features:**
- Reads and aggregates content from multiple markdown files
- Utilizes the specified Ollama model for generating summaries
- Handles errors gracefully, providing informative messages

**Parameters:**
- `query` (str): The user's search query that drives the summarization process.
- `urls` (list): A list of URLs from which to read the scraped content.
- `key` (str): A unique identifier for organizing the scraped content.
- `key_dir` (str): Directory path where the scraped markdown files are stored.
- `model` (str, optional): The Ollama model to be used for generating the summary (default is "llama3.2:1b").

**Returns:**
- `str`: The generated summary based on the user's query and the scraped content,
  or an error message if the summary could not be generated.

**Example Usage:**
```python
summary = ollama_model('What are the benefits of Python?', urls, 'python_search', '/path/to/output')
# Generates a summary based on the scraped content related to Python benefits.
```

### `gemini_smart_summary(query, urls, key, key_dir, model="gemini-1.5-flash-002")`

Content Summarization Function using Google Gemini AI

This function leverages Google's Gemini AI to generate intelligent, 
comprehensive summaries from web page contents, providing a sophisticated 
natural language processing solution for content analysis.

**Key Features:**
- Utilizes Google's Generative AI (Gemini) for advanced text summarization
- Reads markdown files generated from web scraping
- Generates structured, context-aware summaries
- Supports multiple AI model versions
- Saves generated summaries to markdown files

**Parameters:**
- `query` (str): The original search query driving the summarization
- `urls` (list): List of URLs that were scraped
- `key` (str): Unique identifier for the search session
- `key_dir` (str): Directory containing scraped content
- `model` (str, optional): Gemini AI model version to use (default: "gemini-1.5-flash-002")

**Summarization Workflow:**
1. Locate and read markdown files from scraped URLs
2. Prepare comprehensive input for Gemini AI
3. Generate summary using predefined extraction instructions
4. Save summary to a markdown file in the key directory

**AI Model Configuration:**
- Supports flexible model selection
- Uses predefined extraction instructions for consistent output
- Handles potential API rate limits and errors

**File Management:**
- Reads markdown files from URL-specific directories
- Generates summary files with descriptive naming
- Ensures organized storage of generated summaries

**Error Handling:**
- Gracefully handles file reading and AI generation errors
- Provides logging and error tracking
- Continues processing even if individual URL summarization fails

**Example Usage:**
```python
gemini_smart_summary('Python programming', urls, 'python_search', '/output/dir')
# Generates AI-powered summaries for the given URLs
```

## Theme Modification Module (`modify_theme.py`)

### `modify_theme(base, primaryColor, backgroundColor, secondaryBackgroundColor, textColor, font)`

Streamlit Theme Customization Function

This function dynamically modifies the Streamlit configuration file (.streamlit/config.toml)
to customize the application's visual theme, providing a flexible and programmatic 
approach to UI personalization.

**Parameters:**
- `base` (str): The base theme to use as a starting point (e.g., 'light' or 'dark')
- `primaryColor` (str): The primary accent color for interactive elements
- `backgroundColor` (str): The main background color of the application
- `secondaryBackgroundColor` (str): The background color for secondary elements
- `textColor` (str): The primary text color used throughout the application
- `font` (str): The font family to be used for text rendering

**Key Features:**
- Supports dynamic, programmatic theme modification
- Provides granular control over UI color scheme
- Maintains Streamlit's configuration file structure
- Allows easy theme switching and personalization

**Example Usage:**
```python
modify_theme(
    base='light', 
    primaryColor='#FF5733', 
    backgroundColor='#FFFFFF', 
    secondaryBackgroundColor='#F0F0F0', 
    textColor='#000000', 
    font='Arial'
)
# Customizes Streamlit app theme with specified parameters
```

---

**Generated on:** 2024-12-09
**Documentation Version:** 1.1
