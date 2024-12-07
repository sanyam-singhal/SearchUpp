import streamlit as st
import os
from dotenv import load_dotenv, set_key

st.title("Settings ⚙️")

# Load current environment variables
load_dotenv()

def update_env_var(key, value):
    """Update a single environment variable in .env file"""
    env_path = os.path.join(os.getcwd(), '.env')
    set_key(env_path, key, value)
    os.environ[key] = value  # Update runtime environment

# API Keys Section
st.header("API Keys")
brave_key = st.text_input(
    "Brave Search API Key",
    value=os.getenv("BRAVE_KEY", ""),
    type="password"
)
gemini_key = st.text_input(
    "Google Gemini API Key",
    value=os.getenv("GEMINI_KEY", ""),
    type="password"
)

# Search Settings Section
st.header("Search Settings")
simple_search_num = st.number_input(
    "Simple Search Results Count",
    min_value=1,
    max_value=20,
    value=int(os.getenv("SIMPLE_SEARCH_NUMBER", 0))
)
complex_search_num = st.number_input(
    "Advanced Search Results Count",
    min_value=1,
    max_value=20,
    value=int(os.getenv("COMPLEX_SEARCH_NUMBER", 0))
)

# Model Settings Section
st.header("Model Settings")
simple_model = st.selectbox(
    "Simple Search Model",
    options=["gemini-1.5-flash-002", "gemini-1.5-pro-002"],
    index=0 if os.getenv("SIMPLE_LLM_MODEL") == "gemini-1.5-flash-002" else 1
)
complex_model = st.selectbox(
    "Advanced Search Model",
    options=["gemini-1.5-flash-002", "gemini-1.5-pro-002","gemini-exp-1206"],
    index=0 if os.getenv("COMPLEX_LLM_MODEL") == "gemini-1.5-flash-002" else 1 if os.getenv("COMPLEX_LLM_MODEL") == "gemini-1.5-pro-002" else 2
)

# Save Settings Button
if st.button("Save Settings"):
    # Update all environment variables
    update_env_var("BRAVE_KEY", brave_key)
    update_env_var("GEMINI_KEY", gemini_key)
    update_env_var("SIMPLE_SEARCH_NUMBER", str(simple_search_num))
    update_env_var("COMPLEX_SEARCH_NUMBER", str(complex_search_num))
    update_env_var("SIMPLE_LLM_MODEL", simple_model)
    update_env_var("COMPLEX_LLM_MODEL", complex_model)
    
    st.success("Settings saved successfully! Please restart the application for changes to take effect.")