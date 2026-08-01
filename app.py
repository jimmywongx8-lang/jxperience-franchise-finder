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

# Custom styling - Blue Theme
st.markdown("""
    <style>
    .main-header { font-size: 2.5rem; font-weight: 700; color: #1f1f1f; }
    .brand-accent { color: #0066cc; }
    .stat-card {
        background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);
        color: white; padding: 20px; border-radius: 12px; text-align: center; margin: 10px;
    }
    .stat-number { font-size: 2rem; font-weight: 700; display: block; }
    .stat-label { font-size: 0.85rem; opacity: 0.9; }
    .disclaimer-box {
        background-color: #fff3cd; border-left: 4px solid #ffc107;
        padding: 12px 16px; margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header"><span class="brand-accent">JX</span>Perience</div>', unsafe_allow_html=True)
st.markdown("### Japanese Franchise Overseas Expansion Platform")
st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

# Load data
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

# Helper
def get_confidence_badge(confidence):
    if confidence == "YES": return "✅ Confirmed"
    elif confidence == "PROBABLE": return "🟡 Probable"
    elif confidence == "NEEDS_VERIFICATION": return "⚠️ Verify"
    return "❌ No"

df['franchise_status'] = df['overseas_franchise_confirmed'].apply(get_confidence_badge)

# API Key
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    st.warning("⚠️ API Key not configured.")

client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")

# Hero Section
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="stat-card"><span class="stat-number">63+</span><span class="stat-label">Japanese Franchises<br/>Analyzed</span></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="stat-card"><span class="stat-number">$100k-$800k</span><span class="stat-label">Investment Range<br/>(USD)</span></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="stat-card"><span class="stat-number">15+</span><span class="stat-label">Target Markets</span></div>', unsafe_allow_html=True)

st.markdown("---")

# Sidebar
st.sidebar.header(" Search")
search_term = st.sidebar.text_input("", placeholder="Type brand name...")

st.sidebar.header("💎 Discovery Mode")
display_mode = st.sidebar.radio("Show:", ["💎 Hidden Gems (<50 overseas)", "📋 All Brands (A-Z)", "✅ Verified Only"])

st.sidebar.header(" Sort By")
sort_by = st.sidebar.selectbox("Primary sort:", ["Brand Name (A-Z)", "Investment (Low-High)", "Investment (High-Low)", "Franchise Fee (Low-High)"])

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

# Display
st.subheader(f"💎 Found {len(filtered_df)} Brands")

st.markdown("""
    <div class="disclaimer-box">
        <strong>ℹ️ Disclaimer:</strong> All information sourced from public data. JXPerience is not officially affiliated with listed brands.
    </div>
""", unsafe_allow_html=True)

st.markdown("### 📊 Franchise Directory")

# Display with proper navigation buttons
for idx, row in filtered_df.iterrows():
    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
    
    with col1:
        st.markdown(f"**{row['brand_name']}**")
        st.caption(row['category'])
    
    with col2:
        st.write(f"🇯🇵 {row['stores_japan']} stores")
        st.write(f" {row['stores_overseas']} overseas")
    
    with col3:
        st.write(f"💰 {row['investment_usd']}")
        fee_val = f"${int(row['franchise_fee_usd']):,}" if pd.notna(row['franchise_fee_usd']) else 'N/A'
        st.write(f"Fee: {fee_val}")
    
    with col4:
        # Use st.page_link for proper navigation
        st.page_link(
            "pages/3_Brand_Profile.py",
            label="🔍 View Details",
            icon="🔍"
        )
        # Store the brand name in session state when clicked
        st.session_state[f'brand_{idx}'] = row['brand_name']

# Check if any brand button was clicked
for idx in range(len(filtered_df)):
    if st.session_state.get(f'brand_{idx}'):
        st.session_state['selected_brand'] = st.session_state[f'brand_{idx}']
        st.switch_page("pages/3_Brand_Profile.py")

# Rest of your AI assessment and inquiry forms here...
# (Keep the existing code from your current app.py)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #888;'>© 2026 JXPerience</div>", unsafe_allow_html=True)
