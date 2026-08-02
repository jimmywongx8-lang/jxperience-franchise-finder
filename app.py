import streamlit as st
import pandas as pd
from openai import OpenAI
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import os

st.set_page_config(
    page_title="JXPerience | Japanese Franchise Expansion Platform", 
    page_icon="🔴",
    layout="wide"
)

# Header
st.title("🔴 JXPerience")
st.markdown("### Japanese Franchise Overseas Expansion Platform")
st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    paths = ["C:\\jfa_scraper\\franchise_data.csv", "franchise_data.csv"]
    for p in paths:
        try:
            return pd.read_csv(p)
        except:
            continue
    return pd.DataFrame()

df = load_data()
if df.empty:
    st.warning("⚠️ No data loaded.")
    st.stop()

if 'selected_brand' in st.session_state:
    del st.session_state['selected_brand']

# Helper functions
def get_brand_initials(brand_name):
    if not brand_name:
        return "??"
    words = str(brand_name).split()
    if len(words) >= 2:
        return (words[0][0] + words[1][0]).upper()
    return str(brand_name)[:2].upper()

def get_brand_color(brand_name):
    colors = ['#0066cc', '#0052a3', '#1976d2', '#0288d1', '#0097a7', 
              '#00796b', '#388e3c', '#689f38', '#afb42b', '#fbc02d']
    hash_val = sum(ord(c) for c in str(brand_name)) % len(colors)
    return colors[hash_val]

def get_confidence_badge(confidence):
    if confidence == "YES": return "✅ Confirmed"
    elif confidence == "PROBABLE": return "🟡 Probable"
    elif confidence == "NEEDS_VERIFICATION": return "⚠️ Verify"
    return "❌ No"

df['franchise_status'] = df['overseas_franchise_confirmed'].apply(get_confidence_badge)

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    st.warning("⚠️ API Key not configured.")

client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")

# Hero Section
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Japanese Franchises Analyzed", "63+")
with col2:
    st.metric("Investment Range (USD)", "$100k-$800k")
with col3:
    st.metric("Target Markets", "15+")

st.markdown("---")

# Sidebar
st.sidebar.header("🔍 Search")
search_term = st.sidebar.text_input("", placeholder="Type brand name...")

st.sidebar.header("💎 Discovery Mode")
display_mode = st.sidebar.radio("Show:", ["💎 Hidden Gems (<50 overseas)", "📋 All Brands (A-Z)", "✅ Verified Only"])

st.sidebar.header("📊 Sort By")
sort_by = st.sidebar.selectbox("Primary sort:", ["Brand Name (A-Z)", "Investment (Low-High)", "Investment (High-Low)"])

st.sidebar.header("Filter by Category")
selected_category = st.sidebar.multiselect("Select categories:", options=df['category'].unique(), default=df['category'].unique())

# Filter data
filtered_df = df[df['category'].isin(selected_category)].copy()

if "Hidden Gems" in display_mode:
    overseas_nums = pd.to_numeric(filtered_df['stores_overseas'].str.extract('(\d+)')[0], errors='coerce').fillna(999)
    filtered_df = filtered_df[overseas_nums < 50]
elif "Verified Only" in display_mode:
    filtered_df = filtered_df[filtered_df['overseas_franchise_confirmed'] == 'YES']

if "Investment (Low-High)" in sort_by:
    filtered_df['sort_val'] = pd.to_numeric(filtered_df['investment_usd'].str.extract('(\d+)')[0], errors='coerce').fillna(999999)
    filtered_df = filtered_df.sort_values('sort_val').drop(columns=['sort_val'])
elif "Investment (High-Low)" in sort_by:
    filtered_df['sort_val'] = pd.to_numeric(filtered_df['investment_usd'].str.extract('(\d+)')[0], errors='coerce').fillna(0)
    filtered_df = filtered_df.sort_values('sort_val', ascending=False).drop(columns=['sort_val'])
else:
    filtered_df = filtered_df.sort_values('brand_name')

if search_term:
    filtered_df = filtered_df[filtered_df['brand_name'].str.contains(search_term, case=False, na=False)]

st.subheader(f"💎 Found {len(filtered_df)} Brands")

st.info("ℹ️ **Disclaimer:** All information sourced from public data. JXPerience is not officially affiliated with listed brands.")

st.markdown("### 📊 Franchise Directory")

# Display brands with colored initials
for idx, row in filtered_df.iterrows():
    brand_name = row['brand_name']
    initials = get_brand_initials(brand_name)
    brand_color = get_brand_color(brand_name)
    
    # Create container for each brand
    with st.container():
        col_logo, col_name, col_stores, col_investment, col_button = st.columns([1, 3, 2, 2, 1])
        
        with col_logo:
            # Display colored circle with initials
            st.markdown(f"""
                <div style="width:60px;height:60px;border-radius:10px;background-color:{brand_color};
                            display:flex;align-items:center;justify-content:center;
                            color:white;font-weight:bold;font-size:1.5rem;
                            box-shadow:0 2px 8px rgba(0,0,0,0.1);">
                    {initials}
                </div>
            """, unsafe_allow_html=True)
        
        with col_name:
            st.markdown(f"**{brand_name}**")
            st.caption(row['category'])
        
        with col_stores:
            st.write(f"🇯🇵 {row['stores_japan']} stores")
            st.write(f"🌏 {row['stores_overseas']} overseas")
        
        with col_investment:
            st.write(f"💰 {row['investment_usd']}")
            fee_val = f"${int(row['franchise_fee_usd']):,}" if pd.notna(row['franchise_fee_usd']) else 'N/A'
            st.write(f"Fee: {fee_val}")
        
        with col_button:
            if st.button("🔍 View Details", key=f"view_{idx}"):
                st.session_state['selected_brand'] = brand_name
                st.switch_page("pages/3_Brand_Profile.py")
        
        st.markdown("---")

# Keep rest of your code (email capture, AI form, etc.)
st.markdown("---")
st.caption("© 2026 JXPerience | Japanese Franchise Overseas Expansion Platform")
