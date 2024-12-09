import streamlit as st
import os
import pandas as pd
from datetime import datetime
from modules.search_modules import *
from dotenv import load_dotenv
import pyperclip
import toml

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

load_dotenv()
simple_search_number=int(os.getenv("SIMPLE_SEARCH_NUMBER"))
complex_search_number=int(os.getenv("COMPLEX_SEARCH_NUMBER"))
simple_llm_model=os.getenv("SIMPLE_LLM_MODEL")
complex_llm_model=os.getenv("COMPLEX_LLM_MODEL")

search_history_path = os.path.join("search", "search_history.csv")
if os.path.exists(search_history_path):
    history = pd.read_csv(search_history_path)
    current_index=history.shape[0]

elif not os.path.exists(search_history_path):
    history=pd.DataFrame(columns=["datetime","query","search_path","summary_path"])
    history.to_csv(search_history_path,index=False)
    current_index=0

st.title("Search _Upp_ :rocket:")
query = st.text_input(label="Enter your query",key="search_input")
pro_search=st.toggle("Advanced Search")
search_query_path = os.path.join("search", f"search_{current_index}", "web_search.json")
summary_path = os.path.join("search", f"search_{current_index}", "summary.md")

if pro_search:
    num_searches=complex_search_number
    model=complex_llm_model
else:
    num_searches=simple_search_number
    model=simple_llm_model

if query:
    # Get current datetime
    now = datetime.now()
    formatted_datetime = now.strftime("%d-%m-%Y %H:%M:%S")

    

    urls = web_search(query, current_index, num_searches)

    

    new_entry = [formatted_datetime, query, search_query_path, summary_path]
    pd.DataFrame([new_entry], columns=["datetime", "query", "search_path", "summary_path"]).to_csv(search_history_path, mode="a", index=False, header=False)

    
    

results, summary=st.tabs(["Search Results", "Summary"])
with results:
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
    if os.path.exists(search_query_path):
        search_content = json.load(open(search_query_path, encoding='utf-8'))
        urls = search_content[:num_searches]
        with st.spinner('Generating summary...'):
            summary = smart_search(query, current_index, urls, model)
            query=None
    
    try:
        summary_content=open(os.path.join("search", f"search_{current_index}", "summary.md"), 'r', encoding='utf-8').read()
        if summary_content:
            if st.button(label="Copy Summary",key="copy_summary"):
                pyperclip.copy(summary_content)
                st.success("Summary copied to clipboard!")
            st.markdown(summary_content)
    except Exception as e:
        st.warning("No summary generated yet")