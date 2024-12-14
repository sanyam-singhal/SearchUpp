import streamlit as st
import os
import pandas as pd
from datetime import datetime
from modules.search_modules import *
from dotenv import load_dotenv
import toml
import time
import json

import streamlit.components.v1 as components

# Load environment variables from .env file
load_dotenv()

# Set default values for environment variables if not present
if not os.getenv('SIMPLE_SEARCH_NUMBER'):
    os.environ['SIMPLE_SEARCH_NUMBER'] = '5'
if not os.getenv('COMPLEX_SEARCH_NUMBER'):
    os.environ['COMPLEX_SEARCH_NUMBER'] = '10'
if not os.getenv('SIMPLE_LLM_MODEL'):
    os.environ['SIMPLE_LLM_MODEL'] = 'gemini-1.5-flash-002'
if not os.getenv('COMPLEX_LLM_MODEL'):
    os.environ['COMPLEX_LLM_MODEL'] = 'gemini-exp-1206'
if not os.getenv('PROJECT_DIR'):
    os.environ['PROJECT_DIR'] = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not os.getenv('SEARCH_SUMMARY_INSTRUCTIONS'):
    os.environ['SEARCH_SUMMARY_INSTRUCTIONS'] = '''You are a skilled research assistant specializing in analyzing and summarizing information. Your task is to process content from multiple webpages scraped in response to a user query, then summarize and structure the information clearly and logically in 1000–4000 words based on the query's complexity and the depth of the content. Follow these steps to ensure high-quality output:** Understand the Query: Analyze the user's input to determine its intent, complexity, and specific focus areas. Synthesize Information: Combine relevant data from all sources to create a coherent narrative. Avoid repeating redundant details and ensure consistency across all information presented. Organize Structurally: Present the content in a well-structured format, including: Title: A concise and accurate title summarizing the content. Introduction: Provide a brief overview of the topic and what the user will learn. Main Sections: Divide the content into logically ordered sections with clear headings and subheadings. Each section should cover a distinct aspect of the topic. Details and Examples: Where relevant, include examples, statistics, or quotes to enrich the content. Conclusion: Summarize the key points and, if applicable, suggest next steps or resources for further exploration. Ensure Clarity: Write in clear, professional language appropriate for the target audience, avoiding technical jargon unless necessary. Cite Implicitly: Attribute key insights or data to their general source categories without directly quoting the webpages verbatim. Guidelines: Prioritize accuracy and relevance. Include only verifiable and pertinent information. Adjust the level of detail to suit the query's complexity. For simple topics, focus on clarity and conciseness. For complex ones, provide in-depth analysis and context. Eliminate bias or subjective opinions unless explicitly requested. Example Queries: 'Explain the impact of climate change on Arctic wildlife' or 'Summarize recent advancements in quantum computing.' Apply these instructions dynamically to address a wide range of topics'''
if not os.getenv('MODE'):
    os.environ['MODE'] = 'Cloud'

# Load current theme
config_path = os.path.join(os.path.dirname(__file__), '..', '.streamlit', 'config.toml')

# Load existing configuration
with open(config_path, 'r') as f:
    config = toml.load(f)

# Set current theme values from config
base = config.get('theme', {}).get('base', 'light')
primary_color = config.get('theme', {}).get('primaryColor')
background_color = config.get('theme', {}).get('backgroundColor')
secondary_background_color = config.get('theme', {}).get('secondaryBackgroundColor')
text_color = config.get('theme', {}).get('textColor')
font = config.get('theme', {}).get('font')

# Configuring the overall search using environment variables
simple_search_number=int(os.getenv("SIMPLE_SEARCH_NUMBER"))
complex_search_number=int(os.getenv("COMPLEX_SEARCH_NUMBER"))
simple_llm_model=os.getenv("SIMPLE_LLM_MODEL")
complex_llm_model=os.getenv("COMPLEX_LLM_MODEL")

# Reading the existing search history for appending new queries to history
search_history_path = os.path.join("search", "search_history.csv")
if os.path.exists(search_history_path):
    history = pd.read_csv(search_history_path)
    current_index=history.shape[0]

elif not os.path.exists(search_history_path):
    if not os.path.exists("search"):
        os.makedirs("search")
    history=pd.DataFrame(columns=["datetime","query","search_path","summary_path"])
    history.to_csv(search_history_path,index=False)
    current_index=0

search_query_path = os.path.join("search", f"search_{current_index}", "web_search.json")
summary_path = os.path.join("search", f"search_{current_index}", "summary.md")
query=None

# Start of the Streamlit UI

st.title("Search _Upp_ :rocket:")
with st.form(key="search_form",clear_on_submit=True):
    query = st.text_input(label="Enter your query",key="search_input")
    submitted=st.form_submit_button("Search")

pro_search=st.toggle("Advanced Search")

if pro_search:
    num_searches=complex_search_number
    model=complex_llm_model
else:
    num_searches=simple_search_number
    model=simple_llm_model



results, summary=st.tabs(["Search Results", "Summary"])
with results:
    if submitted and query:
        st.write(f"Query: {query}")
        start_time = time.time()
        
        now = datetime.now()
        formatted_datetime = now.strftime("%d-%m-%Y %H:%M:%S")
        with st.spinner('Searching...'):
            urls = web_search(query, current_index, num_searches)
        new_entry = [formatted_datetime, query, search_query_path, summary_path]
        pd.DataFrame([new_entry], columns=["datetime", "query", "search_path", "summary_path"]).to_csv(search_history_path, mode="a", index=False, header=False)

    if os.path.exists(search_query_path):
        search_content = json.load(open(search_query_path, encoding='utf-8'))
        urls = search_content[:num_searches]
        try:
            for url in urls:
                st.html(
                f"""
                <div style="background: {secondary_background_color}; border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); overflow: hidden; transition: transform 0.3s, box-shadow 0.3s;">
                <a href="{url['url']}" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: inherit;">
                    <div style="padding: 15px;">
                    <div style="font-size: 1.25rem; font-weight: bold; color: {text_color}; margin-bottom: 10px;">{url['title']}</div>
                    <div style="font-size: 0.8rem; color: {text_color};">{url['description']}</div>
                    </div>
                </a>
                </div>
                """
            )
        except Exception as e:
            st.warning("No search performed yet")
    else:
        st.warning("No search performed yet")
        
        
with summary:
    summary_file_path = os.path.join("search", f"search_{current_index}", "summary.md")
    
    if os.path.exists(search_query_path) and not os.path.exists(summary_path):
        search_content = json.load(open(search_query_path, encoding='utf-8'))
        urls = search_content[:num_searches]
        with st.spinner('Generating summary...'):
            summary = smart_search(query, current_index, urls, model)
            query=None
    
    if os.path.exists(summary_file_path):
        summary_content = open(summary_file_path, 'r', encoding='utf-8').read()
        end_time = time.time()
        elapsed_time = end_time - start_time
        st.divider()
        st.write(f"Time taken: {elapsed_time:.2f} seconds")
        st.divider()

        # Create the HTML component
        copy_component = f"""
        <style>
            .copy-btn {{
                background-color: {secondary_background_color};
                color: {text_color};
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                transition: all 0.2s ease;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .copy-btn:hover {{
                background-color: {primary_color};
                transform: translateY(-1px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            }}
            .copy-btn:active {{
                transform: translateY(0);
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .copy-btn.copied {{
                background-color: {primary_color};
            }}
        </style>
        <div>
            <button id="copyButton" class="copy-btn">
                Copy Summary
            </button>
        </div>
        <script>
            const copyButton = document.getElementById('copyButton');
            const textToCopy = `{summary_content.replace("`", "\\`").replace("$", "\\$")}`;
            
            copyButton.addEventListener('click', async () => {{
                try {{
                    await navigator.clipboard.writeText(textToCopy);
                    copyButton.textContent = '✓ Copied!';
                    copyButton.classList.add('copied');
                    setTimeout(() => {{
                        copyButton.textContent = 'Copy Summary';
                        copyButton.classList.remove('copied');
                    }}, 2000);
                }} catch (err) {{
                    console.error('Failed to copy:', err);
                    copyButton.textContent = '✗ Failed to copy';
                    setTimeout(() => {{
                        copyButton.textContent = 'Copy Summary';
                    }}, 2000);
                }}
            }});
        </script>
        """
        
        # Render the component
        components.html(copy_component, height=50)
        
        # Display the summary content
        st.markdown("### Summary")
        st.markdown(summary_content)
    else:
        st.warning("No summary generated yet")