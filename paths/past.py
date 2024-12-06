import streamlit as st
import os
import pandas as pd
import datetime
import json

st.title("Recap of a previous search 🤔...")

# Add a back button to return to history
if st.button("← Back to History"):
    st.switch_page("paths/history.py")

st.divider()

if 'clicked_history_row' in st.session_state:
    record = st.session_state.clicked_history_row
    
    # Display the search details in a card-like format
    st.markdown("### Search Details")
    
    col1, col2 = st.columns([3,2])
    
    with col1:
        st.info("**Query Information**")
        st.write(f"**Search Query:** {record['query']}")
        st.write(f"**Date & Time:** {record['datetime']}")
    
    with col2:
        st.info("**File Paths**")
        st.write(f"**Search Path:** {record['search_path']}")
        st.write(f"**Summary Path:** {record['summary_path']}")
    
    # Display file contents if they exist
    st.divider()
    with st.expander("Search Results", expanded=True):
        # Check and display search file contents
        if os.path.exists(record['search_path']):
            search_content = json.load(open(record['search_path'], encoding='utf-8'))
            urls = search_content['web']['results']
            for url in urls:
                st.subheader(f"{url['title']}")
                st.write(f"URL: {url['url']}")
        else:
            st.warning("Search results file not found")
    
    # Check and display summary file contents
    with st.expander("Summary", expanded=False):
        if os.path.exists(record['summary_path']):
            with open(record['summary_path'], 'r', encoding='utf-8') as f:
                summary_content = f.read()
            st.markdown(summary_content, unsafe_allow_html=True)
        else:
            st.warning("Summary file not found")

else:
    st.warning("No search details selected. Please select a record from the History page.")