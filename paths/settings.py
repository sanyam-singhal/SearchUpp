import streamlit as st
import os
from dotenv import load_dotenv, set_key
from modules.modify_theme import modify_theme
import toml
import ollama

st.title("Settings ⚙️")

# Load current environment variables
load_dotenv()

def update_env_var(key, value):
    """Update a single environment variable in .env file"""
    env_path = os.path.join(os.getcwd(), '.env')
    set_key(env_path, key, value)
    os.environ[key] = value  # Update runtime environment

# Load theme settings from config.toml
config_path = os.path.join(os.path.dirname(__file__), '..', '.streamlit', 'config.toml')
with open(config_path, 'r') as f:
    config = toml.load(f)

# Set current theme values from config
base = config.get('theme', {}).get('base', 'light')
primary_color = config.get('theme', {}).get('primaryColor')
background_color = config.get('theme', {}).get('backgroundColor')
secondary_background_color = config.get('theme', {}).get('secondaryBackgroundColor')
text_color = config.get('theme', {}).get('textColor')
font = config.get('theme', {}).get('font')

theme, api_keys, search_settings, model_settings = st.tabs(["Theme", "API Keys", "Search Settings", "Model Settings"])

with theme:
    # Theme Setting Section
    st.header("Theme")

    # Inputs for theme settings

    primary_color = st.color_picker("Primary Color", value=primary_color)
    background_color = st.color_picker("Background Color", value=background_color)
    secondary_background_color = st.color_picker("Secondary Background Color", value=secondary_background_color)
    text_color = st.color_picker("Text Color", value=text_color)
    font = st.selectbox(
        "Select Font",
        options=["sans serif", "serif", "monospace"],
        index=0 if font == "sans serif" else (1 if font == "serif" else 2)
    )

    # Button to apply theme changes
    if st.button("Apply Theme",key="apply_theme"):
        modify_theme(base, primary_color, background_color, secondary_background_color, text_color, font)
        st.success("Theme updated successfully!")

with api_keys:
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
    
    # Save Settings Button
    if st.button("Save Settings",key="api_keys"):
        # Update all environment variables
        update_env_var("BRAVE_KEY", brave_key)
        update_env_var("GEMINI_KEY", gemini_key)
        st.success("Settings saved successfully! Please restart the application for changes to take effect.")

with search_settings:
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
    
    # Save Settings Button
    if st.button("Save Settings",key="search_settings"):
        # Update all environment variables
        update_env_var("SIMPLE_SEARCH_NUMBER", str(simple_search_num))
        update_env_var("COMPLEX_SEARCH_NUMBER", str(complex_search_num))
        
        st.success("Settings saved successfully! Please restart the application for changes to take effect.")

with model_settings:
    # Model Settings Section
    st.header("Model Settings")
    mode=st.selectbox("How to run LLMs?",["Local","Cloud"],index=0 if os.getenv("MODE") == "Local" else 1)

    if mode=="Local": 
        available_local_models=ollama.list()
        available_local_models=[model["model"] for model in available_local_models["models"]]
        simple_model=st.selectbox(label="Simple Search Model (Local)",options=available_local_models,key="local_simple_model")
        complex_model=st.selectbox(label="Advanced Search Model (Local)",options=available_local_models,key="local_complex_model")
    
    else:
        simple_model = st.selectbox(
            label="Simple Search Model (Cloud)",
            options=["gemini-1.5-flash-002", "gemini-1.5-pro-002"],
            key="cloud_simple_model",
            index=0 if os.getenv("SIMPLE_LLM_MODEL") == "gemini-1.5-flash-002" else 1
        )
        complex_model = st.selectbox(
            label="Advanced Search Model (Cloud)",
            options=["gemini-1.5-flash-002", "gemini-1.5-pro-002","gemini-exp-1206"],
            key="cloud_complex_model",
            index=0 if os.getenv("COMPLEX_LLM_MODEL") == "gemini-1.5-flash-002" else 1 if os.getenv("COMPLEX_LLM_MODEL") == "gemini-1.5-pro-002" else 2
        )

    summary_instructions = st.text_area(
        label="LLM Summary Instructions",
        value=os.getenv("SEARCH_SUMMARY_INSTRUCTIONS"),
        height=400
    )

    
    # Save Settings Button
    if st.button("Save Settings",key="model_settings"):
        # Update all environment variables
        update_env_var("MODE", mode)
        update_env_var("SIMPLE_LLM_MODEL", simple_model)
        update_env_var("COMPLEX_LLM_MODEL", complex_model)
        
        # Flatten summary instructions
        flattened_instructions = " ".join(summary_instructions.split())
        update_env_var("SEARCH_SUMMARY_INSTRUCTIONS", flattened_instructions)
        
        st.success("Settings saved successfully! Please restart the application for changes to take effect.")