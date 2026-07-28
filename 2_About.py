import streamlit as st

st.set_page_config(
    page_title="About | JXPerience",
    page_icon="🔴"
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
    .beta-badge {
        background-color: #fff3cd;
        color: #856404;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-left: 10px;
    }
    .mission-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        padding: 25px;
        margin: 20px 0;
        border-left: 4px solid #ff2d55;
    }
    .stat-highlight {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ff2d55;
    }
    .feedback-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 16px;
        padding: 30px;
        margin: 30px 0;
    }
    .feedback-box h3 {
        color: white;
        margin-top: 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header"><span class="brand-accent">JX</span>Perience<span class="beta-badge">🚀 BETA</span></div>', unsafe_allow_html=True)
st.markdown("### About JXPerience")
st.markdown("---")

# Mission Statement
st.markdown("""
    <div class="mission-box">
        <h3 style="margin-top: 0;">📊 Our Mission</h3>
        <p style="font-size: 1.05rem; line-height: 1.6;">
            We're building the definitive platform connecting <strong>Japanese franchise brands</strong> with 
            <strong>serious global investors</strong>. Our goal is to democratize access to Japan's thriving 
            F&B ecosystem and help brands expand internationally.
        </p>
    </div>
""", unsafe_allow_html=True)

# Why We Started This
st.markdown("### 🔴 Why JXPerience?")
st.markdown("""
**The Problem:**
- Japanese franchises have incredible global potential but limited overseas presence
- International investors struggle to find reliable information about Japanese franchise opportunities
- The research process is fragmented, time-consuming, and often requires Japanese language skills

**Our Solution:**
JXPerience aggregates, translates, and analyzes franchise data from 63+ Japanese brands, making it 
accessible to global investors through:
- ✅ **AI-powered qualification** - Get instant assessment of your investment readiness
- ✅ **Comprehensive data** - Investment ranges, fees, target markets, and expansion status
- ✅ **Hidden gems** - Discover lesser-known brands with high growth potential
- ✅ **Zero friction** - Free access to curated franchise information

**The Impact:**
According to <a href="https://www.jetro.go.jp" target="_blank">JETRO</a>, Japanese F&B franchises have grown 
<strong>8x in less than two decades</strong>, yet most remain concentrated in Japan. We're changing that 
by making international expansion accessible and data-driven.
""", unsafe_allow_html=True)

st.markdown("---")

# Beta Status & Co-Creation
st.markdown("""
    <div class="feedback-box">
        <h3>🚀 We're in BETA - Help Us Co-Create!</h3>
        <p style="font-size: 1.05rem; margin-bottom: 20px;">
            JXPerience is currently in <strong>beta</strong>, which means we're actively building and improving 
            the platform with feedback from users like you.
        </p>
        <p style="margin-bottom: 20px;">
            <strong>We invite you to co-create this platform with us:</strong>
        </p>
        <ul style="line-height: 1.8;">
            <li>💡 <strong>Share your feedback</strong> - What features do you need?</li>
            <li>🎯 <strong>Tell us what's missing</strong> - Which brands should we add?</li>
            <li> <strong>Report issues</strong> - Found a bug or data error?</li>
            <li>🌟 <strong>Suggest improvements</strong> - How can we serve you better?</li>
        </ul>
        <p style="margin-top: 20px; margin-bottom: 0;">
            Your input directly shapes the future of JXPerience. 
            <strong>Let's build this together!</strong>
        </p>
    </div>
""", unsafe_allow_html=True)

# Feedback Form
st.markdown("### 💬 Share Your Feedback")
st.write("Help us improve JXPerience. All feedback is reviewed personally by our team.")

with st.form("feedback_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        feedback_name = st.text_input("Your Name (optional)", placeholder="John Doe")
        feedback_email = st.text_input("Your Email (optional)", placeholder="john@example.com")
    
    with col2:
        feedback_type = st.selectbox(
            "Feedback Type",
            ["Feature Request", "Bug Report", "Data Correction", "General Suggestion", "Partnership Inquiry"]
        )
    
    feedback_message = st.text_area(
        "Your Feedback",
        placeholder="Tell us what you think about JXPerience, what features you'd like to see, or any issues you've encountered...",
        height=150
    )
    
    submit_feedback = st.form_submit_button("📤 Submit Feedback", use_container_width=True)
    
    if submit_feedback:
        if not feedback_message:
            st.error("Please enter your feedback message")
        else:
            # In production, save to database/Google Sheets/email
            st.success("""
                ✅ **Thank you for your feedback!**
                
                We've received your input and will review it personally. 
                If you provided an email, we'll follow up with you directly.
                
                Your contribution helps make JXPerience better for everyone. 🙏
            """)
            st.info("💡 Tip: Bookmark this page to check back for updates based on community feedback!")

st.markdown("---")

# Contact & Connect
st.markdown("### 📬 Stay Connected")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        **📧 Email Us**  
        [hello@jxperience.com](mailto:hello@jxperience.com)  
        For partnership inquiries
    """)

with col2:
    st.markdown("""
        **💬 Join the Community**  
        [Join our mailing list](#)  
        Get updates on new features
    """)

with col3:
    st.markdown("""
        ** Follow Us**  
        [@JXPerience](#)  
        Latest updates & insights
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #888; font-size: 0.85rem; margin-top: 40px;">
        <p><strong>JXPerience</strong> - Japanese Franchise Overseas Expansion Platform</p>
        <p>© 2026 JXPerience. Building the future of F&B expansion, one brand at a time.</p>
        <p><em>"Connecting Japanese brands with serious global investors"</em></p>
    </div>
""", unsafe_allow_html=True)