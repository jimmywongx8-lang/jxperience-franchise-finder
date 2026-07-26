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

# --- CUSTOM CSS (ENHANCED) ---
st.markdown("""
<style>
    /* Main background */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Typography */
    h1, h2, h3 {
        color: #1a1a2e;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #ffffff;
    }
    
    /* Card styling for franchises */
    .franchise-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .franchise-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255,255,255,0.2);
        padding: 15px 25px;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        background: #10b981;
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        margin-bottom: 20px;
    }
    
    /* Better spacing */
    .stMarkdown {
        margin-bottom: 1rem;
    }
    
    /* Form styling */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }
    
    /* Alert boxes */
    .stAlert {
        border-radius: 8px;
    }
    
    /* Benefits section */
    .benefit-card {
        background: #f0f7ff;
        border-left: 4px solid #667eea;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    
    .benefit-card h4 {
        color: #1a1a2e;
        margin-top: 0;
    }
</style>
""", unsafe_allow_html=True)

# --- LOAD 63 BRANDS ---
@st.cache_data(ttl=300)
def load_brands():
    try:
        df = pd.read_csv(CSV_URL)
        if 'category' in df.columns:
            st.session_state.categories = df['category'].dropna().unique().tolist()
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# --- 6 DEEP DIVE PROFILES ---
FRANCHISES = {
    "Coco Ichibanya": {
        "story": "Japan's #1 curry house with 1,300+ stores. Aggressively expanding overseas.",
        "investment": "$150k - $300k",
        "royalty": "5% - 7%",
        "sales": "¥50M - ¥80M",
        "overseas_status": "✅ ACTIVELY RECRUITING - USA, Asia, Europe",
        "youtube_search": "Coco Ichibanya franchise overseas",
        "news_search": "Coco Ichibanya international expansion",
        "financials": {"Metric": ["Franchise Fee", "Total Investment", "Royalty", "Store Count"], 
                      "Details": ["¥3M - ¥5M", "$150k - $300k", "5% - 7%", "1,300+ stores"]},
        "pros": ["Proven overseas success", "Low complexity", "Customizable menu"],
        "cons": ["Curry specialization", "Competition in Asia"]
    },
    "Pepper Lunch": {
        "story": "Fast-steak concept with 200+ stores across 15+ countries. Highly successful internationally.",
        "investment": "$200k - $400k",
        "royalty": "5% - 6%",
        "sales": "$400k - $800k",
        "overseas_status": "✅ VERY ACTIVE - 15+ countries",
        "youtube_search": "Pepper Lunch franchise",
        "news_search": "Pepper Lunch global expansion",
        "financials": {"Metric": ["Franchise Fee", "Investment", "Royalty", "Global Stores"], 
                      "Details": ["$30k-$50k", "$200k-$400k", "5%-6%", "200+ stores"]},
        "pros": ["Proven success", "DIY concept", "Fast service"],
        "cons": ["Sizzling equipment", "Premium pricing"]
    },
    "Kura Sushi": {
        "story": "High-tech conveyor belt sushi expanding aggressively in USA.",
        "investment": "$500k - $1M",
        "royalty": "5% - 6%",
        "sales": "$1M - $2M",
        "overseas_status": "✅ EXPANDING IN USA",
        "youtube_search": "Kura Sushi USA",
        "news_search": "Kura Sushi USA expansion",
        "financials": {"Metric": ["Investment", "Royalty", "US Locations"], 
                      "Details": ["$500k-$1M", "5%-6%", "10+ locations"]},
        "pros": ["High-tech", "Strong US growth", "Premium"],
        "cons": ["High investment", "Complex operations"]
    },
    "Sukiya": {
        "story": "Japan's largest gyudon chain with 2,000+ stores. Expanding in Asia.",
        "investment": "$300k - $600k",
        "royalty": "4% - 6%",
        "sales": "¥100M+",
        "overseas_status": "✅ SELECTIVE - Asia focus",
        "youtube_search": "Sukiya franchise Asia",
        "news_search": "Sukiya international expansion",
        "financials": {"Metric": ["Investment", "Royalty", "Global Stores"], 
                      "Details": ["$300k-$600k", "4%-6%", "2,000+ stores"]},
        "pros": ["Massive brand", "Simple menu", "High volume"],
        "cons": ["Selective approval", "Beef regulations"]
    },
    "Hoshino Coffee": {
        "story": "Premium Nagoya coffee shop famous for pancakes. Expanding in Asia.",
        "investment": "$250k - $500k",
        "royalty": "5% - 6%",
        "sales": "¥60M - ¥100M",
        "overseas_status": "✅ ACTIVE IN ASIA",
        "youtube_search": "Hoshino Coffee Asia",
        "news_search": "Hoshino Coffee expansion",
        "financials": {"Metric": ["Investment", "Royalty", "Markets"], 
                      "Details": ["$250k-$500k", "5%-6%", "HK/TW/TH"]},
        "pros": ["Premium", "Unique menu", "Strong branding"],
        "cons": ["Higher price", "Large space needed"]
    },
    "Ootoya": {
        "story": "Premium teishoku restaurant with 500+ stores. Strong US presence.",
        "investment": "$300k - $600k",
        "royalty": "5% - 6%",
        "sales": "$500k - $1M",
        "overseas_status": "✅ ESTABLISHED - USA, Asia",
        "youtube_search": "Ootoya franchise USA",
        "news_search": "Ootoya international",
        "financials": {"Metric": ["Investment", "Royalty", "Overseas"], 
                      "Details": ["$300k-$600k", "5%-6%", "50+ stores"]},
        "pros": ["Premium", "Healthy menu", "US success"],
        "cons": ["Complex menu", "Japanese ingredients"]
    }
}

# --- FUNCTIONS ---
def send_email(subject, body, to_email=None):
    if not to_email:
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

def save_to_sheet(franchise, name, email, capital, experience, industry, location, timeline):
    payload = {"franchise": franchise, "name": name, "email": email, 
               "capital": capital, "experience": experience, 
               "industry": industry, "location": location, "timeline": timeline}
    try:
        requests.post(SHEET_WEBHOOK_URL, json=payload)
        return True
    except Exception as e:
        print(f"Sheet error: {e}")
        return False

def get_leads():
    try:
        resp = requests.get(SHEET_WEBHOOK_URL, timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return []

# --- PAGES ---
def show_home():
    # === HERO SECTION ===
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 50px 30px;
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    '>
        <h1 style='
            color: white; 
            margin: 0 0 15px 0;
            font-size: 2.5em;
            font-weight: 700;
        '>🗾 Discover Japanese Franchise Opportunities</h1>
        <p style='
            font-size: 1.3em; 
            margin: 0 0 20px 0; 
            opacity: 0.95;
        '>
            Connecting global investors with 63+ expansion-ready Japanese brands
        </p>
        <div style='
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
            margin-top: 25px;
        '>
            <div class='metric-card'>
                <div style='font-size: 2em; font-weight: bold;'>63+</div>
                <div style='font-size: 0.9em; opacity: 0.9;'>Brands</div>
            </div>
            <div class='metric-card'>
                <div style='font-size: 2em; font-weight: bold;'>15+</div>
                <div style='font-size: 0.9em; opacity: 0.9;'>Countries</div>
            </div>
            <div class='metric-card'>
                <div style='font-size: 2em; font-weight: bold;'>$100k+</div>
                <div style='font-size: 0.9em; opacity: 0.9;'>Investment</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    # === END HERO SECTION ===
    
    df = load_brands()
    if df.empty:
        st.error("Could not load data")
        return
    
    st.subheader("Found 63 Expansion-Ready Brands")
    
    # Sidebar Filters
    st.sidebar.subheader("🔍 Search & Filter")
    search = st.sidebar.text_input("Search brands", "")
    categories = st.session_state.get('categories', [])
    selected_cat = st.sidebar.multiselect("Filter by Category", categories, default=[])
    
    # Apply filters
    filtered = df.copy()
    if search:
        filtered = filtered[filtered['brand_name'].str.contains(search, case=False, na=False) |
                          filtered['category'].str.contains(search, case=False, na=False)]
    if selected_cat:
        filtered = filtered[filtered['category'].isin(selected_cat)]
    
    st.write(f"Showing {len(filtered)} brands")
    
    # Display brands with CARD LAYOUT
    for idx, row in filtered.iterrows():
        brand = row.get('brand_name', 'Unknown')
        has_dd = brand in FRANCHISES
        
        st.markdown(f"""
        <div class='franchise-card'>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.markdown(f"**{brand}**")
            st.caption(f"{row.get('category', '')} | {row.get('stores_japan', '')} stores")
        with col2:
            st.caption(f"${row.get('investment_usd', '')} | Royalty: {row.get('royalty_pct', '')}%")
        with col3:
            btn = "Deep Dive →" if has_dd else "Apply →"
            if st.button(btn, key=idx):
                st.session_state.selected_franchise = brand
                st.session_state.page = 'profile' if has_dd else 'quiz'
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

def show_profile():
    brand = st.session_state.selected_franchise
    if not brand:
        st.session_state.page = 'home'
        st.rerun()
    
    if st.button("← Back"):
        st.session_state.page = 'home'
        st.rerun()
    
    if brand in FRANCHISES:
        data = FRANCHISES[brand]
        st.title(f"🗾 {brand}")
        
        # Status badge
        st.markdown(f"""
        <div class='status-badge'>
            {data['overseas_status']}
        </div>
        """, unsafe_allow_html=True)
        
        st.info(data["story"])
        
        st.subheader("📺 Watch")
        yt_url = f"https://www.youtube.com/results?search_query={quote(data['youtube_search'])}"
        st.markdown(f"[▶️ Watch Videos]({yt_url})")
        
        st.subheader("📰 News")
        news_url = f"https://www.google.com/search?q={quote(data['news_search'])}&tbm=nws"
        st.markdown(f"[ Read News]({news_url})")
        
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        col1.metric("Investment", data["investment"])
        col2.metric("Royalty", data["royalty"])
        col3.metric("Sales", data["sales"])
        
        st.dataframe(pd.DataFrame(data["financials"]))
        
        st.markdown("---")
        col_p, col_c = st.columns(2)
        col_p.markdown("✅ **Pros**\n" + "\n".join([f"- {p}" for p in data["pros"]]))
        col_c.markdown("⚠️ **Cons**\n" + "\n".join([f"- {c}" for c in data["cons"]]))
        
        st.divider()
        if st.button("Start Application", type="primary"):
            st.session_state.page = 'quiz'
            st.rerun()
    else:
        st.title(brand)
        st.info("Profile coming soon")

def show_quiz():
    brand = st.session_state.selected_franchise or "General"
    st.title(f"Apply: {brand}")
    
    if st.button("← Back"):
        st.session_state.page = 'home'
        st.rerun()
    
    with st.form("quiz"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        capital = st.selectbox("Capital", ["Under $100k", "$100k-$250k", "$250k-$500k", "$500k-$1M", "Over $1M"])
        experience = st.selectbox("Experience", ["None", "1-3 years", "3-5 years", "5+ years", "Franchise Owner"])
        industry = st.selectbox("Industry", ["F&B", "Retail", "Corporate", "Other"])
        location = st.text_input("Location")
        timeline = st.selectbox("Timeline", ["Researching", "1-2 years", "6-12 months", "ASAP"])
        
        if st.form_submit_button("Submit"):
            if name and email:
                send_email(f"Lead: {name} for {brand}", f"Name: {name}\nEmail: {email}")
                save_to_sheet(brand, name, email, capital, experience, industry, location, timeline)
                st.success("✅ Submitted!")
            else:
                st.error("Fill in name and email")

def show_franchisor():
    st.title("🗾 Franchisor Portal")
    
    # Add clear explanation of benefits
    st.markdown("""
    <div style='margin-bottom: 25px;'>
        <h3 style='color: #1a1a2e; margin-top: 0;'>Why Register as a Franchisor?</h3>
        <p style='font-size: 1.1em; line-height: 1.6;'>
            As a Japanese franchise brand, you have unique access to the global market. 
            Our platform connects you directly with qualified international investors.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Benefits section
    st.markdown("""
    <div class='benefit-card'>
        <h4>✅ What You'll Get as a Verified Partner</h4>
        <ul style='padding-left: 20px; margin: 15px 0;'>
            <li><strong>Real-time qualified leads</strong> - See genuine investor applications as they come in</li>
            <li><strong>Pre-screened investors</strong> - All applicants are vetted for serious investment capacity</li>
            <li><strong>Dedicated dashboard</strong> - Track your leads and review applications in one place</li>
            <li><strong>CSV export</strong> - Download your leads in spreadsheet format</li>
            <li><strong>Direct connection</strong> - Contact investors directly through our secure platform</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.franchisor_logged_in:
        # Add explanation for login section
        st.markdown("""
        <div style='margin-bottom: 25px;'>
            <h3 style='color: #1a1a2e; margin-top: 0;'>Access Your Franchise Dashboard</h3>
            <p style='font-size: 1.1em; line-height: 1.6;'>
                If your brand is already approved as a partner, enter your access code to see your leads.
                <br><br>
                <strong>Not sure if you're approved?</strong> Check your email for the access code, or 
                <strong>request access</strong> below if you're a new franchise brand.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        pwd = st.text_input("Password", type="password")
        if st.button("Login"):
            if pwd == "jfa2026":
                st.session_state.franchisor_logged_in = True
                st.rerun()
            else:
                st.error("Wrong password")
        
        # Add explanation for request access
        st.markdown("""
        <div style='margin-top: 30px;'>
            <h3 style='color: #1a1a2e; margin-top: 0;'>New to JXPerience?</h3>
            <p style='font-size: 1.1em; line-height: 1.6;'>
                If you're a Japanese franchise brand looking to expand internationally, 
                you can request access to our platform.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("request"):
            company = st.text_input("Company")
            email = st.text_input("Email")
            st.markdown("""
            <p style='font-size: 0.9em; color: #666;'>
                By submitting this form, you'll receive:
                <ul style='padding-left: 20px; margin-top: 10px;'>
                    <li>Confirmation of your request</li>
                    <li>Review of your brand's expansion readiness</li>
                    <li>Access code within 24-48 hours</li>
                </ul>
            </p>
            """, unsafe_allow_html=True)
            
            if st.form_submit_button("Request Access"):
                send_email("Partner Request", f"{company}: {email}")
                st.success("Request sent! We'll contact you within 24-48 hours.")
        return
    
    st.success("Logged in")
    if st.button("Logout"):
        st.session_state.franchisor_logged_in = False
        st.rerun()
    
    tab1, tab2 = st.tabs(["📊 Leads", "⚙️ Settings"])
    
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
    st.markdown("""
    ### A Personal Journey with Japanese Culture
    
    I'm a passionate advocate of Japanese culture and cuisine. Over the years, I've had the privilege of 
    witnessing the remarkable growth and spread of Japanese culinary culture across Asia, Europe, and the United States.
    
    The numbers tell an incredible story:
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Japanese Restaurants (2006)", "24,000", "Starting point")
    with col2:
        st.metric("Japanese Restaurants (Today)", "200,000+", "+733% growth")
    with col3:
        st.metric("Growth Period", "~18 years", "JETRO Data")
    
    st.markdown("""
    This **8x growth** in less than two decades is unprecedented in global food culture history.
    
    ### Our Mission
    
    As a personal project, I started JXPerience to:
    
    1. ** Aggregate Information** - Bring together comprehensive data on Japanese franchises, 
       from well-known brands to emerging opportunities
    
    2. **🤝 Connect Investors** - Help serious global investors discover and connect with authentic 
       Japanese franchise opportunities
    
    3. **🌍 Support Expansion** - Contribute to the continued global growth of Japanese cuisine 
       and culture
    
    4. ** Cultural Exchange** - Enable more people worldwide to discover authentic Japanese cuisine, 
       fostering deeper understanding and appreciation of Japanese culture
    
    ### The Vision
    
    By making franchise information more accessible, we hope to:
    - Support more people in discovering authentic Japanese cuisine
    - Facilitate meaningful cultural exchanges through food
    - Create shared experiences that bring people together
    - Help Japanese brands find the right partners for global expansion
    
    ---
    
    *This platform is a labor of love, built to support the continued growth and appreciation of 
    Japanese culinary excellence worldwide.*
    """)
    
    st.divider()
    
    st.subheader("🚀 Ready to Explore?")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Browse Franchises", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
    with col_b:
        st.markdown("📧 **Contact:** [jxperience.info@gmail.com](mailto:jxperience.info@gmail.com)")

# --- SIDEBAR NAVIGATION (IMPROVED) ---
st.sidebar.title("🗾 JP Hub")
st.sidebar.markdown("---")

st.sidebar.subheader("Navigation")
if st.sidebar.button("🏠 Home", use_container_width=True):
    st.session_state.page = 'home'
    st.rerun()

if st.sidebar.button("ℹ️ About Us", use_container_width=True):
    st.session_state.page = 'about'
    st.rerun()

if st.sidebar.button(" Franchisor", use_container_width=True):
    st.session_state.page = 'franchisor'
    st.rerun()

st.sidebar.markdown("---")

# --- MAIN ROUTER ---
if st.session_state.page == 'quiz':
    show_quiz()
elif st.session_state.page == 'franchisor':
    show_franchisor()
elif st.session_state.page == 'profile':
    show_profile()
elif st.session_state.page == 'about':
    show_about()
else:
    show_home()
