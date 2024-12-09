import streamlit as st
import os
import pandas as pd
import datetime
import json
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

st.title("Recap of a previous search 🤔...")

# Add a back button to return to history
if st.button("← Back to History"):
    st.switch_page("paths/history.py")

st.divider()

if 'clicked_history_row' in st.session_state:
    record = st.session_state.clicked_history_row
    
    # Display the search details in a card-like format
    st.markdown("### Search Details")
    
    st.write(f"**Search Query:** {record['query']}")
    st.write(f"**Date & Time:** {record['datetime']}")
    
    # Display file contents if they exist
    st.divider()
    results, summary=st.tabs(["Search Results", "Summary"])
    with results:
        if os.path.exists(record['search_path']):
            search_content = json.load(open(record['search_path'], encoding='utf-8'))
            urls = search_content
            
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
        else:
            st.warning("Search results file not found")
    
    # Check and display summary file contents
    with summary:
        if os.path.exists(record['summary_path']):
            with open(record['summary_path'], 'r', encoding='utf-8') as f:
                summary_content = f.read()
            if st.button(label="Copy Summary",key="copy_summary"):
                pyperclip.copy(summary_content)
                st.success("Summary copied to clipboard!")
            st.markdown(summary_content, unsafe_allow_html=True)
            
        else:
            st.warning("Summary file not found")

else:
    st.warning("No search details selected. Please select a record from the History page.")