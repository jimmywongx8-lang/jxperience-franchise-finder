import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64
from datetime import datetime

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
    .compare-info {
        background: #fff3cd;
        padding: 10px 15px;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        font-size: 0.9rem;
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

# ========== COMPARISON FEATURE ==========
if 'brands_to_compare' not in st.session_state:
    st.session_state.brands_to_compare = []
if 'show_comparison' not in st.session_state:
    st.session_state.show_comparison = False

MAX_COMPARE = 3  # Maximum brands to compare

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

# PDF Generation Function
def generate_comparison_pdf(compare_df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Title
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 15, "JXPerience - Brand Comparison", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
    pdf.ln(10)
    
    # Comparison table
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Side-by-Side Comparison", ln=True)
    pdf.set_font("Arial", size=10)
    
    # Headers
    metrics = ['Investment', 'Franchise Fee', 'Royalty', 'Japan Stores', 
               'Overseas', 'Target Markets', 'HQ Location']
    
    col_width = 190 / (len(compare_df) + 1)
    
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(col_width, 10, "Metric", border=1)
    for brand in compare_df['brand_name']:
        pdf.cell(col_width, 10, brand[:15], border=1, align='C')
    pdf.ln()
    
    # Data rows
    pdf.set_font("Arial", size=9)
    for metric in metrics:
        pdf.cell(col_width, 10, metric, border=1)
        for idx, row in compare_df.iterrows():
            if metric == 'Investment':
                value = f"${row['investment_usd']}"
            elif metric == 'Franchise Fee':
                value = f"${int(row['franchise_fee_usd']):,}"
            elif metric == 'Royalty':
                value = f"{row['royalty_pct']}%"
            elif metric == 'Japan Stores':
                value = str(row['stores_japan'])
            elif metric == 'Overseas':
                value = str(row['stores_overseas'])
            elif metric == 'Target Markets':
                value = str(row['target_markets'])[:20]
            elif metric == 'HQ Location':
                value = str(row.get('hq_location', 'N/A'))[:20]
            pdf.cell(col_width, 10, value, border=1, align='C')
        pdf.ln()
    
    return pdf.output(dest='S').encode('latin-1')

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

# ========== COMPARISON TOOLBAR ==========
num_selected = len(st.session_state.brands_to_compare)

if num_selected > 0:
    st.markdown(f"""
    <div style="background:#e3f2fd;padding:20px;border-radius:10px;margin:20px 0;">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
                <strong>📊 Comparing {num_selected} of {MAX_COMPARE} brands:</strong> 
                {', '.join(st.session_state.brands_to_compare)}
            </div>
        </div>
        <div style="margin-top:10px;font-size:0.85rem;color:#666;">
            💡 Tip: Select up to {MAX_COMPARE} brands to compare side-by-side
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📊 View Comparison", use_container_width=True, disabled=num_selected < 2):
            st.session_state.show_comparison = True
            st.rerun()
    with col2:
        if num_selected >= 2:
            compare_df = df[df['brand_name'].isin(st.session_state.brands_to_compare)]
            pdf_bytes = generate_comparison_pdf(compare_df)
            st.download_button(
                label="📄 Export PDF",
                data=pdf_bytes,
                file_name=f"brand_comparison_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    with col3:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.brands_to_compare = []
            st.session_state.show_comparison = False
            st.rerun()
    with col4:
        if st.button("⬅️ Back to Browse", use_container_width=True):
            st.session_state.show_comparison = False
            st.rerun()

# Show comparison view
if st.session_state.show_comparison and num_selected >= 2:
    st.markdown("---")
    st.subheader("📊 Brand Comparison")
    
    compare_df = df[df['brand_name'].isin(st.session_state.brands_to_compare)]
    
    st.markdown("### Side-by-Side Comparison")
    
    comparison_data = {
        'Metric': ['Investment Range', 'Franchise Fee', 'Royalty %', 'Stores in Japan', 
                   'Overseas Stores', 'Target Markets', 'HQ Location', 'Expansion Type'],
    }
    
    for idx, row in compare_df.iterrows():
        comparison_data[row['brand_name']] = [
            f"${row['investment_usd']}",
            f"${int(row['franchise_fee_usd']):,}",
            f"{row['royalty_pct']}%",
            row['stores_japan'],
            row['stores_overseas'],
            row['target_markets'],
            row.get('hq_location', 'N/A') if 'hq_location' in row else 'N/A',
            row.get('expansion_type', 'N/A') if 'expansion_type' in row else 'N/A'
        ]
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    # Visual comparison cards
    st.markdown("### Visual Comparison")
    cols = st.columns(len(st.session_state.brands_to_compare))
    
    for idx, (col, brand_name) in enumerate(zip(cols, st.session_state.brands_to_compare)):
        brand_data = compare_df[compare_df['brand_name'] == brand_name].iloc[0]
        initials = get_brand_initials(brand_name)
        brand_color = get_brand_color(brand_name)
        
        with col:
            st.markdown(f"""
            <div style="background:white;padding:20px;border-radius:12px;border:2px solid {brand_color};margin:10px 0;">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:15px;">
                    <div style="width:50px;height:50px;border-radius:8px;background:{brand_color};
                                display:flex;align-items:center;justify-content:center;
                                color:white;font-weight:bold;font-size:1.5rem;">
                        {initials}
                    </div>
                    <h3 style="margin:0;color:{brand_color};">{brand_name}</h3>
                </div>
                <p><strong>Investment:</strong> ${brand_data['investment_usd']}</p>
                <p><strong>Fee:</strong> ${int(brand_data['franchise_fee_usd']):,}</p>
                <p><strong>Royalty:</strong> {brand_data['royalty_pct']}%</p>
                <p><strong>Markets:</strong> {brand_data['target_markets']}</p>
            </div>
            """, unsafe_allow_html=True)

# BRAND CARDS with comparison checkboxes
for idx, row in filtered_df.iterrows():
    brand_name = row['brand_name']
    initials = get_brand_initials(brand_name)
    brand_color = get_brand_color(brand_name)
    
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
            # Comparison checkbox with max limit info
            is_selected = brand_name in st.session_state.brands_to_compare
            can_select = num_selected < MAX_COMPARE or is_selected
            
            compare_label = f"Compare ({num_selected}/{MAX_COMPARE})"
            checkbox = st.checkbox(compare_label, value=is_selected, key=f"compare_{brand_name}", 
                                  disabled=not can_select)
            
            if checkbox:
                if brand_name not in st.session_state.brands_to_compare:
                    st.session_state.brands_to_compare.append(brand_name)
            else:
                if brand_name in st.session_state.brands_to_compare:
                    st.session_state.brands_to_compare.remove(brand_name)
            
            st.markdown(f"**{brand_name}**")
            st.caption(row['category'])
            
            japan_info = f"🇵 {row['stores_japan']} stores"
            if japan_regions and pd.notna(japan_regions):
                japan_info += f" ({japan_regions})"
            
            overseas_info = f"🌏 {row['stores_overseas']} overseas"
            if overseas_countries and pd.notna(overseas_countries):
                overseas_info += f" ({overseas_countries})"
            
            st.write(f"{japan_info} | {overseas_info}")
            
            if hq_location and pd.notna(hq_location):
                st.write(f"📍 HQ: {hq_location}")
            
            st.write(f"💰 {row['investment_usd']} | Fee: ${int(row['franchise_fee_usd']):,} | {row['royalty_pct']}% royalty")
            
            if row['target_markets'] and pd.notna(row['target_markets']):
                markets = str(row['target_markets']).split(',')
                st.markdown(" ".join([f'<span class="info-tag">🌍 {m.strip()}</span>' for m in markets]), unsafe_allow_html=True)
        
        with col_btn:
            if st.button("🔍 View Details", key=f"view_{idx}"):
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
