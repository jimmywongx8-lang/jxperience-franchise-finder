import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(page_title="JXPerience", page_icon="🔴", layout="wide")

# Custom CSS for scroll to top button
st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);
        color: white; padding: 20px; border-radius: 12px; text-align: center;
    }
    .brand-logo {
        width: 70px; height: 70px; border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        color: white; font-weight: bold; font-size: 1.8rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .scroll-to-top {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #0066cc;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        cursor: pointer;
        z-index: 1000;
    }
    </style>
""", unsafe_allow_html=True)

# Scroll to top button
if st.button("⬆️ Top", key="scroll_top"):
    st.markdown("<script>window.scrollTo(0, 0)</script>", unsafe_allow_html=True)

st.title(" JXPerience")
st.markdown("### Japanese Franchise Overseas Expansion Platform")

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

# Initialize calculator state
if 'calc_reset' not in st.session_state:
    st.session_state.calc_reset = False

def get_brand_initials(brand_name):
    words = str(brand_name).split()
    if len(words) >= 2:
        return (words[0][0] + words[1][0]).upper()
    return str(brand_name)[:2].upper()

def get_brand_color(brand_name):
    colors = ['#0066cc', '#0052a3', '#1976d2', '#0288d1', '#0097a7', 
              '#00796b', '#388e3c', '#689f38', '#afb42b', '#fbc02d']
    return colors[sum(ord(c) for c in str(brand_name)) % len(colors)]

# Hero metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="metric-card"><div style="font-size:2.5rem;font-weight:700;">63+</div><div>Japanese Franchises Analyzed</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card"><div style="font-size:2.5rem;font-weight:700;">$100k-$800k</div><div>Investment Range (USD)</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card"><div style="font-size:2.5rem;font-weight:700;">15+</div><div>Target Markets</div></div>', unsafe_allow_html=True)

st.markdown("---")

# Sidebar with ADVANCED FILTERS
st.sidebar.header(" Advanced Filters")

# Investment Range Slider
investment_range = st.sidebar.slider(
    "Investment Range (USD)",
    min_value=100000, max_value=800000,
    value=(100000, 800000), step=50000
)

# Royalty Filter
royalty_filter = st.sidebar.slider(
    "Royalty Fee (%)",
    min_value=0.0, max_value=10.0,
    value=(0.0, 10.0), step=0.5
)

# Target Markets
target_markets = st.sidebar.multiselect(
    "Target Markets",
    options=["USA", "SE Asia", "Europe", "China", "Australia"],
    default=[]
)

# Store Count
store_filter = st.sidebar.slider(
    "Japan Stores",
    min_value=0, max_value=1000,
    value=(0, 1000), step=50
)

# Sort
sort_by = st.sidebar.selectbox("Sort By", [
    "Brand Name (A-Z)", "Investment (Low-High)", 
    "Investment (High-Low)", "Franchise Fee (Low-High)"
])

# Categories
selected_category = st.sidebar.multiselect(
    "Category", 
    options=df['category'].unique(), 
    default=df['category'].unique()
)

# Filter data
filtered_df = df[df['category'].isin(selected_category)].copy()

# Apply investment filter - FIXED: Handle missing columns
try:
    filtered_df['min_inv'] = filtered_df['investment_usd'].str.extract('(\d+)')[0].fillna('0').astype(int)
    filtered_df = filtered_df[
        (filtered_df['min_inv'] >= investment_range[0]) & 
        (filtered_df['min_inv'] <= investment_range[1])
    ]
except:
    pass  # Skip if column doesn't exist

# Apply royalty filter
try:
    filtered_df = filtered_df[
        (filtered_df['royalty_pct'] >= royalty_filter[0]) & 
        (filtered_df['royalty_pct'] <= royalty_filter[1])
    ]
except:
    pass

# Apply target market filter
if target_markets:
    try:
        filtered_df = filtered_df[filtered_df['target_markets'].apply(
            lambda x: any(m in str(x) for m in target_markets)
        )]
    except:
        pass

# Apply store filter - FIXED: Handle missing columns
try:
    filtered_df['stores_num'] = filtered_df['stores_japan'].str.extract('(\d+)')[0].fillna('0').astype(int)
    filtered_df = filtered_df[
        (filtered_df['stores_num'] >= store_filter[0]) & 
        (filtered_df['stores_num'] <= store_filter[1])
    ]
except:
    pass

# Sort
if "Investment (Low-High)" in sort_by:
    try:
        filtered_df = filtered_df.sort_values('min_inv')
    except:
        pass
elif "Investment (High-Low)" in sort_by:
    try:
        filtered_df = filtered_df.sort_values('min_inv', ascending=False)
    except:
        pass
else:
    filtered_df = filtered_df.sort_values('brand_name')

st.subheader(f"💎 Found {len(filtered_df)} Brands")

# BRAND CARDS
for idx, row in filtered_df.iterrows():
    brand_name = row['brand_name']
    initials = get_brand_initials(brand_name)
    brand_color = get_brand_color(brand_name)
    
    with st.container():
        col_logo, col_content, col_btn = st.columns([1, 4, 1])
        
        with col_logo:
            st.markdown(f"""
                <div class="brand-logo" style="background-color:{brand_color};">
                    {initials}
                </div>
            """, unsafe_allow_html=True)
        
        with col_content:
            st.markdown(f"**{brand_name}**")
            st.caption(row['category'])
            st.write(f"🇯🇵 {row['stores_japan']} stores | 🌏 {row['stores_overseas']} overseas")
            st.write(f"💰 {row['investment_usd']} | Fee: ${int(row['franchise_fee_usd']):,} | {row['royalty_pct']}% royalty")
        
        with col_btn:
            if st.button("🔍 View Details", key=f"view_{idx}"):
                st.session_state['selected_brand'] = brand_name
                st.switch_page("pages/3_Brand_Profile.py")
        
        st.markdown("---")

# INVESTMENT CALCULATOR with RESET button
st.markdown("---")
st.markdown("### 💰 Investment Calculator")

calc_col1, calc_col2 = st.columns([2, 1])
with calc_col1:
    calculator_expanded = st.expander("Open Calculator", expanded=False)

with calculator_expanded:
    # Reset button
    if st.button("🔄 Reset Calculator"):
        st.session_state.calc_reset = not st.session_state.calc_reset
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Use unique keys for reset functionality
        reset_key = st.session_state.calc_reset
        investment = st.number_input("Total Investment ($)", value=300000, step=10000, key=f"inv_{reset_key}")
        revenue = st.number_input("Monthly Revenue ($)", value=50000, step=5000, key=f"rev_{reset_key}")
        margin = st.slider("Profit Margin (%)", 5, 30, 15, key=f"margin_{reset_key}")
        royalty = st.number_input("Royalty (%)", 0.0, 10.0, 5.0, key=f"roy_{reset_key}")
    
    with col2:
        monthly_profit = revenue * (margin / 100)
        monthly_royalty = revenue * (royalty / 100)
        net_profit = monthly_profit - monthly_royalty
        break_even = investment / net_profit if net_profit > 0 else 0
        roi = (net_profit * 12 / investment) * 100
        
        st.metric("Monthly Profit", f"${monthly_profit:,.0f}")
        st.metric("Net Profit (after royalty)", f"${net_profit:,.0f}")
        st.metric("Break-Even", f"{break_even:.1f} months")
        st.metric("Annual ROI", f"{roi:.1f}%")
        
        if roi > 20:
            st.success("✅ Excellent ROI!")
        elif roi > 15:
            st.info("️ Good ROI")
        else:
            st.warning("⚠️ Low ROI")

st.caption("© 2026 JXPerience")
