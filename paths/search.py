import streamlit as st
import os
import pandas as pd
from datetime import datetime
from modules.search_modules import *
from dotenv import load_dotenv

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
query = st.text_input(label="Enter your query")
pro_search=st.toggle("Advanced Search")

if query:
    # Get current datetime
    now = datetime.now()
    formatted_datetime = now.strftime("%d-%m-%Y %H:%M:%S")

    if pro_search:
        num_searches=complex_search_number
        model=complex_llm_model
    else:
        num_searches=simple_search_number
        model=simple_llm_model

    urls = web_search(query, current_index, num_searches)

    search_query_path = os.path.join("search", f"search_{current_index}", "web_search.json")
    summary_path = os.path.join("search", f"search_{current_index}", "summary.md")

    new_entry = [formatted_datetime, query, search_query_path, summary_path]
    pd.DataFrame([new_entry], columns=["datetime", "query", "search_path", "summary_path"]).to_csv(search_history_path, mode="a", index=False, header=False)

    if urls:
        with st.expander("Search Results", expanded=True):
            st.header("Search Results :mag_right:", divider='blue')
            for url in urls:
                st.subheader(f"{url['title']}")
                st.write(f"URL: {url['url']}")
        
        with st.spinner('Generating summary...'):
            summary = smart_search(query, current_index, urls, model)
            if summary:
                st.divider()
                with st.expander("Summary", expanded=True):
                    st.markdown(summary)
