import streamlit as st
import pandas as pd
from openai import OpenAI
import json
import os

# --- CONFIGURATION ---
# SECURE API KEY - reads from Streamlit Secrets (for cloud) or environment
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

# CSV path - works for both local and Streamlit Cloud
if os.path.exists("C:\\jfa_scraper\\franchise_data.csv"):
    CSV_PATH = "C:\\jfa_scraper\\franchise_data.csv"
else:
    CSV_PATH = "franchise_data.csv"

st.set_page_config(page_title="JXPerience | Franchisor Onboarding", layout="wide")

# Custom styling for JXPerience brand
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
    </style>
""", unsafe_allow_html=True)

# Navigation buttons at top
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("⬅️ Back to Main"):
        st.switch_page("app.py")
with col2:
    st.markdown('<div class="main-header"><span class="brand-accent">JX</span>Perience</div>', unsafe_allow_html=True)

st.markdown('<div class="sub-header">Franchisor Onboarding Portal</div>', unsafe_allow_html=True)
st.markdown("Paste your Japanese brochure text below. Our AI will translate and structure it for global investors.")

# Check if API key exists
if not GROQ_API_KEY:
    st.error("⚠️ API Key not configured. Please add GROQ_API_KEY to your Streamlit secrets.")
    st.stop()

# Initialize AI Client
client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")

# --- FORM ---
with st.form("onboarding_form"):
    st.subheader("1. Brand Information")
    brand_name_input = st.text_input("Brand Name (Romaji or English)", placeholder="e.g., Ippudo")
    raw_text = st.text_area(
        "Paste Japanese Brochure/Website Text", 
        height=200, 
        placeholder="Paste the Japanese text describing your franchise, investment requirements, and history here...",
        help="The AI will extract investment amounts, store counts, and translate the description."
    )
    
    submitted = st.form_submit_button("✨ Generate English Investment Teaser")

    if submitted:
        if not brand_name_input or not raw_text:
            st.error("Please provide both a brand name and the raw text.")
        else:
            with st.spinner("🤖 AI is translating and analyzing..."):
                try:
                    prompt = f"""You are an expert franchise data analyst and translator. 
                    Read the following text about a Japanese franchise brand. 
                    Extract the key data points and translate them into professional English.
                    If specific numbers (like investment cost) are not in the text, estimate them based on typical industry standards for this brand, but mark them as 'Estimated'.
                    
                    Return ONLY a valid JSON object with these exact keys (no markdown, just raw JSON):
                    {{
                        "brand_name": "{brand_name_input}",
                        "category": "String (e.g. Ramen, Sushi, Cafe)",
                        "stores_japan": "String (e.g. 100+)",
                        "stores_overseas": "String (e.g. 20+)",
                        "investment_usd": "String (e.g. 150k-300k)",
                        "franchise_fee_usd": "String (e.g. 50000)",
                        "royalty_pct": "String (e.g. 5.0)",
                        "target_markets": "String (e.g. SE Asia, USA)",
                        "website": "String (e.g. brand.com)",
                        "overseas_franchise_confirmed": "String (YES, PROBABLE, or NEEDS_VERIFICATION)",
                        "expansion_type": "String (Single-unit or Master Franchise)",
                        "notes": "String (Brief 1-sentence English summary of the brand's unique selling point)"
                    }}

                    TEXT TO ANALYZE:
                    {raw_text}
                    """

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.3,
                        response_format={"type": "json_object"}
                    )
                    
                    # Store the generated data in session state for the next step
                    st.session_state['generated_data'] = json.loads(response.choices[0].message.content)
                    st.session_state['ready_to_save'] = True

                except Exception as e:
                    st.error(f"AI Error: {e}")

# --- REVIEW AND SAVE ---
if st.session_state.get('ready_to_save'):
    st.markdown("---")
    st.subheader("2. Review & Edit Data")
    st.info("Please review the AI-generated data below. You can edit any field before saving to the database.")
    
    data = st.session_state['generated_data']
    
    # Create editable fields for the user
    col1, col2 = st.columns(2)
    with col1:
        data['category'] = st.text_input("Category", data.get('category', ''))
        data['stores_japan'] = st.text_input("Stores in Japan", data.get('stores_japan', ''))
        data['stores_overseas'] = st.text_input("Stores Overseas", data.get('stores_overseas', ''))
        data['investment_usd'] = st.text_input("Investment (USD)", data.get('investment_usd', ''))
        data['franchise_fee_usd'] = st.text_input("Franchise Fee (USD)", data.get('franchise_fee_usd', ''))
        data['royalty_pct'] = st.text_input("Royalty (%)", data.get('royalty_pct', ''))
    
    with col2:
        data['target_markets'] = st.text_input("Target Markets", data.get('target_markets', ''))
        data['website'] = st.text_input("Website", data.get('website', ''))
        
        # Safe dropdown for overseas_confirmed
        overseas_options = ["YES", "PROBABLE", "NEEDS_VERIFICATION", "NO"]
        current_overseas = data.get('overseas_franchise_confirmed', 'NEEDS_VERIFICATION').upper().strip()
        if current_overseas not in overseas_options:
            current_overseas = 'NEEDS_VERIFICATION'
        data['overseas_franchise_confirmed'] = st.selectbox("Overseas Confirmed?", overseas_options, index=overseas_options.index(current_overseas))
        
        # Safe dropdown for expansion_type
        expansion_options = ["Single-unit", "Master Franchise", "Joint Venture"]
        current_expansion = data.get('expansion_type', 'Single-unit').strip()
        
        # Clean up the value to match exactly
        if 'Single' in current_expansion:
            current_expansion = 'Single-unit'
        elif 'Master' in current_expansion:
            current_expansion = 'Master Franchise'
        elif 'Joint' in current_expansion:
            current_expansion = 'Joint Venture'
        else:
            current_expansion = 'Single-unit'
        
        data['expansion_type'] = st.selectbox("Expansion Type", expansion_options, index=expansion_options.index(current_expansion))
        data['notes'] = st.text_area("Notes / Summary", data.get('notes', ''))

    if st.button("✅ Confirm & Add to Database", type="primary"):
        try:
            # Create a DataFrame from the edited data
            new_row = pd.DataFrame([data])
            
            # Append to CSV
            # Check if file exists to handle headers correctly
            file_exists = os.path.isfile(CSV_PATH)
            new_row.to_csv(CSV_PATH, mode='a', header=not file_exists, index=False, encoding='utf-8')
            
            st.success("✅ Success! Brand added to the database.")
            st.balloons()
            
            # Clear session state
            st.session_state['ready_to_save'] = False
            st.session_state['generated_data'] = None
            
            st.info("Go to the main 'JXPerience' page to see your new brand in the list!")
            
        except Exception as e:
            st.error(f"Error saving to database: {e}")

# Footer branding
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888; font-size: 0.85rem;'>© 2026 <span style='color:#ff2d55'>JX</span>Perience | Japanese Franchise Overseas Expansion Platform</div>", unsafe_allow_html=True)
