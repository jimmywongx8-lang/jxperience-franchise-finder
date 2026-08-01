import streamlit as st
import pandas as pd
from openai import OpenAI
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import os

# App Title - JXPerience Branding
st.set_page_config(
    page_title="JXPerience | Japanese Franchise Expansion Platform", 
    page_icon="🔴",
    layout="wide"
)

# Custom styling - Blue Theme
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f1f1f;
    }
    .brand-accent {
        color: #0066cc;
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
    .disclaimer-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 12px 16px;
        margin: 20px 0;
        font-size: 0.9rem;
        color: #856404;
    }
    .stat-card {
        background: linear-gradient(135deg, #0066cc 0%, #0052a3 100%);
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
    .email-capture-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 16px;
        padding: 30px;
        margin: 20px 0;
        border: 2px solid #dee2e6;
    }
    .inquiry-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 16px;
        padding: 30px;
        margin: 20px 0;
        border: 2px solid #0066cc;
    }
    .view-btn {
        background-color: #0066cc;
        color: white;
        padding: 6px 12px;
        border-radius: 6px;
        text-decoration: none;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    .view-btn:hover {
        background-color: #0052a3;
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

# Helper Functions
def get_confidence_badge(confidence):
    if confidence == "YES":
        return "✅ Confirmed"
    elif confidence == "PROBABLE":
        return " Probable"
    elif confidence == "NEEDS_VERIFICATION":
        return "⚠️ Verify"
    else:
        return "❌ No"

# Pre-process dataframe
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
st.sidebar.markdown("### <span style='color:#0066cc'>JX</span>Perience", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Search
st.sidebar.markdown("#### 🔍 Search")
search_term = st.sidebar.text_input("", placeholder="Type brand name...")
st.sidebar.markdown("---")

# Display Mode
st.sidebar.markdown("#### 💎 Discovery Mode")
display_mode = st.sidebar.radio(
    "Show:",
    ["💎 Hidden Gems (<50 overseas)", "📋 All Brands (A-Z)", "✅ Verified Only"],
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
    st.subheader(f"💎 Found {len(filtered_df)} Hidden Gem Brands")
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

# --- DISPLAY TABLE WITH PROFILE LINKS (HTML) ---
html_table = """
<div style="overflow-x: auto;">
<table style="width: 100%; border-collapse: collapse; font-size: 0.9rem; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
    <thead>
        <tr style="background-color: #f8f9fa; border-bottom: 2px solid #dee2e6;">
            <th style="padding: 12px 8px; text-align: left; font-weight: 600; color: #495057;">Brand</th>
            <th style="padding: 12px 8px; text-align: left; font-weight: 600; color: #495057;">Category</th>
            <th style="padding: 12px 8px; text-align: center; font-weight: 600; color: #495057;">Japan Stores</th>
            <th style="padding: 12px 8px; text-align: center; font-weight: 600; color: #495057;">Overseas</th>
            <th style="padding: 12px 8px; text-align: center; font-weight: 600; color: #495057;">Investment</th>
            <th style="padding: 12px 8px; text-align: center; font-weight: 600; color: #495057;">Fee</th>
            <th style="padding: 12px 8px; text-align: center; font-weight: 600; color: #495057;">Royalty %</th>
            <th style="padding: 12px 8px; text-align: left; font-weight: 600; color: #495057;">Target Markets</th>
            <th style="padding: 12px 8px; text-align: center; font-weight: 600; color: #495057;">Website</th>
            <th style="padding: 12px 8px; text-align: center; font-weight: 600; color: #495057;">Status</th>
        </tr>
    </thead>
    <tbody>
"""

for idx, row in filtered_df.iterrows():
    brand_name = row['brand_name']
    brand_url = f"/Brand_Profile?brand={brand_name.replace(' ', '%20')}"
    
    # Format values
    franchise_fee = f"${int(row['franchise_fee_usd']):,}" if pd.notna(row['franchise_fee_usd']) else 'N/A'
    royalty = f"{row['royalty_pct']}%" if pd.notna(row['royalty_pct']) else 'N/A'
    
    # Create clickable website link
    website = row['website'] if pd.notna(row['website']) else ''
    website_link = f'<a href="https://{website}" target="_blank" style="color:#0066cc;text-decoration:none;">🔗 Visit</a>' if website and str(website) != 'nan' else 'N/A'
    
    html_table += f"""
        <tr style="border-bottom: 1px solid #eee;">
            <td style="padding: 10px 8px;">
                <a href="{brand_url}" class="view-btn">🔍 View {brand_name}</a>
            </td>
            <td style="padding: 10px 8px;">{row['category']}</td>
            <td style="padding: 10px 8px; text-align: center;">{row['stores_japan']}</td>
            <td style="padding: 10px 8px; text-align: center;">{row['stores_overseas']}</td>
            <td style="padding: 10px 8px; text-align: center;">{row['investment_usd']}</td>
            <td style="padding: 10px 8px; text-align: center;">{franchise_fee}</td>
            <td style="padding: 10px 8px; text-align: center;">{royalty}</td>
            <td style="padding: 10px 8px;">{row['target_markets']}</td>
            <td style="padding: 10px 8px; text-align: center;">{website_link}</td>
            <td style="padding: 10px 8px; text-align: center;">{row['franchise_status']}</td>
        </tr>
    """

html_table += """
    </tbody>
</table>
</div>
"""

st.markdown(html_table, unsafe_allow_html=True)

# --- INVESTOR EMAIL CAPTURE (General) ---
st.markdown("---")
st.markdown("""
    <div class="email-capture-box">
        <h3 style="margin-top:0;">📬 Get Early Access to New Brands</h3>
        <p style="margin-bottom:20px;">Don't see what you're looking for? Get notified when we add new brands.</p>
    </div>
""", unsafe_allow_html=True)

with st.form("notification_signup"):
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        investor_email = st.text_input("Your Email", placeholder="investor@example.com")
    with col2:
        investor_category = st.selectbox("Interested Category", ["All Categories"] + list(df['category'].unique()))
    with col3:
        submit_notification = st.form_submit_button("🔔 Notify Me", use_container_width=True)
    
    if submit_notification:
        if not investor_email:
            st.error("Please enter your email")
        else:
            st.success("✅ You're on the list!")

# --- AI ASSESSMENT FORM ---
st.markdown("---")
st.subheader("Interested in a brand?")
st.write("Fill out this form for an **AI-qualified assessment** of your fit.")

# Initialize session state
if 'show_inquiry_form' not in st.session_state:
    st.session_state['show_inquiry_form'] = False
if 'selected_brand_for_inquiry' not in st.session_state:
    st.session_state['selected_brand_for_inquiry'] = ""
if 'last_ai_analysis' not in st.session_state:
    st.session_state['last_ai_analysis'] = None
if 'last_investor_data' not in st.session_state:
    st.session_state['last_investor_data'] = {}

# Pre-select brand if coming from profile page
default_brand = st.session_state.get('selected_brand', filtered_df['brand_name'].iloc[0] if not filtered_df.empty else "")

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
    
    selected_brand = st.selectbox("Which brand interests you?", filtered_df['brand_name'].tolist(), 
                                  index=filtered_df['brand_name'].tolist().index(default_brand) if default_brand in filtered_df['brand_name'].tolist() else 0)
    message = st.text_area("Additional Info (optional)", placeholder="Your background, location plans, etc.")
    
    submitted = st.form_submit_button(" Get AI Assessment")
    
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
                    
                    # Store data for inquiry form
                    st.session_state['show_inquiry_form'] = True
                    st.session_state['selected_brand_for_inquiry'] = selected_brand
                    st.session_state['last_ai_analysis'] = ai_analysis
                    st.session_state['last_investor_data'] = {
                        'name': name, 'email': email, 'country': country, 
                        'capital': capital, 'experience': experience
                    }
                    
                except Exception as e:
                    st.error(f"❌ AI Analysis failed: {str(e)}")

# --- LEAD CAPTURE / INQUIRY FORM ---
if st.session_state.get('show_inquiry_form') and st.session_state.get('last_ai_analysis'):
    st.markdown("---")
    brand_name = st.session_state['selected_brand_for_inquiry']
    ai_score = st.session_state['last_ai_analysis'].get('readiness_score', 'Good')
    
    st.markdown(f"""
        <div class="inquiry-box">
            <h3 style="margin-top:0; color:#0066cc;">🚀 Ready to contact {brand_name}?</h3>
            <p>
                You have a <strong>{ai_score}</strong> fit. 
                The next step is to connect with the franchisor. 
                <br><br>
                <strong>Get the Official Investment Prospectus & Contact Details</strong><br>
                Fill out the form below to receive the full brochure and introduction package directly in your inbox.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("inquiry_form"):
        col1, col2 = st.columns(2)
        with col1:
            prev_data = st.session_state.get('last_investor_data', {})
            inquiry_name = st.text_input("Full Name", value=prev_data.get('name', ""))
            inquiry_email = st.text_input("Business Email", value=prev_data.get('email', ""))
        with col2:
            inquiry_company = st.text_input("Company Name (Optional)")
            inquiry_phone = st.text_input("Phone Number (Optional)")
        
        inquiry_msg = st.text_area(
            "Message to Franchisor", 
            placeholder=f"Hi, I am interested in opening a {brand_name} franchise in {prev_data.get('country', 'my region')}. My available capital is {prev_data.get('capital', 'competitive')}.",
            height=100
        )
        
        submit_inquiry = st.form_submit_button("📤 Send Inquiry & Get Prospectus", type="primary", use_container_width=True)
        
        if submit_inquiry:
            if not inquiry_email:
                st.error("Please enter your email to receive the prospectus.")
            else:
                try:
                    admin_email = st.secrets.get("YOUR_GMAIL", "jxperience.info@gmail.com")
                    app_password = st.secrets.get("YOUR_APP_PASSWORD", "")
                    
                    if app_password and len(app_password) > 10:
                        msg = MIMEMultipart()
                        msg['From'] = admin_email
                        msg['To'] = admin_email
                        msg['Subject'] = f"🔥 NEW LEAD: {inquiry_name} interested in {brand_name}"
                        
                        body = f"""
New Franchise Inquiry Received!
===============================

Brand Interested In: {brand_name}

--- Investor Details ---
Name: {inquiry_name}
Email: {inquiry_email}
Company: {inquiry_company}
Phone: {inquiry_phone}

--- Message ---
{inquiry_msg}

--- AI Assessment Context ---
Score: {ai_score}
Capital: {prev_data.get('capital', 'N/A')}
Country: {prev_data.get('country', 'N/A')}
Experience: {prev_data.get('experience', 'N/A')}

--- Submitted via JXPerience Platform ---
"""
                        msg.attach(MIMEText(body, 'plain'))
                        
                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                        server.login(admin_email, app_password)
                        server.send_message(msg)
                        server.quit()
                        
                        # Optional: Log to Google Sheet
                        webhook_url = st.secrets.get("SHEET_WEBHOOK_URL", "")
                        if webhook_url and len(webhook_url) > 20:
                            try:
                                payload = {
                                    "timestamp": str(pd.Timestamp.now()),
                                    "brand": brand_name,
                                    "name": inquiry_name,
                                    "email": inquiry_email,
                                    "company": inquiry_company,
                                    "phone": inquiry_phone,
                                    "message": inquiry_msg,
                                    "ai_score": ai_score,
                                    "capital": prev_data.get('capital', 'N/A'),
                                    "country": prev_data.get('country', 'N/A')
                                }
                                requests.post(webhook_url, json=payload, timeout=5)
                            except:
                                pass

                        st.success("""
                            ✅ **Inquiry Sent Successfully!**
                            
                            We have received your details. 
                            You will receive the **Official Investment Prospectus** at your email shortly.
                            
                            *A JXPerience consultant will reach out within 24 hours.*
                        """)
                        st.balloons()
                        st.session_state['show_inquiry_form'] = False
                        st.session_state['last_ai_analysis'] = None
                        
                    else:
                        st.success(f"""
                            ✅ **Inquiry Submitted!**
                            
                            Thank you for your interest. We will contact you at {inquiry_email} within 24 hours with the investment prospectus.
                        """)
                        st.session_state['show_inquiry_form'] = False
                        st.session_state['last_ai_analysis'] = None
                    
                except Exception as e:
                    st.error(f"Failed to send inquiry. Please email us directly at jxperience.info@gmail.com")
                    st.session_state['show_inquiry_form'] = False
                    st.session_state['last_ai_analysis'] = None

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888; font-size: 0.85rem;'>© 2026 <span style='color:#0066cc'>JX</span>Perience | Japanese Franchise Overseas Expansion Platform</div>", unsafe_allow_html=True)
