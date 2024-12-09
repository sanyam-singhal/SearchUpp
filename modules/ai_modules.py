import ollama 
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time
from datetime import datetime
import re

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_KEY"))
extract_instructions=os.getenv("SEARCH_SUMMARY_INSTRUCTIONS")


def ollama_model(query, urls, key, key_dir, model="llama3.2:1b"):
    """
    Content Summarization Function using Ollama AI

    This function leverages Ollama AI to generate intelligent, 
    comprehensive summaries from web page contents, providing a sophisticated 
    natural language processing solution for content analysis.

    Key Features:
    - Utilizes Ollama AI for advanced text summarization
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
        Ollama AI model version to use (default: "llama3.2:1b")

    Summarization Workflow:
    ----------------------
    1. Locate and read markdown files from scraped URLs
    2. Prepare comprehensive input for Ollama AI
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
    ollama_model('Python programming', urls, 'python_search', '/output/dir')
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
        return "Could not generate summary. Please try again!"
    
    text = f"User Search Query: {query}\n\n Scraped Webpage Contents:\n\n" + "\n\n---\n\n".join(all_content)
    
    print(f"\nGenerating summary using {model}...")
    try:
        response: ollama.ChatResponse = ollama.chat(model=model, messages=[
        {
            'role': 'system',
            'content': extract_instructions,
        },
        {
            'role': 'user',
            'content': text,
        },
        ])

        return response['message']['content']
    except:
        print("Error generating summary. Please try again.")
        return "Could not generate summary. Please try again!"

def gemini_smart_summary(query, urls, key, key_dir, model="gemini-1.5-flash-002"):
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
        return "Could not generate summary. Please try again!"
    
    text = f"User Search Query: {query}\n\n Scraped Webpage Contents:\n\n" + "\n\n---\n\n".join(all_content)
    
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
        return "Could not generate summary. Please try again!"
