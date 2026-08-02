import streamlit as st
import pandas as pd

st.set_page_config(page_title="JXPerience", page_icon="🔴", layout="wide")

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
    .info-tag {
        background: #f0f0f0;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        display: inline-block;
        margin: 2px;
    }
    </style>
""", unsafe_allow_html=True)

# Scroll to top
if st.button("⬆️ Top", key="scroll_top"):
    st.markdown("<script>window.scrollTo(0, 0)</script>", unsafe_allow_html=True)

st.title("🔴 JXPerience")
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

if 'filter_reset' not in st.session_state:
    st.session_state.filter_reset = 0
if 'calc_reset' not in st.session_state:
    st.session_state.calc_reset = 0

def get_brand_initials(brand_name):
    words = str(brand_name).split()
    if len(words) >= 2:
        return (words[0][0] + words[1][0]).upper()
    return str(brand_name)[:2].upper()

def get_brand_color(brand_name):
    colors = ['#0066cc', '#0052a3', '#1976d2', '#0288d1', '#0097a7', 
              '#00796b', '#388e3c', '#689f38', '#afb42b', '#fbc02d']
    return colors[sum(ord(c) for c in str(brand_name)) % len(colors)]

def parse_investment_to_min(inv_str):
    try:
        inv_str = str(inv_str).lower().replace(',', '')
        if 'k' in inv_str:
            import re
            match = re.search(r'(\d+)', inv_str)
            if match:
                return int(match.group(1)) * 1000
        return int(inv_str)
    except:
        return 0

def parse_investment_to_max(inv_str):
    try:
        inv_str = str(inv_str).lower().replace(',', '')
        if 'k' in inv_str:
            import re
            matches = re.findall(r'(\d+)', inv_str)
            if matches:
                return int(matches[-1]) * 1000
        return int(inv_str)
    except:
        return 0

# Hero metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="metric-card"><div style="font-size:2.5rem;font-weight:700;">63+</div><div>Japanese Franchises Analyzed</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card"><div style="font-size:2.5rem;font-weight:700;">$100k-$800k</div><div>Investment Range (USD)</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card"><div style="font-size:2.5rem;font-weight:700;">15+</div><div>Target Markets</div></div>', unsafe_allow_html=True)

st.markdown("---")

# Sidebar
st.sidebar.header("🔍 Advanced Filters")

if st.sidebar.button("🔄 Reset All Filters", key=f"reset_filters_{st.session_state.filter_reset}"):
    st.session_state.filter_reset += 1
    st.rerun()

investment_range = st.sidebar.slider(
    "Investment Range (USD)",
    min_value=100000, max_value=800000,
    value=(100000, 800000), step=50000,
    key=f"inv_range_{st.session_state.filter_reset}"
)

royalty_filter = st.sidebar.slider(
    "Royalty Fee (%)",
    min_value=0.0, max_value=10.0,
    value=(0.0, 10.0), step=0.5,
    key=f"royalty_{st.session_state.filter_reset}"
)

target_markets = st.sidebar.multiselect(
    "Target Markets",
    options=["USA", "SE Asia", "Europe", "China", "Australia"],
    default=[],
    key=f"markets_{st.session_state.filter_reset}"
)

store_filter = st.sidebar.slider(
    "Japan Stores",
    min_value=0, max_value=1000,
    value=(0, 1000), step=50,
    key=f"stores_{st.session_state.filter_reset}"
)

sort_by = st.sidebar.selectbox(
    "Sort By",
    ["Brand Name (A-Z)", "Investment (Low-High)", "Investment (High-Low)", "Franchise Fee (Low-High)"],
    key=f"sort_{st.session_state.filter_reset}"
)

selected_category = st.sidebar.multiselect(
    "Category", 
    options=df['category'].unique(), 
    default=df['category'].unique(),
    key=f"category_{st.session_state.filter_reset}"
)

# Filter data
filtered_df = df[df['category'].isin(selected_category)].copy()

filtered_df['min_inv'] = filtered_df['investment_usd'].apply(parse_investment_to_min)
filtered_df['max_inv'] = filtered_df['investment_usd'].apply(parse_investment_to_max)
filtered_df = filtered_df[
    (filtered_df['max_inv'] >= investment_range[0]) & 
    (filtered_df['min_inv'] <= investment_range[1])
]

filtered_df = filtered_df[
    (filtered_df['royalty_pct'] >= royalty_filter[0]) & 
    (filtered_df['royalty_pct'] <= royalty_filter[1])
]

if target_markets:
    filtered_df = filtered_df[filtered_df['target_markets'].apply(
        lambda x: any(m in str(x) for m in target_markets)
    )]

filtered_df['stores_num'] = filtered_df['stores_japan'].str.extract('(\d+)')[0].fillna('0').astype(int)
filtered_df = filtered_df[
    (filtered_df['stores_num'] >= store_filter[0]) & 
    (filtered_df['stores_num'] <= store_filter[1])
]

if "Investment (Low-High)" in sort_by:
    filtered_df = filtered_df.sort_values('min_inv')
elif "Investment (High-Low)" in sort_by:
    filtered_df = filtered_df.sort_values('min_inv', ascending=False)
elif "Franchise Fee (Low-High)" in sort_by:
    filtered_df = filtered_df.sort_values('franchise_fee_usd')
else:
    filtered_df = filtered_df.sort_values('brand_name')

st.subheader(f"💎 Found {len(filtered_df)} Brands")

# ENHANCED BRAND CARDS
for idx, row in filtered_df.iterrows():
    brand_name = row['brand_name']
    initials = get_brand_initials(brand_name)
    brand_color = get_brand_color(brand_name)
    
    # Get enriched data (with fallbacks)
    japan_regions = row.get('japan_regions', '') if 'japan_regions' in row else ''
    overseas_countries = row.get('overseas_countries', '') if 'overseas_countries' in row else ''
    hq_location = row.get('hq_location', '') if 'hq_location' in row else ''
    
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
            
            # Japan stores with regions
            japan_info = f"🇯🇵 {row['stores_japan']} stores"
            if japan_regions and pd.notna(japan_regions):
                japan_info += f" ({japan_regions})"
            
            # Overseas stores with countries
            overseas_info = f"🌏 {row['stores_overseas']} overseas"
            if overseas_countries and pd.notna(overseas_countries):
                overseas_info += f" ({overseas_countries})"
            
            st.write(f"{japan_info} | {overseas_info}")
            
            # HQ Location
            if hq_location and pd.notna(hq_location):
                st.write(f"📍 HQ: {hq_location}")
            
            # Investment info
            st.write(f"💰 {row['investment_usd']} | Fee: ${int(row['franchise_fee_usd']):,} | {row['royalty_pct']}% royalty")
            
            # Target markets as tags
            if row['target_markets'] and pd.notna(row['target_markets']):
                markets = str(row['target_markets']).split(',')
                st.markdown(" ".join([f'<span class="info-tag">🌍 {m.strip()}</span>' for m in markets]), unsafe_allow_html=True)
        
        with col_btn:
            if st.button(" View Details", key=f"view_{idx}"):
                st.session_state['selected_brand'] = brand_name
                st.switch_page("pages/3_Brand_Profile.py")
        
        st.markdown("---")

# INVESTMENT CALCULATOR
st.markdown("---")
st.markdown("### 💰 Investment Calculator")

with st.expander("📊 Open Calculator", expanded=False):
    if st.button("🔄 Reset Calculator", key=f"calc_reset_btn_{st.session_state.calc_reset}"):
        st.session_state.calc_reset += 1
        st.rerun()
    
    col1, col2 = st.columns(2)
    
    with col1:
        investment = st.number_input("Total Investment ($)", value=300000, step=10000, key=f"inv_{st.session_state.calc_reset}")
        revenue = st.number_input("Monthly Revenue ($)", value=50000, step=5000, key=f"rev_{st.session_state.calc_reset}")
        margin = st.slider("Profit Margin (%)", 5, 30, 15, key=f"margin_{st.session_state.calc_reset}")
        royalty = st.number_input("Royalty (%)", 0.0, 10.0, 5.0, key=f"roy_{st.session_state.calc_reset}")
    
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
            st.info("ℹ️ Good ROI")
        else:
            st.warning("⚠️ Low ROI")

st.caption("© 2026 JXPerience")
