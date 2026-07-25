import streamlit as st
import pandas as pd
import smtplib
import requests
from email.mime.text import MIMEText
from urllib.parse import quote

# --- ⚠️ SECRETS CONFIGURATION (Loaded from Streamlit Secrets) ⚠️ ---
YOUR_GMAIL = st.secrets.get("YOUR_GMAIL", "kitchengadgetinsiderl@gmail.com")
YOUR_APP_PASSWORD = st.secrets.get("zcxf fgde uvst dgbu")
SHEET_WEBHOOK_URL = st.secrets.get("https://script.google.com/macros/s/AKfycbxyFmg9v8qygV14tOtefxWVNNAlSNqpkXRCDCJlr5itDwtvrdQGMlKiCFCqN29WYnBx/exec")

# --- SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'profile'
if 'selected_franchise' not in st.session_state:
    st.session_state.selected_franchise = "Coco Ichibanya"
if 'franchisor_logged_in' not in st.session_state:
    st.session_state.franchisor_logged_in = False

# --- FRANCHISE DATABASE (VERIFIED OVERSEAS) ---
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

# --- INVESTOR QUIZ PAGE ---
def show_quiz():
    franchise_name = st.session_state.selected_franchise
    st.header(f"Investor Application: {franchise_name}")
    if st.button("Back to Profile"):
        st.session_state.page = 'profile'
        st.rerun()
    st.markdown("---")
    with st.form("quiz"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        capital = st.selectbox("Available Capital (USD)?", ["Under $100k", "$100k-$250k", "$250k-$500k", "$500k-$1M", "Over $1M"])
        experience = st.selectbox("Business Experience?", ["None", "1-3 years", "3-5 years", "5+ years", "Current Franchise Owner"])
        industry = st.selectbox("Industry Background?", ["F&B / Restaurant", "Retail", "Corporate", "Real Estate", "Other"])
        location = st.text_input("Target Location/Country")
        timeline = st.selectbox("Timeline to Open?", ["Just researching", "1-2 years", "6-12 months", "ASAP (<6 months)"])
        submitted = st.form_submit_button("Submit Application", type="primary")
        if submitted:
            if name and email:
                with st.spinner("Submitting your profile..."):
                    email_ok = send_email(f"New Lead: {name} for {franchise_name}", f"Name: {name}\nEmail: {email}\nCapital: {capital}\nLocation: {location}")
                    sheet_ok = save_to_sheet(franchise_name, name, email, capital, experience, industry, location, timeline)
                if email_ok and sheet_ok:
                    st.success(f"✅ Thanks {name}! Application submitted for {franchise_name}.")
                else:
                    st.error("Technical issue. Please try again.")
            else:
                st.error("Please fill in name and email")
    if st.button("Return to Profile"):
        st.session_state.page = 'profile'
        st.rerun()

# --- FRANCHISOR PORTAL PAGE ---
def show_franchisor_portal():
    st.header("🇯🇵 Franchisor Partner Portal")
    if not st.session_state.franchisor_logged_in:
        st.subheader("Partner Login")
        st.info("Access restricted to verified Japanese franchise partners.")
        password = st.text_input("Enter Access Code", type="password")
        if st.button("Login", type="primary"):
            if password == "jfa2026": 
                st.session_state.franchisor_logged_in = True
                st.rerun()
            else:
                st.error("Invalid access code.")
        st.divider()
        st.subheader("Not a partner yet?")
        st.write("Are you a Japanese franchise looking to expand overseas? Request access.")
        with st.form("access_request"):
            company = st.text_input("Company Name")
            contact = st.text_input("Contact Email")
            req_submitted = st.form_submit_button("Request Partner Access")
            if req_submitted and company and contact:
                send_email(f"New Partner Request: {company}", f"Company: {company}\nEmail: {contact}")
                st.success("Request sent! We will contact you within 24 hours.")
        return

    st.success("Logged in as Partner")
    if st.button("Logout"):
        st.session_state.franchisor_logged_in = False
        st.rerun()
    
    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["📊 Lead Dashboard", "📝 Update My Profile", "⚙️ Settings"])
    with tab1:
        st.subheader("Your Qualified Investor Leads")
        st.write("Here is a sample of the high-quality leads we are generating for your brand.")
        mock_data = {
            "Date": ["2026-07-25", "2026-07-24", "2026-07-22"],
            "Investor Name": ["Jimmy Wong", "Sarah Chen", "David Smith"],
            "Location": ["Hong Kong", "Singapore", "California, USA"],
            "Capital": ["$100k-$250k", "$500k-$1M", "Over $1M"],
            "Experience": ["3-5 years (Corporate)", "Current Franchise Owner", "5+ years (F&B)"],
            "Status": [" Pre-Screened", "🟢 Pre-Screened", "🟡 Pending Review"]
        }
        st.dataframe(pd.DataFrame(mock_data), use_container_width=True, hide_index=True)
        st.divider()
        st.subheader("Lead Generation Metrics (Last 30 Days)")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Inquiries", "14", "+3 this week")
        col2.metric("Qualified Leads", "8", "57% conversion")
        col3.metric("Avg. Investor Capital", "$450k", "High quality")
    with tab2:
        st.subheader("Update Your Public Profile")
        st.write("Submit changes to your story, financials, or overseas status.")
        with st.form("profile
