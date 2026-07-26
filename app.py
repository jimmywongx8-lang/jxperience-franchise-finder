import streamlit as st
import pandas as pd
import smtplib
import requests
from email.mime.text import MIMEText
from urllib.parse import quote

# --- SECRETS ---
YOUR_GMAIL = st.secrets.get("YOUR_GMAIL")
YOUR_APP_PASSWORD = st.secrets.get("YOUR_APP_PASSWORD")
SHEET_WEBHOOK_URL = st.secrets.get("SHEET_WEBHOOK_URL")
CSV_URL = "https://raw.githubusercontent.com/jimmywongx8-lang/jxperience-franchise-finder/main/franchise_data.csv"

# --- SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_franchise' not in st.session_state:
    st.session_state.selected_franchise = None
if 'franchisor_logged_in' not in st.session_state:
    st.session_state.franchisor_logged_in = False
if 'categories' not in st.session_state:
    st.session_state.categories = []

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    h1, h2, h3 { color: #1a1a2e; font-weight: 700; margin-bottom: 1rem; }
    .stButton>button { border-radius: 8px; font-weight: 600; padding: 0.5rem 1.5rem; transition: all 0.3s ease; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
    .metric-card { background: rgba(255,255,255,0.2); padding: 15px 25px; border-radius: 10px; backdrop-filter: blur(10px); }
    .status-badge { display: inline-block; background: #10b981; color: white; padding: 8px 16px; border-radius: 20px; font-weight: 600; margin-bottom: 20px; }
    .stMarkdown { margin-bottom: 1rem; }
    .stTextInput>div>div>input, .stSelectbox>div>div>select { border-radius: 8px; border: 1px solid #e0e0e0; }
    .stAlert { border-radius: 8px; }
    .benefit-card { background: #f0f7ff; border-left: 4px solid #667eea; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    .benefit-card h4 { color: #1a1a2e; margin-top: 0; }
    
    .brand-row {
        display: flex;
        align-items: center;
        padding: 20px;
        background: white;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    .brand-row:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.12); transform: translateY(-2px); }
    
    .brand-logo-wrapper {
        position: relative;
        width: 60px;
        height: 60px;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8em;
        font-weight: bold;
        margin-right: 20px;
        overflow: hidden;
        flex-shrink: 0;
    }
    .brand-logo-img {
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        object-fit: contain;
        background: white;
        padding: 8px;
        box-sizing: border-box;
    }
    
    .brand-info { flex: 1; }
    .brand-name { font-size: 1.2em; font-weight: 700; color: #1a1a2e; margin: 0 0 5px 0; }
    .brand-category { font-size: 0.9em; color: #666; margin: 0; }
    .brand-stats { text-align: right; margin-right: 20px; }
    .brand-investment { font-size: 0.95em; color: #333; margin: 0 0 5px 0; font-weight: 600; }
    .brand-royalty { font-size: 0.85em; color: #666; margin: 0; }
    
    .beta-banner {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .beta-banner h4 { color: #92400e; margin-top: 0; margin-bottom: 10px; }
    
    .faq-item {
        background: white;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        border-left: 3px solid #667eea;
    }
    .footer {
        text-align: center;
        padding: 20px;
        color: #666;
        font-size: 0.9em;
        margin-top: 40px;
        border-top: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# --- LOAD BRANDS ---
def extract_domain(url):
    if pd.isna(url) or not url:
        return ""
    try:
        url = str(url).replace("http://", "").replace("https://", "").replace("www.", "")
        return url.split("/")[0].split("?")[0]
    except:
        return ""

@st.cache_data(ttl=300)
def load_brands():
    try:
        df = pd.read_csv(CSV_URL)
        if "category" in df.columns:
            st.session_state.categories = df["category"].dropna().unique().tolist()
        if "website" in df.columns:
            df["domain"] = df["website"].apply(extract_domain)
            df["logo_url"] = df["domain"].apply(lambda d: f"https://www.google.com/s2/favicons?domain={d}&sz=128" if d else "")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# --- FRANCHISES ---
FRANCHISES = {
    "Coco Ichibanya": {"story": "Japan's #1 curry house with 1,300+ stores.", "investment": "$150k - $300k", "royalty": "5% - 7%", "sales": "¥50M - ¥80M", "overseas_status": "✅ ACTIVELY RECRUITING", "youtube_search": "Coco Ichibanya franchise", "news_search": "Coco Ichibanya expansion", "financials": {"Metric": ["Fee", "Investment", "Royalty", "Stores"], "Details": ["¥3M-¥5M", "$150k-$300k", "5-7%", "1,300+"]}, "pros": ["Proven success", "Low complexity"], "cons": ["Curry specialization"]},
    "Pepper Lunch": {"story": "Fast-steak concept with 200+ stores across 15+ countries.", "investment": "$200k - $400k", "royalty": "5% - 6%", "sales": "$400k - $800k", "overseas_status": "✅ VERY ACTIVE", "youtube_search": "Pepper Lunch franchise", "news_search": "Pepper Lunch expansion", "financials": {"Metric": ["Fee", "Investment", "Royalty", "Stores"], "Details": ["$30k-$50k", "$200k-$400k", "5-6%", "200+"]}, "pros": ["Proven success", "DIY concept"], "cons": ["Premium pricing"]},
    "Kura Sushi": {"story": "High-tech conveyor belt sushi expanding in USA.", "investment": "$500k - $1M", "royalty": "5% - 6%", "sales": "$1M - $2M", "overseas_status": "✅ EXPANDING IN USA", "youtube_search": "Kura Sushi USA", "news_search": "Kura Sushi expansion", "financials": {"Metric": ["Investment", "Royalty", "Locations"], "Details": ["$500k-$1M", "5-6%", "10+"]}, "pros": ["High-tech", "Strong growth"], "cons": ["High investment"]},
    "Sukiya": {"story": "Japan's largest gyudon chain with 2,000+ stores.", "investment": "$300k - $600k", "royalty": "4% - 6%", "sales": "¥100M+", "overseas_status": "✅ SELECTIVE", "youtube_search": "Sukiya franchise", "news_search": "Sukiya expansion", "financials": {"Metric": ["Investment", "Royalty", "Stores"], "Details": ["$300k-$600k", "4-6%", "2,000+"]}, "pros": ["Massive brand", "Simple menu"], "cons": ["Selective approval"]},
    "Hoshino Coffee": {"story": "Premium Nagoya coffee shop famous for pancakes.", "investment": "$250k - $500k", "royalty": "5% - 6%", "sales": "¥60M - ¥100M", "overseas_status": "✅ ACTIVE IN ASIA", "youtube_search": "Hoshino Coffee", "news_search": "Hoshino Coffee expansion", "financials": {"Metric": ["Investment", "Royalty", "Markets"], "Details": ["$250k-$500k", "5-6%", "HK/TW/TH"]}, "pros": ["Premium", "Unique menu"], "cons": ["Higher price"]},
    "Ootoya": {"story": "Premium teishoku restaurant with 500+ stores.", "investment": "$300k - $600k", "royalty": "5% - 6%", "sales": "$500k - $1M", "overseas_status": "✅ ESTABLISHED", "youtube_search": "Ootoya franchise", "news_search": "Ootoya international", "financials": {"Metric": ["Investment", "Royalty", "Stores"], "Details": ["$300k-$600k", "5-6%", "50+"]}, "pros": ["Premium", "Healthy menu"], "cons": ["Complex menu"]}
}

# --- FUNCTIONS ---
def send_email(subject, body, to_email=None):
    if not to_email: to_email = YOUR_GMAIL
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = YOUR_GMAIL
    msg["To"] = to_email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(YOUR_GMAIL, YOUR_APP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def save_to_sheet(franchise, name, email, capital, experience, industry, location, timeline):
    payload = {"franchise": franchise, "name": name, "email": email, "capital": capital, "experience": experience, "industry": industry, "location": location, "timeline": timeline}
    try:
        requests.post(SHEET_WEBHOOK_URL, json=payload)
        return True
    except Exception as e:
        print(f"Sheet error: {e}")
        return False

def get_leads():
    try:
        resp = requests.get(SHEET_WEBHOOK_URL, timeout=10)
        if resp.status_code == 200: return resp.json()
    except: pass
    return []

# --- PAGES ---
def show_home():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 50px 30px; border-radius: 15px; color: white; margin-bottom: 30px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
        <h1 style="color: white; margin: 0 0 15px 0; font-size: 2.5em; font-weight: 700;">🗾 Discover Japanese Franchise Opportunities</h1>
        <p style="font-size: 1.3em; margin: 0 0 20px 0; opacity: 0.95;">Connecting global investors with 63+ expansion-ready Japanese brands</p>
        <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-top: 25px;">
            <div class="metric-card"><div style="font-size: 2em; font-weight: bold;">63+</div><div style="font-size: 0.9em; opacity: 0.9;">Brands</div></div>
            <div class="metric-card"><div style="font-size: 2em; font-weight: bold;">15+</div><div style="font-size: 0.9em; opacity: 0.9;">Countries</div></div>
            <div class="metric-card"><div style="font-size: 2em; font-weight: bold;">$100k+</div><div style="font-size: 0.9em; opacity: 0.9;">Investment</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    df = load_brands()
    if df.empty:
        st.error("Could not load data")
        return
    
    st.subheader("Found 63 Expansion-Ready Brands")
    
    st.sidebar.subheader("🔍 Search & Filter")
    search = st.sidebar.text_input("Search brands", "")
    categories = st.session_state.get("categories", [])
    selected_cat = st.sidebar.multiselect("Filter by Category", categories, default=[])
    
    filtered = df.copy()
    if search:
        filtered = filtered[filtered["brand_name"].str.contains(search, case=False, na=False) | filtered["category"].str.contains(search, case=False, na=False)]
    if selected_cat:
        filtered = filtered[filtered["category"].isin(selected_cat)]
    
    st.write(f"Showing {len(filtered)} brands")
    
    for idx, row in filtered.iterrows():
        brand = row.get("brand_name", "Unknown")
        has_dd = brand in FRANCHISES
        logo_url = row.get("logo_url", "")
        first_letter = brand[0].upper() if brand else "?"
        category = row.get("category", "")
        stores = row.get("stores_japan", "")
        investment = row.get("investment_usd", "")
        royalty = row.get("royalty_pct", "")
        
        html = f"""
        <div class="brand-row">
            <div class="brand-logo-wrapper">
                {first_letter}
                <img src="{logo_url}" class="brand-logo-img">
            </div>
            <div class="brand-info">
                <p class="brand-name">{brand}</p>
                <p class="brand-category">{category} | {stores} stores</p>
            </div>
            <div class="brand-stats">
                <p class="brand-investment">${investment}</p>
                <p class="brand-royalty">Royalty: {royalty}%</p>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
        
        btn = "Deep Dive →" if has_dd else "Enquiry →"
        if st.button(btn, key=idx):
            st.session_state.selected_franchise = brand
            st.session_state.page = "profile" if has_dd else "quiz"
            st.rerun()

    # Footer
    st.markdown("""
    <div class="footer">
        <p>© 2026 JXPerience. Connecting Japanese brands with global investors.</p>
        <p>📧 Contact: jxperience.info@gmail.com</p>
    </div>
    """, unsafe_allow_html=True)

def show_profile():
    brand = st.session_state.selected_franchise
    if not brand:
        st.session_state.page = "home"
        st.rerun()
    if st.button("← Back"):
        st.session_state.page = "home"
        st.rerun()
    if brand in FRANCHISES:
        data = FRANCHISES[brand]
        st.title(f"🗾 {brand}")
        st.markdown(f'<div class="status-badge">{data["overseas_status"]}</div>', unsafe_allow_html=True)
        st.info(data["story"])
        st.subheader("📺 Watch")
        st.markdown(f'[▶️ Watch Videos](https://www.youtube.com/results?search_query={quote(data["youtube_search"])})')
        st.subheader("📰 News")
        st.markdown(f'[📰 Read News](https://www.google.com/search?q={quote(data["news_search"])}&tbm=nws)')
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        col1.metric("Investment", data["investment"])
        col2.metric("Royalty", data["royalty"])
        col3.metric("Sales", data["sales"])
        st.dataframe(pd.DataFrame(data["financials"]))
        st.markdown("---")
        col_p, col_c = st.columns(2)
        col_p.markdown("✅ **Pros**\n" + "\n".join([f"- {p}" for p in data["pros"]]))
        col_c.markdown("️ **Cons**\n" + "\n".join([f"- {c}" for c in data["cons"]]))
        st.divider()
        if st.button("Start Enquiry", type="primary"):
            st.session_state.page = "quiz"
            st.rerun()
    else:
        st.title(brand)
        st.info("Profile coming soon")

def show_quiz():
    brand = st.session_state.selected_franchise or "General"
    st.title(f"Enquiry: {brand}")
    if st.button("← Back"):
        st.session_state.page = "home"
        st.rerun()
    with st.form("quiz"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        capital = st.selectbox("Capital", ["Under $100k", "$100k-$250k", "$250k-$500k", "$500k-$1M", "Over $1M"])
        experience = st.selectbox("Experience", ["None", "1-3 years", "3-5 years", "5+ years", "Franchise Owner"])
        industry = st.selectbox("Industry", ["F&B", "Retail", "Corporate", "Other"])
        location = st.text_input("Location")
        timeline = st.selectbox("Timeline", ["Researching", "1-2 years", "6-12 months", "ASAP"])
        if st.form_submit_button("Submit Enquiry"):
            if name and email:
                send_email(f"Enquiry: {name} for {brand}", f"Name: {name}\nEmail: {email}")
                save_to_sheet(brand, name, email, capital, experience, industry, location, timeline)
                st.success("✅ Enquiry submitted!")
            else:
                st.error("Fill in name and email")

def show_franchisor():
    st.title(" Franchisor Portal")
    st.markdown('<div style="margin-bottom: 25px;"><h3 style="color: #1a1a2e; margin-top: 0;">Why Register as a Franchisor?</h3><p style="font-size: 1.1em; line-height: 1.6;">As a Japanese franchise brand, you have unique access to the global market. Our platform connects you directly with qualified international investors.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="benefit-card"><h4>✅ What You\'ll Get as a Verified Partner</h4><ul style="padding-left: 20px; margin: 15px 0;"><li><strong>Real-time qualified leads</strong> - See genuine investor applications as they come in</li><li><strong>Pre-screened investors</strong> - All applicants are vetted for serious investment capacity</li><li><strong>Dedicated dashboard</strong> - Track your leads and review applications in one place</li><li><strong>CSV export</strong> - Download your leads in spreadsheet format</li><li><strong>Direct connection</strong> - Contact investors directly through our secure platform</li></ul></div>', unsafe_allow_html=True)
    
    if not st.session_state.franchisor_logged_in:
        st.markdown('<div style="margin-bottom: 25px;"><h3 style="color: #1a1a2e; margin-top: 0;">Access Your Franchise Dashboard</h3><p style="font-size: 1.1em; line-height: 1.6;">If your brand is already approved as a partner, enter your access code to see your leads.<br><br><strong>Not sure if you\'re approved?</strong> Check your email for the access code, or <strong>request access</strong> below if you\'re a new franchise brand.</p></div>', unsafe_allow_html=True)
        pwd = st.text_input("Password", type="password")
        if st.button("Login"):
            if pwd == "jfa2026":
                st.session_state.franchisor_logged_in = True
                st.rerun()
            else:
                st.error("Wrong password")
        st.markdown('<div style="margin-top: 30px;"><h3 style="color: #1a1a2e; margin-top: 0;">New to JXPerience?</h3><p style="font-size: 1.1em; line-height: 1.6;">If you\'re a Japanese franchise brand looking to expand internationally, you can request access to our platform.</p></div>', unsafe_allow_html=True)
        with st.form("request"):
            company = st.text_input("Company")
            email = st.text_input("Email")
            st.markdown('<p style="font-size: 0.9em; color: #666;">By submitting this form, you\'ll receive:<ul style="padding-left: 20px; margin-top: 10px;"><li>Confirmation of your request</li><li>Review of your brand\'s expansion readiness</li><li>Access code within 24-48 hours</li></ul></p>', unsafe_allow_html=True)
            if st.form_submit_button("Request Access"):
                send_email("Partner Request", f"{company}: {email}")
                st.success("Request sent! We'll contact you within 24-48 hours.")
        return
    
    st.success("Logged in")
    if st.button("Logout"):
        st.session_state.franchisor_logged_in = False
        st.rerun()
    tab1, tab2 = st.tabs([" Leads", "⚙️ Settings"])
    with tab1:
        leads = get_leads()
        if leads:
            df = pd.DataFrame(leads)
            st.write(f"✅ Found {len(leads)} real leads!")
            st.dataframe(df)
            csv = df.to_csv(index=False)
            st.download_button("📥 Download CSV", csv, "leads.csv")
        else:
            st.info("No leads yet")
    with tab2:
        st.info("Settings coming soon")

def show_about():
    st.title("🗾 About JXPerience")
    st.caption("Our Mission & Story")
    st.markdown("---")
    st.subheader("Why We Started This")
    st.markdown("### A Personal Journey with Japanese Culture\n\nI'm a passionate advocate of Japanese culture and cuisine. Over the years, I've had the privilege of witnessing the remarkable growth and spread of Japanese culinary culture across Asia, Europe, and the United States.\n\nThe numbers tell an incredible story:")
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Japanese Restaurants (2006)", "24,000", "Starting point")
    with col2: st.metric("Japanese Restaurants (Today)", "200,000+", "+733% growth")
    with col3: st.metric("Growth Period", "~18 years", "JETRO Data")
    st.markdown("This **8x growth** in less than two decades is unprecedented in global food culture history.\n\n### Our Mission\n\nAs a personal project, I started JXPerience to:\n\n1. **📊 Aggregate Information** - Bring together comprehensive data on Japanese franchises, from well-known brands to emerging opportunities\n2. **🤝 Connect Investors** - Help serious global investors discover and connect with authentic Japanese franchise opportunities\n3. **🌍 Support Expansion** - Contribute to the continued global growth of Japanese cuisine and culture\n4. **🍱 Cultural Exchange** - Enable more people worldwide to discover authentic Japanese cuisine, fostering deeper understanding and appreciation of Japanese culture\n\n### The Vision\n\nBy making franchise information more accessible, we hope to:\n- Support more people in discovering authentic Japanese cuisine\n- Facilitate meaningful cultural exchanges through food\n- Create shared experiences that bring people together\n- Help Japanese brands find the right partners for global expansion\n\n---\n\n*This platform is a labor of love, built to support the continued growth and appreciation of Japanese culinary excellence worldwide.*")
    
    st.markdown("""
    <div class="beta-banner">
        <h4>🚧 This is a Beta Site — Help Us Build It Together!</h4>
        <p style="color: #78350f; margin-bottom: 10px;">
            JXPerience is currently in <strong>beta</strong>. We are actively improving the platform and would love your input.
        </p>
        <p style="color: #78350f; margin-bottom: 10px;">
            <strong>🤝 Co-Create With Us</strong> — Have suggestions, spotted a bug, or want to recommend a franchise brand to add? 
            We invite you to share your comments and improvement ideas directly with us.
        </p>
        <p style="color: #78350f; margin: 0;">
            📧 <strong>Email us at:</strong> <a href="mailto:jxperience.info@gmail.com?subject=JXPerience Feedback&body=Hi, I'd like to share some feedback about JXPerience...">jxperience.info@gmail.com</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- NEW FAQ SECTION ---
    st.markdown("---")
    st.subheader("❓ Frequently Asked Questions")
    
    faqs = [
        {"q": "Is there a fee to use this platform?", "a": "No, browsing and submitting enquiries is completely free for investors."},
        {"q": "How do I know these brands are legitimate?", "a": "We verify overseas expansion status using public data, JETRO reports, and official franchise disclosures. Look for the 'Verified' badge on deep-dive profiles."},
        {"q": "What happens after I submit an enquiry?", "a": "Your details are securely sent to our team. We will pre-screen your profile and connect you with the franchise's international development team if there is a match."},
        {"q": "Can I franchise a brand not listed here?", "a": "Yes! Use the 'Co-Create' email link above to suggest a brand. We are always adding new opportunities."}
    ]
    
    for faq in faqs:
        st.markdown(f"""
        <div class="faq-item">
            <p style="font-weight: bold; color: #1a1a2e; margin-bottom: 5px;">{faq["q"]}</p>
            <p style="color: #666; margin: 0;">{faq["a"]}</p>
        </div>
        """, unsafe_allow_html=True)
    # --- END FAQ ---
    
    st.divider()
    st.subheader("🚀 Ready to Explore?")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Browse Franchises", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
    with col_b:
        st.markdown("📧 **Contact:** [jxperience.info@gmail.com](mailto:jxperience.info@gmail.com)")

# --- SIDEBAR ---
st.sidebar.title(" JP Hub")
st.sidebar.markdown("---")
st.sidebar.subheader("Navigation")
if st.sidebar.button("🏠 Home", use_container_width=True):
    st.session_state.page = "home"
    st.rerun()
if st.sidebar.button("ℹ️ About Us", use_container_width=True):
    st.session_state.page = "about"
    st.rerun()
if st.sidebar.button("🏢 Franchisor", use_container_width=True):
    st.session_state.page = "franchisor"
    st.rerun()
st.sidebar.markdown("---")

# --- ROUTER ---
if st.session_state.page == "quiz": show_quiz()
elif st.session_state.page == "franchisor": show_franchisor()
elif st.session_state.page == "profile": show_profile()
elif st.session_state.page == "about": show_about()
else: show_home()
