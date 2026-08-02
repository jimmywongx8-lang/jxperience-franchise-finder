import streamlit as st
import pandas as pd

st.set_page_config(page_title="Brand Profile | JXPerience", page_icon="🔴", layout="wide")

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

# Back button
if st.button("⬅️ Back to All Brands"):
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

# Get initials and color
initials = get_brand_initials(brand_name)
brand_color = get_brand_color(brand_name)

# Header with colored logo
col_logo, col_info = st.columns([1, 5])
with col_logo:
    st.markdown(f"""
        <div style="width:120px;height:120px;border-radius:12px;background-color:{brand_color};
                    display:flex;align-items:center;justify-content:center;
                    color:white;font-weight:bold;font-size:3rem;
                    box-shadow:0 2px 8px rgba(0,0,0,0.1);">
            {initials}
        </div>
    """, unsafe_allow_html=True)

with col_info:
    st.title(brand_data['brand_name'])
    st.caption(f"{brand_data['category']}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Stores in Japan", brand_data['stores_japan'])
    with col2:
        st.metric("Overseas Stores", brand_data['stores_overseas'])
    with col3:
        st.metric("Expansion Status", brand_data['overseas_franchise_confirmed'])

st.markdown("---")

# Investment Overview
st.subheader("💰 Investment Overview")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Investment", brand_data['investment_usd'], "USD")
with col2:
    fee = int(brand_data['franchise_fee_usd']) if pd.notna(brand_data['franchise_fee_usd']) else 0
    st.metric("Franchise Fee", f"${fee:,}", "One-time fee")
with col3:
    royalty = brand_data['royalty_pct'] if pd.notna(brand_data['royalty_pct']) else 'N/A'
    st.metric("Royalty Fee", f"{royalty}%", "Monthly")

# About
if pd.notna(brand_data.get('notes', '')) and brand_data.get('notes', '') != '':
    st.subheader(" About This Brand")
    st.info(brand_data['notes'])

# Expansion Info
st.subheader("🌍 Expansion Information")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Target Markets**")
    st.write(brand_data['target_markets'])
    
    exp_type = brand_data.get('expansion_type', 'Single-unit') if 'expansion_type' in brand_data else 'Single-unit'
    st.markdown("**Expansion Type**")
    st.write(exp_type)

with col2:
    website = brand_data['website'] if pd.notna(brand_data['website']) else ''
    st.markdown("**Website**")
    if website:
        st.markdown(f"[🔗 {website}](https://{website})")
    else:
        st.write("N/A")
    
    status = brand_data.get('franchise_status', 'N/A')
    st.markdown("**Verification Status**")
    st.write(status if status else 'N/A')

# CTA
st.markdown("---")
st.info(" **Ready to Learn More?** Get the complete investment prospectus and connect directly with the franchisor.")

col1, col2 = st.columns(2)
with col1:
    if st.button("📊 Get AI Assessment", use_container_width=True):
        st.session_state['selected_brand'] = brand_data['brand_name']
        st.switch_page("app.py")
with col2:
    if st.button(" Contact Franchisor", use_container_width=True):
        st.session_state['selected_brand'] = brand_data['brand_name']
        st.switch_page("app.py")

st.markdown("---")
st.caption("© 2026 JXPerience")
