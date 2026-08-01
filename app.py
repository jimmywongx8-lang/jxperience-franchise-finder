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
    .disclaimer-box {
        background-color: #fff3cd; border-left: 4px solid #ffc107;
        padding: 12px 16px; margin: 20px 0;
    }
    .view-btn {
        background-color: #0066cc; color: white; border: none;
        padding: 8px 16px; border-radius: 6px; cursor: pointer;
        font-weight: 600; text-decoration: none; display: inline-block;
    }
    .view-btn:hover { background-color: #0052a3; }
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
    elif confidence == "PROBABLE": return " Probable"
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
st.sidebar.header("🔍 Search")
search_term = st.sidebar.text_input("", placeholder="Type brand name...")

st.sidebar.header("💎 Discovery Mode")
display_mode = st.sidebar.radio("Show:", ["💎 Hidden Gems (<50 overseas)", "📋 All Brands (A-Z)", "✅ Verified Only"])

st.sidebar.header("📊 Sort By")
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

# Display with clickable links using HTML
for idx, row in filtered_df.iterrows():
    brand_url = f"?brand={row['brand_name'].replace(' ', '%20')}"
    
    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
    
    with col1:
        st.markdown(f"**{row['brand_name']}**")
        st.caption(row['category'])
    
    with col2:
        st.write(f"🇯🇵 {row['stores_japan']} stores")
        st.write(f"🌏 {row['stores_overseas']} overseas")
    
    with col3:
        st.write(f"💰 {row['investment_usd']}")
        fee_val = f"${int(row['franchise_fee_usd']):,}" if pd.notna(row['franchise_fee_usd']) else 'N/A'
        st.write(f"Fee: {fee_val}")
    
    with col4:
        # Use a link instead of switch_page
        st.markdown(f'<a href="{brand_url}" class="view-btn">🔍 View Details</a>', unsafe_allow_html=True)

# Check if brand is selected via URL
if 'brand' in st.query_params:
    brand_name = st.query_params['brand']
    st.session_state['selected_brand'] = brand_name
    
    # Redirect to brand profile page
    st.info(f"🔍 Loading profile for **{brand_name}**...")
    st.markdown(f"""
        <div style="text-align: center; margin: 40px;">
            <a href="/3_Brand_Profile?brand={brand_name}" class="view-btn" style="font-size: 1.2rem; padding: 15px 30px;">
                Click here to view brand profile →
            </a>
        </div>
    """, unsafe_allow_html=True)

# Rest of your AI assessment and inquiry forms here...
# (Keep the existing code)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #888;'>© 2026 JXPerience</div>", unsafe_allow_html=True)
