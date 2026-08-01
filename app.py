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

# Custom styling
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
    .brand-logo {
        width: 50px;
        height: 50px;
        border-radius: 8px;
        object-fit: contain;
        background: white;
        padding: 5px;
        border: 1px solid #e0e0e0;
    }
    .brand-initial {
        width: 50px;
        height: 50px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.2rem;
        color: white;
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

# ========== IMPROVED LOGO FUNCTION ==========
def get_brand_logo_url(brand_name, website=None):
    """
    Get brand logo using multiple reliable sources
    Returns URL or None
    """
    # Method 1: Brandfetch API (free, no key needed, very reliable)
    if brand_name:
        brand_slug = brand_name.replace(' ', '').lower()
        brandfetch_url = f"https://cdn.brandfetch.io/{brand_slug}/logo.png"
        # Test if URL works
        try:
            response = requests.head(brandfetch_url, timeout=3)
            if response.status_code == 200:
                return brandfetch_url
        except:
            pass
    
    # Method 2: Clearbit Logo API
    if website and pd.notna(website):
        domain = str(website).replace('https://', '').replace('http://', '').split('/')[0]
        if domain:
            clearbit_url = f"https://logo.clearbit.com/{domain}"
            try:
                response = requests.head(clearbit_url, timeout=3)
                if response.status_code == 200:
                    return clearbit_url
            except:
                pass
    
    # Method 3: Google favicon
    if website and pd.notna(website):
        domain = str(website).replace('https://', '').replace('http://', '').split('/')[0]
        if domain:
            return f"https://www.google.com/s2/favicons?domain={domain}&sz=128"
    
    return None

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

st.subheader(f"💎 Found {len(filtered_df)} Brands")

st.markdown("""
    <div class="disclaimer-box">
        <strong>ℹ️ Disclaimer:</strong> All information sourced from public data. JXPerience is not officially affiliated with listed brands.
    </div>
""", unsafe_allow_html=True)

st.markdown("### 📊 Franchise Directory")

# Display with logos
for idx, row in filtered_df.iterrows():
    brand_name = row['brand_name']
    website = row.get('website', '')
    logo_url = get_brand_logo_url(brand_name, website)
    initials = get_brand_initials(brand_name)
    brand_color = get_brand_color(brand_name)
    
    col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 1])
    
    with col1:
        if logo_url:
            # Use st.image with error handling
            try:
                st.image(logo_url, width=50, use_column_width=False, output_format='auto')
            except Exception as e:
                # Fallback to initials
                st.markdown(f"""
                    <div class="brand-initial" style="background-color: {brand_color};">
                        {initials}
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="brand-initial" style="background-color: {brand_color};">
                    {initials}
                </div>
            """, unsafe_allow_html=True)
    
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

# Rest of the code (email capture, AI form, etc.) remains the same...
# [Keep all the existing code from your current app.py below this point]

st.markdown("---")
st.markdown("<div style='text-align: center; color: #888; font-size: 0.85rem;'>© 2026 <span style='color:#0066cc'>JX</span>Perience | Japanese Franchise Overseas Expansion Platform</div>", unsafe_allow_html=True)
