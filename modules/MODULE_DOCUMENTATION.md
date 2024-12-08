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
a robust and flexible method for retrieving web search results.

**Key Features:**
- Dynamically creates search result storage directories
- Utilizes Brave Search API for web searches
- Configurable number of search results
- Saves search results to a JSON file for further processing
- Extracts and returns URLs from the search results

**Parameters:**
- `query` (str): The search query to be executed
- `key` (str): A unique identifier for organizing search results
- `num_searches` (int, optional): Number of search results to retrieve (default is 5)

**Returns:**
- List or None: A list of dictionaries containing URLs and titles from search results
- Returns None if an error occurs during the search process

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
- `model` (str, optional): AI model version to use (default: "gemini-1.5-flash-002")

**Example Usage:**
```python
gemini_smart_summary('Python programming', urls, 'python_search', '/output/dir')
# Generates AI-powered summaries for the given URLs
```

### `smart_search(query, key, urls, model="gemini-1.5-flash-002")`

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
- `urls` (list, optional): Pre-existing list of URLs to process
- `model` (str, optional): AI model version for summarization (default: "gemini-1.5-flash-002")

**Example Usage:**
```python
smart_search('Machine Learning trends', 'ml_search')
# Performs a complete intelligent search and summarization process
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

**Generated on:** 2024-12-08
**Documentation Version:** 1.0
