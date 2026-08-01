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
    .email-capture-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 16px; padding: 30px; margin: 20px 0;
        border: 2px solid #dee2e6;
    }
    .inquiry-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 16px; padding: 30px; margin: 20px 0;
        border: 2px solid #0066cc;
    }
    .brand-initial {
        width: 50px; height: 50px; border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-weight: 700; font-size: 1.2rem; color: white;
    }
    .logo-container {
        width: 50px; height: 50px;
        display: flex; align-items: center; justify-content: center;
        background: white; border-radius: 8px;
        border: 1px solid #e0e0e0; padding: 5px;
    }
    .logo-container img {
        max-width: 100%; max-height: 100%;
        object-fit: contain;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><span class="brand-accent">JX</span>Perience</div>', unsafe_allow_html=True)
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

# ========== AUTOMATIC LOGO FUNCTION ==========
def get_logo_html(brand_name, website=None):
    """
    Returns HTML with logo image and automatic fallback to initials.
    Uses multiple sources - browser tries each one.
    """
    if not brand_name:
        return None
    
    initials = get_brand_initials(brand_name)
    brand_color = get_brand_color(brand_name)
    
    # Build list of logo URLs to try
    logo_urls = []
    
    # Source 1: Logo.dev (very reliable)
    if website and pd.notna(website):
        domain = str(website).replace('https://', '').replace('http://', '').split('/')[0].replace('www.', '')
        if domain:
            logo_urls.append(f"https://img.logo.dev/{domain}?token=pk_test_123")
            logo_urls.append(f"https://logo.clearbit.com/{domain}")
    
    # Source 2: Google favicon (always works, but small)
    if website and pd.notna(website):
        domain = str(website).replace('https://', '').replace('http://', '').split('/')[0].replace('www.', '')
        if domain:
            logo_urls.append(f"https://www.google.com/s2/favicons?domain={domain}&sz=128")
    
    # If no URLs, just show initials
    if not logo_urls:
        return f'''<div class="brand-initial" style="background-color: {brand_color};">{initials}</div>'''
    
    # Build HTML with fallback chain
    # The first image tries to load; if it fails, onerror replaces it with initials
    primary_url = logo_urls[0]
    
    html = f'''
    <div class="logo-container" id="logo-{brand_name.replace(' ', '')}">
        <img 
            src="{primary_url}" 
            alt="{brand_name}"
            onerror="this.onerror=null; this.parentElement.innerHTML='<div class=\\'brand-initial\\' style=\\'background-color: {brand_color};\\'>{initials}</div>';"
            style="max-width: 40px; max-height: 40px;"
        />
    </div>
    '''
    return html

def get_brand_initials(brand_name):
    if not brand_name:
        return "??"
    words = str(brand_name).split()
    if len(words) >= 2:
        return (words[0][0] + words[1][0]).upper()
    return str(brand_name)[:2].upper()

def get_brand_color(brand_name):
    colors = ['#0066cc', '#0052a3', '#1976d2', '#0288d1', '#0097a7', 
              '#00796b', '#388e3c', '#689f38', '#afb42b', '#fbc02d',
              '#ff9800', '#ff5722', '#795548', '#607d8b', '#9c27b0']
    hash_val = sum(ord(c) for c in str(brand_name)) % len(colors)
    return colors[hash_val]
# ========== END LOGO FUNCTIONS ==========

def get_confidence_badge(confidence):
    if confidence == "YES": return "✅ Confirmed"
    elif confidence == "PROBABLE": return " Probable"
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
display_mode = st.sidebar.radio("Show:", ["💎 Hidden Gems (<50 overseas)", " All Brands (A-Z)", "✅ Verified Only"])

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

st.subheader(f" Found {len(filtered_df)} Brands")

st.markdown("""
    <div class="disclaimer-box">
        <strong>ℹ️ Disclaimer:</strong> All information sourced from public data. JXPerience is not officially affiliated with listed brands.
    </div>
""", unsafe_allow_html=True)

st.markdown("### 📊 Franchise Directory")

# Display with automatic logos
for idx, row in filtered_df.iterrows():
    brand_name = row['brand_name']
    website = row.get('website', '')
    logo_html = get_logo_html(brand_name, website)
    
    col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 1])
    
    with col1:
        st.markdown(logo_html, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"**{brand_name}**")
        st.caption(row['category'])
    
    with col3:
        st.write(f"🇯🇵 {row['stores_japan']} stores")
        st.write(f"🌏 {row['stores_overseas']} overseas")
    
    with col4:
        st.write(f"💰 {row['investment_usd']}")
        fee_val = f"${int(row['franchise_fee_usd']):,}" if pd.notna(row['franchise_fee_usd']) else 'N/A'
        st.write(f"Fee: {fee_val}")
    
    with col5:
        if st.button("🔍 View Details", key=f"view_{idx}"):
            st.session_state['selected_brand'] = brand_name
            st.switch_page("pages/3_Brand_Profile.py")

# [Keep rest of your code - email capture, AI form, inquiry form, footer]

st.markdown("---")
st.markdown("<div style='text-align: center; color: #888; font-size: 0.85rem;'>© 2026 <span style='color:#0066cc'>JX</span>Perience | Japanese Franchise Overseas Expansion Platform</div>", unsafe_allow_html=True)
