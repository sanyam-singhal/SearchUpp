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
load_dotenv()
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
                <a href="{url['url']}" target="_blank" style="text-decoration: none; color: inherit;">
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