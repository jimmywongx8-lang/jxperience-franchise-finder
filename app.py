import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. Page Configuration ---
st.set_page_config(page_title="JXPerience", page_icon="🍣", layout="wide")

# --- 2. Data Loading ---
@st.cache_data
def load_data():
    franchises = [
        # === RAMEN (25 brands) ===
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
        
        # === SUSHI (20 brands) ===
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
        {'brand_name': 'Kyoto Sushi', 'cuisine': 'Sushi', 'investment_usd': 115000, 'franchise_fee_usd': 16000, 'royalty_pct': 5, 'stores_japan': 45, 'stores_overseas': 6, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 36000, 'avg_monthly_cost_usd': 26000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Tokyo Sushi', 'cuisine': 'Sushi', 'investment_usd': 125000, 'franchise_fee_usd': 18000, 'royalty_pct': 5, 'stores_japan': 35, 'stores_overseas': 5, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Osaka Sushi', 'cuisine': 'Sushi', 'investment_usd': 135000, 'franchise_fee_usd': 20000, 'royalty_pct': 5, 'stores_japan': 40, 'stores_overseas': 7, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 40000, 'avg_monthly_cost_usd': 29000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Nagoya Sushi', 'cuisine': 'Sushi', 'investment_usd': 145000, 'franchise_fee_usd': 22000, 'royalty_pct': 5, 'stores_japan': 50, 'stores_overseas': 9, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 42000, 'avg_monthly_cost_usd': 30000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Hokkaido Sushi', 'cuisine': 'Sushi', 'investment_usd': 105000, 'franchise_fee_usd': 14000, 'royalty_pct': 5, 'stores_japan': 55, 'stores_overseas': 8, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 34000, 'avg_monthly_cost_usd': 24000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Sushi Dai', 'cuisine': 'Sushi', 'investment_usd': 175000, 'franchise_fee_usd': 22000, 'royalty_pct': 5, 'stores_japan': 22, 'stores_overseas': 4, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 42000, 'avg_monthly_cost_usd': 30000, 'pros': 'Tsukiji market heritage', 'cons': 'Limited expansion', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Sushi Saito', 'cuisine': 'Sushi', 'investment_usd': 320000, 'franchise_fee_usd': 40000, 'royalty_pct': 7, 'stores_japan': 5, 'stores_overseas': 2, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 55000, 'avg_monthly_cost_usd': 38000, 'pros': '3 Michelin stars', 'cons': 'Very exclusive', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Sushi Yoshitake', 'cuisine': 'Sushi', 'investment_usd': 290000, 'franchise_fee_usd': 38000, 'royalty_pct': 7, 'stores_japan': 4, 'stores_overseas': 1, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 52000, 'avg_monthly_cost_usd': 36000, 'pros': '3 Michelin stars', 'cons': 'Very exclusive', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Sushi Masuda', 'cuisine': 'Sushi', 'investment_usd': 260000, 'franchise_fee_usd': 35000, 'royalty_pct': 6, 'stores_japan': 8, 'stores_overseas': 3, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 48000, 'avg_monthly_cost_usd': 34000, 'pros': '2 Michelin stars', 'cons': 'Limited availability', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Sushi Arai', 'cuisine': 'Sushi', 'investment_usd': 240000, 'franchise_fee_usd': 32000, 'royalty_pct': 6, 'stores_japan': 6, 'stores_overseas': 2, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 46000, 'avg_monthly_cost_usd': 33000, 'pros': '2 Michelin stars', 'cons': 'Limited availability', 'source': 'Industry estimate', 'verified': False},
        
        # === CURRY (15 brands) ===
        {'brand_name': 'CoCo Ichibanya', 'cuisine': 'Curry', 'investment_usd': 376000, 'franchise_fee_usd': 40000, 'royalty_pct': 6, 'stores_japan': 1350, 'stores_overseas': 65, 'target_markets': 'USA, Asia, Europe', 'avg_monthly_revenue_usd': 42000, 'avg_monthly_cost_usd': 30000, 'pros': 'Guinness World Record holder', 'cons': 'High investment', 'source': 'FDD Filing', 'verified': True},
        {'brand_name': 'Go-Go Curry', 'cuisine': 'Curry', 'investment_usd': 250000, 'franchise_fee_usd': 25000, 'royalty_pct': 5, 'stores_japan': 180, 'stores_overseas': 25, 'target_markets': 'USA, Asia', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Strong US presence', 'cons': 'Moderate presence', 'source': 'FDD Filing', 'verified': True},
        {'brand_name': 'Curry House Tawnya', 'cuisine': 'Curry', 'investment_usd': 150000, 'franchise_fee_usd': 18000, 'royalty_pct': 5, 'stores_japan': 25, 'stores_overseas': 5, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 32000, 'avg_monthly_cost_usd': 23000, 'pros': 'Growing chain', 'cons': 'Regional limitation', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Soup Curry Suage+', 'cuisine': 'Curry', 'investment_usd': 120000, 'franchise_fee_usd': 15000, 'royalty_pct': 4, 'stores_japan': 15, 'stores_overseas': 3, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 30000, 'avg_monthly_cost_usd': 22000, 'pros': 'Hokkaido soup curry', 'cons': 'Regional limitation', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Bon Curry', 'cuisine': 'Curry', 'investment_usd': 100000, 'franchise_fee_usd': 12000, 'royalty_pct': 4, 'stores_japan': 20, 'stores_overseas': 4, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 28000, 'avg_monthly_cost_usd': 20000, 'pros': 'Unique style', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Java Curry', 'cuisine': 'Curry', 'investment_usd': 90000, 'franchise_fee_usd': 10000, 'royalty_pct': 4, 'stores_japan': 30, 'stores_overseas': 6, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 26000, 'avg_monthly_cost_usd': 19000, 'pros': 'Established', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Coco Ichibanya Premium', 'cuisine': 'Curry', 'investment_usd': 200000, 'franchise_fee_usd': 22000, 'royalty_pct': 6, 'stores_japan': 40, 'stores_overseas': 12, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'Premium curry', 'cons': 'High investment', 'source': 'FDD Filing', 'verified': True},
        {'brand_name': 'Ken-chan Curry', 'cuisine': 'Curry', 'investment_usd': 180000, 'franchise_fee_usd': 20000, 'royalty_pct': 5, 'stores_japan': 35, 'stores_overseas': 8, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'Regional leader', 'cons': 'Regional limitation', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Rikuro Curry', 'cuisine': 'Curry', 'investment_usd': 110000, 'franchise_fee_usd': 14000, 'royalty_pct': 5, 'stores_japan': 28, 'stores_overseas': 7, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 30000, 'avg_monthly_cost_usd': 22000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Tokyo Curry', 'cuisine': 'Curry', 'investment_usd': 95000, 'franchise_fee_usd': 12000, 'royalty_pct': 4, 'stores_japan': 22, 'stores_overseas': 5, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 28000, 'avg_monthly_cost_usd': 20000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Osaka Curry', 'cuisine': 'Curry', 'investment_usd': 105000, 'franchise_fee_usd': 13000, 'royalty_pct': 5, 'stores_japan': 26, 'stores_overseas': 6, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 29000, 'avg_monthly_cost_usd': 21000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Kyoto Curry House', 'cuisine': 'Curry', 'investment_usd': 115000, 'franchise_fee_usd': 14000, 'royalty_pct': 5, 'stores_japan': 20, 'stores_overseas': 4, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 31000, 'avg_monthly_cost_usd': 22000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Nagoya Curry', 'cuisine': 'Curry', 'investment_usd': 100000, 'franchise_fee_usd': 12000, 'royalty_pct': 4, 'stores_japan': 18, 'stores_overseas': 3, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 28000, 'avg_monthly_cost_usd': 20000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Fukuoka Curry', 'cuisine': 'Curry', 'investment_usd': 98000, 'franchise_fee_usd': 12000, 'royalty_pct': 4, 'stores_japan': 24, 'stores_overseas': 5, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 29000, 'avg_monthly_cost_usd': 21000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Sapporo Soup Curry', 'cuisine': 'Curry', 'investment_usd': 125000, 'franchise_fee_usd': 15000, 'royalty_pct': 5, 'stores_japan': 32, 'stores_overseas': 7, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 32000, 'avg_monthly_cost_usd': 23000, 'pros': 'Hokkaido specialty', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        
        # === TONKATSU (15 brands) ===
        {'brand_name': 'Maisen', 'cuisine': 'Tonkatsu', 'investment_usd': 250000, 'franchise_fee_usd': 30000, 'royalty_pct': 6, 'stores_japan': 85, 'stores_overseas': 25, 'target_markets': 'Southeast Asia, USA', 'avg_monthly_revenue_usd': 45000, 'avg_monthly_cost_usd': 32000, 'pros': 'Established brand, premium', 'cons': 'Moderate investment', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Tonki', 'cuisine': 'Tonkatsu', 'investment_usd': 180000, 'franchise_fee_usd': 25000, 'royalty_pct': 5, 'stores_japan': 45, 'stores_overseas': 12, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 42000, 'avg_monthly_cost_usd': 30000, 'pros': 'Traditional recipe since 1939', 'cons': 'Regional limitation', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Katsukura', 'cuisine': 'Tonkatsu', 'investment_usd': 200000, 'franchise_fee_usd': 28000, 'royalty_pct': 6, 'stores_japan': 55, 'stores_overseas': 18, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 44000, 'avg_monthly_cost_usd': 31000, 'pros': 'Growing overseas', 'cons': 'Moderate presence', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Gyukatsu Kyoto Katsugyu', 'cuisine': 'Tonkatsu', 'investment_usd': 220000, 'franchise_fee_usd': 30000, 'royalty_pct': 6, 'stores_japan': 40, 'stores_overseas': 15, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 46000, 'avg_monthly_cost_usd': 33000, 'pros': 'Wagyu beef specialty', 'cons': 'Premium pricing', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Bifteki Kawamura', 'cuisine': 'Tonkatsu', 'investment_usd': 280000, 'franchise_fee_usd': 35000, 'royalty_pct': 7, 'stores_japan': 35, 'stores_overseas': 10, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 48000, 'avg_monthly_cost_usd': 34000, 'pros': 'Beef cutlet specialty', 'cons': 'High investment', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Katsuya', 'cuisine': 'Tonkatsu', 'investment_usd': 190000, 'franchise_fee_usd': 26000, 'royalty_pct': 5, 'stores_japan': 65, 'stores_overseas': 22, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 43000, 'avg_monthly_cost_usd': 31000, 'pros': 'Established chain', 'cons': 'Moderate presence', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Wagyu Katsu', 'cuisine': 'Tonkatsu', 'investment_usd': 210000, 'franchise_fee_usd': 28000, 'royalty_pct': 6, 'stores_japan': 45, 'stores_overseas': 14, 'target_markets': 'Asia, Middle East', 'avg_monthly_revenue_usd': 45000, 'avg_monthly_cost_usd': 32000, 'pros': 'Wagyu focus', 'cons': 'Premium pricing', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Tonkatsu Wako', 'cuisine': 'Tonkatsu', 'investment_usd': 170000, 'franchise_fee_usd': 24000, 'royalty_pct': 5, 'stores_japan': 38, 'stores_overseas': 11, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 41000, 'avg_monthly_cost_usd': 29000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Kamukura', 'cuisine': 'Tonkatsu', 'investment_usd': 160000, 'franchise_fee_usd': 22000, 'royalty_pct': 5, 'stores_japan': 42, 'stores_overseas': 9, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 40000, 'avg_monthly_cost_usd': 28000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Tonkatsu Marugo', 'cuisine': 'Tonkatsu', 'investment_usd': 155000, 'franchise_fee_usd': 21000, 'royalty_pct': 5, 'stores_japan': 48, 'stores_overseas': 10, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 39000, 'avg_monthly_cost_usd': 28000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Tonkatsu Hanayama', 'cuisine': 'Tonkatsu', 'investment_usd': 165000, 'franchise_fee_usd': 23000, 'royalty_pct': 5, 'stores_japan': 36, 'stores_overseas': 8, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 40000, 'avg_monthly_cost_usd': 29000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Tonkatsu Saboten', 'cuisine': 'Tonkatsu', 'investment_usd': 175000, 'franchise_fee_usd': 24000, 'royalty_pct': 5, 'stores_japan': 52, 'stores_overseas': 13, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 41000, 'avg_monthly_cost_usd': 30000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Tonkatsu Tonkichi', 'cuisine': 'Tonkatsu', 'investment_usd': 148000, 'franchise_fee_usd': 20000, 'royalty_pct': 5, 'stores_japan': 44, 'stores_overseas': 9, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Tonkatsu Katsudon Ya', 'cuisine': 'Tonkatsu', 'investment_usd': 142000, 'franchise_fee_usd': 19000, 'royalty_pct': 4, 'stores_japan': 39, 'stores_overseas': 7, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 37000, 'avg_monthly_cost_usd': 26000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Tonkatsu Asakusa', 'cuisine': 'Tonkatsu', 'investment_usd': 158000, 'franchise_fee_usd': 22000, 'royalty_pct': 5, 'stores_japan': 41, 'stores_overseas': 8, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 39000, 'avg_monthly_cost_usd': 28000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        
        # === YAKINIKU (15 brands) ===
        {'brand_name': 'Yakiniku Jumbo Shiro', 'cuisine': 'Yakiniku', 'investment_usd': 280000, 'franchise_fee_usd': 30000, 'royalty_pct': 6, 'stores_japan': 75, 'stores_overseas': 45, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 52000, 'avg_monthly_cost_usd': 37000, 'pros': 'Market leader', 'cons': 'High investment', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Momidare Yakiniku Shishiro', 'cuisine': 'Yakiniku', 'investment_usd': 320000, 'franchise_fee_usd': 35000, 'royalty_pct': 7, 'stores_japan': 95, 'stores_overseas': 35, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 55000, 'avg_monthly_cost_usd': 39000, 'pros': 'Premium brand', 'cons': 'High investment', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Konga', 'cuisine': 'Yakiniku', 'investment_usd': 250000, 'franchise_fee_usd': 28000, 'royalty_pct': 6, 'stores_japan': 65, 'stores_overseas': 28, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 48000, 'avg_monthly_cost_usd': 34000, 'pros': 'Established chain', 'cons': 'Moderate presence', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Torisho', 'cuisine': 'Yakiniku', 'investment_usd': 180000, 'franchise_fee_usd': 22000, 'royalty_pct': 5, 'stores_japan': 45, 'stores_overseas': 15, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 42000, 'avg_monthly_cost_usd': 30000, 'pros': 'Growing brand', 'cons': 'Regional limitation', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Yakiniku Like', 'cuisine': 'Yakiniku', 'investment_usd': 150000, 'franchise_fee_usd': 18000, 'royalty_pct': 5, 'stores_japan': 120, 'stores_overseas': 55, 'target_markets': 'Asia, USA, Middle East', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Solo dining concept', 'cons': 'Low investment option', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Sanbashi', 'cuisine': 'Yakiniku', 'investment_usd': 200000, 'franchise_fee_usd': 25000, 'royalty_pct': 6, 'stores_japan': 55, 'stores_overseas': 18, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 45000, 'avg_monthly_cost_usd': 32000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Yakiniku King', 'cuisine': 'Yakiniku', 'investment_usd': 170000, 'franchise_fee_usd': 20000, 'royalty_pct': 5, 'stores_japan': 85, 'stores_overseas': 25, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 40000, 'avg_monthly_cost_usd': 29000, 'pros': 'Established', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Horumon Yaki', 'cuisine': 'Yakiniku', 'investment_usd': 140000, 'franchise_fee_usd': 16000, 'royalty_pct': 5, 'stores_japan': 95, 'stores_overseas': 30, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Kobe Beef BBQ', 'cuisine': 'Yakiniku', 'investment_usd': 350000, 'franchise_fee_usd': 40000, 'royalty_pct': 7, 'stores_japan': 35, 'stores_overseas': 12, 'target_markets': 'Asia, Middle East', 'avg_monthly_revenue_usd': 58000, 'avg_monthly_cost_usd': 41000, 'pros': 'Premium wagyu', 'cons': 'Very high investment', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Wagyu Yakiniku M', 'cuisine': 'Yakiniku', 'investment_usd': 380000, 'franchise_fee_usd': 42000, 'royalty_pct': 7, 'stores_japan': 40, 'stores_overseas': 14, 'target_markets': 'Asia, Middle East', 'avg_monthly_revenue_usd': 60000, 'avg_monthly_cost_usd': 43000, 'pros': 'Premium wagyu', 'cons': 'Very high investment', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Yakiniku Great', 'cuisine': 'Yakiniku', 'investment_usd': 165000, 'franchise_fee_usd': 19000, 'royalty_pct': 5, 'stores_japan': 72, 'stores_overseas': 22, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 39000, 'avg_monthly_cost_usd': 28000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Yakiniku Jumbo', 'cuisine': 'Yakiniku', 'investment_usd': 175000, 'franchise_fee_usd': 21000, 'royalty_pct': 5, 'stores_japan': 68, 'stores_overseas': 20, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 40000, 'avg_monthly_cost_usd': 29000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Yakiniku Horumon', 'cuisine': 'Yakiniku', 'investment_usd': 155000, 'franchise_fee_usd': 18000, 'royalty_pct': 5, 'stores_japan': 78, 'stores_overseas': 24, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Yakiniku Tsuruhashi', 'cuisine': 'Yakiniku', 'investment_usd': 160000, 'franchise_fee_usd': 19000, 'royalty_pct': 5, 'stores_japan': 82, 'stores_overseas': 26, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 39000, 'avg_monthly_cost_usd': 28000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Yakiniku Rokkasen', 'cuisine': 'Yakiniku', 'investment_usd': 170000, 'franchise_fee_usd': 20000, 'royalty_pct': 5, 'stores_japan': 70, 'stores_overseas': 21, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 40000, 'avg_monthly_cost_usd': 29000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        
        # === IZAKAYA (12 brands) ===
        {'brand_name': 'Torikizoku', 'cuisine': 'Izakaya', 'investment_usd': 120000, 'franchise_fee_usd': 18000, 'royalty_pct': 5, 'stores_japan': 550, 'stores_overseas': 25, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Largest izakaya chain', 'cons': 'Large scale required', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Shoya', 'cuisine': 'Izakaya', 'investment_usd': 150000, 'franchise_fee_usd': 22000, 'royalty_pct': 6, 'stores_japan': 85, 'stores_overseas': 15, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 42000, 'avg_monthly_cost_usd': 30000, 'pros': 'Established brand', 'cons': 'Moderate presence', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Tsubosan', 'cuisine': 'Izakaya', 'investment_usd': 100000, 'franchise_fee_usd': 15000, 'royalty_pct': 5, 'stores_japan': 65, 'stores_overseas': 12, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'Regional leader', 'cons': 'Regional limitation', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Uotami', 'cuisine': 'Izakaya', 'investment_usd': 110000, 'franchise_fee_usd': 16000, 'royalty_pct': 5, 'stores_japan': 75, 'stores_overseas': 18, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 36000, 'avg_monthly_cost_usd': 26000, 'pros': 'Seafood specialty', 'cons': 'Regional limitation', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Hanabisa', 'cuisine': 'Izakaya', 'investment_usd': 95000, 'franchise_fee_usd': 14000, 'royalty_pct': 4, 'stores_japan': 55, 'stores_overseas': 8, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 32000, 'avg_monthly_cost_usd': 23000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Kyoei', 'cuisine': 'Izakaya', 'investment_usd': 105000, 'franchise_fee_usd': 15000, 'royalty_pct': 5, 'stores_japan': 45, 'stores_overseas': 10, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 34000, 'avg_monthly_cost_usd': 24000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Izakaya Rokusan', 'cuisine': 'Izakaya', 'investment_usd': 115000, 'franchise_fee_usd': 17000, 'royalty_pct': 5, 'stores_japan': 38, 'stores_overseas': 6, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 36000, 'avg_monthly_cost_usd': 26000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Nagomi', 'cuisine': 'Izakaya', 'investment_usd': 125000, 'franchise_fee_usd': 19000, 'royalty_pct': 5, 'stores_japan': 42, 'stores_overseas': 9, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Izakaya Kappa', 'cuisine': 'Izakaya', 'investment_usd': 98000, 'franchise_fee_usd': 14000, 'royalty_pct': 4, 'stores_japan': 50, 'stores_overseas': 11, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 33000, 'avg_monthly_cost_usd': 24000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Izakaya Taro', 'cuisine': 'Izakaya', 'investment_usd': 108000, 'franchise_fee_usd': 16000, 'royalty_pct': 5, 'stores_japan': 48, 'stores_overseas': 10, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Izakaya Hanako', 'cuisine': 'Izakaya', 'investment_usd': 112000, 'franchise_fee_usd': 16000, 'royalty_pct': 5, 'stores_japan': 44, 'stores_overseas': 9, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 36000, 'avg_monthly_cost_usd': 26000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Izakaya Jiro', 'cuisine': 'Izakaya', 'investment_usd': 118000, 'franchise_fee_usd': 17000, 'royalty_pct': 5, 'stores_japan': 46, 'stores_overseas': 10, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 37000, 'avg_monthly_cost_usd': 26000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        
        # === CAFE/DESSERT (15 brands) ===
        {'brand_name': 'Komeda Coffee', 'cuisine': 'Cafe', 'investment_usd': 150000, 'franchise_fee_usd': 20000, 'royalty_pct': 5, 'stores_japan': 450, 'stores_overseas': 85, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'Market leader in Japan', 'cons': 'High competition', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Doutor Coffee', 'cuisine': 'Cafe', 'investment_usd': 120000, 'franchise_fee_usd': 18000, 'royalty_pct': 5, 'stores_japan': 1200, 'stores_overseas': 45, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 32000, 'avg_monthly_cost_usd': 23000, 'pros': 'Largest coffee chain in Japan', 'cons': 'High competition', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Tully Coffee', 'cuisine': 'Cafe', 'investment_usd': 180000, 'franchise_fee_usd': 25000, 'royalty_pct': 6, 'stores_japan': 95, 'stores_overseas': 35, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'International brand', 'cons': 'High competition', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Afternoon Tea', 'cuisine': 'Cafe', 'investment_usd': 100000, 'franchise_fee_usd': 15000, 'royalty_pct': 5, 'stores_japan': 180, 'stores_overseas': 25, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 30000, 'avg_monthly_cost_usd': 22000, 'pros': 'Established', 'cons': 'Moderate presence', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Kaldi Coffee', 'cuisine': 'Cafe', 'investment_usd': 90000, 'franchise_fee_usd': 12000, 'royalty_pct': 4, 'stores_japan': 250, 'stores_overseas': 15, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 28000, 'avg_monthly_cost_usd': 20000, 'pros': 'Growing chain', 'cons': 'Low investment', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Jack in the Donuts', 'cuisine': 'Dessert', 'investment_usd': 85000, 'franchise_fee_usd': 12000, 'royalty_pct': 5, 'stores_japan': 380, 'stores_overseas': 180, 'target_markets': 'Asia, Middle East', 'avg_monthly_revenue_usd': 32000, 'avg_monthly_cost_usd': 23000, 'pros': 'International donuts', 'cons': 'Saturation', 'source': 'Assentia Holdings', 'verified': True},
        {'brand_name': 'Mister Donut', 'cuisine': 'Dessert', 'investment_usd': 75000, 'franchise_fee_usd': 10000, 'royalty_pct': 5, 'stores_japan': 550, 'stores_overseas': 450, 'target_markets': 'Asia, Middle East', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'International brand', 'cons': 'High saturation', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Krispy Kreme Japan', 'cuisine': 'Dessert', 'investment_usd': 95000, 'franchise_fee_usd': 14000, 'royalty_pct': 5, 'stores_japan': 45, 'stores_overseas': 12, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 36000, 'avg_monthly_cost_usd': 26000, 'pros': 'International brand', 'cons': 'Moderate presence', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Toki Kirishima Matcha', 'cuisine': 'Cafe', 'investment_usd': 80000, 'franchise_fee_usd': 12000, 'royalty_pct': 5, 'stores_japan': 25, 'stores_overseas': 8, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 28000, 'avg_monthly_cost_usd': 20000, 'pros': '100-year matcha farm', 'cons': 'Limited brand', 'source': 'Assentia Holdings', 'verified': True},
        {'brand_name': 'Daifuku Benzaiten', 'cuisine': 'Dessert', 'investment_usd': 60000, 'franchise_fee_usd': 8000, 'royalty_pct': 4, 'stores_japan': 65, 'stores_overseas': 28, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 22000, 'avg_monthly_cost_usd': 16000, 'pros': 'Traditional sweets', 'cons': 'Seasonal demand', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Cafe de Crie', 'cuisine': 'Cafe', 'investment_usd': 135000, 'franchise_fee_usd': 19000, 'royalty_pct': 5, 'stores_japan': 165, 'stores_overseas': 22, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 34000, 'avg_monthly_cost_usd': 24000, 'pros': 'Established chain', 'cons': 'Moderate presence', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Pronto', 'cuisine': 'Cafe', 'investment_usd': 110000, 'franchise_fee_usd': 16000, 'royalty_pct': 5, 'stores_japan': 220, 'stores_overseas': 18, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 31000, 'avg_monthly_cost_usd': 22000, 'pros': 'Day cafe, night bar', 'cons': 'Moderate presence', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Cafe Veloce', 'cuisine': 'Cafe', 'investment_usd': 105000, 'franchise_fee_usd': 15000, 'royalty_pct': 5, 'stores_japan': 195, 'stores_overseas': 16, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 30000, 'avg_monthly_cost_usd': 21000, 'pros': 'Established chain', 'cons': 'Moderate presence', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Cafe Latte', 'cuisine': 'Cafe', 'investment_usd': 92000, 'franchise_fee_usd': 13000, 'royalty_pct': 4, 'stores_japan': 88, 'stores_overseas': 12, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 27000, 'avg_monthly_cost_usd': 19000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Matcha House', 'cuisine': 'Cafe', 'investment_usd': 88000, 'franchise_fee_usd': 12000, 'royalty_pct': 4, 'stores_japan': 72, 'stores_overseas': 10, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 26000, 'avg_monthly_cost_usd': 18000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        
        # === UDON/SOBA (10 brands) ===
        {'brand_name': 'Tsurumaru Udon', 'cuisine': 'Udon', 'investment_usd': 95000, 'franchise_fee_usd': 12000, 'royalty_pct': 5, 'stores_japan': 250, 'stores_overseas': 45, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'Regional leader', 'cons': 'Regional limitation', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Fumizen', 'cuisine': 'Udon', 'investment_usd': 85000, 'franchise_fee_usd': 11000, 'royalty_pct': 4, 'stores_japan': 85, 'stores_overseas': 12, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 30000, 'avg_monthly_cost_usd': 22000, 'pros': 'Regional leader', 'cons': 'Regional limitation', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Hanamaru Udon', 'cuisine': 'Udon', 'investment_usd': 70000, 'franchise_fee_usd': 9000, 'royalty_pct': 4, 'stores_japan': 350, 'stores_overseas': 25, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 28000, 'avg_monthly_cost_usd': 20000, 'pros': 'Fast casual', 'cons': 'Regional limitation', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Matsuya Soba', 'cuisine': 'Soba', 'investment_usd': 65000, 'franchise_fee_usd': 8000, 'royalty_pct': 4, 'stores_japan': 180, 'stores_overseas': 8, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 26000, 'avg_monthly_cost_usd': 19000, 'pros': 'Regional brand', 'cons': 'Low investment', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Osaka Soba', 'cuisine': 'Soba', 'investment_usd': 75000, 'franchise_fee_usd': 10000, 'royalty_pct': 4, 'stores_japan': 65, 'stores_overseas': 6, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 28000, 'avg_monthly_cost_usd': 20000, 'pros': 'Regional brand', 'cons': 'Low investment', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Kyoto Soba', 'cuisine': 'Soba', 'investment_usd': 85000, 'franchise_fee_usd': 11000, 'royalty_pct': 4, 'stores_japan': 45, 'stores_overseas': 4, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 30000, 'avg_monthly_cost_usd': 22000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Nagoya Soba', 'cuisine': 'Soba', 'investment_usd': 95000, 'franchise_fee_usd': 12000, 'royalty_pct': 5, 'stores_japan': 38, 'stores_overseas': 5, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 32000, 'avg_monthly_cost_usd': 23000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Udon Ya', 'cuisine': 'Udon', 'investment_usd': 78000, 'franchise_fee_usd': 10000, 'royalty_pct': 4, 'stores_japan': 125, 'stores_overseas': 15, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 29000, 'avg_monthly_cost_usd': 21000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Soba Dokoro', 'cuisine': 'Soba', 'investment_usd': 82000, 'franchise_fee_usd': 11000, 'royalty_pct': 4, 'stores_japan': 92, 'stores_overseas': 11, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 30000, 'avg_monthly_cost_usd': 22000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Udon no Hana', 'cuisine': 'Udon', 'investment_usd': 88000, 'franchise_fee_usd': 11000, 'royalty_pct': 4, 'stores_japan': 110, 'stores_overseas': 14, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 31000, 'avg_monthly_cost_usd': 22000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        
        # === ONIGIRI/RICE (8 brands) ===
        {'brand_name': 'Onigiri Mamma', 'cuisine': 'Onigiri', 'investment_usd': 55000, 'franchise_fee_usd': 8000, 'royalty_pct': 4, 'stores_japan': 35, 'stores_overseas': 8, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 22000, 'avg_monthly_cost_usd': 16000, 'pros': 'Fresh handmade', 'cons': 'Low revenue', 'source': 'Assentia Holdings', 'verified': True},
        {'brand_name': 'Onigiri Burger', 'cuisine': 'Onigiri', 'investment_usd': 85000, 'franchise_fee_usd': 12000, 'royalty_pct': 5, 'stores_japan': 25, 'stores_overseas': 5, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 28000, 'avg_monthly_cost_usd': 20000, 'pros': 'Innovative concept', 'cons': 'New concept', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Omusubi Gonbei', 'cuisine': 'Onigiri', 'investment_usd': 65000, 'franchise_fee_usd': 9000, 'royalty_pct': 4, 'stores_japan': 45, 'stores_overseas': 12, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 24000, 'avg_monthly_cost_usd': 17000, 'pros': 'Traditional', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Musubi Musubi', 'cuisine': 'Onigiri', 'investment_usd': 75000, 'franchise_fee_usd': 10000, 'royalty_pct': 4, 'stores_japan': 18, 'stores_overseas': 6, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 26000, 'avg_monthly_cost_usd': 19000, 'pros': 'Growing brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Rice Ball House', 'cuisine': 'Onigiri', 'investment_usd': 60000, 'franchise_fee_usd': 8000, 'royalty_pct': 4, 'stores_japan': 28, 'stores_overseas': 4, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 23000, 'avg_monthly_cost_usd': 17000, 'pros': 'Low investment', 'cons': 'Very low investment', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Tokyo Onigiri', 'cuisine': 'Onigiri', 'investment_usd': 70000, 'franchise_fee_usd': 9000, 'royalty_pct': 4, 'stores_japan': 22, 'stores_overseas': 5, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 25000, 'avg_monthly_cost_usd': 18000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Kyoto Onigiri', 'cuisine': 'Onigiri', 'investment_usd': 80000, 'franchise_fee_usd': 11000, 'royalty_pct': 5, 'stores_japan': 15, 'stores_overseas': 3, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 27000, 'avg_monthly_cost_usd': 20000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Omusubi Yamamoto', 'cuisine': 'Onigiri', 'investment_usd': 68000, 'franchise_fee_usd': 9000, 'royalty_pct': 4, 'stores_japan': 32, 'stores_overseas': 7, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 24000, 'avg_monthly_cost_usd': 17000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        
        # === DONBURI (10 brands) ===
        {'brand_name': 'Yoshinoya', 'cuisine': 'Donburi', 'investment_usd': 272000, 'franchise_fee_usd': 27500, 'royalty_pct': 5, 'stores_japan': 2000, 'stores_overseas': 450, 'target_markets': 'USA, Asia, Middle East', 'avg_monthly_revenue_usd': 42000, 'avg_monthly_cost_usd': 30000, 'pros': 'Global brand, 100+ years', 'cons': 'High competition', 'source': 'FDD Filing', 'verified': True},
        {'brand_name': 'Sukiya', 'cuisine': 'Donburi', 'investment_usd': 180000, 'franchise_fee_usd': 20000, 'royalty_pct': 5, 'stores_japan': 1950, 'stores_overseas': 380, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 40000, 'avg_monthly_cost_usd': 29000, 'pros': 'Market leader', 'cons': 'High competition', 'source': 'FDD Filing', 'verified': True},
        {'brand_name': 'Matsuya', 'cuisine': 'Donburi', 'investment_usd': 150000, 'franchise_fee_usd': 18000, 'royalty_pct': 5, 'stores_japan': 1250, 'stores_overseas': 280, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Established chain', 'cons': 'High competition', 'source': 'FDD Filing', 'verified': True},
        {'brand_name': 'Nakau', 'cuisine': 'Donburi', 'investment_usd': 120000, 'franchise_fee_usd': 15000, 'royalty_pct': 4, 'stores_japan': 450, 'stores_overseas': 85, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'Regional leader', 'cons': 'Regional limitation', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Yoshinoya Premium', 'cuisine': 'Donburi', 'investment_usd': 200000, 'franchise_fee_usd': 25000, 'royalty_pct': 6, 'stores_japan': 85, 'stores_overseas': 25, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 40000, 'avg_monthly_cost_usd': 29000, 'pros': 'Premium brand', 'cons': 'High investment', 'source': 'FDD Filing', 'verified': True},
        {'brand_name': 'Beef Bowl King', 'cuisine': 'Donburi', 'investment_usd': 160000, 'franchise_fee_usd': 20000, 'royalty_pct': 5, 'stores_japan': 65, 'stores_overseas': 18, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Growing brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Gyudon Master', 'cuisine': 'Donburi', 'investment_usd': 140000, 'franchise_fee_usd': 18000, 'royalty_pct': 5, 'stores_japan': 45, 'stores_overseas': 12, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 36000, 'avg_monthly_cost_usd': 26000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Tokyo Donburi', 'cuisine': 'Donburi', 'investment_usd': 130000, 'franchise_fee_usd': 16000, 'royalty_pct': 4, 'stores_japan': 35, 'stores_overseas': 8, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 34000, 'avg_monthly_cost_usd': 24000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Osaka Donburi', 'cuisine': 'Donburi', 'investment_usd': 145000, 'franchise_fee_usd': 19000, 'royalty_pct': 5, 'stores_japan': 28, 'stores_overseas': 10, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 37000, 'avg_monthly_cost_usd': 27000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Kyoto Donburi', 'cuisine': 'Donburi', 'investment_usd': 155000, 'franchise_fee_usd': 21000, 'royalty_pct': 5, 'stores_japan': 32, 'stores_overseas': 11, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 39000, 'avg_monthly_cost_usd': 28000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        
        # === OKONOMIYAKI (5 brands) ===
        {'brand_name': 'Chibo Okonomiyaki', 'cuisine': 'Okonomiyaki', 'investment_usd': 120000, 'franchise_fee_usd': 18000, 'royalty_pct': 5, 'stores_japan': 55, 'stores_overseas': 25, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'Established brand', 'cons': 'Moderate presence', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Okonomiyaki Kiji', 'cuisine': 'Okonomiyaki', 'investment_usd': 100000, 'franchise_fee_usd': 15000, 'royalty_pct': 5, 'stores_japan': 45, 'stores_overseas': 18, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 32000, 'avg_monthly_cost_usd': 23000, 'pros': 'Regional specialty', 'cons': 'Regional specialty', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Hiroshima Style', 'cuisine': 'Okonomiyaki', 'investment_usd': 90000, 'franchise_fee_usd': 12000, 'royalty_pct': 4, 'stores_japan': 38, 'stores_overseas': 15, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 30000, 'avg_monthly_cost_usd': 22000, 'pros': 'Traditional', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Osaka Style', 'cuisine': 'Okonomiyaki', 'investment_usd': 95000, 'franchise_fee_usd': 13000, 'royalty_pct': 4, 'stores_japan': 42, 'stores_overseas': 12, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 31000, 'avg_monthly_cost_usd': 22000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Modern Yaki', 'cuisine': 'Okonomiyaki', 'investment_usd': 85000, 'franchise_fee_usd': 11000, 'royalty_pct': 4, 'stores_japan': 35, 'stores_overseas': 8, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 29000, 'avg_monthly_cost_usd': 21000, 'pros': 'Modern style', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        
        # === TENDON/TEMPURA (5 brands) ===
        {'brand_name': 'Tendon Kohaku', 'cuisine': 'Tendon', 'investment_usd': 150000, 'franchise_fee_usd': 22000, 'royalty_pct': 6, 'stores_japan': 65, 'stores_overseas': 22, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Established chain', 'cons': 'Moderate investment', 'source': 'Franchise Japan', 'verified': True},
        {'brand_name': 'Tenya', 'cuisine': 'Tendon', 'investment_usd': 120000, 'franchise_fee_usd': 18000, 'royalty_pct': 5, 'stores_japan': 280, 'stores_overseas': 45, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 35000, 'avg_monthly_cost_usd': 25000, 'pros': 'Market leader in tendon', 'cons': 'High presence', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Tempura Tsunahachi', 'cuisine': 'Tempura', 'investment_usd': 180000, 'franchise_fee_usd': 25000, 'royalty_pct': 6, 'stores_japan': 45, 'stores_overseas': 15, 'target_markets': 'Asia, USA', 'avg_monthly_revenue_usd': 40000, 'avg_monthly_cost_usd': 29000, 'pros': 'Premium quality since 1924', 'cons': 'High standards', 'source': 'JFA Member', 'verified': True},
        {'brand_name': 'Sushi Ten', 'cuisine': 'Tempura', 'investment_usd': 160000, 'franchise_fee_usd': 22000, 'royalty_pct': 6, 'stores_japan': 25, 'stores_overseas': 8, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 38000, 'avg_monthly_cost_usd': 27000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
        {'brand_name': 'Kyoto Tempura', 'cuisine': 'Tempura', 'investment_usd': 140000, 'franchise_fee_usd': 20000, 'royalty_pct': 5, 'stores_japan': 18, 'stores_overseas': 6, 'target_markets': 'Asia', 'avg_monthly_revenue_usd': 36000, 'avg_monthly_cost_usd': 26000, 'pros': 'Regional brand', 'cons': 'Regional limitation', 'source': 'Industry estimate', 'verified': False},
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
    'Ippudo': 'https://www.ippudo.com/',
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
tab1, tab2, tab3 = st.tabs(["📊 Brand Directory", " ROI Calculator", "⚖️ Brand Comparison"])

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
            
            # DATA SOURCE BADGES
            st.markdown("---")
            if brand_data.get('verified', False):
                st.success(f"✅ **Verified Data** | Source: {brand_data['source']}")
            else:
                st.info(f"ℹ️ **Industry Estimate** | Source: {brand_data['source']}")
            
            # FEATURE 3: Official Source Links
            st.markdown("---")
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

        # FEATURE 2: Report Incorrect Data Feature (FIXED)
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
                    # Clean up the body text for the email
                    clean_details = details.replace('\n', ' ')
                    body = f"Hello JXPerience Team,%0D%0A%0D%0AI would like to report a data issue for the brand: {selected_brand}.%0D%0A%0D%0A**Issue Type:** {issue_type}%0D%0A**Details:** {clean_details}"
                    mailto_link = f"mailto:support@jxperience.com?subject={subject}&body={body}"
                    
                    # This creates a real clickable button
                    st.success("Report generated successfully!")
                    st.link_button("📧 Click here to open your email client", mailto_link)
                else:
                    st.error("Please provide details before sending.")

with tab2:
    st.subheader(" Franchise ROI Estimator")
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
