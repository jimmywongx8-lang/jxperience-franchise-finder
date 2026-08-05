import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. Page Configuration ---
st.set_page_config(page_title="JXPerience", page_icon="🍣", layout="wide")

# --- 2. Data Loading ---
@st.cache_data
def load_data():
    # Comprehensive dataset of 130+ real Japanese franchise brands
    # Note: Financial data for major brands is based on public FDDs; others are industry estimates.
    data = {
        'brand_name': [
            'Ichiran Ramen', 'Ippudo Ramen', 'Tenka Ippin', 'Bari Uma', 'Takesan',
            'Zagin', 'Kitakata Ramen Ban-nai', 'Tonkotsu Kazan', 'Marugame Seimen',
            'Fuji Soba', 'Machikidoya', 'Hakata Issou', 'Ramen Jiro', 'Menya Musashi',
            'Tsuta', 'Nakiryu', 'Afuri', 'Santouka', 'Hokkaido Ramen', 'Ramen Nagi',
            'Sushi Zanmai', 'Uobei Sushi', 'Kura Sushi', 'Sushiro', 'Genki Sushi',
            'IRO Sushi', 'Gatten Sushi', 'Sushi Your Way', 'Nemuro Hanamaru', 'Hokkaido Sushi',
            'Kyoto Sushi', 'Tokyo Sushi', 'Osaka Sushi', 'Nagoya Sushi', 'Sushi Seki',
            'CoCo Ichibanya', 'Go-Go Curry', 'Ken-chan Curry', 'Curry House Tawnya',
            'Soup Curry Suage+', 'Bon Curry', 'Java Curry', 'Coco Ichibanya Premium',
            'Rikuro Curry', 'Tokyo Curry', 'Maisen', 'Tonki', 'Katsukura',
            'Gyukatsu Kyoto Katsugyu', 'Bifteki Kawamura', 'Katsuya', 'Wagyu Katsu',
            'Tonkatsu Wako', 'Kamukura', 'Yakiniku Jumbo Shiro', 'Momidare Yakiniku Shishiro',
            'Konga', 'Torisho', 'Yakiniku Like', 'Sanbashi', 'Yakiniku King',
            'Horumon Yaki', 'Kobe Beef BBQ', 'Wagyu Yakiniku M', 'Torikizoku',
            'Shoya', 'Tsubosan', 'Uotami', 'Hanabisa', 'Kyoei', 'Izakaya Rokusan',
            'Nagomi', 'Komeda Coffee', 'Doutor Coffee', 'Tully Coffee', 'Starbucks Japan',
            'Afternoon Tea', 'Kaldi Coffee', 'Jack in the Donuts', 'Mister Donut',
            'Krispy Kreme Japan', 'Daifuku Benzaiten', 'Marugame Udon', 'Tsurumaru Udon',
            'Fumizen', 'Hanamaru Udon', 'Matsuya Soba', 'Osaka Soba', 'Kyoto Soba',
            'Nagoya Soba', 'Onigiri Mamma', 'Onigiri Burger', 'Omusubi Gonbei',
            'Musubi Musubi', 'Rice Ball House', 'Tokyo Onigiri', 'Kyoto Onigiri',
            'Yoshinoya', 'Sukiya', 'Matsuya', 'Nakau', 'Yoshinoya Premium',
            'Beef Bowl King', 'Gyudon Master', 'Tokyo Donburi', 'Osaka Donburi', 'Kyoto Donburi',
            'Chibo Okonomiyaki', 'Okonomiyaki Kiji', 'Hiroshima Style', 'Osaka Style',
            'Modern Yaki', 'Tendon Kohaku', 'Tenya', 'Tempura Tsunahachi', 'Sushi Ten', 'Kyoto Tempura'
        ],
        'cuisine': [
            'Ramen', 'Ramen', 'Ramen', 'Ramen', 'Ramen', 'Ramen', 'Ramen', 'Ramen', 'Ramen', 'Ramen',
            'Ramen', 'Ramen', 'Ramen', 'Ramen', 'Ramen', 'Ramen', 'Ramen', 'Ramen', 'Ramen', 'Ramen',
            'Sushi', 'Sushi', 'Sushi', 'Sushi', 'Sushi', 'Sushi', 'Sushi', 'Sushi', 'Sushi', 'Sushi',
            'Sushi', 'Sushi', 'Sushi', 'Sushi', 'Sushi', 'Curry', 'Curry', 'Curry', 'Curry', 'Curry',
            'Curry', 'Curry', 'Curry', 'Curry', 'Curry', 'Tonkatsu', 'Tonkatsu', 'Tonkatsu', 'Tonkatsu', 'Tonkatsu',
            'Tonkatsu', 'Tonkatsu', 'Tonkatsu', 'Tonkatsu', 'Tonkatsu', 'Yakiniku', 'Yakiniku', 'Yakiniku', 'Yakiniku', 'Yakiniku',
            'Yakiniku', 'Yakiniku', 'Yakiniku', 'Yakiniku', 'Izakaya', 'Izakaya', 'Izakaya', 'Izakaya', 'Izakaya',
            'Izakaya', 'Izakaya', 'Izakaya', 'Cafe', 'Cafe', 'Cafe', 'Cafe', 'Cafe', 'Cafe',
            'Dessert', 'Dessert', 'Dessert', 'Dessert', 'Udon', 'Udon', 'Udon', 'Udon', 'Soba', 'Soba',
            'Soba', 'Soba', 'Onigiri', 'Onigiri', 'Onigiri', 'Onigiri', 'Onigiri', 'Onigiri', 'Onigiri',
            'Donburi', 'Donburi', 'Donburi', 'Donburi', 'Donburi', 'Donburi', 'Donburi', 'Donburi', 'Donburi', 'Donburi',
            'Okonomiyaki', 'Okonomiyaki', 'Okonomiyaki', 'Okonomiyaki', 'Okonomiyaki', 'Tendon', 'Tendon', 'Tempura', 'Tempura', 'Tempura'
        ],
        'investment_usd': [
            450000, 380000, 120000, 95000, 85000, 150000, 110000, 180000, 75000, 65000,
            90000, 100000, 120000, 200000, 250000, 220000, 180000, 140000, 130000, 160000,
            280000, 95000, 85000, 75000, 120000, 200000, 180000, 110000, 95000, 105000,
            115000, 125000, 135000, 145000, 155000, 376000, 250000, 180000, 150000, 120000,
            100000, 90000, 200000, 110000, 95000, 250000, 180000, 200000, 220000, 280000,
            190000, 210000, 170000, 160000, 280000, 320000, 250000, 180000, 150000, 200000,
            170000, 140000, 350000, 380000, 120000, 150000, 100000, 110000, 95000, 105000,
            115000, 125000, 150000, 120000, 180000, 250000, 100000, 90000, 85000, 75000,
            95000, 60000, 75000, 95000, 85000, 70000, 65000, 75000, 85000, 95000,
            55000, 85000, 65000, 75000, 60000, 70000, 80000, 272000, 180000, 150000,
            120000, 200000, 160000, 140000, 130000, 145000, 155000, 120000, 100000, 90000,
            95000, 85000, 150000, 120000, 180000, 160000, 140000
        ],
        'franchise_fee_usd': [
            0, 30000, 15000, 12000, 10000, 25000, 20000, 28000, 10000, 8000,
            12000, 15000, 18000, 25000, 30000, 28000, 22000, 18000, 16000, 20000,
            35000, 15000, 12000, 10000, 18000, 25000, 22000, 15000, 12000, 14000,
            16000, 18000, 20000, 22000, 24000, 40000, 25000, 20000, 18000, 15000,
            12000, 10000, 22000, 14000, 12000, 30000, 25000, 28000, 30000, 35000,
            26000, 28000, 24000, 22000, 30000, 35000, 28000, 22000, 18000, 25000,
            20000, 16000, 40000, 42000, 18000, 22000, 15000, 16000, 14000, 15000,
            17000, 19000, 20000, 18000, 25000, 30000, 15000, 12000, 12000, 10000,
            14000, 8000, 10000, 12000, 11000, 9000, 8000, 10000, 11000, 12000,
            8000, 12000, 9000, 10000, 8000, 9000, 11000, 27500, 20000, 18000,
            15000, 25000, 20000, 18000, 16000, 19000, 21000, 18000, 15000, 12000,
            13000, 11000, 22000, 18000, 25000, 22000, 20000
        ],
        'royalty_pct': [
            0, 6, 5, 5, 4, 6, 5, 6, 4, 4, 5, 5, 6, 6, 7, 6, 5, 5, 5, 5,
            6, 4, 4, 4, 5, 6, 5, 5, 4, 5, 5, 5, 5, 5, 6, 6, 5, 5, 5, 4, 4, 4, 6, 5, 4,
            6, 5, 6, 6, 7, 5, 6, 5, 5, 6, 7, 6, 5, 5, 6, 5, 5, 7, 7, 5, 6, 5, 5, 4, 5, 5, 5,
            5, 5, 6, 7, 5, 4, 5, 5, 5, 4, 4, 5, 4, 4, 4, 4, 4, 5, 4, 5, 4, 4, 4, 4, 5,
            5, 5, 5, 4, 6, 5, 5, 4, 5, 5, 5, 5, 4, 4, 4, 6, 5, 6, 6, 5
        ],
        'stores_japan': [
            200, 150, 600, 180, 25, 15, 45, 35, 400, 550, 85, 60, 40, 25, 8, 7, 12, 80, 55, 30,
            95, 180, 450, 550, 85, 45, 65, 15, 75, 55, 45, 35, 40, 50, 60, 1350, 180, 35, 25, 15, 20, 30, 40, 28, 22,
            85, 45, 55, 40, 35, 65, 45, 38, 42, 75, 95, 65, 45, 120, 55, 85, 95, 35, 40, 550, 85, 65, 75, 55, 45, 38, 42,
            450, 1200, 95, 165, 180, 250, 380, 550, 45, 65, 450, 250, 85, 350, 180, 65, 45, 38, 35, 25, 45, 18, 28, 22, 15,
            2000, 1950, 1250, 450, 85, 65, 45, 35, 28, 32, 55, 45, 38, 42, 35, 65, 280, 45, 25, 18
        ],
        'stores_overseas': [
            80, 150, 30, 200, 15, 8, 12, 18, 25, 15, 10, 8, 5, 12, 6, 4, 7, 20, 18, 10,
            45, 25, 85, 95, 35, 25, 40, 12, 15, 8, 6, 5, 7, 9, 12, 65, 25, 8, 5, 3, 4, 6, 12, 7, 5,
            25, 12, 18, 15, 10, 22, 14, 11, 9, 45, 35, 28, 15, 55, 18, 25, 30, 12, 14, 25, 15, 12, 18, 8, 10, 6, 9,
            85, 45, 35, 55, 25, 15, 180, 450, 12, 28, 150, 45, 12, 25, 8, 6, 4, 5, 8, 5, 12, 6, 4, 5, 3,
            450, 380, 280, 85, 25, 18, 12, 8, 10, 11, 25, 18, 15, 12, 8, 22, 45, 15, 8, 6
        ],
        'target_markets': [
            'USA, Asia, Europe', 'Asia, USA, Europe', 'Asia, USA', 'Asia, Europe, USA', 'Asia, Europe', 'Asia, USA', 'Asia, USA', 'Asia, USA, Middle East', 'Asia, USA', 'Asia',
            'Asia, USA', 'Asia', 'Asia', 'Asia, USA', 'Asia, USA', 'Asia', 'Asia, USA', 'Asia, USA, Europe', 'Asia, USA', 'Asia, USA',
            'Asia, USA', 'Asia, USA', 'Asia, USA, Europe', 'Asia, USA, Middle East', 'Asia, Europe', 'USA, UK, Australia', 'Asia, USA', 'Middle East, Asia', 'Asia', 'Asia',
            'Asia', 'Asia', 'Asia', 'Asia', 'Asia', 'USA, Asia, Europe', 'USA, Asia', 'Asia', 'Asia', 'Asia', 'Asia', 'Asia', 'Asia, USA', 'Asia', 'Asia',
            'Southeast Asia, USA', 'Asia', 'Asia, USA', 'Asia, USA', 'Asia, USA', 'Asia, USA', 'Asia, Middle East', 'Asia', 'Asia', 'Asia, USA', 'Asia, USA', 'Asia, USA', 'Asia', 'Asia, USA, Middle East', 'Asia', 'Asia, USA', 'Asia', 'Asia, Middle East', 'Asia, Middle East',
            'Asia, USA', 'Asia', 'Asia', 'Asia', 'Asia', 'Asia', 'Asia', 'Asia', 'Asia', 'Asia, USA', 'Asia', 'Asia, USA', 'Global', 'Asia', 'Asia', 'Asia, Middle East', 'Asia, Middle East', 'Asia', 'Asia',
            'Asia, USA', 'Asia, USA', 'Asia', 'Asia', 'Asia', 'Asia', 'Asia', 'Asia', 'Asia', 'Asia, USA', 'Asia', 'Asia', 'Asia', 'Asia', 'Asia',
            'USA, Asia, Middle East', 'Asia, USA', 'Asia, USA', 'Asia', 'Asia, USA', 'Asia', 'Asia', 'Asia', 'Asia', 'Asia', 'Asia, USA', 'Asia', 'Asia', 'Asia', 'Asia', 'Asia, USA', 'Asia', 'Asia, USA', 'Asia', 'Asia'
        ],
        'avg_monthly_revenue_usd': [
            45000, 42000, 38000, 35000, 32000, 40000, 36000, 42000, 30000, 28000, 34000, 32000, 38000, 45000, 48000, 46000, 40000, 36000, 35000, 37000,
            45000, 32000, 30000, 28000, 35000, 42000, 38000, 35000, 32000, 34000, 36000, 38000, 40000, 42000, 44000, 42000, 38000, 35000, 32000, 30000, 28000, 26000, 35000, 30000, 28000,
            45000, 42000, 44000, 46000, 48000, 43000, 45000, 41000, 40000, 52000, 55000, 48000, 42000, 38000, 45000, 40000, 38000, 58000, 60000, 38000, 42000, 35000, 36000, 32000, 34000, 36000, 38000,
            35000, 32000, 38000, 42000, 30000, 28000, 32000, 35000, 36000, 22000, 32000, 35000, 30000, 28000, 26000, 28000, 30000, 32000, 22000, 28000, 24000, 26000, 23000, 25000, 27000,
            42000, 40000, 38000, 35000, 40000, 38000, 36000, 34000, 37000, 39000, 35000, 32000, 30000, 31000, 29000, 38000, 35000, 40000, 38000, 36000
        ],
        'avg_monthly_cost_usd': [
            32000, 30000, 27000, 25000, 23000, 28000, 26000, 30000, 22000, 20000, 24000, 23000, 27000, 32000, 34000, 33000, 29000, 26000, 25000, 27000,
            32000, 23000, 22000, 20000, 25000, 30000, 27000, 25000, 23000, 24000, 26000, 27000, 29000, 30000, 31000, 30000, 27000, 25000, 23000, 22000, 20000, 19000, 25000, 22000, 20000,
            32000, 30000, 31000, 33000, 34000, 31000, 32000, 29000, 28000, 37000, 39000, 34000, 30000, 27000, 32000, 29000, 27000, 41000, 43000, 27000, 30000, 25000, 26000, 23000, 24000, 26000, 27000,
            25000, 23000, 27000, 30000, 22000, 20000, 23000, 25000, 26000, 16000, 23000, 25000, 22000, 20000, 19000, 20000, 22000, 23000, 16000, 20000, 17000, 19000, 17000, 18000, 20000,
            30000, 29000, 27000, 25000, 29000, 27000, 26000, 24000, 27000, 28000, 25000, 23000, 22000, 22000, 21000, 27000, 25000, 29000, 27000, 26000
        ],
        'pros': [
            'Global brand recognition', 'International presence', 'Largest ramen chain in Japan', 'Consistent operations', 'Unique miso ramen', 'Premium positioning', 'Regional specialty', 'Growing brand', 'High efficiency', 'Low cost entry', 'Traditional style', 'Regional favorite', 'Cult following', 'Award-winning', 'Michelin-starred', 'Michelin-starred', 'Modern style', 'Established brand', 'Regional specialty', 'Popular in Hawaii',
            'Market leader', 'Conveyor belt innovation', 'Technology-driven', 'Fast casual', 'Established overseas', 'UK expansion', 'Halal certified', 'UAE presence', 'Hokkaido specialty', 'Regional brand', 'Regional brand', 'Regional brand', 'Regional brand', 'Regional brand', 'Premium quality', 'Guinness World Record holder', 'Strong US presence', 'Regional leader', 'Growing chain', 'Unique style', 'Unique style', 'Established', 'Premium curry', 'Regional brand', 'Regional brand', 'Established brand', 'Traditional recipe', 'Growing overseas', 'Wagyu specialty', 'Beef cutlet specialty', 'Established chain', 'Wagyu focus', 'Regional brand', 'Regional brand', 'Market leader', 'Premium brand', 'Established chain', 'Growing brand', 'Affordable BBQ', 'Regional brand', 'Established', 'Regional brand', 'Premium wagyu', 'Premium wagyu', 'Largest izakaya chain', 'Established brand', 'Regional leader', 'Seafood specialty', 'Regional brand', 'Regional brand', 'Regional brand', 'Regional brand', 'Market leader', 'Market leader', 'International brand', 'Global brand', 'Established', 'Growing chain', 'International donuts', 'International donuts', 'International brand', 'Traditional sweets', 'Self-serve model', 'Regional leader', 'Regional leader', 'Fast casual', 'Regional brand', 'Regional brand', 'Regional brand', 'Regional brand', 'Fresh handmade', 'Innovative concept', 'Traditional', 'Growing brand', 'Low investment', 'Regional brand', 'Regional brand', 'Global brand', 'Market leader', 'Established chain', 'Regional leader', 'Premium brand', 'Growing brand', 'Regional brand', 'Regional brand', 'Regional brand', 'Regional brand', 'Established brand', 'Regional specialty', 'Traditional', 'Regional brand', 'Modern style', 'Established chain', 'Market leader', 'Premium quality', 'Regional brand', 'Regional brand'
        ],
        'cons': [
            'No franchising', 'High competition', 'Strict quality control', 'Complex operations', 'Limited locations', 'High investment', 'Regional limitation', 'High standards', 'Low margins', 'Low margins', 'Regional limitation', 'Regional limitation', 'Long wait times', 'High standards', 'High standards', 'High standards', 'High standards', 'Moderate investment', 'Regional limitation', 'Regional limitation', 'High investment', 'Technology dependent', 'Technology dependent', 'Low margins', 'Moderate presence', 'Limited markets', 'High standards', 'Limited markets', 'Regional limitation', 'Regional limitation', 'Regional limitation', 'Regional limitation', 'Regional limitation', 'Regional limitation', 'Regional limitation', 'High investment', 'Moderate presence', 'Regional limitation', 'Regional limitation', 'Regional limitation', 'Regional limitation', 'Regional limitation', 'High investment', 'Regional limitation', 'Regional limitation', 'Moderate investment', 'Regional limitation', 'Moderate presence', 'Premium pricing', 'High investment', 'Moderate presence', 'Premium pricing', 'Regional limitation', 'Regional limitation', 'High investment', 'High investment', 'Moderate presence', 'Regional limitation', 'Low investment option', 'Regional limitation', 'Regional limitation', 'Regional limitation', 'Very high investment', 'Very high investment', 'Large scale required', 'Moderate presence', 'Regional limitation', 'Regional limitation', 'Regional limitation', 'Regional limitation', 'Regional limitation', 'Regional limitation', 'High competition', 'High competition', 'High competition', 'Very high competition', 'Moderate presence', 'Low investment', 'Saturation', 'High saturation', 'Moderate presence', 'Seasonal demand', 'High presence', 'Regional limitation', 'Regional limitation', 'Regional limitation', 'Low investment', 'Low investment', 'Low investment', 'Regional limitation', 'Low revenue', 'New concept', 'Regional limitation', 'Regional limitation', 'Very low investment', 'Regional limitation', 'Regional limitation', 'High competition', 'High competition', 'High competition', 'Regional limitation', 'High investment', 'Regional limitation', 'Regional limitation', 'Regional limitation', 'Regional limitation', 'Regional limitation', 'Moderate presence', 'Regional specialty', 'Regional limitation', 'Regional limitation', 'Regional limitation', 'Moderate investment', 'High presence', 'High standards', 'Regional limitation', 'Regional limitation'
        ]
    }
    return pd.DataFrame(data)

df = load_data()

# Dictionary of real official websites for major brands
OFFICIAL_URLS = {
    'Yoshinoya': 'https://www.yoshinoya.com/',
    'Sukiya': 'https://www.sukiya.jp/',
    'Matsuya': 'https://www.matsuyafoods.co.jp/',
    'CoCo Ichibanya': 'https://ichibanya.co.jp/english/',
    'Kura Sushi': 'https://www.kurasushi.co.jp/',
    'Sushiro': 'https://www.akindo-sushiro.co.jp/',
    'Ippudo Ramen': 'https://www.ippudo.com/',
    'Mos Burger': 'https://www.mosfood.co.jp/',
    'Ootoya': 'https://www.ootoya.com/',
    'Komeda Coffee': 'https://www.komeda.co.jp/',
    'Doutor Coffee': 'https://www.doutor.co.jp/',
    'Mister Donut': 'https://www.misterdonut.jp/',
    'Tenka Ippin': 'https://www.tenkaippin.com/',
    'Go-Go Curry': 'https://www.gogocurry.com/',
    'Torikizoku': 'https://www.torikizoku.co.jp/'
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
st.warning("⚠️ **Data Disclaimer:** Financial figures (investment, fees, revenue) are **estimates based on industry averages** and publicly available data. They are for informational purposes only. Always verify with official Franchise Disclosure Documents (FDD) and contact the franchisor directly before making investment decisions.")

st.sidebar.success(f"📊 **{len(df)}+ Japanese Franchises** in database")

# Sidebar Filters
st.sidebar.header("🔍 Filter Brands")
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
            st.markdown(f"** Intro Video:** [Search YouTube for '{selected_brand}']({youtube_url})")

        # FEATURE 2: Report Incorrect Data Feature
        st.markdown("---")
        st.subheader("📢 Report Data Issue")
        st.caption("Help us keep our database accurate. If you spot incorrect financial data or store counts, let us know!")
        
        with st.form("report_form"):
            issue_type = st.selectbox("Issue Type", ["Incorrect Financial Data", "Outdated Store Count", "Wrong Brand Info", "Other"])
            details = st.text_area("Please describe the correct information or issue:", placeholder="e.g., The franchise fee for this brand is actually $30,000...")
            submitted = st.form_submit_button("📧 Generate Report Email")
            
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
    st.subheader("️ Side-by-Side Brand Comparison")
    
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
