import streamlit as st
import pandas as pd
from openai import OpenAI
import json

st.set_page_config(
    page_title="JXPerience | Japanese Franchise Expansion Platform", 
    page_icon="🔴",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header { font-size: 2.5rem; font-weight: 700; color: #1f1f1f; }
    .brand-accent { color: #0066cc; }
    .metric-card {
        background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);
        color: white; padding: 20px; border-radius: 12px; text-align: center;
    }
    .brand-card {
        background: white; border-radius: 12px; padding: 20px; margin: 15px 0;
        border-left: 5px solid; box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .brand-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .brand-logo {
        width: 70px; height: 70px; border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        color: white; font-weight: bold; font-size: 1.8rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .filter-section {
        background: #f8f9fa; padding: 20px; border-radius: 12px;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
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
    st.markdown('<div class="metric-card"><div style="font-size:2.5rem;font-weight:700;">63+</div><div>Japanese Franchises Analyzed</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card"><div style="font-size:2.5rem;font-weight:700;">$100k-$800k</div><div>Investment Range (USD)</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card"><div style="font-size:2.5rem;font-weight:700;">15+</div><div>Target Markets</div></div>', unsafe_allow_html=True)

st.markdown("---")

# Sidebar with Advanced Filters
st.sidebar.header("🔍 Search & Filters")
search_term = st.sidebar.text_input("Search brand name...", placeholder="Type brand name...")

st.sidebar.markdown("---")
st.sidebar.header(" Discovery Mode")
display_mode = st.sidebar.radio("Show:", ["💎 Hidden Gems (<50 overseas)", "📋 All Brands (A-Z)", "✅ Verified Only"])

# ========== ADVANCED FILTERS (Step 3) ==========
st.sidebar.markdown("---")
st.sidebar.header("📊 Advanced Filters")

# Investment Range Slider
investment_range = st.sidebar.slider(
    "Investment Range (USD)",
    min_value=100000,
    max_value=800000,
    value=(100000, 800000),
    step=50000,
    format="$%d"
)

# Royalty Percentage Filter
royalty_filter = st.sidebar.slider(
    "Royalty Fee (%)",
    min_value=0.0,
    max_value=10.0,
    value=(0.0, 10.0),
    step=0.5
)

# Target Markets
target_markets = st.sidebar.multiselect(
    "Target Markets",
    options=["USA", "SE Asia", "Europe", "China", "Australia"],
    default=[]
)

# Store Count Filter
store_count_filter = st.sidebar.slider(
    "Japan Store Count",
    min_value=0,
    max_value=1000,
    value=(0, 1000),
    step=50
)

# Sort Options
sort_by = st.sidebar.selectbox(
    "Sort By",
    ["Brand Name (A-Z)", "Investment (Low-High)", "Investment (High-Low)", 
     "Franchise Fee (Low-High)", "Royalty % (Low-High)"]
)

st.sidebar.markdown("---")

# Category Filter
st.sidebar.header("️ Filter by Category")
selected_category = st.sidebar.multiselect(
    "Select categories:", 
    options=df['category'].unique(), 
    default=df['category'].unique()
)

# ========== FILTERING LOGIC ==========
filtered_df = df[df['category'].isin(selected_category)].copy()

# Apply investment range filter
def parse_investment_range(inv_str):
    try:
        if '-' in str(inv_str):
            min_inv = int(str(inv_str).replace('k', '000').replace('-', '').split('-')[0])
            max_inv = int(str(inv_str).replace('k', '000').replace('-', '').split('-')[1])
            return min_inv, max_inv
        return 0, 1000000
    except:
        return 0, 1000000

# Filter by investment range
filtered_df['min_investment'] = filtered_df['investment_usd'].apply(lambda x: parse_investment_range(x)[0])
filtered_df['max_investment'] = filtered_df['investment_usd'].apply(lambda x: parse_investment_range(x)[1])
filtered_df = filtered_df[
    (filtered_df['max_investment'] >= investment_range[0]) & 
    (filtered_df['min_investment'] <= investment_range[1])
]

# Filter by royalty
filtered_df = filtered_df[
    (filtered_df['royalty_pct'] >= royalty_filter[0]) & 
    (filtered_df['royalty_pct'] <= royalty_filter[1])
]

# Filter by target markets
if target_markets:
    def check_market(row_markets):
        return any(market in str(row_markets) for market in target_markets)
    filtered_df = filtered_df[filtered_df['target_markets'].apply(check_market)]

# Filter by store count
filtered_df = filtered_df[
    (filtered_df['stores_japan'].str.extract('(\d+)')[0].astype(int) >= store_count_filter[0]) &
    (filtered_df['stores_japan'].str.extract('(\d+)')[0].astype(int) <= store_count_filter[1])
]

# Apply Hidden Gems filter
if "Hidden Gems" in display_mode:
    overseas_nums = pd.to_numeric(filtered_df['stores_overseas'].str.extract('(\d+)')[0], errors='coerce').fillna(999)
    filtered_df = filtered_df[overseas_nums < 50]
elif "Verified Only" in display_mode:
    filtered_df = filtered_df[filtered_df['overseas_franchise_confirmed'] == 'YES']

# Apply sorting
if "Investment (Low-High)" in sort_by:
    filtered_df = filtered_df.sort_values('min_investment')
elif "Investment (High-Low)" in sort_by:
    filtered_df = filtered_df.sort_values('min_investment', ascending=False)
elif "Franchise Fee (Low-High)" in sort_by:
    filtered_df = filtered_df.sort_values('franchise_fee_usd')
elif "Royalty % (Low-High)" in sort_by:
    filtered_df = filtered_df.sort_values('royalty_pct')
else:
    filtered_df = filtered_df.sort_values('brand_name')

# Apply search
if search_term:
    filtered_df = filtered_df[filtered_df['brand_name'].str.contains(search_term, case=False, na=False)]

# Display count
st.subheader(f"💎 Found {len(filtered_df)} Brands")

st.info("️ **Disclaimer:** All information sourced from public data. JXPerience is not officially affiliated with listed brands.")

# ========== IMPROVED BRAND CARDS (Step 4) ==========
st.markdown("###  Franchise Directory")

for idx, row in filtered_df.iterrows():
    brand_name = row['brand_name']
    initials = get_brand_initials(brand_name)
    brand_color = get_brand_color(brand_name)
    
    # Improved brand card layout
    with st.container():
        col_logo, col_content, col_button = st.columns([1, 4, 1])
        
        with col_logo:
            st.markdown(f"""
                <div class="brand-logo" style="background-color:{brand_color};">
                    {initials}
                </div>
            """, unsafe_allow_html=True)
        
        with col_content:
            st.markdown(f"""
                <div style="border-left:4px solid {brand_color}; padding-left:15px;">
                    <h3 style="margin:0 0 5px 0; color:#1f1f1f;">{brand_name}</h3>
                    <p style="margin:0; color:#666; font-size:0.9rem;">{row['category']}</p>
                    <div style="margin-top:10px; display:flex; gap:15px; flex-wrap:wrap;">
                        <span style="background:#f0f0f0; padding:4px 12px; border-radius:20px; font-size:0.85rem;">
                            🇯🇵 {row['stores_japan']} stores
                        </span>
                        <span style="background:#f0f0f0; padding:4px 12px; border-radius:20px; font-size:0.85rem;">
                             {row['stores_overseas']} overseas
                        </span>
                        <span style="background:#fff3cd; padding:4px 12px; border-radius:20px; font-size:0.85rem;">
                            💰 {row['investment_usd']}
                        </span>
                        <span style="background:#e3f2fd; padding:4px 12px; border-radius:20px; font-size:0.85rem;">
                            Fee: ${int(row['franchise_fee_usd']):,}
                        </span>
                        <span style="background:#e8f5e9; padding:4px 12px; border-radius:20px; font-size:0.85rem;">
                            {row['royalty_pct']}% royalty
                        </span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col_button:
            if st.button("🔍 View Details", key=f"view_{idx}", use_container_width=True):
                st.session_state['selected_brand'] = brand_name
                st.switch_page("pages/3_Brand_Profile.py")
        
        st.markdown("---")

# ========== INVESTMENT CALCULATOR (Step 2) ==========
st.markdown("---")
st.markdown("### 💰 Investment Calculator")
st.markdown("Calculate your potential ROI and break-even timeline")

with st.expander("📊 Open Investment Calculator", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Your Investment Details")
        calc_investment = st.number_input("Total Investment ($)", min_value=100000, max_value=1000000, value=300000, step=10000)
        calc_revenue = st.number_input("Expected Monthly Revenue ($)", min_value=10000, max_value=200000, value=50000, step=5000)
        calc_margin = st.slider("Profit Margin (%)", min_value=5, max_value=30, value=15)
        calc_royalty = st.number_input("Royalty Fee (%)", min_value=0.0, max_value=10.0, value=5.0, step=0.5)
    
    with col2:
        st.subheader("Results")
        
        # Calculate metrics
        monthly_profit = calc_revenue * (calc_margin / 100)
        monthly_royalty = calc_revenue * (calc_royalty / 100)
        net_monthly_profit = monthly_profit - monthly_royalty
        break_even_months = calc_investment / net_monthly_profit if net_monthly_profit > 0 else 0
        break_even_years = break_even_months / 12
        annual_roi = (net_monthly_profit * 12 / calc_investment) * 100
        
        st.metric("Monthly Profit (Before Royalty)", f"${monthly_profit:,.0f}")
        st.metric("Monthly Royalty Fee", f"${monthly_royalty:,.0f}")
        st.metric("Net Monthly Profit", f"${net_monthly_profit:,.0f}")
        st.metric("Break-Even Time", f"{break_even_months:.1f} months ({break_even_years:.1f} years)")
        st.metric("Annual ROI", f"{annual_roi:.1f}%")
        
        if annual_roi > 20:
            st.success("✅ Excellent ROI potential!")
        elif annual_roi > 15:
            st.info("ℹ️ Good ROI potential")
        else:
            st.warning("⚠️ Consider negotiating better terms")

# Footer
st.markdown("---")
st.caption("© 2026 JXPerience | Japanese Franchise Overseas Expansion Platform")
