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
        letter-spacing: -0.5px;
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
    <div class="main-header"><span class="brand-accent">JX</span>Perience</div>
    <div class="sub-header">Japanese Franchise Overseas Expansion Platform</div>
    <div class="tagline">Connecting Japanese brands with serious global investors</div>
    <div style="margin-bottom: 1rem;"></div>
""", unsafe_allow_html=True)

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv("C:\\jfa_scraper\\franchise_data.csv")
    return df

df = load_data()

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

# HARDCODE YOUR API KEY HERE
GROQ_API_KEY = "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"

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

# Display table with clickable links using HTML
def render_clickable_table(df):
    # Create HTML table with clickable links
    html = """
    <div style="overflow-x: auto;">
    <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">
        <thead>
            <tr style="background-color: #f8f9fa; border-bottom: 2px solid #dee2e6;">
                <th style="padding: 12px; text-align: left;">Brand</th>
                <th style="padding: 12px; text-align: left;">Category</th>
                <th style="padding: 12px; text-align: center;">Japan Stores</th>
                <th style="padding: 12px; text-align: center;">Overseas</th>
                <th style="padding: 12px; text-align: center;">Investment</th>
                <th style="padding: 12px; text-align: center;">Fee</th>
                <th style="padding: 12px; text-align: center;">Royalty</th>
                <th style="padding: 12px; text-align: left;">Target Markets</th>
                <th style="padding: 12px; text-align: center;">Website</th>
                <th style="padding: 12px; text-align: center;">Status</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for idx, row in df.iterrows():
        website = row['website'] if pd.notna(row['website']) else ''
        if website and not website.startswith('http'):
            website_url = f"https://{website}"
        else:
            website_url = website
        
        html += f"""
            <tr style="border-bottom: 1px solid #eee;">
                <td style="padding: 10px;"><strong>{row['brand_name']}</strong></td>
                <td style="padding: 10px;">{row['category']}</td>
                <td style="padding: 10px; text-align: center;">{row['stores_japan']}</td>
                <td style="padding: 10px; text-align: center;">{row['stores_overseas']}</td>
                <td style="padding: 10px; text-align: center;">{row['investment_usd']}</td>
                <td style="padding: 10px; text-align: center;">${row['franchise_fee_usd']:,.0f}</td>
                <td style="padding: 10px; text-align: center;">{row['royalty_pct']}%</td>
                <td style="padding: 10px;">{row['target_markets']}</td>
                <td style="padding: 10px; text-align: center;"><a href="{website_url}" target="_blank" class="clickable-link">🔗 Visit</a></td>
                <td style="padding: 10px; text-align: center;">{row['franchise_status']}</td>
            </tr>
        """
    
    html += """
        </tbody>
    </table>
    </div>
    """
    return html

st.markdown(render_clickable_table(filtered_df), unsafe_allow_html=True)

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
        if not name or not email:
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
                            st.warning("️ **Concerns:**\n" + "\n".join(ai_analysis.get('concerns', [])))
                    
                    st.markdown(f"💡 **Recommendation:** {ai_analysis.get('recommendation', 'N/A')}")
                    st.markdown("---")
                    st.write("Your assessment has been saved. A franchise consultant will contact you within 48 hours.")
                    
                except Exception as e:
                    st.error(f" AI Analysis failed: {str(e)}")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888; font-size: 0.85rem;'>© 2026 <span style='color:#ff2d55'>JX</span>Perience | Japanese Franchise Overseas Expansion Platform</div>", unsafe_allow_html=True)