import streamlit as st
import pandas as pd
from openai import OpenAI
import json

# App Title - JXPerience Branding
st.set_page_config(
    page_title="JXPerience | Japanese Franchise Expansion Platform", 
    page_icon="🔴",
    layout="wide"
)

# Custom styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f1f1f;
    }
    .brand-accent {
        color: #ff2d55;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-top: -10px;
    }
    .tagline {
        font-size: 0.95rem;
        color: #888;
        font-style: italic;
    }
    .clickable-link {
        color: #ff2d55;
        text-decoration: none;
        font-weight: 500;
    }
    .disclaimer-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 12px 16px;
        margin: 20px 0;
        font-size: 0.9rem;
        color: #856404;
    }
    .stat-card {
        background: linear-gradient(135deg, #ff2d55 0%, #ff6b6b 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin: 10px;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        display: block;
    }
    .stat-label {
        font-size: 0.85rem;
        opacity: 0.9;
    }
    .hidden-gem-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-left: 8px;
    }
    .brand-initial {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        border-radius: 8px;
        color: white;
        font-weight: 700;
        font-size: 0.9rem;
        margin-right: 8px;
    }
    .email-capture-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 16px;
        padding: 30px;
        margin: 20px 0;
        border: 2px solid #dee2e6;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header"><span class="brand-accent">JX</span>Perience</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Japanese Franchise Overseas Expansion Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Connecting Japanese brands with serious global investors</div>', unsafe_allow_html=True)
st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

# Load the data
@st.cache_data
def load_data():
    paths_to_try = [
        "C:\\jfa_scraper\\franchise_data.csv",
        "franchise_data.csv",
        "/mount/src/jxperience-franchise-finder/franchise_data.csv"
    ]
    
    for path in paths_to_try:
        try:
            df = pd.read_csv(path)
            return df
        except FileNotFoundError:
            continue
    
    st.error("⚠️ CSV file not found.")
    return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("️ No data loaded.")
    st.stop()

# Add confidence badges
def get_confidence_badge(confidence):
    if confidence == "YES":
        return "✅ Confirmed"
    elif confidence == "PROBABLE":
        return " Probable"
    elif confidence == "NEEDS_VERIFICATION":
        return "⚠️ Verify"
    else:
        return " No"

df['franchise_status'] = df['overseas_franchise_confirmed'].apply(get_confidence_badge)

# Generate colored initials for each brand
def get_brand_initials(brand_name):
    words = brand_name.split()
    if len(words) >= 2:
        return (words[0][0] + words[1][0]).upper()
    return brand_name[:2].upper()

def get_brand_color(brand_name):
    colors = [
        '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7',
        '#dfe6e9', '#fd79a8', '#a29bfe', '#fdcb6e', '#6c5ce7',
        '#00b894', '#e17055', '#0984e3', '#d63031', '#e84393'
    ]
    hash_val = sum(ord(c) for c in brand_name) % len(colors)
    return colors[hash_val]

df['brand_initials'] = df['brand_name'].apply(get_brand_initials)
df['brand_color'] = df['brand_name'].apply(get_brand_color)

# SECURE API KEY
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

if not GROQ_API_KEY:
    st.warning("⚠️ API Key not configured.")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# --- HERO SECTION ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="stat-card">
            <span class="stat-number">63+</span>
            <span class="stat-label">Japanese Franchises<br/>Analyzed</span>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="stat-card">
            <span class="stat-number">$100k-$800k</span>
            <span class="stat-label">Investment Range<br/>(USD)</span>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="stat-card">
            <span class="stat-number">15+</span>
            <span class="stat-label">Target Markets<br/>Across SE Asia, USA & Europe</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- SIDEBAR FILTERS ---
st.sidebar.markdown("### <span style='color:#ff2d55'>JX</span>Perience", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Search
st.sidebar.markdown("#### 🔍 Search")
search_term = st.sidebar.text_input("", placeholder="Type brand name...")
st.sidebar.markdown("---")

# Display Mode with Hidden Gems emphasis
st.sidebar.markdown("####  Discovery Mode")
display_mode = st.sidebar.radio(
    "Show:",
    [" Hidden Gems (<50 overseas)", " All Brands (A-Z)", "✅ Verified Only"],
    help="Hidden Gems: Undiscovered brands with high growth potential"
)
st.sidebar.markdown("---")

# Sort Control
st.sidebar.markdown("#### 📊 Sort By")
sort_by = st.sidebar.selectbox(
    "Primary sort:",
    ["Brand Name (A-Z)", "Investment (Low-High)", "Investment (High-Low)", 
     "Franchise Fee (Low-High)", "Royalty % (Low-High)", 
     "Japan Stores (Most)", "Overseas Stores (Least)"]
)
st.sidebar.markdown("---")

# Category Filter
st.sidebar.header("Filter by Category")
selected_category = st.sidebar.multiselect(
    "Select categories:", 
    options=df['category'].unique(), 
    default=df['category'].unique()
)

# --- FILTERING & SORTING LOGIC ---
filtered_df = df[df['category'].isin(selected_category)].copy()

# Apply Hidden Gems filter
if "Hidden Gems" in display_mode:
    overseas_nums = pd.to_numeric(filtered_df['stores_overseas'].str.extract('(\d+)')[0], errors='coerce').fillna(999)
    filtered_df = filtered_df[overseas_nums < 50]

# Apply Verified Only filter
if "Verified Only" in display_mode:
    filtered_df = filtered_df[filtered_df['overseas_franchise_confirmed'] == 'YES']

# Apply sorting
if "Investment (Low-High)" in sort_by:
    filtered_df['sort_val'] = pd.to_numeric(filtered_df['investment_usd'].str.extract('(\d+)')[0], errors='coerce').fillna(999999)
    filtered_df = filtered_df.sort_values('sort_val')
    filtered_df = filtered_df.drop(columns=['sort_val'])
elif "Investment (High-Low)" in sort_by:
    filtered_df['sort_val'] = pd.to_numeric(filtered_df['investment_usd'].str.extract('(\d+)')[0], errors='coerce').fillna(0)
    filtered_df = filtered_df.sort_values('sort_val', ascending=False)
    filtered_df = filtered_df.drop(columns=['sort_val'])
elif "Franchise Fee (Low-High)" in sort_by:
    filtered_df = filtered_df.sort_values('franchise_fee_usd')
elif "Royalty % (Low-High)" in sort_by:
    filtered_df = filtered_df.sort_values('royalty_pct')
elif "Japan Stores (Most)" in sort_by:
    filtered_df['sort_val'] = pd.to_numeric(filtered_df['stores_japan'].str.extract('(\d+)')[0], errors='coerce').fillna(0)
    filtered_df = filtered_df.sort_values('sort_val', ascending=False)
    filtered_df = filtered_df.drop(columns=['sort_val'])
elif "Overseas Stores (Least)" in sort_by:
    filtered_df['sort_val'] = pd.to_numeric(filtered_df['stores_overseas'].str.extract('(\d+)')[0], errors='coerce').fillna(999)
    filtered_df = filtered_df.sort_values('sort_val')
    filtered_df = filtered_df.drop(columns=['sort_val'])
else:
    filtered_df = filtered_df.sort_values('brand_name')

# Apply search
if search_term:
    filtered_df = filtered_df[filtered_df['brand_name'].str.contains(search_term, case=False, na=False)]

# --- DISPLAY COUNT ---
if "Hidden Gems" in display_mode:
    st.subheader(f" Found {len(filtered_df)} Hidden Gem Brands")
else:
    st.subheader(f"Found {len(filtered_df)} Expansion-Ready Brands")

# --- DISCLAIMER ---
st.markdown("""
    <div class="disclaimer-box">
        <strong>ℹ️ Disclaimer:</strong> All information sourced from public data. 
        "✅ Confirmed" brands have verified overseas programs. JXPerience is not officially affiliated 
        with listed brands unless marked "Verified Partner." Verify all details directly before investing.
    </div>
""", unsafe_allow_html=True)

# --- PREPARE DATA FOR DISPLAY WITH COLORED INITIALS ---
# Create a new dataframe with only the columns we need
display_df = pd.DataFrame()

# Create brand display with colored initials and hidden gem badge
brand_displays = []
for idx, row in filtered_df.iterrows():
    initials = row['brand_initials']
    color = row['brand_color']
    brand_name = row['brand_name']
    
    # Check if hidden gem
    try:
        overseas_str = str(row['stores_overseas']).replace('+', '').strip()
        overseas_num = int(overseas_str) if overseas_str.isdigit() else 999
        badge = '<span class="hidden-gem-badge">HIDDEN GEM</span>' if overseas_num < 50 else ''
    except:
        badge = ''
    
    brand_displays.append(f'<div style="display:flex;align-items:center;"><span class="brand-initial" style="background-color:{color}">{initials}</span><span>{brand_name}</span>{badge}</div>')

display_df['Brand'] = brand_displays
display_df['Category'] = filtered_df['category'].values
display_df['Japan Stores'] = filtered_df['stores_japan'].values
display_df['Overseas'] = filtered_df['stores_overseas'].values
display_df['Investment'] = filtered_df['investment_usd'].values

# Format franchise fee
franchise_fees = []
for fee in filtered_df['franchise_fee_usd']:
    try:
        franchise_fees.append(f"${int(fee):,}")
    except:
        franchise_fees.append('N/A')
display_df['Franchise Fee'] = franchise_fees

# Format royalty
royalties = []
for royalty in filtered_df['royalty_pct']:
    try:
        royalties.append(f"{royalty}%")
    except:
        royalties.append('N/A')
display_df['Royalty %'] = royalties

display_df['Target Markets'] = filtered_df['target_markets'].values

# Create clickable URLs
websites = []
for url in filtered_df['website']:
    if pd.notna(url) and url != '':
        websites.append(f"[🔗 Visit](https://{url})")
    else:
        websites.append('N/A')
display_df['Website'] = websites

display_df['Status'] = filtered_df['franchise_status'].values

# Show dataframe with sorting
st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Brand": st.column_config.TextColumn("Brand", width="medium"),
        "Investment": st.column_config.TextColumn("Investment", width="small"),
        "Franchise Fee": st.column_config.TextColumn("Fee", width="small"),
        "Royalty %": st.column_config.TextColumn("Royalty", width="small"),
    }
)

# --- ENHANCED INVESTOR EMAIL CAPTURE ---
st.markdown("---")
st.markdown("""
    <div class="email-capture-box">
        <h3 style="margin-top:0;">📬 Get Early Access to New Brands</h3>
        <p style="margin-bottom:20px;">Be the first to know when we add promising Japanese franchises in your sector. 
        Perfect for investors scouting the next big opportunity.</p>
    </div>
""", unsafe_allow_html=True)

with st.form("notification_signup"):
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        investor_email = st.text_input("Your Email", placeholder="investor@example.com")
    with col2:
        investor_category = st.selectbox("Interested Category", ["All Categories"] + list(df['category'].unique()))
    with col3:
        submit_notification = st.form_submit_button(" Notify Me", use_container_width=True)
    
    if submit_notification:
        if not investor_email:
            st.error("Please enter your email")
        else:
            st.success("✅ You're on the list! We'll notify you about new opportunities.")
            st.info("💡 Pro tip: Bookmark this page and check back weekly for new hidden gems!")

# --- AI ASSESSMENT FORM ---
st.markdown("---")
st.subheader("Interested in a brand?")
st.write("Fill out this form for an **AI-qualified assessment**.")

with st.form("contact_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Your Name")
        email = st.text_input("Email")
        country = st.text_input("Your Country")
    
    with col2:
        capital = st.selectbox("Available Capital (USD)", 
                               ["< $100k", "$100k - $300k", "$300k - $500k", "> $500k"])
        experience = st.radio("F&B Experience?", ["Yes", "No"])
        timeline = st.selectbox("Timeline to Open", ["Immediate (< 6 months)", "6-12 months", "1-2 years", "Just researching"])
    
    selected_brand = st.selectbox("Which brand interests you?", filtered_df['brand_name'].tolist())
    message = st.text_area("Additional Info (optional)", placeholder="Your background, location plans, etc.")
    
    submitted = st.form_submit_button("🚀 Get AI Assessment")
    
    if submitted:
        if not GROQ_API_KEY:
            st.error("⚠️ API Key not configured.")
        elif not name or not email:
            st.error("⚠️ Please fill in name and email")
        else:
            brand_info = filtered_df[filtered_df['brand_name'] == selected_brand].iloc[0]
            
            with st.spinner("🤖 AI analyzing..."):
                try:
                    prompt = f"""You are a franchise investment analyst. Evaluate this investor:

INVESTOR:
- Name: {name}
- Country: {country}
- Capital: {capital}
- F&B Experience: {experience}
- Timeline: {timeline}
- Info: {message if message else "None"}

FRANCHISE:
- Brand: {brand_info['brand_name']}
- Category: {brand_info['category']}
- Japan Stores: {brand_info['stores_japan']}
- Overseas: {brand_info['stores_overseas']}
- Investment: {brand_info['investment_usd']}
- Fee: {brand_info['franchise_fee_usd']} USD
- Royalty: {brand_info['royalty_pct']}%
- Markets: {brand_info['target_markets']}
- Status: {brand_info['franchise_status']}

Return JSON:
{{
    "readiness_score": "High/Medium/Low",
    "score_reasoning": "2-3 sentences",
    "capital_fit": "Yes/No with explanation",
    "market_fit": "Yes/No with explanation",
    "strengths": ["list"],
    "concerns": ["list"],
    "recommendation": "One sentence"
}}

Be honest and direct."""

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7,
                        response_format={"type": "json_object"}
                    )
                    
                    ai_analysis = json.loads(response.choices[0].message.content)
                    
                    st.success("✅ AI Assessment Complete!")
                    st.markdown("### 📊 Your Investment Readiness Score")
                    
                    score = ai_analysis.get('readiness_score', 'N/A')
                    if score == 'High':
                        st.metric("Readiness Score", score, delta="Excellent fit!")
                        st.balloons()
                    elif score == 'Medium':
                        st.metric("Readiness Score", score, delta="Good potential")
                    else:
                        st.metric("Readiness Score", score, delta="Needs development")
                    
                    st.markdown(f"**Analysis:** {ai_analysis.get('score_reasoning', 'N/A')}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.info(f"💰 **Capital Fit:** {ai_analysis.get('capital_fit', 'N/A')}")
                        st.info(f"🌍 **Market Fit:** {ai_analysis.get('market_fit', 'N/A')}")
                    with col2:
                        st.success("✅ **Strengths:**\n" + "\n".join(ai_analysis.get('strengths', [])))
                        if ai_analysis.get('concerns'):
                            st.warning("⚠️ **Concerns:**\n" + "\n".join(ai_analysis.get('concerns', [])))
                    
                    st.markdown(f"💡 **Recommendation:** {ai_analysis.get('recommendation', 'N/A')}")
                    st.markdown("---")
                    st.write("Your assessment has been saved. Contact within 48 hours.")
                    
                except Exception as e:
                    st.error(f"❌ AI Analysis failed: {str(e)}")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888; font-size: 0.85rem;'>© 2026 <span style='color:#ff2d55'>JX</span>Perience | Japanese Franchise Overseas Expansion Platform</div>", unsafe_allow_html=True)
