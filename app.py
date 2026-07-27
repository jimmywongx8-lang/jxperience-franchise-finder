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
    st.warning("⚠️ No data loaded.")
    st.stop()

# Add confidence badges
def get_confidence_badge(confidence):
    if confidence == "YES":
        return "✅ Confirmed"
    elif confidence == "PROBABLE":
        return "🟡 Probable"
    elif confidence == "NEEDS_VERIFICATION":
        return "⚠️ Verify"
    else:
        return "❌ No"

df['franchise_status'] = df['overseas_franchise_confirmed'].apply(get_confidence_badge)

# SECURE API KEY
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

if not GROQ_API_KEY:
    st.warning("️ API Key not configured.")

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
st.sidebar.markdown("#### 🔍 Search")
search_term = st.sidebar.text_input("", placeholder="Type brand name...")
st.sidebar.markdown("---")

st.sidebar.markdown("####  Display Mode")
display_mode = st.sidebar.radio(
    "Show:",
    ["🌟 Hidden Gems First", " All Brands (A-Z)", "✅ Verified Only"],
    help="Hidden Gems: Brands with <50 overseas stores"
)

st.sidebar.markdown("---")
st.sidebar.header("Filter by Category")

selected_category = st.sidebar.multiselect(
    "Select categories:", 
    options=df['category'].unique(), 
    default=df['category'].unique()
)

# --- FILTERING LOGIC ---
filtered_df = df[df['category'].isin(selected_category)]

# Apply display mode sorting
if "Hidden Gems" in display_mode:
    filtered_df = filtered_df.copy()
    filtered_df['overseas_numeric'] = pd.to_numeric(filtered_df['stores_overseas'].str.extract('(\d+)')[0], errors='coerce').fillna(999)
    filtered_df = filtered_df.sort_values(['overseas_numeric', 'brand_name'])
    filtered_df = filtered_df.drop(columns=['overseas_numeric'])
elif "Verified Only" in display_mode:
    filtered_df = filtered_df[filtered_df['overseas_franchise_confirmed'] == 'YES']
    filtered_df = filtered_df.sort_values('brand_name')
else:
    filtered_df = filtered_df.sort_values('brand_name')

if search_term:
    filtered_df = filtered_df[filtered_df['brand_name'].str.contains(search_term, case=False, na=False)]

# --- DISPLAY COUNT ---
st.subheader(f"Found {len(filtered_df)} Expansion-Ready Brands")

# --- DISCLAIMER ---
st.markdown("""
    <div class="disclaimer-box">
        <strong>ℹ️ Disclaimer:</strong> All information sourced from public data. 
        "✅ Confirmed" brands have verified overseas programs. JXPerience is not officially affiliated 
        with listed brands unless marked "Verified Partner." Verify all details directly before investing.
    </div>
""", unsafe_allow_html=True)

# --- PREPARE DATA FOR DISPLAY ---
display_df = filtered_df.copy()

# Create clickable URLs using markdown
display_df['Website'] = display_df['website'].apply(
    lambda x: f"[🔗 Visit](https://{x if not pd.isna(x) else ''})" if pd.notna(x) and x != '' else 'N/A'
)

# Format numbers
display_df['Franchise Fee'] = display_df['franchise_fee_usd'].apply(
    lambda x: f"${int(x):,}" if pd.notna(x) else 'N/A'
)
display_df['Royalty %'] = display_df['royalty_pct'].apply(
    lambda x: f"{x}%" if pd.notna(x) else 'N/A'
)

# Select and rename columns for display
display_df = display_df.rename(columns={
    'brand_name': 'Brand',
    'category': 'Category',
    'stores_japan': 'Japan Stores',
    'stores_overseas': 'Overseas',
    'investment_usd': 'Investment',
    'target_markets': 'Target Markets',
    'franchise_status': 'Status'
})

# Show dataframe with built-in sorting (Streamlit handles this automatically)
st.dataframe(
    display_df[['Brand', 'Category', 'Japan Stores', 'Overseas', 'Investment', 'Franchise Fee', 'Royalty %', 'Target Markets', 'Website', 'Status']],
    use_container_width=True,
    hide_index=True
)

# --- INVESTOR EMAIL CAPTURE ---
st.markdown("---")
st.subheader("📬 Get Notified About New Brands")
st.write("Don't see what you're looking for? Get notified when we add new brands.")

with st.form("notification_signup"):
    col1, col2 = st.columns(2)
    with col1:
        investor_email = st.text_input("Your Email", placeholder="investor@example.com")
    with col2:
        investor_category = st.selectbox("Interested Category", ["All Categories"] + list(df['category'].unique()))
    
    submit_notification = st.form_submit_button(" Notify Me")
    
    if submit_notification:
        if not investor_email:
            st.error("Please enter your email")
        else:
            st.success(f"✅ Thanks! We'll notify you about new {investor_category.lower()} brands.")

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
st.markdown("<div style='text-align: center; color: #888; font-size: 0.85rem;'>© 2026 <span style='color:#ff2d55'>JX</span>Perience</div>", unsafe_allow_html=True)
