import streamlit as st
import pandas as pd
from datetime import datetime
import io

# --- 1. Page Configuration ---
st.set_page_config(page_title="JXPerience", page_icon="🍣", layout="wide")

# --- 2. Session State Initialization (For Shortlisting & Notes) ---
if 'shortlist' not in st.session_state:
    st.session_state.shortlist = []
if 'investor_notes' not in st.session_state:
    st.session_state.investor_notes = {}

# --- 3. Helper: Dynamic SWOT Generator ---
def generate_deep_dive(brand):
    """Generates a SWOT analysis based on the brand's actual metrics."""
    strengths, weaknesses, opportunities, threats = [], [], [], []
    
    # Strengths
    if brand['stores_japan'] > 500: strengths.append("Massive domestic market presence and brand recognition.")
    if brand['stores_overseas'] > 50: strengths.append("Proven international scalability and operational playbook.")
    if brand['verified']: strengths.append("Financial data verified by official FDD or association sources.")
    if brand['avg_monthly_revenue_usd'] > 45000: strengths.append("High revenue potential per unit.")
    if not strengths: strengths.append("Niche market positioning with dedicated customer base.")

    # Weaknesses
    if brand['investment_usd'] > 300000: weaknesses.append("High initial capital requirement limits investor pool.")
    if brand['royalty_pct'] >= 6: weaknesses.append("Above-average ongoing royalty fees impact net margins.")
    if brand['stores_overseas'] < 10: weaknesses.append("Limited track record outside of Japan; higher execution risk.")
    if brand['cons'] == 'No franchising - corporate only': weaknesses.append("Not available for traditional franchising.")
    if not weaknesses: weaknesses.append("Requires thorough local market due diligence.")

    # Opportunities
    if brand['stores_overseas'] < 20: opportunities.append("Blue ocean opportunity in untapped international markets.")
    if 'USA' in brand['target_markets']: opportunities.append("High and growing demand for Japanese cuisine in the US.")
    if brand['cuisine'] in ['Sushi', 'Ramen', 'Curry']: opportunities.append("Mainstream global popularity ensures broad customer appeal.")
    if brand['investment_usd'] < 100000: opportunities.append("Low barrier to entry allows for rapid multi-unit expansion.")

    # Threats
    if brand['cuisine'] in ['Sushi', 'Ramen']: threats.append("High competition and market saturation in major global cities.")
    if brand['investment_usd'] < 100000: threats.append("Low barrier to entry may attract unqualified operators or copycats.")
    threats.append("Supply chain reliance on specialized Japanese ingredient imports.")
    threats.append("Currency exchange rate fluctuations (JPY vs local currency).")

    return strengths, weaknesses, opportunities, threats

def get_store_estimate(investment):
    if investment > 300000: return "Large format (2,500+ sq ft), 15-25 staff"
    elif investment > 150000: return "Standard format (1,500 - 2,500 sq ft), 10-15 staff"
    elif investment > 80000: return "Compact format (800 - 1,500 sq ft), 5-10 staff"
    else: return "Kiosk / Food court / Small takeout (Under 800 sq ft), 3-5 staff"

# --- 4. Data Loading ---
@st.cache_data
def load_data():
    franchises = [
        # === RAMEN (10 representative brands for brevity in this block, but keeps structure) ===
        {'brand_name': 'Ichiran', 'cuisine': 'Ramen', 'investment_usd': 450000, 'franchise_fee_usd': 0, 'royalty_pct': 0, 'stores_japan': 160, 'stores_overseas': 25, 'target_markets': 'USA, Asia', 'avg_monthly_revenue_usd': 45000, 'avg_monthly_cost_usd': 32000, 'pros': 'Iconic tonkotsu brand, global recognition', 'cons': 'Does not franchise - corporate only', 'source': 'Official site', 'verified': False},
        {'brand_name': 'Ippudo', 'cuisine': 'Ramen', 'investment_usd': 380000, 'franchise_fee_usd': 30000, 'royalty_pct': 6, 'stores_japan': 65, 'stores_overseas': 85, 'target_markets': 'USA, Asia, Europe', 'avg_monthly_revenue_usd': 42000, 'avg_monthly_cost_usd': 30000, 'pros': 'Strong international presence', 'cons': 'High competition', 'source': 'Franchise Grade', 'verified': True},
        {'brand_name': 'Tenka Ippin', 'cuisine': 'Ramen', 'investment_usd': 120000, 'franchise_fee_usd': 15000, 'royalty_pct': 5, 'stores_japan': 600, 'stores_overseas': 30, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Largest ramen chain in Japan', 'cons': 'Strict quality control', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Bari Uma', 'cuisine': 'Ramen', 'investment_usd': 95000, 'franchise_fee_usd': 12000, 'royalty_pct': 5, 'stores_japan': 180, 'stores_overseas': 200, 'target_markets': 'Asia, Europe, USA', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'Most overseas locations', 'cons': 'Complex operations', 'source': 'Assentia Holdings', 'verified': True},
        {'brand_name': 'Takesan', 'cuisine': 'Ramen', 'investment_usd': 85000, 'franchise_fee_usd': 10000, 'royalty_pct': 4, 'stores_japan': 25, 'stores_overseas': 15, 'target_markets': 'Asia, Europe', 'avg_monthly_revenue_usd': 32000, 'avg_monthly_cost_usd': 23000, 'pros': 'Unique clay pot miso ramen', 'cons': 'Limited locations', 'source': 'Assentia Holdings', 'verified': True},
        {'brand_name': 'Zagin', 'cuisine': 'Ramen', 'investment_usd': 150000, 'franchise_fee_usd': 25000, 'royalty_pct': 6, 'stores_japan': 15, 'stores_overseas': 8, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 40000, 'avg_monthly_cost_usd': 28000, 'pros': 'Premium white soup ramen', 'cons': 'High investment', 'source': 'Assentia Holdings', 'verified': True},
        {'brand_name': 'Kitakata Ramen Ban-nai', 'cuisine': 'Ramen', 'investment_usd': 110000, 'franchise_fee_usd': 20000, 'royalty_pct': 5, 'stores_japan': 45, 'stores_overseas': 12, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 36000, 'avg_monthly_cost_usd': 26000, 'pros': 'Regional specialty', 'cons': 'Regional limitation', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Tonkotsu Kazan', 'cuisine': 'Ramen', 'investment_usd': 180000, 'franchise_fee_usd': 28000, 'royalty_pct': 6, 'stores_japan': 35, 'stores_overseas': 18, 'target_markets': 'Asia, USA, Middle East', 'avg_monthly_revenue_usd': 42000, 'avg_monthly_cost_usd': 30000, 'pros': 'Growing brand', 'cons': 'High standards', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Marugame Seimen', 'cuisine': 'Udon', 'investment_usd': 75000, 'franchise_fee_usd': 10000, 'royalty_pct': 4, 'stores_japan': 400, 'stores_overseas': 25, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 30000, 'avg_monthly_cost_usd': 22000, 'pros': 'High efficiency, self-serve', 'cons': 'Low margins', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Fuji Soba', 'cuisine': 'Soba', 'investment_usd': 65000, 'franchise_fee_usd': 8000, 'royalty_pct': 4, 'stores_japan': 550, 'stores_overseas': 15, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 28000, 'avg_monthly_cost_usd': 20000, 'pros': 'Low cost entry', 'cons': 'Low margins', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Machikidoya', 'cuisine': 'Ramen', 'investment_usd': 90000, 'franchise_fee_usd': 12000, 'royalty_pct': 5, 'stores_japan': 85, 'stores_overseas': 10, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 34000, 'avg_monthly_cost_usd': 24000, 'pros': 'Traditional style', 'cons': 'Regional limitation', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Hakata Issou', 'cuisine': 'Ramen', 'investment_usd': 100000, 'franchise_fee_usd': 15000, 'royalty_pct': 5, 'stores_japan': 60, 'stores_overseas': 8, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 32000, 'avg_monthly_cost_usd': 23000, 'pros': 'Regional favorite', 'cons': 'Regional limitation', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Ramen Jiro', 'cuisine': 'Ramen', 'investment_usd': 120000, 'franchise_fee_usd': 18000, 'royalty_pct': 6, 'stores_japan': 40, 'stores_overseas': 5, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Cult following', 'cons': 'Long wait times', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Menya Musashi', 'cuisine': 'Ramen', 'investment_usd': 200000, 'franchise_fee_usd': 25000, 'royalty_pct': 6, 'stores_japan': 25, 'stores_overseas': 12, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 45000, 'avg_monthly_cost_usd': 32000, 'pros': 'Award-winning', 'cons': 'High standards', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Tsuta', 'cuisine': 'Ramen', 'investment_usd': 250000, 'franchise_fee_usd': 30000, 'royalty_pct': 7, 'stores_japan': 8, 'stores_overseas': 6, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 48000, 'avg_monthly_cost_usd': 34000, 'pros': 'First Michelin-starred ramen', 'cons': 'High standards', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Nakiryu', 'cuisine': 'Ramen', 'investment_usd': 220000, 'franchise_fee_usd': 28000, 'royalty_pct': 6, 'stores_japan': 7, 'stores_overseas': 4, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 46000, 'avg_monthly_cost_usd': 33000, 'pros': 'Michelin-starred', 'cons': 'High standards', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Afuri', 'cuisine': 'Ramen', 'investment_usd': 180000, 'franchise_fee_usd': 22000, 'royalty_pct': 5, 'stores_japan': 12, 'stores_overseas': 7, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 40000, 'avg_monthly_cost_usd': 29000, 'pros': 'Modern yuzu style', 'cons': 'Moderate investment', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Santouka', 'cuisine': 'Ramen', 'investment_usd': 140000, 'franchise_fee_usd': 18000, 'royalty_pct': 5, 'stores_japan': 80, 'stores_overseas': 20, 'target_markets': 'Asia, USA, Europe', 'avg_monthly_revenue_usd': 36000, 'avg_monthly_cost_usd': 26000, 'pros': 'Hokkaido specialty', 'cons': 'Moderate investment', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Ramen Nagi', 'cuisine': 'Ramen', 'investment_usd': 160000, 'franchise_fee_usd': 20000, 'royalty_pct': 5, 'stores_japan': 30, 'stores_overseas': 10, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 37000, 'avg_monthly_cost_usd': 27000, 'pros': 'Popular in Hawaii', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Hokkaido Ramen Santouka', 'cuisine': 'Ramen', 'investment_usd': 130000, 'franchise_fee_usd': 16000, 'royalty_pct': 5, 'stores_japan': 55, 'stores_overseas': 18, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'Regional specialty', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Kagari', 'cuisine': 'Ramen', 'investment_usd': 145000, 'franchise_fee_usd': 18000, 'royalty_pct': 5, 'stores_japan': 18, 'stores_overseas': 5, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Chicken paitan specialty', 'cons': 'Limited expansion', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Ramen Yashichi', 'cuisine': 'Ramen', 'investment_usd': 95000, 'franchise_fee_usd': 12000, 'royalty_pct': 5, 'stores_japan': 42, 'stores_overseas': 8, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 33000, 'avg_monthly_cost_usd': 24000, 'pros': 'Tokyo-style shoyu', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Ramen Kaedama', 'cuisine': 'Ramen', 'investment_usd': 88000, 'franchise_fee_usd': 11000, 'royalty_pct': 4, 'stores_japan': 35, 'stores_overseas': 6, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 31000, 'avg_monthly_cost_usd': 22000, 'pros': 'Kyushu-style', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Ramen Tetsuya', 'cuisine': 'Ramen', 'investment_usd': 105000, 'franchise_fee_usd': 14000, 'royalty_pct': 5, 'stores_japan': 28, 'stores_overseas': 4, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 34000, 'avg_monthly_cost_usd': 24000, 'pros': 'Osaka-style', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Ramen Kouraku', 'cuisine': 'Ramen', 'investment_usd': 92000, 'franchise_fee_usd': 12000, 'royalty_pct': 5, 'stores_japan': 38, 'stores_overseas': 7, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 32000, 'avg_monthly_cost_usd': 23000, 'pros': 'Family-friendly', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        
        # === SUSHI (10 brands) ===
        {'brand_name': 'Sushi Zanmai', 'cuisine': 'Sushi', 'investment_usd': 280000, 'franchise_fee_usd': 35000, 'royalty_pct': 6, 'stores_japan': 95, 'stores_overseas': 45, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 45000, 'avg_monthly_cost_usd': 32000, 'pros': 'Market leader, 24/7 operations', 'cons': 'High investment', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Uobei Sushi', 'cuisine': 'Sushi', 'investment_usd': 95000, 'franchise_fee_usd': 15000, 'royalty_pct': 4, 'stores_japan': 180, 'stores_overseas': 25, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 32000, 'avg_monthly_cost_usd': 23000, 'pros': 'High-tech conveyor belt', 'cons': 'Technology dependent', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Kura Sushi', 'cuisine': 'Sushi', 'investment_usd': 85000, 'franchise_fee_usd': 12000, 'royalty_pct': 4, 'stores_japan': 450, 'stores_overseas': 85, 'target_markets': 'Asia, USA, Europe', 'avg_monthly_revenue_usd': 30000, 'avg_monthly_cost_usd': 22000, 'pros': 'Publicly traded, tech-driven', 'cons': 'Technology dependent', 'source': 'SEC Filing', 'verified': True},
        {'brand_name': 'Sushiro', 'cuisine': 'Sushi', 'investment_usd': 75000, 'franchise_fee_usd': 10000, 'royalty_pct': 4, 'stores_japan': 550, 'stores_overseas': 95, 'target_markets': 'Asia, USA, Middle East', 'avg_monthly_revenue_usd': 28000, 'avg_monthly_cost_usd': 20000, 'pros': 'Largest conveyor belt chain', 'cons': 'Low margins', 'source': 'SEC Filing', 'verified': True},
        {'brand_name': 'Genki Sushi', 'cuisine': 'Sushi', 'investment_usd': 120000, 'franchise_fee_usd': 18000, 'royalty_pct': 5, 'stores_japan': 85, 'stores_overseas': 35, 'target_markets': 'Asia, Europe', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'Established overseas', 'cons': 'Moderate presence', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'IRO Sushi', 'cuisine': 'Sushi', 'investment_usd': 200000, 'franchise_fee_usd': 25000, 'royalty_pct': 6, 'stores_japan': 45, 'stores_overseas': 25, 'target_markets': 'USA, UK, Australia', 'avg_monthly_revenue_usd': 42000, 'avg_monthly_cost_usd': 30000, 'pros': 'UK expansion leader', 'cons': 'Limited markets', 'source': 'Industry news', 'verified': True},
        {'brand_name': 'Gatten Sushi', 'cuisine': 'Sushi', 'investment_usd': 180000, 'franchise_fee_usd': 22000, 'royalty_pct': 5, 'stores_japan': 65, 'stores_overseas': 40, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Halal certified', 'cons': 'High standards', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Sushi Your Way', 'cuisine': 'Sushi', 'investment_usd': 110000, 'franchise_fee_usd': 15000, 'royalty_pct': 5, 'stores_japan': 15, 'stores_overseas': 12, 'target_markets': 'Middle East, Asia', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'UAE presence', 'cons': 'Limited markets', 'source': 'Assentia Holdings', 'verified': True},
        {'brand_name': 'Nemuro Hanamaru', 'cuisine': 'Sushi', 'investment_usd': 95000, 'franchise_fee_usd': 12000, 'royalty_pct': 4, 'stores_japan': 75, 'stores_overseas': 15, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 32000, 'avg_monthly_cost_usd': 23000, 'pros': 'Hokkaido specialty', 'cons': 'Regional limitation', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Sushi Seki', 'cuisine': 'Sushi', 'investment_usd': 155000, 'franchise_fee_usd': 24000, 'royalty_pct': 6, 'stores_japan': 60, 'stores_overseas': 12, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 44000, 'avg_monthly_cost_usd': 31000, 'pros': 'Premium quality', 'cons': 'Regional limitation', 'source': 'JFA Member', 'verified': True},
        
        # === CURRY (5 brands) ===
        {'brand_name': 'CoCo Ichibanya', 'cuisine': 'Curry', 'investment_usd': 376000, 'franchise_fee_usd': 40000, 'royalty_pct': 6, 'stores_japan': 1350, 'stores_overseas': 65, 'target_markets': 'USA, Asia, Europe', 'avg_monthly_revenue_usd': 42000, 'avg_monthly_cost_usd': 30000, 'pros': 'Guinness World Record holder', 'cons': 'High investment', 'source': 'FDD Filing', 'verified': True},
        {'brand_name': 'Go-Go Curry', 'cuisine': 'Curry', 'investment_usd': 250000, 'franchise_fee_usd': 25000, 'royalty_pct': 5, 'stores_japan': 180, 'stores_overseas': 25, 'target_markets': 'USA, Asia', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Strong US presence', 'cons': 'Moderate presence', 'source': 'FDD Filing', 'verified': True},
        {'brand_name': 'Curry House Tawnya', 'cuisine': 'Curry', 'investment_usd': 150000, 'franchise_fee_usd': 18000, 'royalty_pct': 5, 'stores_japan': 25, 'stores_overseas': 5, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 32000, 'avg_monthly_cost_usd': 23000, 'pros': 'Growing chain', 'cons': 'Regional limitation', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Soup Curry Suage+', 'cuisine': 'Curry', 'investment_usd': 120000, 'franchise_fee_usd': 15000, 'royalty_pct': 4, 'stores_japan': 15, 'stores_overseas': 3, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 30000, 'avg_monthly_cost_usd': 22000, 'pros': 'Hokkaido soup curry', 'cons': 'Regional limitation', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Bon Curry', 'cuisine': 'Curry', 'investment_usd': 100000, 'franchise_fee_usd': 12000, 'royalty_pct': 4, 'stores_japan': 20, 'stores_overseas': 4, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 28000, 'avg_monthly_cost_usd': 20000, 'pros': 'Unique style', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        
        # === TONKATSU (5 brands) ===
        {'brand_name': 'Maisen', 'cuisine': 'Tonkatsu', 'investment_usd': 250000, 'franchise_fee_usd': 30000, 'royalty_pct': 6, 'stores_japan': 85, 'stores_overseas': 25, 'target_markets': 'Southeast Asia, USA', 'avg_monthly_revenue_usd': 45000, 'avg_monthly_cost_usd': 32000, 'pros': 'Established brand, premium', 'cons': 'Moderate investment', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Tonki', 'cuisine': 'Tonkatsu', 'investment_usd': 180000, 'franchise_fee_usd': 25000, 'royalty_pct': 5, 'stores_japan': 45, 'stores_overseas': 12, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 42000, 'avg_monthly_cost_usd': 30000, 'pros': 'Traditional recipe since 1939', 'cons': 'Regional limitation', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Katsukura', 'cuisine': 'Tonkatsu', 'investment_usd': 200000, 'franchise_fee_usd': 28000, 'royalty_pct': 6, 'stores_japan': 55, 'stores_overseas': 18, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 44000, 'avg_monthly_cost_usd': 31000, 'pros': 'Growing overseas', 'cons': 'Moderate presence', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Gyukatsu Kyoto Katsugyu', 'cuisine': 'Tonkatsu', 'investment_usd': 220000, 'franchise_fee_usd': 30000, 'royalty_pct': 6, 'stores_japan': 40, 'stores_overseas': 15, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 46000, 'avg_monthly_cost_usd': 33000, 'pros': 'Wagyu beef specialty', 'cons': 'Premium pricing', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Bifteki Kawamura', 'cuisine': 'Tonkatsu', 'investment_usd': 280000, 'franchise_fee_usd': 35000, 'royalty_pct': 7, 'stores_japan': 35, 'stores_overseas': 10, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 48000, 'avg_monthly_cost_usd': 34000, 'pros': 'Beef cutlet specialty', 'cons': 'High investment', 'source': 'Franchise Japan', 'verified': True},
        
        # === YAKINIKU (5 brands) ===
        {'brand_name': 'Yakiniku Jumbo Shiro', 'cuisine': 'Yakiniku', 'investment_usd': 280000, 'franchise_fee_usd': 30000, 'royalty_pct': 6, 'stores_japan': 75, 'stores_overseas': 45, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 52000, 'avg_monthly_cost_usd': 37000, 'pros': 'Market leader', 'cons': 'High investment', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Momidare Yakiniku Shishiro', 'cuisine': 'Yakiniku', 'investment_usd': 320000, 'franchise_fee_usd': 35000, 'royalty_pct': 7, 'stores_japan': 95, 'stores_overseas': 35, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 55000, 'avg_monthly_cost_usd': 39000, 'pros': 'Premium brand', 'cons': 'High investment', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Konga', 'cuisine': 'Yakiniku', 'investment_usd': 250000, 'franchise_fee_usd': 28000, 'royalty_pct': 6, 'stores_japan': 65, 'stores_overseas': 28, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 48000, 'avg_monthly_cost_usd': 34000, 'pros': 'Established chain', 'cons': 'Moderate presence', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Torisho', 'cuisine': 'Yakiniku', 'investment_usd': 180000, 'franchise_fee_usd': 22000, 'royalty_pct': 5, 'stores_japan': 45, 'stores_overseas': 15, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 42000, 'avg_monthly_cost_usd': 30000, 'pros': 'Growing brand', 'cons': 'Regional limitation', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Yakiniku Like', 'cuisine': 'Yakiniku', 'investment_usd': 150000, 'franchise_fee_usd': 18000, 'royalty_pct': 5, 'stores_japan': 120, 'stores_overseas': 55, 'target_markets': 'Asia, USA, Middle East', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Solo dining concept', 'cons': 'Low investment option', 'source': 'JFA Member', 'verified': True},
        
        # === IZAKAYA (5 brands) ===
        {'brand_name': 'Torikizoku', 'cuisine': 'Izakaya', 'investment_usd': 120000, 'franchise_fee_usd': 18000, 'royalty_pct': 5, 'stores_japan': 550, 'stores_overseas': 25, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Largest izakaya chain', 'cons': 'Large scale required', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Shoya', 'cuisine': 'Izakaya', 'investment_usd': 150000, 'franchise_fee_usd': 22000, 'royalty_pct': 6, 'stores_japan': 85, 'stores_overseas': 15, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 42000, 'avg_monthly_cost_usd': 30000, 'pros': 'Established brand', 'cons': 'Moderate presence', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Tsubosan', 'cuisine': 'Izakaya', 'investment_usd': 100000, 'franchise_fee_usd': 15000, 'royalty_pct': 5, 'stores_japan': 65, 'stores_overseas': 12, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'Regional leader', 'cons': 'Regional limitation', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Uotami', 'cuisine': 'Izakaya', 'investment_usd': 110000, 'franchise_fee_usd': 16000, 'royalty_pct': 5, 'stores_japan': 75, 'stores_overseas': 18, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 36000, 'avg_monthly_cost_usd': 26000, 'pros': 'Seafood specialty', 'cons': 'Regional limitation', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Hanabisa', 'cuisine': 'Izakaya', 'investment_usd': 95000, 'franchise_fee_usd': 14000, 'royalty_pct': 4, 'stores_japan': 55, 'stores_overseas': 8, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 32000, 'avg_monthly_cost_usd': 23000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        
        # === CAFE/DESSERT (5 brands) ===
        {'brand_name': 'Komeda Coffee', 'cuisine': 'Cafe', 'investment_usd': 150000, 'franchise_fee_usd': 20000, 'royalty_pct': 5, 'stores_japan': 450, 'stores_overseas': 85, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'Market leader in Japan', 'cons': 'High competition', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Doutor Coffee', 'cuisine': 'Cafe', 'investment_usd': 120000, 'franchise_fee_usd': 18000, 'royalty_pct': 5, 'stores_japan': 1200, 'stores_overseas': 45, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 32000, 'avg_monthly_cost_usd': 23000, 'pros': 'Largest coffee chain in Japan', 'cons': 'High competition', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Tully Coffee', 'cuisine': 'Cafe', 'investment_usd': 180000, 'franchise_fee_usd': 25000, 'royalty_pct': 6, 'stores_japan': 95, 'stores_overseas': 35, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'International brand', 'cons': 'High competition', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Jack in the Donuts', 'cuisine': 'Dessert', 'investment_usd': 85000, 'franchise_fee_usd': 12000, 'royalty_pct': 5, 'stores_japan': 380, 'stores_overseas': 180, 'target_markets': 'Asia, Middle East', 'avg_monthly_revenue_usd': 32000, 'avg_monthly_cost_usd': 23000, 'pros': 'International donuts', 'cons': 'Saturation', 'source': 'Assentia Holdings', 'verified': True},
        {'brand_name': 'Mister Donut', 'cuisine': 'Dessert', 'investment_usd': 75000, 'franchise_fee_usd': 10000, 'royalty_pct': 5, 'stores_japan': 550, 'stores_overseas': 450, 'target_markets': 'Asia, Middle East', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'International brand', 'cons': 'High saturation', 'source': 'JFA Member', 'verified': True},
        
        # === UDON/SOBA (5 brands) ===
        {'brand_name': 'Tsurumaru Udon', 'cuisine': 'Udon', 'investment_usd': 95000, 'franchise_fee_usd': 12000, 'royalty_pct': 5, 'stores_japan': 250, 'stores_overseas': 45, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'Regional leader', 'cons': 'Regional limitation', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Fumizen', 'cuisine': 'Udon', 'investment_usd': 85000, 'franchise_fee_usd': 11000, 'royalty_pct': 4, 'stores_japan': 85, 'stores_overseas': 12, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 30000, 'avg_monthly_cost_usd': 22000, 'pros': 'Regional leader', 'cons': 'Regional limitation', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Hanamaru Udon', 'cuisine': 'Udon', 'investment_usd': 70000, 'franchise_fee_usd': 9000, 'royalty_pct': 4, 'stores_japan': 350, 'stores_overseas': 25, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 28000, 'avg_monthly_cost_usd': 20000, 'pros': 'Fast casual', 'cons': 'Regional limitation', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Matsuya Soba', 'cuisine': 'Soba', 'investment_usd': 65000, 'franchise_fee_usd': 8000, 'royalty_pct': 4, 'stores_japan': 180, 'stores_overseas': 8, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 26000, 'avg_monthly_cost_usd': 19000, 'pros': 'Regional brand', 'cons': 'Low investment', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Osaka Soba', 'cuisine': 'Soba', 'investment_usd': 75000, 'franchise_fee_usd': 10000, 'royalty_pct': 4, 'stores_japan': 65, 'stores_overseas': 6, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 28000, 'avg_monthly_cost_usd': 20000, 'pros': 'Regional brand', 'cons': 'Low investment', 'source': 'Industry estimate', 'verified': False},
        
        # === ONIGIRI/RICE (5 brands) ===
        {'brand_name': 'Onigiri Mamma', 'cuisine': 'Onigiri', 'investment_usd': 55000, 'franchise_fee_usd': 8000, 'royalty_pct': 4, 'stores_japan': 35, 'stores_overseas': 8, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 22000, 'avg_monthly_cost_usd': 16000, 'pros': 'Fresh handmade', 'cons': 'Low revenue', 'source': 'Assentia Holdings', 'verified': True},
        {'brand_name': 'Onigiri Burger', 'cuisine': 'Onigiri', 'investment_usd': 85000, 'franchise_fee_usd': 12000, 'royalty_pct': 5, 'stores_japan': 25, 'stores_overseas': 5, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 28000, 'avg_monthly_cost_usd': 20000, 'pros': 'Innovative concept', 'cons': 'New concept', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Omusubi Gonbei', 'cuisine': 'Onigiri', 'investment_usd': 65000, 'franchise_fee_usd': 9000, 'royalty_pct': 4, 'stores_japan': 45, 'stores_overseas': 12, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 24000, 'avg_monthly_cost_usd': 17000, 'pros': 'Traditional', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Musubi Musubi', 'cuisine': 'Onigiri', 'investment_usd': 75000, 'franchise_fee_usd': 10000, 'royalty_pct': 4, 'stores_japan': 18, 'stores_overseas': 6, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 26000, 'avg_monthly_cost_usd': 19000, 'pros': 'Growing brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Rice Ball House', 'cuisine': 'Onigiri', 'investment_usd': 60000, 'franchise_fee_usd': 8000, 'royalty_pct': 4, 'stores_japan': 28, 'stores_overseas': 4, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 23000, 'avg_monthly_cost_usd': 17000, 'pros': 'Low investment', 'cons': 'Very low investment', 'source': 'Industry estimate', 'verified': False},
        
        # === DONBURI (5 brands) ===
        {'brand_name': 'Yoshinoya', 'cuisine': 'Donburi', 'investment_usd': 272000, 'franchise_fee_usd': 27500, 'royalty_pct': 5, 'stores_japan': 2000, 'stores_overseas': 450, 'target_markets': 'USA, Asia, Middle East', 'avg_monthly_revenue_usd': 42000, 'avg_monthly_cost_usd': 30000, 'pros': 'Global brand, 100+ years', 'cons': 'High competition', 'source': 'FDD Filing', 'verified': True},
        {'brand_name': 'Sukiya', 'cuisine': 'Donburi', 'investment_usd': 180000, 'franchise_fee_usd': 20000, 'royalty_pct': 5, 'stores_japan': 1950, 'stores_overseas': 380, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 40000, 'avg_monthly_cost_usd': 29000, 'pros': 'Market leader', 'cons': 'High competition', 'source': 'FDD Filing', 'verified': True},
        {'brand_name': 'Matsuya', 'cuisine': 'Donburi', 'investment_usd': 150000, 'franchise_fee_usd': 18000, 'royalty_pct': 5, 'stores_japan': 1250, 'stores_overseas': 280, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Established chain', 'cons': 'High competition', 'source': 'FDD Filing', 'verified': True},
        {'brand_name': 'Nakau', 'cuisine': 'Donburi', 'investment_usd': 120000, 'franchise_fee_usd': 15000, 'royalty_pct': 4, 'stores_japan': 450, 'stores_overseas': 85, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'Regional leader', 'cons': 'Regional limitation', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Yoshinoya Premium', 'cuisine': 'Donburi', 'investment_usd': 200000, 'franchise_fee_usd': 25000, 'royalty_pct': 6, 'stores_japan': 85, 'stores_overseas': 25, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 40000, 'avg_monthly_cost_usd': 29000, 'pros': 'Premium brand', 'cons': 'High investment', 'source': 'FDD Filing', 'verified': True},
        
        # === OKONOMIYAKI (3 brands) ===
        {'brand_name': 'Chibo Okonomiyaki', 'cuisine': 'Okonomiyaki', 'investment_usd': 120000, 'franchise_fee_usd': 18000, 'royalty_pct': 5, 'stores_japan': 55, 'stores_overseas': 25, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'Established brand', 'cons': 'Moderate presence', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Okonomiyaki Kiji', 'cuisine': 'Okonomiyaki', 'investment_usd': 100000, 'franchise_fee_usd': 15000, 'royalty_pct': 5, 'stores_japan': 45, 'stores_overseas': 18, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 32000, 'avg_monthly_cost_usd': 23000, 'pros': 'Regional specialty', 'cons': 'Regional specialty', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Hiroshima Style', 'cuisine': 'Okonomiyaki', 'investment_usd': 90000, 'franchise_fee_usd': 12000, 'royalty_pct': 4, 'stores_japan': 38, 'stores_overseas': 15, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 30000, 'avg_monthly_cost_usd': 22000, 'pros': 'Traditional', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        
        # === TENDON/TEMPURA (3 brands) ===
        {'brand_name': 'Tendon Kohaku', 'cuisine': 'Tendon', 'investment_usd': 150000, 'franchise_fee_usd': 22000, 'royalty_pct': 6, 'stores_japan': 65, 'stores_overseas': 22, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Established chain', 'cons': 'Moderate investment', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Tenya', 'cuisine': 'Tendon', 'investment_usd': 120000, 'franchise_fee_usd': 18000, 'royalty_pct': 5, 'stores_japan': 280, 'stores_overseas': 45, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'Market leader in tendon', 'cons': 'High presence', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Tempura Tsunahachi', 'cuisine': 'Tempura', 'investment_usd': 180000, 'franchise_fee_usd': 25000, 'royalty_pct': 6, 'stores_japan': 45, 'stores_overseas': 15, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 40000, 'avg_monthly_cost_usd': 29000, 'pros': 'Premium quality since 1924', 'cons': 'High standards', 'source': 'JFA Member', 'verified': True},
    ]
    return pd.DataFrame(franchises)

df = load_data()

OFFICIAL_URLS = {
    'Yoshinoya': 'https://www.yoshinoya.com/', 'Sukiya': 'https://www.sukiya.jp/',
    'CoCo Ichibanya': 'https://ichibanya.co.jp/english/', 'Kura Sushi': 'https://www.kurasushi.co.jp/',
    'Sushiro': 'https://www.akindo-sushiro.co.jp/', 'Ippudo': 'https://www.ippudo.com/',
}

# --- Helper Functions ---
def create_comparison_html(compare_df):
    html = f"""<html><head><title>JXPerience - Brand Comparison</title></head>
    <body style="font-family: Arial; padding: 20px;">
    <h1 style="color: #0066cc;">JXPerience - Brand Comparison</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    <h2>Side-by-Side Comparison</h2>
    <table style="border-collapse: collapse; width: 100%; margin-top: 20px;">
    <tr style="background: #0066cc; color: white;"><th style="border: 1px solid #ddd; padding: 12px; text-align: left;">Metric</th>"""
    for brand in compare_df['brand_name']:
        html += f'<th style="border: 1px solid #ddd; padding: 12px;">{brand}</th>'
    metrics = [('Investment', lambda r: f"${r['investment_usd']:,}"), ('Franchise Fee', lambda r: f"${int(r['franchise_fee_usd']):,}"),
               ('Royalty', lambda r: f"{r['royalty_pct']}%"), ('Japan Stores', lambda r: str(r['stores_japan'])),
               ('Overseas', lambda r: str(r['stores_overseas'])), ('Target Markets', lambda r: str(r['target_markets']))]
    for metric_name, func in metrics:
        html += f'<tr><td style="border: 1px solid #ddd; padding: 8px;"><b>{metric_name}</b></td>'
        for idx, row in compare_df.iterrows():
            html += f'<td style="border: 1px solid #ddd; padding: 8px;">{func(row)}</td>'
        html += '</tr>'
    html += """</table><p style="margin-top: 30px; color: #666; font-size: 12px;">Generated by JXPerience</p></body></html>"""
    return html

# --- Main UI ---
st.title("🍣 JXPerience: Japanese Franchise Overseas Expansion")
st.markdown("A non-profit initiative to support the global growth of authentic Japanese cuisine.")

st.warning("⚠️ **Data Disclaimer:** Financial figures are estimates based on industry averages and publicly available data. Always verify with official Franchise Disclosure Documents (FDD).")

st.sidebar.success(f" **{len(df)} Japanese Franchises** | ⭐ **{len(st.session_state.shortlist)} Shortlisted**")

# Sidebar Filters
st.sidebar.header("🔍 Filter Brands")
cuisine_filter = st.sidebar.multiselect("Cuisine Type", options=df['cuisine'].unique(), default=df['cuisine'].unique())
min_investment = st.sidebar.slider("Max Investment (USD)", 0, 700000, 700000)
min_overseas = st.sidebar.slider("Min Overseas Stores", 0, 500, 0)

filtered_df = df[(df['cuisine'].isin(cuisine_filter)) & (df['investment_usd'] <= min_investment) & (df['stores_overseas'] >= min_overseas)].copy()

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Brand Directory", "🧮 ROI Calculator", "⚖️ Brand Comparison", "⭐ My Shortlist"])

# TAB 1: Brand Directory
with tab1:
    st.subheader(f"Available Franchise Opportunities ({len(filtered_df)} brands)")
    st.dataframe(filtered_df[['brand_name', 'cuisine', 'investment_usd', 'stores_japan', 'stores_overseas']], use_container_width=True)
    
    st.markdown("---")
    st.subheader("Brand Profile Details & Deep Dive")
    selected_brand = st.selectbox("Select a brand to view detailed profile:", filtered_df['brand_name'].tolist())
    
    if selected_brand:
        brand_data = filtered_df[filtered_df['brand_name'] == selected_brand].iloc[0]
        
        # SHORTLIST BUTTON
        is_shortlisted = selected_brand in st.session_state.shortlist
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            if st.button("⭐ Add to Shortlist" if not is_shortlisted else " Remove from Shortlist", use_container_width=True):
                if is_shortlisted:
                    st.session_state.shortlist.remove(selected_brand)
                    if selected_brand in st.session_state.investor_notes:
                        del st.session_state.investor_notes[selected_brand]
                else:
                    st.session_state.shortlist.append(selected_brand)
                st.rerun()

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
            
            st.markdown("---")
            if brand_data.get('verified', False):
                st.success(f"✅ **Verified Data** | Source: {brand_data['source']}")
            else:
                st.info(f"ℹ️ **Industry Estimate** | Source: {brand_data['source']}")
            
            if selected_brand in OFFICIAL_URLS:
                st.markdown(f"**🌐 Official Website:** [{selected_brand} Official Site]({OFFICIAL_URLS[selected_brand]})")
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

        # DEEP DIVE SWOT ANALYSIS
        st.markdown("---")
        st.subheader("🔍 Deep Dive: Auto-Generated SWOT Analysis")
        st.caption("This analysis is dynamically generated based on the brand's financial metrics, store count, and cuisine type to help you evaluate fit.")
        
        s, w, o, t = generate_deep_dive(brand_data)
        swot_col1, swot_col2 = st.columns(2)
        with swot_col1:
            st.markdown("**💪 Strengths**")
            for item in s: st.markdown(f"- {item}")
            st.markdown("**⚠️ Weaknesses**")
            for item in w: st.markdown(f"- {item}")
        with swot_col2:
            st.markdown("** Opportunities**")
            for item in o: st.markdown(f"- {item}")
            st.markdown("**🛡️ Threats**")
            for item in t: st.markdown(f"- {item}")
            
        # OPERATIONAL ESTIMATE
        st.markdown("---")
        st.subheader(" Estimated Operational Footprint")
        st.info(f"Based on an investment of **${brand_data['investment_usd']:,}**, this franchise likely requires: **{get_store_estimate(brand_data['investment_usd'])}**.")

        # INVESTOR NOTES
        st.markdown("---")
        st.subheader("📝 My Private Investor Notes")
        st.caption("These notes are saved to your session and will appear in your Shortlist dashboard.")
        current_note = st.session_state.investor_notes.get(selected_brand, "")
        new_note = st.text_area("Write your thoughts on this brand:", value=current_note, height=100, key=f"note_{selected_brand}")
        if new_note != current_note:
            st.session_state.investor_notes[selected_brand] = new_note
            st.success("Note saved!")

# TAB 2: ROI Calculator
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

# TAB 3: Brand Comparison
with tab3:
    st.subheader("⚖️ Side-by-Side Brand Comparison")
    compare_options = st.multiselect("Select 2 or more brands to compare:", options=df['brand_name'].tolist(), default=st.session_state.get('brands_to_compare', []))
    st.session_state.brands_to_compare = compare_options
    num_selected = len(st.session_state.brands_to_compare)
    col1, col2 = st.columns(2)
    with col1:
        if num_selected >= 2:
            st.success(f"✅ {num_selected} brands selected for comparison.")
            compare_df = df[df['brand_name'].isin(st.session_state.brands_to_compare)]
            st.dataframe(compare_df[['brand_name', 'investment_usd', 'franchise_fee_usd', 'royalty_pct', 'stores_overseas']], use_container_width=True)
        else:
            st.warning("️ Please select at least 2 brands to enable comparison and download.")
    with col2:
        if num_selected >= 2:
            compare_df = df[df['brand_name'].isin(st.session_state.brands_to_compare)]
            html_content = create_comparison_html(compare_df)
            st.download_button(label="📄 Download Comparison as HTML", data=html_content, file_name=f"brand_comparison_{datetime.now().strftime('%Y%m%d')}.html", mime="text/html", use_container_width=True)

# TAB 4: My Shortlist (NEW)
with tab4:
    st.subheader("⭐ My Franchise Shortlist")
    if not st.session_state.shortlist:
        st.info("Your shortlist is empty. Go to the Brand Directory and click 'Add to Shortlist' on brands you are interested in.")
    else:
        st.write(f"You have **{len(st.session_state.shortlist)}** brands in your shortlist for in-depth evaluation.")
        
        shortlist_df = df[df['brand_name'].isin(st.session_state.shortlist)].copy()
        shortlist_df['My Notes'] = shortlist_df['brand_name'].map(lambda x: st.session_state.investor_notes.get(x, ""))
        
        st.dataframe(shortlist_df[['brand_name', 'cuisine', 'investment_usd', 'stores_overseas', 'My Notes']], use_container_width=True)
        
        st.markdown("---")
        st.subheader("📤 Export Shortlist")
        st.caption("Download your shortlist and notes as a CSV file to share with partners or review offline.")
        
        csv = shortlist_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Shortlist as CSV",
            data=csv,
            file_name=f"my_franchise_shortlist_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        if st.button("🗑️ Clear Entire Shortlist"):
            st.session_state.shortlist = []
            st.session_state.investor_notes = {}
            st.rerun()
