import streamlit as st
import os
import pandas as pd
from datetime import datetime
from modules.parallel_search import *

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

if query:
    # Get current datetime
    now = datetime.now()
    formatted_datetime = now.strftime("%d-%m-%Y %H:%M:%S")

    urls = web_search(query, current_index)

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
            summary = smart_search(query, current_index, urls)
            if summary:
                st.divider()
                with st.expander("Summary", expanded=True):
                    st.markdown(summary)
