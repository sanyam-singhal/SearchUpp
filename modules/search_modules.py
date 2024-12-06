from bs4 import BeautifulSoup
import json
import time
import os
import re
from datetime import datetime
from fake_useragent import UserAgent
import random
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import google.generativeai as genai
from dotenv import load_dotenv

# Initial Setup
load_dotenv()
ua = UserAgent()
genai.configure(api_key=os.getenv("GEMINI_KEY"))
brave_key=os.getenv("BRAVE_KEY")

# Random viewport sizes for more human-like behavior
viewport_widths = [1366, 1440, 1536, 1600, 1920]
viewport_heights = [768, 900, 864, 1024, 1080]

extract_instructions = """
You are an expert at extracting and summarizing information from web pages.
Your task is to analyze the provided web content and create a comprehensive markdown summary that:

1. Identifies and highlights the most important information
2. Organizes the content in a clear, logical structure
3. Uses appropriate markdown formatting for better readability
4. Preserves key details while eliminating redundant information
5. Maintains proper context and relationships between ideas
6. You should structure the output based on the user query like whether they want to make notes, write an article.


Focus on providing a summary that is both informative and easy to read.

Respond in 1000-4000 words based on the user query and the complexity of the content.
"""
def extract_urls_from_json(file_path):
    """
    Extracts URLs from the search results JSON file
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

def web_search(query, key,num_searches=5):
    """
    Performs a web search using the Brave Search API
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
        'q': query,
        'count': num_searches,
    }

    response = requests.get('https://api.search.brave.com/res/v1/web/search', params=params, headers=headers)

    data=response.json()

    file_path = os.path.join(key_dir, "web_search.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print(f"Search results saved to: {file_path}")
        
    # Extract and return URLs
    return extract_urls_from_json(file_path)

def scrape_page(driver, url, key_dir):
    """
    Scrapes a single webpage using Selenium
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

def orchestrate_scraping(urls, key, key_dir):
    """
    Orchestrates the scraping of multiple URLs using Selenium
    """
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument(f'user-agent={ua.random}')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        for url in urls:
            scrape_page(driver, url, key_dir)
    finally:
        driver.quit()

def gemini_smart_summary(query, urls, key, key_dir,model="gemini-1.5-flash-002"):
    """
    Generates a summary using Gemini AI
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
    Performs a smart search using the given query
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
