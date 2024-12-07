#!/bin/bash
export $(grep -v '^#' .env | xargs)  # Load variables from .env file
cd "$PROJECT_DIR"  # Use the variable from .env
streamlit run app.py  
