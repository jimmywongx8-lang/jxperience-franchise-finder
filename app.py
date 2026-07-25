import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="JP Franchise Hub", layout="wide")

st.title("🇯🇵 JP Franchise Hub")
st.write("App is loading...")

# Test basic functionality
try:
    CSV_URL = "https://raw.githubusercontent.com/jimmywongx8-lang/jxperience-franchise-finder/main/franchise_data.csv"
    df = pd.read_csv(CSV_URL)
    st.success(f"✅ Loaded {len(df)} brands!")
    
    # Show first few rows
    st.write("Sample data:")
    st.dataframe(df.head(3))
    
except Exception as e:
    st.error(f"Error: {e}")

# Test Google Sheets
SHEET_URL = st.secrets.get("SHEET_WEBHOOK_URL")
if SHEET_URL:
    try:
        resp = requests.get(SHEET_URL, timeout=10)
        if resp.status_code == 200:
            leads = resp.json()
            st.success(f"✅ Google Sheets connected! Found {len(leads)} leads")
    except Exception as e:
        st.warning(f"Sheets error: {e}")
