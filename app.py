import streamlit as st
import pandas as pd
from openai import OpenAI
import json

# App Title - JXPerience Branding
st.set_page_config(
    page_title="JXPerience | JP Franchise Finder", 
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
    .clickable-link:hover {
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header"><span class="brand-accent">JX</span>Perience</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Japanese Franchise Overseas Expansion Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Connecting Japanese brands with serious global investors</div>', unsafe_allow_html=True)
st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

# Load the data - works for both local and cloud
@st.cache_data
def load_data():
    # Try multiple paths for local vs cloud deployment
    paths_to_try = [
        "C:\\jfa_scraper\\franchise_data.csv",  # Local Windows
        "franchise_data.csv",  # Streamlit Cloud root
        "/mount/src/jxperience-franchise-finder/franchise_data.csv"  # Alternative cloud path
    ]
    
    for path in paths_to_try:
        try:
            df = pd.read_csv(path)
            return df
        except FileNotFoundError:
            continue
    
    # If all paths fail, return empty DataFrame
    st.error("⚠️ CSV file not found. Please ensure franchise_data.csv is uploaded to GitHub.")
    return pd.DataFrame()

df = load_data()

# Check if we have data
if df.empty:
    st.warning("⚠️ No data loaded. Please ensure franchise_data.csv exists in your repository.")
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

# SECURE API KEY - reads from Streamlit Secrets (for cloud) or environment
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

# Check if API key exists
if not GROQ_API_KEY:
    st.warning("⚠️ API Key not configured. Please add GROQ_API_KEY to your Streamlit secrets.")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# Sidebar
st.sidebar.markdown("### <span style='color:#ff2d55'>JX</span>Perience", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown("#### 🔍 Search")
search_term = st.sidebar.text_input("", placeholder="Type brand name...")
st.sidebar.markdown("---")
st.sidebar.header("Filter by Category")

selected_category = st.sidebar.multiselect(
    "Select categories:", 
    options=df['category'].unique(), 
    default=df['category'].unique()
)

# Filter
filtered_df = df[df['category'].isin(selected_category)]
if search_term:
    filtered_df = filtered_df[filtered_df['brand_name'].str.contains(search_term, case=False, na=False)]

# Display count
st.subheader(f"Found {len(filtered_df)} Expansion-Ready Brands")

# Display table with clickable links
def make_clickable_url(url):
    if pd.isna(url) or url == '':
        return 'N/A'
    if not url.startswith('http'):
        url = f'https://{url}'
    return f'<a href="{url}" target="_blank" class="clickable-link">🔗 Visit</a>'

# Create a copy for display
display_df = filtered_df.copy()

# Add clickable URLs
display_df['website'] = display_df['website'].apply(make_clickable_url)

# Rename columns for better display
display_df = display_df.rename(columns={
    'brand_name': 'Brand',
    'category': 'Category',
    'stores_japan': 'Japan Stores',
    'stores_overseas': 'Overseas',
    'investment_usd': 'Investment',
    'franchise_fee_usd': 'Franchise Fee',
    'royalty_pct': 'Royalty %',
    'target_markets': 'Target Markets',
    'website': 'Website',
    'franchise_status': 'Status'
})

# Display as HTML table
st.markdown(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)

# Smart Contact Form with AI Scoring
st.markdown("---")
st.subheader("Interested in a brand?")
st.write("Fill out this form for an **AI-qualified assessment** of your fit.")

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
    message = st.text_area("Additional Information (optional)", 
                          placeholder="Tell us about your background, location plans, etc.")
    
    submitted = st.form_submit_button("🚀 Get AI Assessment")
    
    if submitted:
        if not GROQ_API_KEY:
            st.error("⚠️ API Key is not configured. Please contact the administrator.")
        elif not name or not email:
            st.error("⚠️ Please fill in your name and email")
        else:
            brand_info = filtered_df[filtered_df['brand_name'] == selected_brand].iloc[0]
            
            with st.spinner("🤖 AI is analyzing your profile..."):
                try:
                    prompt = f"""You are a franchise investment analyst. Evaluate this investor's fit for a Japanese franchise opportunity.

INVESTOR PROFILE:
- Name: {name}
- Country: {country}
- Available Capital: {capital}
- F&B Experience: {experience}
- Timeline: {timeline}
- Additional Info: {message if message else "None provided"}

FRANCHISE OPPORTUNITY:
- Brand: {brand_info['brand_name']}
- Category: {brand_info['category']}
- Stores in Japan: {brand_info['stores_japan']}
- Overseas Stores: {brand_info['stores_overseas']}
- Investment Required: {brand_info['investment_usd']}
- Franchise Fee: {brand_info['franchise_fee_usd']} USD
- Royalty: {brand_info['royalty_pct']}%
- Target Markets: {brand_info['target_markets']}
- Expansion Status: {brand_info['franchise_status']}

Provide your assessment in this JSON format:
{{
    "readiness_score": "High/Medium/Low",
    "score_reasoning": "2-3 sentences explaining the score",
    "capital_fit": "Yes/No - explain if their capital matches the investment requirement",
    "market_fit": "Yes/No - explain if their country is in the target markets",
    "strengths": ["list", "of", "strengths"],
    "concerns": ["list", "of", "concerns"],
    "recommendation": "One sentence recommendation"
}}

Be honest and direct. If they're not a good fit, say so."""

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
                    st.write("Your assessment has been saved. A franchise consultant will contact you within 48 hours.")
                    
                except Exception as e:
                    st.error(f"❌ AI Analysis failed: {str(e)}")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888; font-size: 0.85rem;'>© 2026 <span style='color:#ff2d55'>JX</span>Perience | Japanese Franchise Overseas Expansion Platform</div>", unsafe_allow_html=True)
