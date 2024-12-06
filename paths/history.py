import streamlit as st
import os
import pandas as pd
import datetime

st.title("History 📜")

history_path=os.path.join("search","search_history.csv")

if os.path.exists(history_path):
    history=pd.read_csv(history_path)
    history=history.sort_values(by="datetime",ascending=False)
    
    # Convert DataFrame to a list of dictionaries for easier handling
    history_records = history.to_dict('records')
    
    # Display each record with a button
    for idx, record in enumerate(history_records):
        col1, col2 = st.columns([3,1])
        with col1:
            st.write(f"**Query:** {record['query']}")
            st.write(f"**Date & Time:** {record['datetime']}")
        with col2:
            if st.button('View Details', key=f'btn_{idx}'):
                st.session_state.clicked_history_row = record
                st.switch_page("paths/past.py")
        st.divider()

elif not os.path.exists(history_path):
    st.write("No history found")