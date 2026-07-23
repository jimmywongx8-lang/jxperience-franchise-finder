import streamlit as st
import pandas as pd
from openai import OpenAI
import json
import os

# --- CONFIGURATION ---
GROQ_API_KEY = "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" 
CSV_PATH = "C:\\jfa_scraper\\franchise_data.csv"

st.set_page_config(page_title="Franchisor Onboarding", layout="wide")

# Navigation buttons at top
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("️ Back to Main"):
        st.switch_page("app.py")
with col2:
    st.title("🇯🇵 Franchisor Onboarding Portal")

st.markdown("Paste your Japanese brochure text below. Our AI will translate and structure it for global investors.")

# ... rest of the code stays the same ...
