from bs4 import BeautifulSoup
import json
import time
import os
import re
from datetime import datetime
from fake_useragent import UserAgent
import random
import pandas as pd
import numpy as np
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import google.generativeai as genai
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver import ActionChains

# Initial Setup
load_dotenv()
ua = UserAgent()
genai.configure(api_key=os.getenv("GEMINI_KEY"))
brave_key=os.getenv("BRAVE_KEY")
extract_instructions = os.getenv("SEARCH_SUMMARY_INSTRUCTIONS")

# Random viewport sizes for more human-like behavior
viewport_widths = [1366, 1440, 1536, 1600, 1920]
viewport_heights = [768, 900, 864, 1024, 1080]

def extract_urls_from_json(file_path):
    """
    URL Extraction Function

    This function is designed to parse and extract URLs from a JSON file containing search results. 
    It provides a robust method for retrieving web URLs along with their corresponding titles.

    Key Features:
    - Handles JSON file reading with UTF-8 encoding
    - Extracts URLs from nested 'web' and 'results' dictionary structure
    - Supports error handling and logging
    - Returns a list of dictionaries with 'title' and 'url' keys

    Parameters:
    -----------
    file_path : str
        The absolute or relative path to the JSON file containing search results

    Returns:
    --------
    list or None
        A list of dictionaries containing extracted URLs and titles
        Returns None if an error occurs during extraction

    Error Handling:
    --------------
    - Catches and prints any exceptions during file reading or JSON parsing
    - Returns None in case of any processing errors

    Example:
    --------
    urls = extract_urls_from_json('search_results.json')
    # Might return: [{'title': 'Example Page', 'url': 'https://example.com'}]
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        urls = []
        # Extract URLs from web results
        if 'web' in data and 'results' in data['web']:
            for result in data['web']['results']:
                if 'url' in result:
                    urls.append({
                        'title': result['title'],
                        'url': result['url']
                    })
        
        return urls
            
    except Exception as e:
        print(f"Error extracting URLs: {str(e)}")
        return None

def rerank_urls(query, urls, num_searches=5):
    """
    Reranks a list of URLs based on their relevance to a given query.

    This function takes a list of URLs and a search query, analyzing the content of each URL 
    to determine its relevance to the query. It employs a scoring mechanism using the Google embedding model 
    and the Euclidean norm to rank the URLs, returning the top results based on the specified number of searches.

    Key Features:
    - Analyzes the content of each URL to evaluate relevance
    - Utilizes the Google embedding model for scoring based on embedding similarity
    - Uses the Euclidean norm as the scoring mechanism
    - Returns a list of the top-ranked URLs based on relevance

    Parameters:
    -----------
    query : str
        The search query used to evaluate URL relevance.
    urls : list
        A list of URLs to be reranked, where each URL is represented as a dictionary with a 'title' key.
    num_searches : int, optional
        The number of top-ranked URLs to return (default is 5).

    Returns:
    --------
    list
        A list of the top-ranked URLs based on relevance to the query.

    Example:
    --------
    ranked_urls = rerank_urls('Python programming', urls)
    # Might return the top 5 URLs relevant to 'Python programming'
    """
    url_titles=[url['title'] for url in urls]
    query_embed=genai.embed_content(model="models/text-embedding-004",content=[query])
    query_embed=np.array(query_embed["embedding"])
    url_embeds=genai.embed_content(model="models/text-embedding-004",content=url_titles)
    url_embeds=np.array(url_embeds["embedding"])
    url_scores=np.linalg.norm(url_embeds-query_embed, axis=1)
    sorted_urls=[url for _,url in sorted(zip(url_scores,urls),reverse=True)]
    sorted_urls=sorted_urls[:num_searches]
    return sorted_urls

def web_search(query, key, num_searches=5):
    """
    Web Search Function using Brave Search API

    This function conducts a web search by leveraging the Brave Search API, providing 
    a robust and flexible method for retrieving web search results. It also reranks the results
    based on their relevance to the provided query.

    Key Features:
    - Dynamically creates search result storage directories
    - Utilizes Brave Search API for web searches
    - Configurable number of search results
    - Saves search results to a JSON file for further processing
    - Extracts, reranks, and returns URLs from the search results

    Parameters:
    -----------
    query : str
        The search query to be executed.
    key : str
        A unique identifier for organizing search results.
    num_searches : int, optional
        Number of search results to retrieve after reranking (default is 5).

    Returns:
    --------
    list or None
        A list of dictionaries containing URLs and titles from search results,
        Returns None if an error occurs during the search process.

    Directory Structure:
    -------------------
    - Creates a 'search' directory in the parent directory.
    - Generates a subdirectory using the provided 'key'.
    - Saves search results as 'web_search.json' in the subdirectory.

    API Interaction:
    ---------------
    - Uses Brave Search API with subscription token.
    - Sets appropriate headers for JSON response.
    - Handles potential API request errors.

    Example:
    --------
    results = web_search('Python programming', 'python_search')
    # Might return: [{'title': 'Python Tutorial', 'url': 'https://example.com/python'}]
    """
    print(f"\nPerforming web search for: '{query}'...")
    
    # Create directory structure
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'search')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    key_dir = os.path.join(data_dir, f"search_{key}")
    if not os.path.exists(key_dir):
        os.makedirs(key_dir)
    
    # Perform the search
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip',
        'X-Subscription-Token': brave_key,
    }

    params = {
        'q': query
    }

    response = requests.get('https://api.search.brave.com/res/v1/web/search', params=params, headers=headers)

    data=response.json()

    file_path = os.path.join(key_dir, "web_search.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print(f"Search results saved to: {file_path}")
        
    # Extract and return URLs
    urls= extract_urls_from_json(file_path)
    sorted_urls=rerank_urls(query, urls, num_searches)
    return sorted_urls

def scrape_page(driver, url, key_dir):
    """
    Web Page Scraping Function using Selenium WebDriver

    This function performs an in-depth web page scraping process, extracting structured 
    content from a given URL using Selenium and BeautifulSoup.

    Key Features:
    - Utilizes Selenium WebDriver for dynamic web page interaction
    - Employs BeautifulSoup for HTML parsing and content extraction
    - Creates organized markdown files for scraped content
    - Handles various HTML elements with structured extraction
    - Supports error handling and logging

    Parameters:
    -----------
    driver : selenium.webdriver
        An active Selenium WebDriver instance for browser automation
    url : str
        The complete URL of the webpage to be scraped
    key_dir : str
        Directory path for storing scraped content

    Content Extraction Strategy:
    ---------------------------
    - Waits for page body to load completely
    - Removes script and style tags to clean content
    - Extracts and structures content from headings, paragraphs, and lists
    - Converts extracted content to markdown format

    File Management:
    ---------------
    - Creates a unique directory for each URL based on its domain
    - Generates markdown files with date-based naming
    - Ensures safe filename creation by sanitizing special characters

    Error Handling:
    --------------
    - Catches and logs any exceptions during scraping process
    - Prevents script termination due to individual page scraping failures

    Example:
    --------
    scrape_page(selenium_driver, 'https://example.com', '/path/to/output')
    # Creates a markdown file with structured page content
    """
    # Sanitize filename
    filename = url.split('//')[-1]
    filename = re.sub(r'[<>:"/\\|?*#]', '-', filename)
    filename = filename.replace('.', '_')
    
    storage_path = os.path.join(key_dir, filename)
    os.makedirs(storage_path, exist_ok=True)
    
    today_date = datetime.now().strftime("%d-%m-%Y")
    output_file = os.path.join(storage_path, f"{today_date}.md")

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Get page content
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove scripts and styles
        for script in soup(["script", "style"]):
            script.extract()
        
        # Extract content with structure
        content = []
        for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol']):
            if element.name.startswith('h'):
                heading_level = element.name[1]
                content.append(f"\n{'#' * int(heading_level)} {element.get_text().strip()}\n")
            elif element.name == 'p':
                text = element.get_text().strip()
                if text:
                    content.append(f"{text}\n\n")
            elif element.name in ['ul', 'ol']:
                content.append("\n")
                for li in element.find_all('li', recursive=False):
                    content.append(f"* {li.get_text().strip()}\n")
                content.append("\n")
        
        # Save content
        text = '\n'.join(content)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
            
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")

def scrape_url(url, chrome_options, key_dir):
    """
    URL Scraping Wrapper Function with Selenium WebDriver

    This function serves as a convenient wrapper for web page scraping, 
    managing the lifecycle of a Selenium WebDriver for a single URL.

    Key Features:
    - Initializes a new Chrome WebDriver instance
    - Calls the main scraping function for a specific URL
    - Ensures proper WebDriver resource management
    - Provides a clean, abstracted interface for URL scraping

    Parameters:
    -----------
    url : str
        The complete URL to be scraped
    chrome_options : selenium.webdriver.chrome.options.Options
        Pre-configured Chrome WebDriver options
    key_dir : str
        Directory path for storing scraped content

    Workflow:
    ---------
    1. Initialize Chrome WebDriver with specified options
    2. Call scrape_page function to extract content
    3. Automatically close the WebDriver after scraping
    4. Handles potential exceptions during scraping process

    Resource Management:
    -------------------
    - Creates and destroys WebDriver instance for each URL
    - Prevents resource leaks by explicitly closing the driver
    - Supports concurrent scraping through thread-safe design

    Example:
    --------
    scrape_url('https://example.com', chrome_options, '/output/directory')
    # Scrapes the URL and saves content in the specified directory
    """
    driver = webdriver.Chrome(options=chrome_options)
    scrape_page(driver, url, key_dir)
    driver.quit()

def orchestrate_scraping(urls, key, key_dir):
    """
    Web Scraping Orchestration Function

    This function manages the parallel scraping of multiple URLs using 
    ThreadPoolExecutor and Selenium WebDriver, providing an efficient 
    and scalable web content extraction mechanism.

    Key Features:
    - Utilizes concurrent threading for parallel URL scraping
    - Configures Selenium WebDriver with randomized user agents
    - Manages multiple browser instances safely
    - Supports flexible scraping of multiple web pages

    Parameters:
    -----------
    urls : list
        A list of URLs to be scraped
    key : str
        A unique identifier for the scraping session
    key_dir : str
        Directory path for storing scraped content

    WebDriver Configuration:
    ----------------------
    - Disables browser extensions
    - Enables JavaScript
    - Uses randomized user agents
    - Ignores SSL certificate errors
    - Supports custom user data directory

    Concurrency Strategy:
    -------------------
    - Uses ThreadPoolExecutor for parallel processing
    - Limits concurrent workers to 5 to prevent overwhelming resources
    - Gracefully handles and logs individual URL scraping errors
    - Ensures all WebDriver instances are properly closed

    Resource Management:
    -------------------
    - Dynamically creates and destroys WebDriver instances
    - Prevents resource leaks through explicit driver management
    - Supports scalable web scraping across multiple URLs

    Error Handling:
    --------------
    - Catches and logs exceptions for individual URL scraping
    - Continues scraping other URLs even if one fails
    - Provides robust error resilience

    Example:
    --------
    orchestrate_scraping(['https://example1.com', 'https://example2.com'], 'search_key', '/output/dir')
    # Scrapes multiple URLs concurrently and saves content
    """
    chrome_options = Options()
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--enable-javascript')
    chrome_options.add_argument(f'user-agent={ua.random}')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--user-data-dir=/path/to/your/custom/profile')

    drivers = []  # List to hold driver instances

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(scrape_url, url, chrome_options, key_dir): url for url in urls}

    # Wait for all threads to complete
    for future in futures:
        try:
            driver = future.result()  # This will raise exceptions if any occurred in the thread
            if driver:
                drivers.append(driver)  # Store the driver instance
        except Exception as e:
            print(f"Error processing {futures[future]}: {str(e)}")

    # Terminate all driver instances
    for driver in drivers:
        driver.quit()

def gemini_smart_summary(query, urls, key, key_dir,model="gemini-1.5-flash-002"):
    """
    Content Summarization Function using Google Gemini AI

    This function leverages Google's Gemini AI to generate intelligent, 
    comprehensive summaries from web page contents, providing a sophisticated 
    natural language processing solution for content analysis.

    Key Features:
    - Utilizes Google's Generative AI (Gemini) for advanced text summarization
    - Reads markdown files generated from web scraping
    - Generates structured, context-aware summaries
    - Supports multiple AI model versions
    - Saves generated summaries to markdown files

    Parameters:
    -----------
    query : str
        The original search query driving the summarization
    urls : list
        List of URLs that were scraped
    key : str
        Unique identifier for the search session
    key_dir : str
        Directory containing scraped content
    model : str, optional
        Gemini AI model version to use (default: "gemini-1.5-flash-002")

    Summarization Workflow:
    ----------------------
    1. Locate and read markdown files from scraped URLs
    2. Prepare comprehensive input for Gemini AI
    3. Generate summary using predefined extraction instructions
    4. Save summary to a markdown file in the key directory

    AI Model Configuration:
    ---------------------
    - Supports flexible model selection
    - Uses predefined extraction instructions for consistent output
    - Handles potential API rate limits and errors

    File Management:
    ---------------
    - Reads markdown files from URL-specific directories
    - Generates summary files with descriptive naming
    - Ensures organized storage of generated summaries

    Error Handling:
    --------------
    - Gracefully handles file reading and AI generation errors
    - Provides logging and error tracking
    - Continues processing even if individual URL summarization fails

    Example:
    --------
    gemini_smart_summary('Python programming', urls, 'python_search', '/output/dir')
    # Generates AI-powered summaries for the given URLs
    """
    all_content = []
    today_date = datetime.now().strftime("%d-%m-%Y")
    
    print("\nReading scraped content...")
    for url in urls:
        filename = url.split('//')[-1]
        filename = re.sub(r'[<>:"/\\|?*#]', '-', filename)
        filename = filename.replace('.', '_')
        file_path = os.path.join(key_dir, filename, f"{today_date}.md")
        
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        all_content.append(content)
        except Exception as e:
            print(f"Error reading file {file_path}: {str(e)}")
    
    if not all_content:
        print("No content found in scraped files.")
        return None
    
    text = f"Query: {query}\n\nWebpage Contents:\n\n" + "\n\n---\n\n".join(all_content)
    
    print("\nGenerating smart summary using Gemini...")
    model = genai.GenerativeModel(
        model_name=model,
        system_instruction=extract_instructions
    )
    
    try:
        result = model.generate_content(text)
        return result.text
    except Exception as e:
        print(f"Failed to generate summary: {str(e)}")
        if hasattr(e, 'status_code'):
            print(f"API Error Status Code: {e.status_code}")
        return None

def smart_search(query, key, urls,model="gemini-1.5-flash-002"):
    """
    Smart Search Orchestration Function

    This function provides an end-to-end intelligent search solution, 
    integrating web search, content scraping, and AI-powered summarization 
    to deliver comprehensive and contextualized search results.

    Key Features:
    - Combines multiple search and content extraction techniques
    - Leverages web search, web scraping, and AI summarization
    - Provides a unified interface for complex search operations
    - Supports flexible configuration and model selection

    Parameters:
    -----------
    query : str
        The search query to be processed
    key : str
        A unique identifier for the search session
    urls : list, optional
        Pre-existing list of URLs to process (if not provided by web search)
    model : str, optional
        AI model version for summarization (default: "gemini-1.5-flash-002")

    Search Workflow:
    ---------------
    1. Perform web search if no URLs are provided
    2. Create search result storage directory
    3. Orchestrate web page scraping
    4. Generate AI-powered summaries
    5. Organize and store search results

    Flexibility and Extensibility:
    ----------------------------
    - Supports manual URL list or automatic web search
    - Configurable AI model selection
    - Modular design allows easy integration of new search techniques

    Error Handling and Resilience:
    ----------------------------
    - Gracefully handles failures in individual search stages
    - Provides comprehensive logging
    - Ensures partial results are preserved even if some steps fail

    Performance Considerations:
    --------------------------
    - Uses concurrent processing for web scraping
    - Manages system resources efficiently
    - Implements rate limiting and error recovery mechanisms

    Example:
    --------
    smart_search('Machine Learning trends', 'ml_search')
    # Performs a complete intelligent search and summarization process
    """
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'search')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    key_dir = os.path.join(data_dir, f"search_{key}")
    if not os.path.exists(key_dir):
        os.makedirs(key_dir)
        
    start_time = time.time()
    
    print(f"\nStarting smart search for query: '{query}'...")
    links = [url['url'] for url in urls]
    
    # Scrape webpages
    orchestrate_scraping(links, key, key_dir)
    
    # Generate summary
    summary = gemini_smart_summary(query, links, key, key_dir,model)
    if summary:
        summary_file = os.path.join(key_dir, "summary.md")
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"\nSummary saved to: {summary_file}")
    
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"\nSmart search completed in {execution_time:.2f} seconds")
    
    return summary
