import streamlit as st
import os
import pandas as pd
import datetime


search=os.path.join("paths","search.py")
history=os.path.join("paths","history.py")
settings=os.path.join("paths","settings.py")
past=os.path.join("paths","past.py")

pages={
    "App":[
        st.Page(search,title="Search", icon="🔍"),
        st.Page(history,title="History", icon="📜"),
        st.Page(past,title="Recap", icon="🤔")
    ],
    "Account":[
        st.Page(settings,title="Settings", icon="⚙")
    ]
}

pg=st.navigation(pages)

pg.run()