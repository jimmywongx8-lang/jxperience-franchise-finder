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

# --- TRANSLATIONS (Phase 1: UI Only) ---
TRANSLATIONS = {
    "English": {
        # Sidebar
        "sidebar_title": " JP Hub",
        "nav_header": "Navigation",
        "home": " Home",
        "about": "ℹ️ About Us",
        "franchisor": "🏢 Franchisor",
        "search_header": "🔍 Search & Filter",
        "search_placeholder": "Search brands",
        "filter_category": "Filter by Category",
        "choose_options": "Choose options",
        
        # Hero
        "hero_title": " Discover Japanese Franchise Opportunities",
        "hero_subtitle": "Connecting global investors with 63+ expansion-ready Japanese brands",
        "metric_brands": "Brands",
        "metric_countries": "Countries",
        "metric_investment": "Investment",
        
        # Home page
        "found_brands": "Found 63 Expansion-Ready Brands",
        "showing_brands": "Showing {count} brands",
        "stores": "stores",
        "royalty": "Royalty",
        "view_details": " View Details",
        "enquiry": "Enquiry →",
        
        # Footer
        "footer_text": "© 2026 JXPerience. Connecting Japanese brands with global investors.",
        "footer_contact": "📧 Contact: jxperience.info@gmail.com",
        
        # Details page
        "back_brands": "← Back to Brands",
        "company_history": " Company History",
        "menu_highlights": "🍱 Menu Highlights",
        "investment_overview": "💰 Investment Overview",
        "requirements": "📋 Franchise Requirements",
        "support": "🤝 Support Provided",
        "success_story": "⭐ Success Story",
        "contact_info": "📞 Contact Information",
        "submit_enquiry": "📝 Submit Enquiry",
        "watch_videos": "▶️ Watch Videos",
        
        # Quiz form
        "enquiry_title": "Enquiry: {brand}",
        "back": "← Back",
        "name": "Name",
        "email": "Email",
        "capital": "Capital",
        "experience": "Experience",
        "industry": "Industry",
        "location": "Location",
        "timeline": "Timeline",
        "submit": "Submit Enquiry",
        "success_msg": "✅ Enquiry submitted!",
        "error_msg": "Fill in name and email",
        
        # Capital options
        "cap_under": "Under $100k",
        "cap_100_250": "$100k-$250k",
        "cap_250_500": "$250k-$500k",
        "cap_500_1m": "$500k-$1M",
        "cap_over": "Over $1M",
        
        # Experience options
        "exp_none": "None",
        "exp_1_3": "1-3 years",
        "exp_3_5": "3-5 years",
        "exp_5_plus": "5+ years",
        "exp_owner": "Franchise Owner",
        
        # Industry options
        "ind_fb": "F&B",
        "ind_retail": "Retail",
        "ind_corp": "Corporate",
        "ind_other": "Other",
        
        # Timeline options
        "time_research": "Researching",
        "time_1_2": "1-2 years",
        "time_6_12": "6-12 months",
        "time_asap": "ASAP",
        
        # About page
        "about_title": " About JXPerience",
        "about_caption": "Our Mission & Story",
        "why_started": "Why We Started This",
        "faq_title": "❓ Frequently Asked Questions",
        "ready_explore": "🚀 Ready to Explore?",
        "browse": "Browse Franchises",
        "contact_label": " **Contact:**",
        
        # Franchisor page
        "franchisor_title": "🗾 Franchisor Portal",
        "why_register": "Why Register as a Franchisor?",
        "what_you_get": "✅ What You'll Get as a Verified Partner",
        "access_dashboard": "Access Your Franchise Dashboard",
        "new_to_jx": "New to JXPerience?",
        "password": "Password",
        "login": "Login",
        "wrong_password": "Wrong password",
        "company": "Company",
        "request_access": "Request Access",
        "request_sent": "Request sent! We'll contact you within 24-48 hours.",
        "logged_in": "Logged in",
        "logout": "Logout",
        "leads": "📊 Leads",
        "settings": "⚙️ Settings",
        "found_leads": "✅ Found {count} real leads!",
        "download_csv": " Download CSV",
        "no_leads": "No leads yet",
        "settings_soon": "Settings coming soon",
        
        # Language
        "language": "🌐 Language",
    },
    "日本語": {
        # Sidebar
        "sidebar_title": "🗾 JPハブ",
        "nav_header": "ナビゲーション",
        "home": "🏠 ホーム",
        "about": "ℹ️ 私たちについて",
        "franchisor": "🏢 フランチャイザー",
        "search_header": " 検索とフィルター",
        "search_placeholder": "ブランドを検索",
        "filter_category": "カテゴリでフィルター",
        "choose_options": "オプションを選択",
        
        # Hero
        "hero_title": "🗾 日本のフランチャイズ機会を発見",
        "hero_subtitle": "63以上の展開-readyな日本ブランドとグローバル投資家をつなぐ",
        "metric_brands": "ブランド",
        "metric_countries": "国・地域",
        "metric_investment": "投資額",
        
        # Home page
        "found_brands": "63の展開-readyブランドを発見",
        "showing_brands": "{count}ブランドを表示",
        "stores": "店舗",
        "royalty": "ロイヤリティ",
        "view_details": "📋 詳細を見る",
        "enquiry": "お問い合わせ →",
        
        # Footer
        "footer_text": "© 2026 JXPerience. 日本ブランドとグローバル投資家をつなぐ。",
        "footer_contact": "📧 お問い合わせ: jxperience.info@gmail.com",
        
        # Details page
        "back_brands": "← ブランド一覧に戻る",
        "company_history": " 会社の歴史",
        "menu_highlights": "🍱 メニューの特徴",
        "investment_overview": "💰 投資概要",
        "requirements": "📋 フランチャイズ要件",
        "support": "🤝 サポート内容",
        "success_story": "⭐ 成功事例",
        "contact_info": "📞 お問い合わせ情報",
        "submit_enquiry": "📝 お問い合わせを送信",
        "watch_videos": "▶️ 動画を見る",
        
        # Quiz form
        "enquiry_title": "お問い合わせ: {brand}",
        "back": "← 戻る",
        "name": "お名前",
        "email": "メールアドレス",
        "capital": "資金",
        "experience": "経験",
        "industry": "業界",
        "location": "場所",
        "timeline": "スケジュール",
        "submit": "送信",
        "success_msg": "✅ お問い合わせを送信しました！",
        "error_msg": "名前とメールアドレスを入力してください",
        
        # Capital options
        "cap_under": "$100k未満",
        "cap_100_250": "$100k-$250k",
        "cap_250_500": "$250k-$500k",
        "cap_500_1m": "$500k-$1M",
        "cap_over": "$1M超",
        
        # Experience options
        "exp_none": "なし",
        "exp_1_3": "1-3年",
        "exp_3_5": "3-5年",
        "exp_5_plus": "5年以上",
        "exp_owner": "フランチャイズオーナー",
        
        # Industry options
        "ind_fb": "飲食",
        "ind_retail": "小売",
        "ind_corp": "企業",
        "ind_other": "その他",
        
        # Timeline options
        "time_research": "調査中",
        "time_1_2": "1-2年",
        "time_6_12": "6-12ヶ月",
        "time_asap": " ASAP（できるだけ早く）",
        
        # About page
        "about_title": "🗾 JXPerienceについて",
        "about_caption": "私たちのミッションとストーリー",
        "why_started": "なぜ始めたのか",
        "faq_title": "❓ よくある質問",
        "ready_explore": " 探索する準備はできましたか？",
        "browse": "ブランドを見る",
        "contact_label": "📧 **お問い合わせ:**",
        
        # Franchisor page
        "franchisor_title": " フランチャイザーポータル",
        "why_register": "なぜフランチャイザーとして登録するのか？",
        "what_you_get": "✅ 認定パートナーの特典",
        "access_dashboard": "フランチャイズダッシュボードにアクセス",
        "new_to_jx": "JXPerienceが初めてですか？",
        "password": "パスワード",
        "login": "ログイン",
        "wrong_password": "パスワードが違います",
        "company": "会社名",
        "request_access": "アクセスをリクエスト",
        "request_sent": "リクエストを送信しました！24-48時間以内にご連絡します。",
        "logged_in": "ログインしました",
        "logout": "ログアウト",
        "leads": "📊 リード",
        "settings": "⚙️ 設定",
        "found_leads": "✅ {count}件のリアルリードを発見！",
        "download_csv": "📥 CSVをダウンロード",
        "no_leads": "リードはまだありません",
        "settings_soon": "設定は近日公開",
        
        # Language
        "language": " 言語",
    }
}

# --- SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_franchise' not in st.session_state:
    st.session_state.selected_franchise = None
if 'franchisor_logged_in' not in st.session_state:
    st.session_state.franchisor_logged_in = False
if 'categories' not in st.session_state:
    st.session_state.categories = []
if 'language' not in st.session_state:
    st.session_state.language = 'English'

# --- TRANSLATION HELPER ---
def t(key, **kwargs):
    """Translate a key to the current language"""
    lang = st.session_state.language
    text = TRANSLATIONS.get(lang, TRANSLATIONS["English"]).get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text

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
    .detail-section {
        background: white;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .requirement-box {
        background: #f0f7ff;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
    .success-story {
        background: #f0fdf4;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 4px solid #10b981;
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

# --- FRANCHISES (Content stays in English for Phase 1) ---
FRANCHISES = {
    "Yoshinoya": {
        "story": "World-famous gyudon chain with 1,000+ stores in Japan and 200+ overseas.",
        "investment": "$150k - $300k", "royalty": "5.0%", "sales": "$400k - $800k",
        "overseas_status": "✅ ACTIVELY RECRUITING - USA, Asia, Middle East",
        "youtube_search": "Yoshinoya franchise", "news_search": "Yoshinoya expansion",
        "financials": {"Metric": ["Franchise Fee", "Total Investment", "Royalty", "Store Count"], "Details": ["$30k-$50k", "$150k-$300k", "5%", "1,000+"]},
        "pros": ["Global brand recognition", "Simple menu", "Fast service model"], "cons": ["Beef import regulations", "High competition"],
        "history": "Founded in 1899 in Tokyo's fish market, Yoshinoya is one of Japan's oldest and most iconic fast-food chains. Specializing in gyudon (beef bowls), the company has grown to over 1,200 locations worldwide.",
        "requirements": ["Minimum net worth: $400k USD", "Liquid capital: $150k+ USD", "Restaurant experience preferred", "High-traffic location: 800-1,500 sq ft"],
        "support": ["Initial training (2-4 weeks)", "Site selection assistance", "Store design package", "Supply chain for beef", "Marketing support"],
        "success_story": {"title": "California Success", "story": "A franchisee in Los Angeles opened in 2018. 'The gyudon concept resonates with health-conscious Americans.'", "metrics": "5 locations | $520k avg revenue | 22-month ROI"},
        "menu_highlights": ["Gyudon (Beef Bowl)", "Chicken Teriyaki", "Karaage", "Miso Soup"],
        "contact_info": "International Franchise: overseas@yoshinoya.com | +81-3-5555-1111"
    },
    "Sushiro": {
        "story": "Japan's #1 conveyor belt sushi chain with 600+ stores.",
        "investment": "$200k - $500k", "royalty": "6.0%", "sales": "$600k - $1.2M",
        "overseas_status": "✅ EXPANDING - Asia, USA",
        "youtube_search": "Sushiro franchise", "news_search": "Sushiro expansion",
        "financials": {"Metric": ["Franchise Fee", "Investment", "Royalty", "Global Stores"], "Details": ["$50k-$80k", "$200k-$500k", "6%", "600+"]},
        "pros": ["Market leader", "High volume", "Technology integration"], "cons": ["Higher investment", "Complex operations"],
        "history": "Sushiro was established in 1995 and has become Japan's largest conveyor belt sushi chain. Known for high-quality sushi at affordable prices.",
        "requirements": ["Minimum net worth: $800k USD", "Liquid capital: $250k+ USD", "Restaurant experience required", "Large space: 2,000-3,500 sq ft"],
        "support": ["Sushi chef training", "Conveyor belt installation", "Fresh fish supply chain", "Technology systems"],
        "success_story": {"title": "Hong Kong Expansion", "story": "A master franchisee secured HK rights in 2018. Now 15 locations across HK.", "metrics": "15 stores | $850k avg revenue | 26-month ROI"},
        "menu_highlights": ["Conveyor belt sushi", "Fresh fish daily", "Touch-screen ordering", "Seasonal specialties"],
        "contact_info": "Franchise: franchise@sushiro.co.jp | +81-6-5555-2222"
    },
    "Coco Ichibanya": {
        "story": "Japan's #1 curry house with 1,300+ stores.",
        "investment": "$150k - $300k", "royalty": "5% - 7%", "sales": "¥50M - ¥80M",
        "overseas_status": "✅ ACTIVELY RECRUITING - USA, Asia, Europe",
        "youtube_search": "Coco Ichibanya franchise", "news_search": "Coco Ichibanya expansion",
        "financials": {"Metric": ["Fee", "Investment", "Royalty", "Stores"], "Details": ["¥3M-¥5M", "$150k-$300k", "5-7%", "1,300+"]},
        "pros": ["Proven success", "Low complexity", "Customizable menu"], "cons": ["Curry specialization", "Competition"],
        "history": "Founded in 1978 in Aichi Prefecture. Revolutionized Japanese curry with customizable spice levels. Now 1,300+ stores in Japan and 200+ internationally.",
        "requirements": ["Minimum net worth: $500k USD", "Liquid capital: $150k+ USD", "8-week training in Japan", "Space: 1,500-2,500 sq ft"],
        "support": ["8-week training in Japan", "Site selection", "Store design", "Equipment support", "Ongoing consulting"],
        "success_story": {"title": "Thailand Success", "story": "First Bangkok location in 2015. Expanded to 12 locations in 3 years.", "metrics": "12 stores | $540k avg revenue | 18-month ROI"},
        "menu_highlights": ["Japanese Curry Rice", "Katsu Curry", "Cheese Curry", "20+ toppings"],
        "contact_info": "International: international@coco-curry.com | +81-3-5555-1234"
    },
    "Pepper Lunch": {
        "story": "Fast-steak concept with 200+ stores across 15+ countries.",
        "investment": "$200k - $400k", "royalty": "5% - 6%", "sales": "$400k - $800k",
        "overseas_status": "✅ VERY ACTIVE - 15+ countries",
        "youtube_search": "Pepper Lunch franchise", "news_search": "Pepper Lunch expansion",
        "financials": {"Metric": ["Fee", "Investment", "Royalty", "Stores"], "Details": ["$30k-$50k", "$200k-$400k", "5-6%", "200+"]},
        "pros": ["Proven success", "DIY concept", "Fast service"], "cons": ["Sizzling equipment", "Premium pricing"],
        "history": "Founded in 1994 by Chef Kunio Ichinose. Revolutionary DIY dining on sizzling iron plates. Expanded to 15+ countries.",
        "requirements": ["Minimum net worth: $600k USD", "Liquid capital: $200k+ USD", "Restaurant experience required", "High-traffic location"],
        "support": ["4-week training", "Store design", "Sizzling plate tech", "Marketing", "R&D support"],
        "success_story": {"title": "Singapore Success", "story": "First Orchard Road location in 2012. Now 8 locations across SG and MY.", "metrics": "8 stores | $650k avg revenue | 24-month ROI"},
        "menu_highlights": ["Sizzling Beef Steak", "Salmon Meuniere", "Spicy Curry Beef", "3-minute cooking"],
        "contact_info": "Franchise: franchise@pepperlunch.com | +81-3-5555-5678"
    },
    "Kura Sushi": {
        "story": "High-tech conveyor belt sushi expanding in USA.",
        "investment": "$500k - $1M", "royalty": "5% - 6%", "sales": "$1M - $2M",
        "overseas_status": "✅ EXPANDING IN USA",
        "youtube_search": "Kura Sushi USA", "news_search": "Kura Sushi expansion",
        "financials": {"Metric": ["Investment", "Royalty", "Locations"], "Details": ["$500k-$1M", "5-6%", "10+"]},
        "pros": ["High-tech", "Strong growth", "Premium"], "cons": ["High investment", "Complex operations"],
        "history": "Established in 1999 in Nara. Known for touch-screen ordering, automated conveyor systems, and gamified dining. Public since 2013.",
        "requirements": ["Minimum net worth: $1.5M USD", "Liquid capital: $500k+ USD", "Multi-unit experience preferred", "Space: 3,000-5,000 sq ft"],
        "support": ["12-week training", "Conveyor system", "POS technology", "Sushi chef certification", "Fish supply chain"],
        "success_story": {"title": "California Expansion", "story": "First Irvine location in 2019. Attracted tech-savvy millennials and families.", "metrics": "3 locations | $1.2M avg revenue | 36-month ROI"},
        "menu_highlights": ["Premium conveyor sushi", "Touch-screen ordering", "Prize drawing system", "Sake selection"],
        "contact_info": "USA: usa@kurasushi.com | +1-949-555-0123"
    },
    "Sukiya": {
        "story": "Japan's largest gyudon chain with 2,000+ stores.",
        "investment": "$300k - $600k", "royalty": "4% - 6%", "sales": "¥100M+",
        "overseas_status": "✅ SELECTIVE - Asia focus",
        "youtube_search": "Sukiya franchise", "news_search": "Sukiya expansion",
        "financials": {"Metric": ["Investment", "Royalty", "Stores"], "Details": ["$300k-$600k", "4-6%", "2,000+"]},
        "pros": ["Massive brand", "Simple menu", "High volume"], "cons": ["Selective approval", "Beef regulations"],
        "history": "Founded in 1982. Japan's largest gyudon chain with 2,000+ locations. Part of Zenrin Group. Known for 24-hour operations.",
        "requirements": ["Minimum net worth: $800k USD", "Liquid capital: $300k+ USD", "Multi-unit QSR experience", "Master franchise preferred"],
        "support": ["Master franchise support", "Training programs", "Beef supply chain", "Store layout", "Marketing"],
        "success_story": {"title": "Hong Kong Dominance", "story": "Master franchisee since 2010. Now 35 locations across HK and Macau.", "metrics": "35 stores | $850k avg revenue | 20-month ROI"},
        "menu_highlights": ["Gyudon (Beef Bowl)", "Various sizes", "Side dishes", "24/7 operation"],
        "contact_info": "International: overseas@sukiya.co.jp | +81-45-555-9876"
    },
    "Hoshino Coffee": {
        "story": "Premium Nagoya coffee shop famous for pancakes.",
        "investment": "$250k - $500k", "royalty": "5% - 6%", "sales": "¥60M - ¥100M",
        "overseas_status": "✅ ACTIVE IN ASIA",
        "youtube_search": "Hoshino Coffee", "news_search": "Hoshino Coffee expansion",
        "financials": {"Metric": ["Investment", "Royalty", "Markets"], "Details": ["$250k-$500k", "5-6%", "HK/TW/TH"]},
        "pros": ["Premium", "Unique menu", "Strong branding"], "cons": ["Higher price", "Large space needed"],
        "history": "Established in 1978 in Nagoya. Famous for fluffy pancakes and retro Showa-era atmosphere. Expanding across Asia.",
        "requirements": ["Minimum net worth: $600k USD", "Liquid capital: $250k+ USD", "Café experience preferred", "Premium location", "Space: 1,200-2,000 sq ft"],
        "support": ["Barista training", "Pancake preparation", "Interior design", "Equipment sourcing", "Menu development"],
        "success_story": {"title": "Taiwan Premium Success", "story": "First Taipei location in 2016. Retro atmosphere created instant buzz.", "metrics": "6 stores | $420k avg revenue | 28-month ROI"},
        "menu_highlights": ["Fluffy pancakes", "Hand-drip coffee", "Morning sets", "Retro atmosphere"],
        "contact_info": "Asia: asia@hoshino-coffee.com | +81-52-555-4321"
    },
    "Ootoya": {
        "story": "Premium teishoku restaurant with 500+ stores.",
        "investment": "$300k - $600k", "royalty": "5% - 6%", "sales": "$500k - $1M",
        "overseas_status": "✅ ESTABLISHED - USA, Asia",
        "youtube_search": "Ootoya franchise", "news_search": "Ootoya international",
        "financials": {"Metric": ["Investment", "Royalty", "Stores"], "Details": ["$300k-$600k", "5-6%", "50+"]},
        "pros": ["Premium", "Healthy menu", "US success"], "cons": ["Complex menu", "Japanese ingredients"],
        "history": "Founded in 1983 in Tokyo. Specializes in teishoku (traditional Japanese set meals). 500+ locations globally with strong US presence.",
        "requirements": ["Minimum net worth: $700k USD", "Liquid capital: $300k+ USD", "Full-service restaurant experience", "Space: 1,500-2,500 sq ft"],
        "support": ["Culinary training", "Ingredient sourcing", "Menu planning", "Store design", "Staff training"],
        "success_story": {"title": "California Success", "story": "San Mateo location in 2015. Targets Japanese-American and health-conscious diners.", "metrics": "4 locations | $680k avg revenue | 30-month ROI"},
        "menu_highlights": ["Teishoku set meals", "Grilled fish", "Tempura", "Healthy options"],
        "contact_info": "Franchise: franchise@otoya.co.jp | +81-3-5555-7890"
    }
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
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 50px 30px; border-radius: 15px; color: white; margin-bottom: 30px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
        <h1 style="color: white; margin: 0 0 15px 0; font-size: 2.5em; font-weight: 700;">{t('hero_title')}</h1>
        <p style="font-size: 1.3em; margin: 0 0 20px 0; opacity: 0.95;">{t('hero_subtitle')}</p>
        <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-top: 25px;">
            <div class="metric-card"><div style="font-size: 2em; font-weight: bold;">63+</div><div style="font-size: 0.9em; opacity: 0.9;">{t('metric_brands')}</div></div>
            <div class="metric-card"><div style="font-size: 2em; font-weight: bold;">15+</div><div style="font-size: 0.9em; opacity: 0.9;">{t('metric_countries')}</div></div>
            <div class="metric-card"><div style="font-size: 2em; font-weight: bold;">$100k+</div><div style="font-size: 0.9em; opacity: 0.9;">{t('metric_investment')}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    df = load_brands()
    if df.empty:
        st.error("Could not load data")
        return
    
    st.subheader(t("found_brands"))
    
    st.sidebar.subheader(t("search_header"))
    search = st.sidebar.text_input(t("search_placeholder"), "")
    categories = st.session_state.get("categories", [])
    selected_cat = st.sidebar.multiselect(t("filter_category"), categories, default=[], help=t("choose_options"))
    
    filtered = df.copy()
    if search:
        filtered = filtered[filtered["brand_name"].str.contains(search, case=False, na=False) | filtered["category"].str.contains(search, case=False, na=False)]
    if selected_cat:
        filtered = filtered[filtered["category"].isin(selected_cat)]
    
    st.write(t("showing_brands", count=len(filtered)))
    
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
                <p class="brand-category">{category} | {stores} {t('stores')}</p>
            </div>
            <div class="brand-stats">
                <p class="brand-investment">${investment}</p>
                <p class="brand-royalty">{t('royalty')}: {royalty}%</p>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
        
        if has_dd:
            col1, col2 = st.columns([2, 1])
            with col1:
                if st.button(t("view_details"), key=f"detail_{idx}"):
                    st.session_state.selected_franchise = brand
                    st.session_state.page = "details"
                    st.rerun()
            with col2:
                if st.button(t("enquiry"), key=f"enq_{idx}"):
                    st.session_state.selected_franchise = brand
                    st.session_state.page = "quiz"
                    st.rerun()
        else:
            if st.button(t("enquiry"), key=idx):
                st.session_state.selected_franchise = brand
                st.session_state.page = "quiz"
                st.rerun()

    st.markdown(f"""
    <div class="footer">
        <p>{t('footer_text')}</p>
        <p>{t('footer_contact')}</p>
    </div>
    """, unsafe_allow_html=True)

def show_brand_details():
    brand = st.session_state.selected_franchise
    if not brand or brand not in FRANCHISES:
        st.session_state.page = "home"
        st.rerun()
    
    data = FRANCHISES[brand]
    
    if st.button(t("back_brands")):
        st.session_state.page = "home"
        st.rerun()
    
    st.title(f"🗾 {brand}")
    st.markdown(f'<div class="status-badge">{data["overseas_status"]}</div>', unsafe_allow_html=True)
    
    st.markdown(f"""<div class="detail-section"><h2 style="margin-top:0;">{t('company_history')}</h2></div>""", unsafe_allow_html=True)
    st.write(data["history"])
    
    st.markdown(f"""<div class="detail-section"><h2 style="margin-top:0;">{t('menu_highlights')}</h2></div>""", unsafe_allow_html=True)
    st.write(", ".join(data["menu_highlights"]))
    
    st.markdown(f"""<div class="detail-section"><h2 style="margin-top:0;">{t('investment_overview')}</h2></div>""", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Investment", data["investment"])
    col2.metric("Royalty", data["royalty"])
    col3.metric("Avg. Sales", data["sales"])
    
    st.markdown(f"""<div class="detail-section"><h2 style="margin-top:0;">{t('requirements')}</h2></div>""", unsafe_allow_html=True)
    for req in data["requirements"]:
        st.markdown(f"""<div class="requirement-box">✅ {req}</div>""", unsafe_allow_html=True)
    
    st.markdown(f"""<div class="detail-section"><h2 style="margin-top:0;">{t('support')}</h2></div>""", unsafe_allow_html=True)
    for support in data["support"]:
        st.markdown(f"• {support}")
    
    if "success_story" in data:
        story = data["success_story"]
        st.markdown(f"""<div class="detail-section"><h2 style="margin-top:0;">{t('success_story')}</h2></div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="success-story">
            <h3 style="margin-top:0; color:#059669;">{story["title"]}</h3>
            <p>{story["story"]}</p>
            <p style="font-weight:bold; color:#059669; margin-bottom:0;">📊 {story["metrics"]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""<div class="detail-section"><h2 style="margin-top:0;">{t('contact_info')}</h2></div>""", unsafe_allow_html=True)
    st.info(data["contact_info"])
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button(t("submit_enquiry"), type="primary", use_container_width=True):
            st.session_state.page = "quiz"
            st.rerun()
    with col2:
        youtube_url = f"https://www.youtube.com/results?search_query={quote(data['youtube_search'])}"
        st.markdown(f"[{t('watch_videos')}]({youtube_url})")

def show_quiz():
    brand = st.session_state.selected_franchise or "General"
    st.title(t("enquiry_title", brand=brand))
    if st.button(t("back")):
        st.session_state.page = "home"
        st.rerun()
    with st.form("quiz"):
        name = st.text_input(t("name"))
        email = st.text_input(t("email"))
        capital = st.selectbox(t("capital"), [t("cap_under"), t("cap_100_250"), t("cap_250_500"), t("cap_500_1m"), t("cap_over")])
        experience = st.selectbox(t("experience"), [t("exp_none"), t("exp_1_3"), t("exp_3_5"), t("exp_5_plus"), t("exp_owner")])
        industry = st.selectbox(t("industry"), [t("ind_fb"), t("ind_retail"), t("ind_corp"), t("ind_other")])
        location = st.text_input(t("location"))
        timeline = st.selectbox(t("timeline"), [t("time_research"), t("time_1_2"), t("time_6_12"), t("time_asap")])
        if st.form_submit_button(t("submit")):
            if name and email:
                send_email(f"Enquiry: {name} for {brand}", f"Name: {name}\nEmail: {email}")
                save_to_sheet(brand, name, email, capital, experience, industry, location, timeline)
                st.success(t("success_msg"))
            else:
                st.error(t("error_msg"))

def show_franchisor():
    st.title(t("franchisor_title"))
    st.markdown(f'<div style="margin-bottom: 25px;"><h3 style="color: #1a1a2e; margin-top: 0;">{t("why_register")}</h3><p style="font-size: 1.1em; line-height: 1.6;">As a Japanese franchise brand, you have unique access to the global market. Our platform connects you directly with qualified international investors.</p></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="benefit-card"><h4>{t("what_you_get")}</h4><ul style="padding-left: 20px; margin: 15px 0;"><li><strong>Real-time qualified leads</strong> - See genuine investor applications as they come in</li><li><strong>Pre-screened investors</strong> - All applicants are vetted for serious investment capacity</li><li><strong>Dedicated dashboard</strong> - Track your leads and review applications in one place</li><li><strong>CSV export</strong> - Download your leads in spreadsheet format</li><li><strong>Direct connection</strong> - Contact investors directly through our secure platform</li></ul></div>', unsafe_allow_html=True)
    
    if not st.session_state.franchisor_logged_in:
        st.markdown(f'<div style="margin-bottom: 25px;"><h3 style="color: #1a1a2e; margin-top: 0;">{t("access_dashboard")}</h3><p style="font-size: 1.1em; line-height: 1.6;">If your brand is already approved as a partner, enter your access code to see your leads.</p></div>', unsafe_allow_html=True)
        pwd = st.text_input(t("password"), type="password")
        if st.button(t("login")):
            if pwd == "jfa2026":
                st.session_state.franchisor_logged_in = True
                st.rerun()
            else:
                st.error(t("wrong_password"))
        st.markdown(f'<div style="margin-top: 30px;"><h3 style="color: #1a1a2e; margin-top: 0;">{t("new_to_jx")}</h3><p style="font-size: 1.1em; line-height: 1.6;">If you\'re a Japanese franchise brand looking to expand internationally, you can request access to our platform.</p></div>', unsafe_allow_html=True)
        with st.form("request"):
            company = st.text_input(t("company"))
            email = st.text_input(t("email"))
            if st.form_submit_button(t("request_access")):
                send_email("Partner Request", f"{company}: {email}")
                st.success(t("request_sent"))
        return
    
    st.success(t("logged_in"))
    if st.button(t("logout")):
        st.session_state.franchisor_logged_in = False
        st.rerun()
    tab1, tab2 = st.tabs([t("leads"), t("settings")])
    with tab1:
        leads = get_leads()
        if leads:
            df = pd.DataFrame(leads)
            st.write(t("found_leads", count=len(leads)))
            st.dataframe(df)
            csv = df.to_csv(index=False)
            st.download_button(t("download_csv"), csv, "leads.csv")
        else:
            st.info(t("no_leads"))
    with tab2:
        st.info(t("settings_soon"))

def show_about():
    st.title(t("about_title"))
    st.caption(t("about_caption"))
    st.markdown("---")
    st.subheader(t("why_started"))
    st.markdown("### A Personal Journey with Japanese Culture\n\nI'm a passionate advocate of Japanese culture and cuisine. Over the years, I've had the privilege of witnessing the remarkable growth and spread of Japanese culinary culture across Asia, Europe, and the United States.\n\nThe numbers tell an incredible story:")
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Japanese Restaurants (2006)", "24,000", "Starting point")
    with col2: st.metric("Japanese Restaurants (Today)", "200,000+", "+733% growth")
    with col3: st.metric("Growth Period", "~18 years", "JETRO Data")
    st.markdown("This **8x growth** in less than two decades is unprecedented in global food culture history.\n\n### Our Mission\n\nAs a personal project, I started JXPerience to:\n\n1. **📊 Aggregate Information** - Bring together comprehensive data on Japanese franchises\n2. **🤝 Connect Investors** - Help serious global investors discover authentic Japanese franchise opportunities\n3. ** Support Expansion** - Contribute to the continued global growth of Japanese cuisine\n4. **🍱 Cultural Exchange** - Enable more people worldwide to discover authentic Japanese cuisine\n\n### The Vision\n\nBy making franchise information more accessible, we hope to:\n- Support more people in discovering authentic Japanese cuisine\n- Facilitate meaningful cultural exchanges through food\n- Create shared experiences that bring people together\n- Help Japanese brands find the right partners for global expansion\n\n---\n\n*This platform is a labor of love, built to support the continued growth and appreciation of Japanese culinary excellence worldwide.*")
    
    st.markdown("""
    <div class="beta-banner">
        <h4>🚧 This is a Beta Site — Help Us Build It Together!</h4>
        <p style="color: #78350f; margin-bottom: 10px;">JXPerience is currently in <strong>beta</strong>. We are actively improving the platform and would love your input.</p>
        <p style="color: #78350f; margin-bottom: 10px;"><strong>🤝 Co-Create With Us</strong> — Have suggestions, spotted a bug, or want to recommend a franchise brand to add? We invite you to share your comments and improvement ideas directly with us.</p>
        <p style="color: #78350f; margin: 0;">📧 <strong>Email us at:</strong> <a href="mailto:jxperience.info@gmail.com?subject=JXPerience Feedback">jxperience.info@gmail.com</a></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader(t("faq_title"))
    
    faqs = [
        {"q": "Is there a fee to use this platform?", "a": "No, browsing and submitting enquiries is completely free for investors."},
        {"q": "How do I know these brands are legitimate?", "a": "We verify overseas expansion status using public data, JETRO reports, and official franchise disclosures."},
        {"q": "What happens after I submit an enquiry?", "a": "Your details are securely sent to our team. We will pre-screen your profile and connect you with the franchise's international development team."},
        {"q": "Can I franchise a brand not listed here?", "a": "Yes! Use the email link above to suggest a brand. We are always adding new opportunities."}
    ]
    
    for faq in faqs:
        st.markdown(f"""
        <div class="faq-item">
            <p style="font-weight: bold; color: #1a1a2e; margin-bottom: 5px;">{faq["q"]}</p>
            <p style="color: #666; margin: 0;">{faq["a"]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader(t("ready_explore"))
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button(t("browse"), use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
    with col_b:
        st.markdown(f"{t('contact_label')} [jxperience.info@gmail.com](mailto:jxperience.info@gmail.com)")

# --- SIDEBAR ---
st.sidebar.title(t("sidebar_title"))
st.sidebar.markdown("---")

# Language selector at top of sidebar
st.sidebar.subheader(t("language"))
language = st.sidebar.radio("Select Language / 言語を選択", 
                            ["English", "日本語"],
                            index=0 if st.session_state.language == "English" else 1,
                            horizontal=True)
if language != st.session_state.language:
    st.session_state.language = language
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader(t("nav_header"))
if st.sidebar.button(t("home"), use_container_width=True):
    st.session_state.page = "home"
    st.rerun()
if st.sidebar.button(t("about"), use_container_width=True):
    st.session_state.page = "about"
    st.rerun()
if st.sidebar.button(t("franchisor"), use_container_width=True):
    st.session_state.page = "franchisor"
    st.rerun()
st.sidebar.markdown("---")

# --- ROUTER ---
if st.session_state.page == "quiz": show_quiz()
elif st.session_state.page == "franchisor": show_franchisor()
elif st.session_state.page == "profile": show_brand_details()
elif st.session_state.page == "details": show_brand_details()
elif st.session_state.page == "about": show_about()
else: show_home()
