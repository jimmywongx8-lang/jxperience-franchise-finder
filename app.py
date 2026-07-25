import streamlit as st
import pandas as pd
import smtplib
import requests
from email.mime.text import MIMEText
from urllib.parse import quote
import json
import io

# --- SECRETS ---
YOUR_GMAIL = st.secrets.get("YOUR_GMAIL")
YOUR_APP_PASSWORD = st.secrets.get("YOUR_APP_PASSWORD")
SHEET_WEBHOOK_URL = st.secrets.get("SHEET_WEBHOOK_URL")

# --- CSV URL (63 brands) ---
CSV_URL = "https://raw.githubusercontent.com/jimmywongx8-lang/jxperience-franchise-finder/main/franchise_data.csv"

# --- SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_franchise' not in st.session_state:
    st.session_state.selected_franchise = None
if 'franchisor_logged_in' not in st.session_state:
    st.session_state.franchisor_logged_in = False

# --- LOAD 63 BRANDS FROM CSV ---
@st.cache_data(ttl=300)
def load_brands():
    try:
        df = pd.read_csv(CSV_URL)
        return df
    except:
        return pd.DataFrame()

# --- 6 DEEP DIVE PROFILES ---
FRANCHISES = {
    "Coco Ichibanya": {
        "story": "Coco Ichibanya is Japan's #1 curry house chain with over 1,300 stores. They are AGGRESSIVELY expanding overseas with locations in USA, China, Korea, Singapore, and Europe. They actively recruit overseas franchisees and have a well-established international support system.",
        "investment": "$150k - $300k",
        "royalty": "5% - 7%",
        "sales": "¥50M - ¥80M (domestic avg)",
        "overseas_status": "✅ ACTIVELY RECRUITING - USA, Asia, Europe",
        "youtube_search": "Coco Ichibanya franchise overseas",
        "news_search": "Coco Ichibanya international expansion franchise",
        "financials": {"Metric": ["Franchise Fee", "Total Investment", "Royalty", "Store Count"], "Details": ["¥3M - ¥5M", "$150k - $300k", "5% - 7% of sales", "1,300+ stores (200+ overseas)"]},
        "pros": ["Proven overseas success", "Low kitchen complexity", "Highly customizable menu", "Strong brand recognition"],
        "cons": ["Requires curry specialization", "Competition in Asian markets", "Adaptation needed for local tastes"]
    },
    "Pepper Lunch": {
        "story": "Pepper Lunch is a fast-steak concept with over 200 stores across 15+ countries. They are ONE OF THE MOST SUCCESSFUL Japanese franchises overseas. Their DIY sizzling plate concept is unique and highly franchise-friendly.",
        "investment": "$200k - $400k",
        "royalty": "5% - 6%",
        "sales": "$400k - $800k (overseas avg)",
        "overseas_status": "✅ VERY ACTIVE - 15+ countries, 200+ stores",
        "youtube_search": "Pepper Lunch franchise international",
        "news_search": "Pepper Lunch global expansion franchise",
        "financials": {"Metric": ["Franchise Fee", "Total Investment", "Royalty", "Global Stores"], "Details": ["$30k - $50k", "$200k - $400k", "5% - 6%", "200+ stores in 15 countries"]},
        "pros": ["Proven international success", "Unique DIY concept", "Fast service model", "Strong in malls"],
        "cons": ["Requires sizzling plate equipment", "Premium pricing may limit market", "Competition in food courts"]
    },
    "Kura Sushi": {
        "story": "Kura Sushi is a revolutionary conveyor belt sushi chain with high-tech features. They are EXPANDING AGGRESSIVELY IN USA with locations in California, Texas, and more planned.",
        "investment": "$500k - $1M",
        "royalty": "5% - 6%",
        "sales": "$1M - $2M (US locations)",
        "overseas_status": "✅ EXPANDING IN USA - Actively recruiting",
        "youtube_search": "Kura Sushi USA franchise",
        "news_search": "Kura Sushi USA expansion franchise",
        "financials": {"Metric": ["Initial Investment", "Total Cost", "Royalty", "US Locations"], "Details": ["$500k+", "$500k - $1M", "5% - 6%", "10+ locations, 100+ planned"]},
        "pros": ["High-tech unique concept", "Strong US growth", "Premium positioning", "Young demographic appeal"],
        "cons": ["High initial investment", "Complex sushi operations", "Requires fresh seafood supply chain"]
    },
    "Sukiya": {
        "story": "Sukiya is Japan's largest gyudon (beef bowl) chain with 2,000+ stores. They have significant presence in Asia and are expanding. They accept master franchisees and joint venture partners.",
        "investment": "$300k - $600k",
        "royalty": "4% - 6%",
        "sales": "¥100M+ (top locations)",
        "overseas_status": "✅ SELECTIVE - Asia focus, JV/master franchise",
        "youtube_search": "Sukiya overseas franchise Asia",
        "news_search": "Sukiya international expansion franchise Asia",
        "financials": {"Metric": ["Franchise Fee", "Investment Range", "Royalty", "Global Presence"], "Details": ["Negotiable", "$300k - $600k", "4% - 6%", "2,000+ stores (200+ overseas)"]},
        "pros": ["Massive brand power", "Proven Asian success", "Simple menu", "High volume potential"],
        "cons": ["Selective approval", "Beef import regulations", "Lower margins", "Competition from Yoshinoya"]
    },
    "Hoshino Coffee": {
        "story": "Hoshino Coffee is a premium Nagoya-style coffee shop famous for thick pancakes and retro atmosphere. They are EXPANDING IN ASIA with locations in Hong Kong, Taiwan, and Thailand.",
        "investment": "$250k - $500k",
        "royalty": "5% - 6%",
        "sales": "¥60M - ¥100M",
        "overseas_status": "✅ ACTIVE IN ASIA - Hong Kong, Taiwan, Thailand",
        "youtube_search": "Hoshino Coffee franchise Asia",
        "news_search": "Hoshino Coffee international expansion",
        "financials": {"Metric": ["Franchise Fee", "Total Investment", "Royalty", "Overseas Markets"], "Details": ["¥3M - ¥5M", "$250k - $500k", "5% - 6%", "Hong Kong, Taiwan, Thailand"]},
        "pros": ["Premium positioning", "Unique pancake menu", "Strong Asian presence", "Distinctive branding"],
        "cons": ["Higher price point", "Requires larger space", "Slower turnover", "Competition from cafes"]
    },
    "Ootoya": {
        "story": "Ootoya is a premium Japanese home-style restaurant (teishoku) with 500+ stores. They have successful locations in USA, China, Taiwan, Singapore, and Thailand.",
        "investment": "$300k - $600k",
        "royalty": "5% - 6%",
        "sales": "$500k - $1M (US locations)",
        "overseas_status": "✅ ESTABLISHED - USA, Asia, 50+ overseas stores",
        "youtube_search": "Ootoya franchise USA",
        "news_search": "Ootoya international franchise expansion",
        "financials": {"Metric": ["Initial Fee", "Investment", "Royalty", "Overseas Stores"], "Details": ["$30k - $50k", "$300k - $600k", "5% - 6%", "50+ stores overseas"]},
        "pros": ["Premium positioning", "Healthy menu appeal", "Proven US success", "Unique teishoku concept"],
        "cons": ["Higher investment", "Complex menu operations", "Requires Japanese ingredients", "Premium pricing"]
    }
}

# --- HELPER FUNCTIONS ---
def send_email(subject, body, to_email=None):
    if to_email is None:
        to_email = YOUR_GMAIL
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = YOUR_GMAIL
    msg['To'] = to_email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(YOUR_GMAIL, YOUR_APP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def save_to_sheet(franchise_name, name, email, capital, experience, industry, location, timeline):
    payload = {
        "franchise": franchise_name, "name": name, "email": email, "capital": capital, 
        "experience": experience, "industry": industry, "location": location, "timeline": timeline
    }
    try:
        requests.post(SHEET_WEBHOOK_URL, json=payload)
        return True
    except Exception as e:
        print(f"Sheet error: {e}")
        return False

def get_leads_from_sheet():
    """Fetch real leads from Google Sheet"""
    try:
        response = requests.get(SHEET_WEBHOOK_URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                return data
    except Exception as e:
        st.error(f"Error fetching leads: {e}")
    return None

# --- HOME PAGE (63 BRANDS TABLE) ---
def show_home():
    st.header("🇵 JXPerience: Japanese Franchise Finder")
    st.caption("Connecting Japanese brands with serious global investors")
    
    df = load_brands()
    
    if df.empty:
        st.error("Could not load franchise data. Please check the CSV file.")
        return
    
    st.subheader(f"Found {len(df)} Expansion-Ready Brands")
    
    # Search and filters
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input(" Search brands...", "")
    with col2:
        categories = df['Category'].dropna().unique().tolist() if 'Category' in df.columns else []
        selected_cat = st.multiselect("Filter by Category", categories, default=[])
    
    # Apply filters
    filtered = df.copy()
    if search:
        filtered = filtered[filtered['Brand'].str.contains(search, case=False, na=False)]
    if selected_cat:
        filtered = filtered[filtered['Category'].isin(selected_cat)]
    
    st.write(f"Showing {len(filtered)} brands")
    
    # Display table with clickable rows
    for idx, row in filtered.iterrows():
        brand = row.get('Brand', 'Unknown')
        category = row.get('Category', '')
        japan
