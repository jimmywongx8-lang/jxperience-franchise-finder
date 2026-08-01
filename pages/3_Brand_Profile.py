import streamlit as st
import pandas as pd
import os
import requests

st.set_page_config(page_title="Brand Profile | JXPerience", page_icon="", layout="wide")

st.markdown("""
    <style>
    .brand-header {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 30px; border-radius: 16px; margin-bottom: 30px;
        border-left: 6px solid #0066cc;
    }
    .brand-name { font-size: 2.5rem; font-weight: 700; color: #0066cc; }
    .brand-logo-large {
        width: 100px;
        height: 100px;
        border-radius: 12px;
        object-fit: contain;
        background: white;
        padding: 10px;
        border: 2px solid #e0e0e0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .info-card {
        background: white; border-radius: 12px; padding: 25px; margin: 15px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid #e0e0e0;
    }
    .info-card h3 { color: #0066cc; margin-top: 0; border-bottom: 2px solid #e3f2fd; padding-bottom: 10px; }
    .stat-box { display: inline-block; background: #f5f5f5; padding: 15px 25px; border-radius: 8px; margin: 5px; text-align: center; }
    .stat-value { font-size: 1.5rem; font-weight: 700; color: #0066cc; }
    .stat-label { font-size: 0.85rem; color: #666; }
    .brand-initial-large {
        width: 100px;
        height: 100px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 2.5rem;
        color: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# ========== SAME LOGO FUNCTIONS ==========
def get_brand_logo_url(brand_name, website=None):
    """Get brand logo using multiple reliable sources"""
    # Method 1: Brandfetch API
    if brand_name:
        brand_slug = brand_name.replace(' ', '').lower()
        brandfetch_url = f"https://cdn.brandfetch.io/{brand_slug}/logo.png"
        try:
            response = requests.head(brandfetch_url, timeout=3)
            if response.status_code == 200:
                return brandfetch_url
        except:
            pass
    
    # Method 2: Clearbit
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

col1, col2 = st.columns([1, 5])
with col1:
    if st.button("⬅️ Back to All Brands", key="back_button"):
        if 'selected_brand' in st.session_state:
            del st.session_state['selected_brand']
        st.switch_page("app.py")

brand_name = st.session_state.get('selected_brand', '')

if not brand_name or df.empty:
    st.warning("Please select a brand from the main page")
    st.stop()

brand_data = df[df['brand_name'].str.lower() == brand_name.lower()]
if brand_data.empty:
    st.error(f"Brand '{brand_name}' not found")
    st.stop()
brand_data = brand_data.iloc[0]

# Get logo
website = brand_data.get('website', '')
logo_url = get_brand_logo_url(brand_name, website)
initials = get_brand_initials(brand_name)
brand_color = get_brand_color(brand_name)

# Header with Logo
col_logo, col_info = st.columns([1, 4])
with col_logo:
    if logo_url:
        try:
            st.image(logo_url, width=100, use_column_width=False)
        except:
            st.markdown(f"""
                <div class="brand-initial-large" style="background-color: {brand_color};">
                    {initials}
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="brand-initial-large" style="background-color: {brand_color};">
                {initials}
            </div>
        """, unsafe_allow_html=True)

with col_info:
    st.markdown(f"""
        <div class="brand-header">
            <div class="brand-name">{brand_data['brand_name']}</div>
            <div style="font-size: 1.1rem; color: #666;">{brand_data['category']}</div>
            <div style="margin-top: 15px;">
                <span class="stat-box"><div class="stat-value">{brand_data['stores_japan']}</div><div class="stat-label">Stores in Japan</div></span>
                <span class="stat-box"><div class="stat-value">{brand_data['stores_overseas']}</div><div class="stat-label">Overseas Stores</div></span>
                <span class="stat-box"><div class="stat-value">{brand_data['overseas_franchise_confirmed']}</div><div class="stat-label">Expansion Status</div></span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Rest of the profile page code...
st.markdown("### 💰 Investment Overview")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""<div class="info-card"><h3>Total Investment</h3><div style="font-size: 1.8rem; font-weight: 700; color: #0066cc;">{brand_data['investment_usd']}</div><div style="color: #666;">USD</div></div>""", unsafe_allow_html=True)
with col2:
    try:
        fee = int(brand_data['franchise_fee_usd']) if pd.notna(brand_data['franchise_fee_usd']) else 0
    except:
        fee = 0
    st.markdown(f"""<div class="info-card"><h3>Franchise Fee</h3><div style="font-size: 1.8rem; font-weight: 700; color: #0066cc;">${fee:,}</div><div style="color: #666;">One-time fee</div></div>""", unsafe_allow_html=True)
with col3:
    try:
        royalty = brand_data['royalty_pct'] if pd.notna(brand_data['royalty_pct']) else 'N/A'
    except:
        royalty = 'N/A'
    st.markdown(f"""<div class="info-card"><h3>Royalty Fee</h3><div style="font-size: 1.8rem; font-weight: 700; color: #0066cc;">{royalty}%</div><div style="color: #666;">Monthly</div></div>""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #888; font-size: 0.85rem;'>© 2026 JXPerience</div>", unsafe_allow_html=True)
