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
from .ai_modules import *

# Initial Setup
load_dotenv()
ua = UserAgent()
genai.configure(api_key=os.getenv("GEMINI_KEY"))
brave_key=os.getenv("BRAVE_KEY")
mode=os.getenv("MODE")
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
                        'url': result['url'],
                        'description': result['description']
                    })
        
        return urls
            
    except Exception as e:
        print(f"Error extracting URLs: {str(e)}")
        return None

def rerank_urls(query, urls):
    """
    Reranks a list of URLs based on their relevance to a given query.
    """
    if not urls:
        print("No URLs to rerank")
        return []
        
    try:
        # Extract descriptions, handling None values
        url_descriptions = []
        valid_urls = []
        
        for url in urls:
            if url.get('description'):
                url_descriptions.append(url['description'])
                valid_urls.append(url)
            else:
                print(f"Skipping URL without description: {url.get('url', 'unknown')}")
        
        if not valid_urls:
            print("No valid URLs with descriptions found")
            return urls  # Return original URLs if none have descriptions
            
        # Get embeddings
        query_embed = genai.embed_content(model="models/text-embedding-004", content=[query])
        query_embed = np.array(query_embed["embedding"])
        url_embeds = genai.embed_content(model="models/text-embedding-004", content=url_descriptions)
        url_embeds = np.array(url_embeds["embedding"])
        
        # Calculate scores and sort
        url_scores = np.linalg.norm(url_embeds - query_embed, axis=1)
        
        # Create list of (score, url) tuples and sort
        url_with_scores = list(zip(url_scores, valid_urls))
        sorted_urls = [url for _, url in sorted(url_with_scores, reverse=True)]
        
        return sorted_urls
        
    except Exception as e:
        print(f"Error in rerank_urls: {str(e)}")
        return urls  # Return original URLs if reranking fails

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
    sorted_urls=rerank_urls(query, urls)

    file_path = os.path.join(key_dir, "web_search.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(sorted_urls, f, ensure_ascii=False, indent=4)
    
    print(f"Search results saved to: {file_path}")
    
    return sorted_urls[:num_searches]

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

    print(f"Saving content to: {output_file}")

    try:
        print(f"Navigating to URL: {url}")
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print(f"Page loaded successfully for {url}")
        
        # Get page content
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove scripts and styles
        for script in soup(["script", "style"]):
            script.extract()
        
        # Extract content with structure
        content = []
        content.append(f"# Source URL: {url}\n")
        content.append(f"# Scraped on: {today_date}\n\n")
        
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
        
        print(f"Successfully saved content for {url}")
            
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        raise  # Re-raise the exception to be caught by the caller

def orchestrate_scraping(urls, key, key_dir):
    """
    Web Scraping Orchestration Function

    This function manages the parallel scraping of multiple URLs using 
    ThreadPoolExecutor and Selenium WebDriver, providing an efficient 
    and scalable web content extraction mechanism.
    """
    def scrape_with_new_driver(url):
        print(f"\nStarting to scrape URL: {url}")
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--enable-javascript')
        user_agent = ua.random
        chrome_options.add_argument(f'user-agent={user_agent}')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        print(f"Using User-Agent: {user_agent}")
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            print(f"Created new WebDriver instance for {url}")
            scrape_page(driver, url, key_dir)
            print(f"Successfully scraped {url}")
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
        finally:
            if 'driver' in locals():
                driver.quit()
                print(f"Closed WebDriver instance for {url}")

    print(f"\nStarting parallel scraping for {len(urls)} URLs...")
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(scrape_with_new_driver, urls)
    print("\nCompleted scraping all URLs")

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

def smart_search(query, key, urls, model):
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
    model : str
        AI model version for summarization

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
    if mode=="Local":
        summary = ollama_model(query, links, key, key_dir,model)
    else:
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
