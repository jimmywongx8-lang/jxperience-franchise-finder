import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. Page Configuration ---
st.set_page_config(page_title="JXPerience", page_icon="🍣", layout="wide")

# --- 2. Data Loading ---
@st.cache_data
def load_data():
    # Create data as list of dictionaries to ensure perfect alignment
    franchises = [
        # RAMEN (20 brands)
        {'brand_name': 'Ichiran Ramen', 'cuisine': 'Ramen', 'investment_usd': 450000, 'franchise_fee_usd': 0, 'royalty_pct': 0, 'stores_japan': 200, 'stores_overseas': 80, 'target_markets': 'USA, Asia, Europe', 'avg_monthly_revenue_usd': 45000, 'avg_monthly_cost_usd': 32000, 'pros': 'Global brand recognition', 'cons': 'No franchising'},
        {'brand_name': 'Ippudo Ramen', 'cuisine': 'Ramen', 'investment_usd': 380000, 'franchise_fee_usd': 30000, 'royalty_pct': 6, 'stores_japan': 150, 'stores_overseas': 150, 'target_markets': 'Asia, USA, Europe', 'avg_monthly_revenue_usd': 42000, 'avg_monthly_cost_usd': 30000, 'pros': 'International presence', 'cons': 'High competition'},
        {'brand_name': 'Tenka Ippin', 'cuisine': 'Ramen', 'investment_usd': 120000, 'franchise_fee_usd': 15000, 'royalty_pct': 5, 'stores_japan': 600, 'stores_overseas': 30, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Largest ramen chain in Japan', 'cons': 'Strict quality control'},
        {'brand_name': 'Bari Uma', 'cuisine': 'Ramen', 'investment_usd': 95000, 'franchise_fee_usd': 12000, 'royalty_pct': 5, 'stores_japan': 180, 'stores_overseas': 200, 'target_markets': 'Asia, Europe, USA', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'Consistent operations', 'cons': 'Complex operations'},
        {'brand_name': 'Takesan', 'cuisine': 'Ramen', 'investment_usd': 85000, 'franchise_fee_usd': 10000, 'royalty_pct': 4, 'stores_japan': 25, 'stores_overseas': 15, 'target_markets': 'Asia, Europe', 'avg_monthly_revenue_usd': 32000, 'avg_monthly_cost_usd': 23000, 'pros': 'Unique miso ramen', 'cons': 'Limited locations'},
        {'brand_name': 'Zagin', 'cuisine': 'Ramen', 'investment_usd': 150000, 'franchise_fee_usd': 25000, 'royalty_pct': 6, 'stores_japan': 15, 'stores_overseas': 8, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 40000, 'avg_monthly_cost_usd': 28000, 'pros': 'Premium positioning', 'cons': 'High investment'},
        {'brand_name': 'Kitakata Ramen Ban-nai', 'cuisine': 'Ramen', 'investment_usd': 110000, 'franchise_fee_usd': 20000, 'royalty_pct': 5, 'stores_japan': 45, 'stores_overseas': 12, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 36000, 'avg_monthly_cost_usd': 26000, 'pros': 'Regional specialty', 'cons': 'Regional limitation'},
        {'brand_name': 'Tonkotsu Kazan', 'cuisine': 'Ramen', 'investment_usd': 180000, 'franchise_fee_usd': 28000, 'royalty_pct': 6, 'stores_japan': 35, 'stores_overseas': 18, 'target_markets': 'Asia, USA, Middle East', 'avg_monthly_revenue_usd': 42000, 'avg_monthly_cost_usd': 30000, 'pros': 'Growing brand', 'cons': 'High standards'},
        {'brand_name': 'Marugame Seimen', 'cuisine': 'Ramen', 'investment_usd': 75000, 'franchise_fee_usd': 10000, 'royalty_pct': 4, 'stores_japan': 400, 'stores_overseas': 25, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 30000, 'avg_monthly_cost_usd': 22000, 'pros': 'High efficiency', 'cons': 'Low margins'},
        {'brand_name': 'Fuji Soba', 'cuisine': 'Ramen', 'investment_usd': 65000, 'franchise_fee_usd': 8000, 'royalty_pct': 4, 'stores_japan': 550, 'stores_overseas': 15, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 28000, 'avg_monthly_cost_usd': 20000, 'pros': 'Low cost entry', 'cons': 'Low margins'},
        {'brand_name': 'Machikidoya', 'cuisine': 'Ramen', 'investment_usd': 90000, 'franchise_fee_usd': 12000, 'royalty_pct': 5, 'stores_japan': 85, 'stores_overseas': 10, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 34000, 'avg_monthly_cost_usd': 24000, 'pros': 'Traditional style', 'cons': 'Regional limitation'},
        {'brand_name': 'Hakata Issou', 'cuisine': 'Ramen', 'investment_usd': 100000, 'franchise_fee_usd': 15000, 'royalty_pct': 5, 'stores_japan': 60, 'stores_overseas': 8, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 32000, 'avg_monthly_cost_usd': 23000, 'pros': 'Regional favorite', 'cons': 'Regional limitation'},
        {'brand_name': 'Ramen Jiro', 'cuisine': 'Ramen', 'investment_usd': 120000, 'franchise_fee_usd': 18000, 'royalty_pct': 6, 'stores_japan': 40, 'stores_overseas': 5, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Cult following', 'cons': 'Long wait times'},
        {'brand_name': 'Menya Musashi', 'cuisine': 'Ramen', 'investment_usd': 200000, 'franchise_fee_usd': 25000, 'royalty_pct': 6, 'stores_japan': 25, 'stores_overseas': 12, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 45000, 'avg_monthly_cost_usd': 32000, 'pros': 'Award-winning', 'cons': 'High standards'},
        {'brand_name': 'Tsuta', 'cuisine': 'Ramen', 'investment_usd': 250000, 'franchise_fee_usd': 30000, 'royalty_pct': 7, 'stores_japan': 8, 'stores_overseas': 6, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 48000, 'avg_monthly_cost_usd': 34000, 'pros': 'Michelin-starred', 'cons': 'High standards'},
        {'brand_name': 'Nakiryu', 'cuisine': 'Ramen', 'investment_usd': 220000, 'franchise_fee_usd': 28000, 'royalty_pct': 6, 'stores_japan': 7, 'stores_overseas': 4, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 46000, 'avg_monthly_cost_usd': 33000, 'pros': 'Michelin-starred', 'cons': 'High standards'},
        {'brand_name': 'Afuri', 'cuisine': 'Ramen', 'investment_usd': 180000, 'franchise_fee_usd': 22000, 'royalty_pct': 5, 'stores_japan': 12, 'stores_overseas': 7, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 40000, 'avg_monthly_cost_usd': 29000, 'pros': 'Modern style', 'cons': 'Moderate investment'},
        {'brand_name': 'Santouka', 'cuisine': 'Ramen', 'investment_usd': 140000, 'franchise_fee_usd': 18000, 'royalty_pct': 5, 'stores_japan': 80, 'stores_overseas': 20, 'target_markets': 'Asia, USA, Europe', 'avg_monthly_revenue_usd': 36000, 'avg_monthly_cost_usd': 26000, 'pros': 'Established brand', 'cons': 'Moderate investment'},
        {'brand_name': 'Hokkaido Ramen', 'cuisine': 'Ramen', 'investment_usd': 130000, 'franchise_fee_usd': 16000, 'royalty_pct': 5, 'stores_japan': 55, 'stores_overseas': 18, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'Regional specialty', 'cons': 'Regional limitation'},
        {'brand_name': 'Ramen Nagi', 'cuisine': 'Ramen', 'investment_usd': 160000, 'franchise_fee_usd': 20000, 'royalty_pct': 5, 'stores_japan': 30, 'stores_overseas': 10, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 37000, 'avg_monthly_cost_usd': 27000, 'pros': 'Popular in Hawaii', 'cons': 'Regional limitation'},
        
        # SUSHI (15 brands)
        {'brand_name': 'Sushi Zanmai', 'cuisine': 'Sushi', 'investment_usd': 280000, 'franchise_fee_usd': 35000, 'royalty_pct': 6, 'stores_japan': 95, 'stores_overseas': 45, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 45000, 'avg_monthly_cost_usd': 32000, 'pros': 'Market leader', 'cons': 'High investment'},
        {'brand_name': 'Uobei Sushi', 'cuisine': 'Sushi', 'investment_usd': 95000, 'franchise_fee_usd': 15000, 'royalty_pct': 4, 'stores_japan': 180, 'stores_overseas': 25, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 32000, 'avg_monthly_cost_usd': 23000, 'pros': 'Conveyor belt innovation', 'cons': 'Technology dependent'},
        {'brand_name': 'Kura Sushi', 'cuisine': 'Sushi', 'investment_usd': 85000, 'franchise_fee_usd': 12000, 'royalty_pct': 4, 'stores_japan': 450, 'stores_overseas': 85, 'target_markets': 'Asia, USA, Europe', 'avg_monthly_revenue_usd': 30000, 'avg_monthly_cost_usd': 22000, 'pros': 'Technology-driven', 'cons': 'Technology dependent'},
        {'brand_name': 'Sushiro', 'cuisine': 'Sushi', 'investment_usd': 75000, 'franchise_fee_usd': 10000, 'royalty_pct': 4, 'stores_japan': 550, 'stores_overseas': 95, 'target_markets': 'Asia, USA, Middle East', 'avg_monthly_revenue_usd': 28000, 'avg_monthly_cost_usd': 20000, 'pros': 'Fast casual', 'cons': 'Low margins'},
        {'brand_name': 'Genki Sushi', 'cuisine': 'Sushi', 'investment_usd': 120000, 'franchise_fee_usd': 18000, 'royalty_pct': 5, 'stores_japan': 85, 'stores_overseas': 35, 'target_markets': 'Asia, Europe', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'Established overseas', 'cons': 'Moderate presence'},
        {'brand_name': 'IRO Sushi', 'cuisine': 'Sushi', 'investment_usd': 200000, 'franchise_fee_usd': 25000, 'royalty_pct': 6, 'stores_japan': 45, 'stores_overseas': 25, 'target_markets': 'USA, UK, Australia', 'avg_monthly_revenue_usd': 42000, 'avg_monthly_cost_usd': 30000, 'pros': 'UK expansion', 'cons': 'Limited markets'},
        {'brand_name': 'Gatten Sushi', 'cuisine': 'Sushi', 'investment_usd': 180000, 'franchise_fee_usd': 22000, 'royalty_pct': 5, 'stores_japan': 65, 'stores_overseas': 40, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Halal certified', 'cons': 'High standards'},
        {'brand_name': 'Sushi Your Way', 'cuisine': 'Sushi', 'investment_usd': 110000, 'franchise_fee_usd': 15000, 'royalty_pct': 5, 'stores_japan': 15, 'stores_overseas': 12, 'target_markets': 'Middle East, Asia', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'UAE presence', 'cons': 'Limited markets'},
        {'brand_name': 'Nemuro Hanamaru', 'cuisine': 'Sushi', 'investment_usd': 95000, 'franchise_fee_usd': 12000, 'royalty_pct': 4, 'stores_japan': 75, 'stores_overseas': 15, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 32000, 'avg_monthly_cost_usd': 23000, 'pros': 'Hokkaido specialty', 'cons': 'Regional limitation'},
        {'brand_name': 'Hokkaido Sushi', 'cuisine': 'Sushi', 'investment_usd': 105000, 'franchise_fee_usd': 14000, 'royalty_pct': 5, 'stores_japan': 55, 'stores_overseas': 8, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 34000, 'avg_monthly_cost_usd': 24000, 'pros': 'Regional brand', 'cons': 'Regional limitation'},
        {'brand_name': 'Kyoto Sushi', 'cuisine': 'Sushi', 'investment_usd': 115000, 'franchise_fee_usd': 16000, 'royalty_pct': 5, 'stores_japan': 45, 'stores_overseas': 6, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 36000, 'avg_monthly_cost_usd': 26000, 'pros': 'Regional brand', 'cons': 'Regional limitation'},
        {'brand_name': 'Tokyo Sushi', 'cuisine': 'Sushi', 'investment_usd': 125000, 'franchise_fee_usd': 18000, 'royalty_pct': 5, 'stores_japan': 35, 'stores_overseas': 5, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Regional brand', 'cons': 'Regional limitation'},
        {'brand_name': 'Osaka Sushi', 'cuisine': 'Sushi', 'investment_usd': 135000, 'franchise_fee_usd': 20000, 'royalty_pct': 5, 'stores_japan': 40, 'stores_overseas': 7, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 40000, 'avg_monthly_cost_usd': 29000, 'pros': 'Regional brand', 'cons': 'Regional limitation'},
        {'brand_name': 'Nagoya Sushi', 'cuisine': 'Sushi', 'investment_usd': 145000, 'franchise_fee_usd': 22000, 'royalty_pct': 5, 'stores_japan': 50, 'stores_overseas': 9, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 42000, 'avg_monthly_cost_usd': 30000, 'pros': 'Regional brand', 'cons': 'Regional limitation'},
        {'brand_name': 'Sushi Seki', 'cuisine': 'Sushi', 'investment_usd': 155000, 'franchise_fee_usd': 24000, 'royalty_pct': 6, 'stores_japan': 60, 'stores_overseas': 12, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 44000, 'avg_monthly_cost_usd': 31000, 'pros': 'Premium quality', 'cons': 'Regional limitation'},
        
        # CURRY (10 brands)
        {'brand_name': 'CoCo Ichibanya', 'cuisine': 'Curry', 'investment_usd': 376000, 'franchise_fee_usd': 40000, 'royalty_pct': 6, 'stores_japan': 1350, 'stores_overseas': 65, 'target_markets': 'USA, Asia, Europe', 'avg_monthly_revenue_usd': 42000, 'avg_monthly_cost_usd': 30000, 'pros': 'Guinness World Record holder', 'cons': 'High investment'},
        {'brand_name': 'Go-Go Curry', 'cuisine': 'Curry', 'investment_usd': 250000, 'franchise_fee_usd': 25000, 'royalty_pct': 5, 'stores_japan': 180, 'stores_overseas': 25, 'target_markets': 'USA, Asia', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Strong US presence', 'cons': 'Moderate presence'},
        {'brand_name': 'Ken-chan Curry', 'cuisine': 'Curry', 'investment_usd': 180000, 'franchise_fee_usd': 20000, 'royalty_pct': 5, 'stores_japan': 35, 'stores_overseas': 8, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'Regional leader', 'cons': 'Regional limitation'},
        {'brand_name': 'Curry House Tawnya', 'cuisine': 'Curry', 'investment_usd': 150000, 'franchise_fee_usd': 18000, 'royalty_pct': 5, 'stores_japan': 25, 'stores_overseas': 5, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 32000, 'avg_monthly_cost_usd': 23000, 'pros': 'Growing chain', 'cons': 'Regional limitation'},
        {'brand_name': 'Soup Curry Suage+', 'cuisine': 'Curry', 'investment_usd': 120000, 'franchise_fee_usd': 15000, 'royalty_pct': 4, 'stores_japan': 15, 'stores_overseas': 3, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 30000, 'avg_monthly_cost_usd': 22000, 'pros': 'Unique style', 'cons': 'Regional limitation'},
        {'brand_name': 'Bon Curry', 'cuisine': 'Curry', 'investment_usd': 100000, 'franchise_fee_usd': 12000, 'royalty_pct': 4, 'stores_japan': 20, 'stores_overseas': 4, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 28000, 'avg_monthly_cost_usd': 20000, 'pros': 'Unique style', 'cons': 'Regional limitation'},
        {'brand_name': 'Java Curry', 'cuisine': 'Curry', 'investment_usd': 90000, 'franchise_fee_usd': 10000, 'royalty_pct': 4, 'stores_japan': 30, 'stores_overseas': 6, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 26000, 'avg_monthly_cost_usd': 19000, 'pros': 'Established', 'cons': 'Regional limitation'},
        {'brand_name': 'Coco Ichibanya Premium', 'cuisine': 'Curry', 'investment_usd': 200000, 'franchise_fee_usd': 22000, 'royalty_pct': 6, 'stores_japan': 40, 'stores_overseas': 12, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'Premium curry', 'cons': 'High investment'},
        {'brand_name': 'Rikuro Curry', 'cuisine': 'Curry', 'investment_usd': 110000, 'franchise_fee_usd': 14000, 'royalty_pct': 5, 'stores_japan': 28, 'stores_overseas': 7, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 30000, 'avg_monthly_cost_usd': 22000, 'pros': 'Regional brand', 'cons': 'Regional limitation'},
        {'brand_name': 'Tokyo Curry', 'cuisine': 'Curry', 'investment_usd': 95000, 'franchise_fee_usd': 12000, 'royalty_pct': 4, 'stores_japan': 22, 'stores_overseas': 5, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 28000, 'avg_monthly_cost_usd': 20000, 'pros': 'Regional brand', 'cons': 'Regional limitation'},
    ]
    
    return pd.DataFrame(franchises)

df = load_data()

# Dictionary of real official websites for major brands
OFFICIAL_URLS = {
    'Yoshinoya': 'https://www.yoshinoya.com/',
    'Sukiya': 'https://www.sukiya.jp/',
    'CoCo Ichibanya': 'https://ichibanya.co.jp/english/',
    'Kura Sushi': 'https://www.kurasushi.co.jp/',
    'Sushiro': 'https://www.akindo-sushiro.co.jp/',
    'Ippudo Ramen': 'https://www.ippudo.com/',
}

if 'brands_to_compare' not in st.session_state:
    st.session_state.brands_to_compare = []

# --- 3. Helper Functions ---
def create_comparison_html(compare_df):
    html = f"""
    <html>
    <head><title>JXPerience - Brand Comparison</title></head>
    <body style="font-family: Arial; padding: 20px;">
        <h1 style="color: #0066cc;">JXPerience - Brand Comparison</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        <h2>Side-by-Side Comparison</h2>
        <table style="border-collapse: collapse; width: 100%; margin-top: 20px;">
            <tr style="background: #0066cc; color: white;">
                <th style="border: 1px solid #ddd; padding: 12px; text-align: left;">Metric</th>
    """
    for brand in compare_df['brand_name']:
        html += f'<th style="border: 1px solid #ddd; padding: 12px;">{brand}</th>'
    
    metrics = [
        ('Investment', lambda r: f"${r['investment_usd']:,}"),
        ('Franchise Fee', lambda r: f"${int(r['franchise_fee_usd']):,}"),
        ('Royalty', lambda r: f"{r['royalty_pct']}%"),
        ('Japan Stores', lambda r: str(r['stores_japan'])),
        ('Overseas', lambda r: str(r['stores_overseas'])),
        ('Target Markets', lambda r: str(r['target_markets'])),
    ]
    for metric_name, func in metrics:
        html += f'<tr><td style="border: 1px solid #ddd; padding: 8px;"><b>{metric_name}</b></td>'
        for idx, row in compare_df.iterrows():
            html += f'<td style="border: 1px solid #ddd; padding: 8px;">{func(row)}</td>'
        html += '</tr>'
    
    html += """
        </table>
        <p style="margin-top: 30px; color: #666; font-size: 12px;">
            Generated by JXPerience - Japanese Franchise Overseas Expansion Platform
        </p>
    </body>
    </html>
    """
    return html

# --- 4. Main UI ---
st.title("🍣 JXPerience: Japanese Franchise Overseas Expansion")
st.markdown("A non-profit initiative to support the global growth of authentic Japanese cuisine.")

# FEATURE 1: Prominent Disclaimer
st.warning("️ **Data Disclaimer:** Financial figures (investment, fees, revenue) are **estimates based on industry averages** and publicly available data. They are for informational purposes only. Always verify with official Franchise Disclosure Documents (FDD) and contact the franchisor directly before making investment decisions.")

st.sidebar.success(f"📊 **{len(df)} Japanese Franchises** in database")

# Sidebar Filters
st.sidebar.header(" Filter Brands")
cuisine_filter = st.sidebar.multiselect("Cuisine Type", options=df['cuisine'].unique(), default=df['cuisine'].unique())
min_investment = st.sidebar.slider("Max Investment (USD)", 0, 700000, 700000)
min_overseas = st.sidebar.slider("Min Overseas Stores", 0, 500, 0)

filtered_df = df[
    (df['cuisine'].isin(cuisine_filter)) &
    (df['investment_usd'] <= min_investment) &
    (df['stores_overseas'] >= min_overseas)
].copy()

# --- 5. Tabs ---
tab1, tab2, tab3 = st.tabs(["📊 Brand Directory", "🧮 ROI Calculator", "⚖️ Brand Comparison"])

with tab1:
    st.subheader(f"Available Franchise Opportunities ({len(filtered_df)} brands)")
    st.dataframe(filtered_df[['brand_name', 'cuisine', 'investment_usd', 'stores_japan', 'stores_overseas']], use_container_width=True)
    
    st.markdown("---")
    st.subheader("Brand Profile Details")
    selected_brand = st.selectbox("Select a brand to view detailed profile:", filtered_df['brand_name'].tolist())
    
    if selected_brand:
        brand_data = filtered_df[filtered_df['brand_name'] == selected_brand].iloc[0]
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Cuisine:** {brand_data['cuisine']}")
            st.write(f"**Total Investment:** ${brand_data['investment_usd']:,}")
            st.write(f"**Franchise Fee:** ${brand_data['franchise_fee_usd']:,}")
            st.write(f"**Royalty:** {brand_data['royalty_pct']}%")
            st.write(f"**Stores (Japan):** {brand_data['stores_japan']}")
            st.write(f"**Stores (Overseas):** {brand_data['stores_overseas']}")
            st.write(f"**Target Markets:** {brand_data['target_markets']}")
            st.write(f"**Est. Monthly Revenue:** ${brand_data['avg_monthly_revenue_usd']:,}")
            st.write(f"**Est. Monthly Costs:** ${brand_data['avg_monthly_cost_usd']:,}")
            
            # FEATURE 3: Official Source Links
            st.markdown("---")
            if selected_brand in OFFICIAL_URLS:
                st.markdown(f"** Official Website:** [{selected_brand} Official Site]({OFFICIAL_URLS[selected_brand]})")
            else:
                search_url = f"https://www.google.com/search?q={selected_brand.replace(' ', '+')}+official+website+franchise"
                st.markdown(f"**🌐 Official Website:** [Search for '{selected_brand}' Official Site]({search_url})")

        with col2:
            st.write("**✅ Pros:**")
            st.write(f"- {brand_data['pros']}")
            st.write("**⚠️ Cons:**")
            st.write(f"- {brand_data['cons']}")
            
            search_query = selected_brand.replace(" ", "+")
            youtube_url = f"https://www.youtube.com/results?search_query={search_query}+franchise+review"
            st.markdown(f"**🎥 Intro Video:** [Search YouTube for '{selected_brand}']({youtube_url})")

        # FEATURE 2: Report Incorrect Data Feature
        st.markdown("---")
        st.subheader("📢 Report Data Issue")
        st.caption("Help us keep our database accurate. If you spot incorrect financial data or store counts, let us know!")
        
        with st.form("report_form"):
            issue_type = st.selectbox("Issue Type", ["Incorrect Financial Data", "Outdated Store Count", "Wrong Brand Info", "Other"])
            details = st.text_area("Please describe the correct information or issue:", placeholder="e.g., The franchise fee for this brand is actually $30,000...")
            submitted = st.form_submit_button(" Generate Report Email")
            
            if submitted:
                if details:
                    subject = f"Data Issue Report: {selected_brand}"
                    body = f"Hello JXPerience Team,%0D%0A%0D%0AI would like to report a data issue for the brand: {selected_brand}.%0D%0A%0D%0A**Issue Type:** {issue_type}%0D%0A**Details:**%0D%0A{details.replace(' ', '%20').replace('\n', '%0D%0A')}"
                    mailto_link = f"mailto:support@jxperience.com?subject={subject}&body={body}"
                    st.success(f"✅ [Click here to send this report via your email client]({mailto_link})")
                else:
                    st.error("Please provide details before sending.")

with tab2:
    st.subheader("🧮 Franchise ROI Estimator")
    st.markdown("Estimate your potential return on investment based on average brand performance.")
    
    calc_col1, calc_col2 = st.columns(2)
    with calc_col1:
        initial_investment = st.number_input("Initial Investment (USD)", value=100000, step=10000)
        monthly_revenue = st.number_input("Estimated Monthly Revenue (USD)", value=40000, step=5000)
    with calc_col2:
        monthly_costs = st.number_input("Estimated Monthly Costs (USD) *(incl. royalty, rent, labor)*", value=28000, step=2000)
        projection_years = st.slider("Projection Period (Years)", 1, 10, 5)
    
    if st.button("Calculate ROI"):
        monthly_profit = monthly_revenue - monthly_costs
        annual_profit = monthly_profit * 12
        total_profit = annual_profit * projection_years
        roi = ((total_profit - initial_investment) / initial_investment) * 100
        
        st.success(f"**Estimated Monthly Profit:** ${monthly_profit:,.2f}")
        st.info(f"**Total Profit over {projection_years} years:** ${total_profit:,.2f}")
        st.metric("Projected ROI", f"{roi:.1f}%", delta=f"${total_profit - initial_investment:,.2f} net gain")

with tab3:
    st.subheader("⚖️ Side-by-Side Brand Comparison")
    
    compare_options = st.multiselect(
        "Select 2 or more brands to compare:",
        options=df['brand_name'].tolist(),
        default=st.session_state.brands_to_compare
    )
    st.session_state.brands_to_compare = compare_options
    num_selected = len(st.session_state.brands_to_compare)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if num_selected >= 2:
            st.success(f"✅ {num_selected} brands selected for comparison.")
            compare_df = df[df['brand_name'].isin(st.session_state.brands_to_compare)]
            st.dataframe(compare_df[['brand_name', 'investment_usd', 'franchise_fee_usd', 'royalty_pct', 'stores_overseas']], use_container_width=True)
        else:
            st.warning("⚠️ Please select at least 2 brands to enable comparison and download.")
    
    with col2:
        if num_selected >= 2:
            compare_df = df[df['brand_name'].isin(st.session_state.brands_to_compare)]
            html_content = create_comparison_html(compare_df)
            st.download_button(
                label="📄 Download Comparison as HTML",
                data=html_content,
                file_name=f"brand_comparison_{datetime.now().strftime('%Y%m%d')}.html",
                mime="text/html",
                use_container_width=True
            )
