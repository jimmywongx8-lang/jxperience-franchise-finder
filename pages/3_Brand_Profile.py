import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Brand Profile | JXPerience",
    page_icon="🔴",
    layout="wide"
)

# Custom styling
st.markdown("""
    <style>
    .brand-header {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 30px;
        border-radius: 16px;
        margin-bottom: 30px;
        border-left: 6px solid #0066cc;
    }
    .brand-name {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0066cc;
        margin-bottom: 10px;
    }
    .info-card {
        background: white;
        border-radius: 12px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e0e0e0;
    }
    .info-card h3 {
        color: #0066cc;
        margin-top: 0;
        border-bottom: 2px solid #e3f2fd;
        padding-bottom: 10px;
    }
    .stat-box {
        display: inline-block;
        background: #f5f5f5;
        padding: 15px 25px;
        border-radius: 8px;
        margin: 5px;
        text-align: center;
    }
    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0066cc;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #666;
    }
    .cta-button {
        background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);
        color: white;
        padding: 15px 30px;
        border-radius: 8px;
        text-decoration: none;
        display: inline-block;
        font-weight: 600;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    paths_to_try = [
        "C:\\jfa_scraper\\franchise_data.csv",
        "franchise_data.csv",
        "/mount/src/jxperience-franchise-finder/franchise_data.csv"
    ]
    
    for path in paths_to_try:
        try:
            df = pd.read_csv(path)
            return df
        except FileNotFoundError:
            continue
    
    return pd.DataFrame()

df = load_data()

# Navigation
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("⬅️ Back to All Brands"):
        st.switch_page("app.py")

# Get brand from URL parameter or session state
if 'selected_brand' in st.session_state:
    brand_name = st.session_state['selected_brand']
elif 'brand' in st.query_params:
    brand_name = st.query_params['brand']
else:
    st.warning("Please select a brand from the main page")
    st.stop()

# Find brand data
if not df.empty:
    brand_data = df[df['brand_name'].str.lower() == brand_name.lower()]
    if brand_data.empty:
        st.error(f"Brand '{brand_name}' not found")
        st.stop()
    brand_data = brand_data.iloc[0]
else:
    st.error("No data loaded")
    st.stop()

# Header Section
st.markdown(f"""
    <div class="brand-header">
        <div class="brand-name">{brand_data['brand_name']}</div>
        <div style="font-size: 1.1rem; color: #666;">{brand_data['category']}</div>
        <div style="margin-top: 15px;">
            <span class="stat-box">
                <div class="stat-value">{brand_data['stores_japan']}</div>
                <div class="stat-label">Stores in Japan</div>
            </span>
            <span class="stat-box">
                <div class="stat-value">{brand_data['stores_overseas']}</div>
                <div class="stat-label">Overseas Stores</div>
            </span>
            <span class="stat-box">
                <div class="stat-value">{brand_data['overseas_franchise_confirmed']}</div>
                <div class="stat-label">Expansion Status</div>
            </span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Investment Details
st.markdown("###  Investment Overview")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="info-card">
            <h3>Total Investment</h3>
            <div style="font-size: 1.8rem; font-weight: 700; color: #0066cc;">
                ${brand_data['investment_usd']}
            </div>
            <div style="color: #666; margin-top: 5px;">USD</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="info-card">
            <h3>Franchise Fee</h3>
            <div style="font-size: 1.8rem; font-weight: 700; color: #0066cc;">
                ${int(brand_data['franchise_fee_usd']):,}
            </div>
            <div style="color: #666; margin-top: 5px;">One-time fee</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="info-card">
            <h3>Royalty Fee</h3>
            <div style="font-size: 1.8rem; font-weight: 700; color: #0066cc;">
                {brand_data['royalty_pct']}%
            </div>
            <div style="color: #666; margin-top: 5px;">Monthly</div>
        </div>
    """, unsafe_allow_html=True)

# Brand Story / Notes
if pd.notna(brand_data['notes']) and brand_data['notes'] != '':
    st.markdown("###  About This Brand")
    st.markdown(f"""
        <div class="info-card">
            {brand_data['notes']}
        </div>
    """, unsafe_allow_html=True)

# Expansion Details
st.markdown("### 🌍 Expansion Information")
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
        <div class="info-card">
            <h3>Target Markets</h3>
            <p>{brand_data['target_markets']}</p>
            
            <h3 style="margin-top: 20px;">Expansion Type</h3>
            <p>{brand_data.get('expansion_type', 'Single-unit')}</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="info-card">
            <h3>Website</h3>
            <p><a href="https://{brand_data['website']}" target="_blank" style="color: #0066cc;">
                🔗 {brand_data['website']}
            </a></p>
            
            <h3 style="margin-top: 20px;">Verification Status</h3>
            <p>{brand_data['franchise_status']}</p>
        </div>
    """, unsafe_allow_html=True)

# Call to Action
st.markdown("---")
st.markdown("""
    <div class="info-card" style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); border: 2px solid #0066cc;">
        <h3 style="color: #0066cc;">🚀 Ready to Learn More?</h3>
        <p>Get the complete investment prospectus and connect directly with the franchisor.</p>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("📊 Get AI Assessment", use_container_width=True):
        st.switch_page("app.py")
        st.session_state['selected_brand'] = brand_data['brand_name']
        st.rerun()

with col2:
    if st.button(" Contact Franchisor", use_container_width=True):
        st.switch_page("app.py")
        st.session_state['selected_brand'] = brand_data['brand_name']
        st.rerun()

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888; font-size: 0.85rem;'>© 2026 JXPerience | Japanese Franchise Overseas Expansion Platform</div>", unsafe_allow_html=True)
