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
        "sidebar_title": " JP Hub", "nav_header": "Navigation", "home": " Home", "about": "ℹ️ About Us", "franchisor": "🏢 Franchisor",
        "search_header": "🔍 Search & Filter", "search_placeholder": "Search brands", "filter_category": "Filter by Category", "choose_options": "Choose options",
        "hero_title": " Discover Japanese Franchise Opportunities", "hero_subtitle": "Connecting global investors with 63+ expansion-ready Japanese brands",
        "metric_brands": "Brands", "metric_countries": "Countries", "metric_investment": "Investment",
        "found_brands": "Found 63 Expansion-Ready Brands", "showing_brands": "Showing {count} brands", "stores": "stores", "royalty": "Royalty",
        "view_details": " View Details", "enquiry": "Enquiry →",
        "footer_text": "© 2026 JXPerience. Connecting Japanese brands with global investors.", "footer_contact": "📧 Contact: jxperience.info@gmail.com",
        "back_brands": "← Back to Brands", "company_history": " Company History", "menu_highlights": "🍱 Menu Highlights", "investment_overview": "💰 Investment Overview",
        "requirements": "📋 Franchise Requirements", "support": "🤝 Support Provided", "success_story": "⭐ Success Story", "contact_info": "📞 Contact Information",
        "submit_enquiry": "📝 Submit Enquiry", "watch_videos": "▶️ Watch Videos",
        "enquiry_title": "Enquiry: {brand}", "back": "← Back", "name": "Name", "email": "Email", "capital": "Capital", "experience": "Experience", "industry": "Industry", "location": "Location", "timeline": "Timeline",
        "submit": "Submit Enquiry", "success_msg": "✅ Enquiry submitted!", "error_msg": "Fill in name and email",
        "cap_under": "Under $100k", "cap_100_250": "$100k-$250k", "cap_250_500": "$250k-$500k", "cap_500_1m": "$500k-$1M", "cap_over": "Over $1M",
        "exp_none": "None", "exp_1_3": "1-3 years", "exp_3_5": "3-5 years", "exp_5_plus": "5+ years", "exp_owner": "Franchise Owner",
        "ind_fb": "F&B", "ind_retail": "Retail", "ind_corp": "Corporate", "ind_other": "Other",
        "time_research": "Researching", "time_1_2": "1-2 years", "time_6_12": "6-12 months", "time_asap": "ASAP",
        "about_title": " About JXPerience", "about_caption": "Our Mission & Story", "why_started": "Why We Started This", "faq_title": "❓ Frequently Asked Questions",
        "ready_explore": " Ready to Explore?", "browse": "Browse Franchises", "contact_label": " **Contact:**",
        "franchisor_title": " Franchisor Portal", "why_register": "Why Register as a Franchisor?", "what_you_get": "✅ What You'll Get as a Verified Partner",
        "access_dashboard": "Access Your Franchise Dashboard", "new_to_jx": "New to JXPerience?", "password": "Password", "login": "Login", "wrong_password": "Wrong password",
        "company": "Company", "request_access": "Request Access", "request_sent": "Request sent! We'll contact you within 24-48 hours.", "logged_in": "Logged in", "logout": "Logout",
        "leads": "📊 Leads", "settings": "⚙️ Settings", "found_leads": "✅ Found {count} real leads!", "download_csv": " Download CSV", "no_leads": "No leads yet", "settings_soon": "Settings coming soon",
        "language": "🌐 Language",
    },
    "日本語": {
        "sidebar_title": " JPハブ", "nav_header": "ナビゲーション", "home": "🏠 ホーム", "about": "ℹ️ 私たちについて", "franchisor": "🏢 フランチャイザー",
        "search_header": " 検索とフィルター", "search_placeholder": "ブランドを検索", "filter_category": "カテゴリでフィルター", "choose_options": "オプションを選択",
        "hero_title": "🗾 日本のフランチャイズ機会を発見", "hero_subtitle": "63以上の展開-readyな日本ブランドとグローバル投資家をつなぐ",
        "metric_brands": "ブランド", "metric_countries": "国・地域", "metric_investment": "投資額",
        "found_brands": "63の展開-readyブランドを発見", "showing_brands": "{count}ブランドを表示", "stores": "店舗", "royalty": "ロイヤリティ",
        "view_details": " 詳細を見る", "enquiry": "お問い合わせ →",
        "footer_text": "© 2026 JXPerience. 日本ブランドとグローバル投資家をつなぐ。", "footer_contact": "📧 お問い合わせ: jxperience.info@gmail.com",
        "back_brands": "← ブランド一覧に戻る", "company_history": " 会社の歴史", "menu_highlights": "🍱 メニューの特徴", "investment_overview": "💰 投資概要",
        "requirements": "📋 フランチャイズ要件", "support": " サポート内容", "success_story": "⭐ 成功事例", "contact_info": "📞 お問い合わせ情報",
        "submit_enquiry": " お問い合わせを送信", "watch_videos": "▶️ 動画を見る",
        "enquiry_title": "お問い合わせ: {brand}", "back": "← 戻る", "name": "お名前", "email": "メールアドレス", "capital": "資金", "experience": "経験", "industry": "業界", "location": "場所", "timeline": "スケジュール",
        "submit": "送信", "success_msg": "✅ お問い合わせを送信しました！", "error_msg": "名前とメールアドレスを入力してください",
        "cap_under": "$100k未満", "cap_100_250": "$100k-$250k", "cap_250_500": "$250k-$500k", "cap_500_1m": "$500k-$1M", "cap_over": "$1M超",
        "exp_none": "なし", "exp_1_3": "1-3年", "exp_3_5": "3-5年", "exp_5_plus": "5年以上", "exp_owner": "フランチャイズオーナー",
        "ind_fb": "飲食", "ind_retail": "小売", "ind_corp": "企業", "ind_other": "その他",
        "time_research": "調査中", "time_1_2": "1-2年", "time_6_12": "6-12ヶ月", "time_asap": " ASAP（できるだけ早く）",
        "about_title": "🗾 JXPerienceについて", "about_caption": "私たちのミッションとストーリー", "why_started": "なぜ始めたのか", "faq_title": "❓ よくある質問",
        "ready_explore": " 探索する準備はできましたか？", "browse": "ブランドを見る", "contact_label": "📧 **お問い合わせ:**",
        "franchisor_title": " フランチャイザーポータル", "why_register": "なぜフランチャイザーとして登録するのか？", "what_you_get": "✅ 認定パートナーの特典",
        "access_dashboard": "フランチャイズダッシュボードにアクセス", "new_to_jx": "JXPerienceが初めてですか？", "password": "パスワード", "login": "ログイン", "wrong_password": "パスワードが違います",
        "company": "会社名", "request_access": "アクセスをリクエスト", "request_sent": "リクエストを送信しました！24-48時間以内にご連絡します。", "logged_in": "ログインしました", "logout": "ログアウト",
        "leads": "📊 リード", "settings": "⚙️ 設定", "found_leads": "✅ {count}件のリアルリードを発見！", "download_csv": "📥 CSVをダウンロード", "no_leads": "リードはまだありません", "settings_soon": "設定は近日公開",
        "language": " 言語",
    }
}

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'selected_franchise' not in st.session_state: st.session_state.selected_franchise = None
if 'franchisor_logged_in' not in st.session_state: st.session_state.franchisor_logged_in = False
if 'categories' not in st.session_state: st.session_state.categories = []
if 'language' not in st.session_state: st.session_state.language = 'English'

# --- TRANSLATION HELPER ---
def t(key, **kwargs):
    lang = st.session_state.language
    text = TRANSLATIONS.get(lang, TRANSLATIONS["English"]).get(key, key)
    return text.format(**kwargs) if kwargs else text

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    h1, h2, h3 { color: #1a1a2e; font-weight: 700; margin-bottom: 1rem; }
    .stButton>button { border-radius: 8px; font-weight: 600; padding: 0.5rem 1.5rem; transition: all 0.3s ease; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
    .metric-card { background: rgba(255,255,255,0.2); padding: 15px 25px; border-radius: 10px; backdrop-filter: blur(10px); }
    .status-badge { display: inline-block; background: #10b981; color: white; padding: 8px 16px; border-radius: 20px; font-weight: 600; margin-bottom: 20px; }
    .benefit-card { background: #f0f7ff; border-left: 4px solid #667eea; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    .benefit-card h4 { color: #1a1a2e; margin-top: 0; }
    .brand-row { display: flex; align-items: center; padding: 20px; background: white; border-radius: 12px; margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: all 0.3s ease; }
    .brand-row:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.12); transform: translateY(-2px); }
    .brand-logo-wrapper { position: relative; width: 60px; height: 60px; border-radius: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; display: flex; align-items: center; justify-content: center; font-size: 1.8em; font-weight: bold; margin-right: 20px; overflow: hidden; flex-shrink: 0; }
    .brand-logo-img { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: contain; background: white; padding: 8px; box-sizing: border-box; }
    .brand-info { flex: 1; }
    .brand-name { font-size: 1.2em; font-weight: 700; color: #1a1a2e; margin: 0 0 5px 0; }
    .brand-category { font-size: 0.9em; color: #666; margin: 0; }
    .brand-stats { text-align: right; margin-right: 20px; }
    .brand-investment { font-size: 0.95em; color: #333; margin: 0 0 5px 0; font-weight: 600; }
    .brand-royalty { font-size: 0.85em; color: #666; margin: 0; }
    .beta-banner { background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-left: 4px solid #f59e0b; padding: 20px; border-radius: 10px; margin: 20px 0; }
    .beta-banner h4 { color: #92400e; margin-top: 0; margin-bottom: 10px; }
    .faq-item { background: white; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 3px solid #667eea; }
    .footer { text-align: center; padding: 20px; color: #666; font-size: 0.9em; margin-top: 40px; border-top: 1px solid #e0e0e0; }
    .detail-section { background: white; padding: 25px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
    .requirement-box { background: #f0f7ff; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #667eea; }
    .success-story { background: #f0fdf4; padding: 20px; border-radius: 10px; margin: 15px 0; border-left: 4px solid #10b981; }
</style>
""", unsafe_allow_html=True)

# --- LOAD BRANDS ---
def extract_domain(url):
    if pd.isna(url) or not url: return ""
    try: return str(url).replace("http://", "").replace("https://", "").replace("www.", "").split("/")[0].split("?")[0]
    except: return ""

@st.cache_data(ttl=300)
def load_brands():
    try:
        df = pd.read_csv(CSV_URL)
        if "category" in df.columns: st.session_state.categories = df["category"].dropna().unique().tolist()
        if "website" in df.columns:
            df["domain"] = df["website"].apply(extract_domain)
            df["logo_url"] = df["domain"].apply(lambda d: f"https://www.google.com/s2/favicons?domain={d}&sz=128" if d else "")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# --- ENGLISH CONTENT (Base) ---
FRANCHISES = {
    "Yoshinoya": {"story": "World-famous gyudon chain with 1,000+ stores.", "investment": "$150k - $300k", "royalty": "5.0%", "sales": "$400k - $800k", "overseas_status": "✅ ACTIVELY RECRUITING - USA, Asia, Middle East", "youtube_search": "Yoshinoya franchise", "news_search": "Yoshinoya expansion", "financials": {"Metric": ["Fee", "Investment", "Royalty", "Stores"], "Details": ["$30k-$50k", "$150k-$300k", "5%", "1,000+"]}, "pros": ["Global brand", "Simple menu", "Fast service"], "cons": ["Beef regulations", "High competition"], "history": "Founded in 1899 in Tokyo's fish market, Yoshinoya is one of Japan's oldest fast-food chains. Specializing in gyudon (beef bowls), it has grown to over 1,200 locations worldwide.", "requirements": ["Minimum net worth: $400k USD", "Liquid capital: $150k+ USD", "Restaurant experience preferred", "High-traffic location: 800-1,500 sq ft"], "support": ["Initial training (2-4 weeks)", "Site selection assistance", "Store design package", "Supply chain for beef", "Marketing support"], "success_story": {"title": "California Success", "story": "A franchisee in Los Angeles opened in 2018. 'The gyudon concept resonates with health-conscious Americans.'", "metrics": "5 locations | $520k avg revenue | 22-month ROI"}, "menu_highlights": ["Gyudon (Beef Bowl)", "Chicken Teriyaki", "Karaage", "Miso Soup"], "contact_info": "International: overseas@yoshinoya.com | +81-3-5555-1111"},
    "Sushiro": {"story": "Japan's #1 conveyor belt sushi chain with 600+ stores.", "investment": "$200k - $500k", "royalty": "6.0%", "sales": "$600k - $1.2M", "overseas_status": "✅ EXPANDING - Asia, USA", "youtube_search": "Sushiro franchise", "news_search": "Sushiro expansion", "financials": {"Metric": ["Fee", "Investment", "Royalty", "Stores"], "Details": ["$50k-$80k", "$200k-$500k", "6%", "600+"]}, "pros": ["Market leader", "High volume", "Tech integration"], "cons": ["Higher investment", "Complex ops"], "history": "Sushiro was established in 1995 and has become Japan's largest conveyor belt sushi chain. Known for high-quality sushi at affordable prices.", "requirements": ["Minimum net worth: $800k USD", "Liquid capital: $250k+ USD", "Restaurant experience required", "Large space: 2,000-3,500 sq ft"], "support": ["Sushi chef training", "Conveyor belt installation", "Fresh fish supply chain", "Technology systems"], "success_story": {"title": "Hong Kong Expansion", "story": "A master franchisee secured HK rights in 2018. Now 15 locations across HK.", "metrics": "15 stores | $850k avg revenue | 26-month ROI"}, "menu_highlights": ["Conveyor belt sushi", "Fresh fish daily", "Touch-screen ordering", "Seasonal specialties"], "contact_info": "Franchise: franchise@sushiro.co.jp | +81-6-5555-2222"},
    "Coco Ichibanya": {"story": "Japan's #1 curry house with 1,300+ stores.", "investment": "$150k - $300k", "royalty": "5% - 7%", "sales": "¥50M - ¥80M", "overseas_status": "✅ ACTIVELY RECRUITING - USA, Asia, Europe", "youtube_search": "Coco Ichibanya franchise", "news_search": "Coco Ichibanya expansion", "financials": {"Metric": ["Fee", "Investment", "Royalty", "Stores"], "Details": ["¥3M-¥5M", "$150k-$300k", "5-7%", "1,300+"]}, "pros": ["Proven success", "Low complexity", "Customizable"], "cons": ["Curry specialization", "Competition"], "history": "Founded in 1978 in Aichi Prefecture. Revolutionized Japanese curry with customizable spice levels. Now 1,300+ stores in Japan and 200+ internationally.", "requirements": ["Minimum net worth: $500k USD", "Liquid capital: $150k+ USD", "8-week training in Japan", "Space: 1,500-2,500 sq ft"], "support": ["8-week training in Japan", "Site selection", "Store design", "Equipment support", "Ongoing consulting"], "success_story": {"title": "Thailand Success", "story": "First Bangkok location in 2015. Expanded to 12 locations in 3 years.", "metrics": "12 stores | $540k avg revenue | 18-month ROI"}, "menu_highlights": ["Japanese Curry Rice", "Katsu Curry", "Cheese Curry", "20+ toppings"], "contact_info": "International: international@coco-curry.com | +81-3-5555-1234"},
    "Pepper Lunch": {"story": "Fast-steak concept with 200+ stores across 15+ countries.", "investment": "$200k - $400k", "royalty": "5% - 6%", "sales": "$400k - $800k", "overseas_status": "✅ VERY ACTIVE - 15+ countries", "youtube_search": "Pepper Lunch franchise", "news_search": "Pepper Lunch expansion", "financials": {"Metric": ["Fee", "Investment", "Royalty", "Stores"], "Details": ["$30k-$50k", "$200k-$400k", "5-6%", "200+"]}, "pros": ["Proven success", "DIY concept", "Fast service"], "cons": ["Sizzling equipment", "Premium pricing"], "history": "Founded in 1994 by Chef Kunio Ichinose. Revolutionary DIY dining on sizzling iron plates. Expanded to 15+ countries.", "requirements": ["Minimum net worth: $600k USD", "Liquid capital: $200k+ USD", "Restaurant experience required", "High-traffic location"], "support": ["4-week training", "Store design", "Sizzling plate tech", "Marketing", "R&D support"], "success_story": {"title": "Singapore Success", "story": "First Orchard Road location in 2012. Now 8 locations across SG and MY.", "metrics": "8 stores | $650k avg revenue | 24-month ROI"}, "menu_highlights": ["Sizzling Beef Steak", "Salmon Meuniere", "Spicy Curry Beef", "3-minute cooking"], "contact_info": "Franchise: franchise@pepperlunch.com | +81-3-5555-5678"},
    "Kura Sushi": {"story": "High-tech conveyor belt sushi expanding in USA.", "investment": "$500k - $1M", "royalty": "5% - 6%", "sales": "$1M - $2M", "overseas_status": "✅ EXPANDING IN USA", "youtube_search": "Kura Sushi USA", "news_search": "Kura Sushi expansion", "financials": {"Metric": ["Investment", "Royalty", "Locations"], "Details": ["$500k-$1M", "5-6%", "10+"]}, "pros": ["High-tech", "Strong growth", "Premium"], "cons": ["High investment", "Complex ops"], "history": "Established in 1999 in Nara. Known for touch-screen ordering, automated conveyor systems, and gamified dining. Public since 2013.", "requirements": ["Minimum net worth: $1.5M USD", "Liquid capital: $500k+ USD", "Multi-unit experience preferred", "Space: 3,000-5,000 sq ft"], "support": ["12-week training", "Conveyor system", "POS technology", "Sushi chef certification", "Fish supply chain"], "success_story": {"title": "California Expansion", "story": "First Irvine location in 2019. Attracted tech-savvy millennials and families.", "metrics": "3 locations | $1.2M avg revenue | 36-month ROI"}, "menu_highlights": ["Premium conveyor sushi", "Touch-screen ordering", "Prize drawing system", "Sake selection"], "contact_info": "USA: usa@kurasushi.com | +1-949-555-0123"},
    "Sukiya": {"story": "Japan's largest gyudon chain with 2,000+ stores.", "investment": "$300k - $600k", "royalty": "4% - 6%", "sales": "¥100M+", "overseas_status": "✅ SELECTIVE - Asia focus", "youtube_search": "Sukiya franchise", "news_search": "Sukiya expansion", "financials": {"Metric": ["Investment", "Royalty", "Stores"], "Details": ["$300k-$600k", "4-6%", "2,000+"]}, "pros": ["Massive brand", "Simple menu", "High volume"], "cons": ["Selective approval", "Beef regulations"], "history": "Founded in 1982. Japan's largest gyudon chain with 2,000+ locations. Part of Zenrin Group. Known for 24-hour operations.", "requirements": ["Minimum net worth: $800k USD", "Liquid capital: $300k+ USD", "Multi-unit QSR experience", "Master franchise preferred"], "support": ["Master franchise support", "Training programs", "Beef supply chain", "Store layout", "Marketing"], "success_story": {"title": "Hong Kong Dominance", "story": "Master franchisee since 2010. Now 35 locations across HK and Macau.", "metrics": "35 stores | $850k avg revenue | 20-month ROI"}, "menu_highlights": ["Gyudon (Beef Bowl)", "Various sizes", "Side dishes", "24/7 operation"], "contact_info": "International: overseas@sukiya.co.jp | +81-45-555-9876"},
    "Hoshino Coffee": {"story": "Premium Nagoya coffee shop famous for pancakes.", "investment": "$250k - $500k", "royalty": "5% - 6%", "sales": "¥60M - ¥100M", "overseas_status": "✅ ACTIVE IN ASIA", "youtube_search": "Hoshino Coffee", "news_search": "Hoshino Coffee expansion", "financials": {"Metric": ["Investment", "Royalty", "Markets"], "Details": ["$250k-$500k", "5-6%", "HK/TW/TH"]}, "pros": ["Premium", "Unique menu", "Strong branding"], "cons": ["Higher price", "Large space needed"], "history": "Established in 1978 in Nagoya. Famous for fluffy pancakes and retro Showa-era atmosphere. Expanding across Asia.", "requirements": ["Minimum net worth: $600k USD", "Liquid capital: $250k+ USD", "Café experience preferred", "Premium location", "Space: 1,200-2,000 sq ft"], "support": ["Barista training", "Pancake preparation", "Interior design", "Equipment sourcing", "Menu development"], "success_story": {"title": "Taiwan Premium Success", "story": "First Taipei location in 2016. Retro atmosphere created instant buzz.", "metrics": "6 stores | $420k avg revenue | 28-month ROI"}, "menu_highlights": ["Fluffy pancakes", "Hand-drip coffee", "Morning sets", "Retro atmosphere"], "contact_info": "Asia: asia@hoshino-coffee.com | +81-52-555-4321"},
    "Ootoya": {"story": "Premium teishoku restaurant with 500+ stores.", "investment": "$300k - $600k", "royalty": "5% - 6%", "sales": "$500k - $1M", "overseas_status": "✅ ESTABLISHED - USA, Asia", "youtube_search": "Ootoya franchise", "news_search": "Ootoya international", "financials": {"Metric": ["Investment", "Royalty", "Stores"], "Details": ["$300k-$600k", "5-6%", "50+"]}, "pros": ["Premium", "Healthy menu", "US success"], "cons": ["Complex menu", "Japanese ingredients"], "history": "Founded in 1983 in Tokyo. Specializes in teishoku (traditional Japanese set meals). 500+ locations globally with strong US presence.", "requirements": ["Minimum net worth: $700k USD", "Liquid capital: $300k+ USD", "Full-service restaurant experience", "Space: 1,500-2,500 sq ft"], "support": ["Culinary training", "Ingredient sourcing", "Menu planning", "Store design", "Staff training"], "success_story": {"title": "California Success", "story": "San Mateo location in 2015. Targets Japanese-American and health-conscious diners.", "metrics": "4 locations | $680k avg revenue | 30-month ROI"}, "menu_highlights": ["Teishoku set meals", "Grilled fish", "Tempura", "Healthy options"], "contact_info": "Franchise: franchise@otoya.co.jp | +81-3-5555-7890"}
}

# --- JAPANESE CONTENT (Phase 2: Overrides) ---
FRANCHISES_JA = {
    "Yoshinoya": {"story": "世界的に有名な牛丼チェーン。日本国内に1,000以上、海外に200以上の店舗を展開。", "overseas_status": "✅ 積極募集 - 米国、アジア、中東", "history": "1899年、東京の魚市場で創業した吉野家は、日本最古のファストフードチェーンの一つです。牛丼を専門とし、現在では世界1,200以上のお店で展開しています。", "requirements": ["最低純資産：40万米ドル", "流動資産：15万米ドル以上", "飲食店経験者優遇", "人通りの多い立地：800-1,500平方フィート"], "support": ["初期研修（2-4週間）", "出店支援", "店舗デザインパッケージ", "牛肉サプライチェーン", "マーケティング支援"], "success_story": {"title": "カリフォルニアでの成功", "story": "2018年にロサンゼルスで出店。「牛丼のコンセプトは、健康志向のアメリカ人に支持されています。」", "metrics": "5店舗 | 平均売上$520k | 22ヶ月でROI"}, "menu_highlights": ["牛丼", "チキン照り焼き", "唐揚げ", "味噌汁"], "contact_info": "国際フランチャイズ: overseas@yoshinoya.com | +81-3-5555-1111"},
    "Sushiro": {"story": "日本最大の回転寿司チェーン。600以上のお店で展開。", "overseas_status": "✅ 展開中 - アジア、米国", "history": "1995年に設立され、日本最大の回転寿司チェーンとなりました。高品質な寿司を手頃な価格で提供することで知られています。", "requirements": ["最低純資産：80万米ドル", "流動資産：25万米ドル以上", "飲食店経験必須", "広いスペース：2,000-3,500平方フィート"], "support": ["寿司職人研修", "回転ベルト設置", "新鮮な魚のサプライチェーン", "テクノロジーシステム"], "success_story": {"title": "香港展開", "story": "2018年に香港のマスターフランチャイズ権を取得。現在、香港全域に15店舗を展開。", "metrics": "15店舗 | 平均売上$850k | 26ヶ月でROI"}, "menu_highlights": ["回転寿司", "毎日新鮮な魚", "タッチパネル注文", "季節限定メニュー"], "contact_info": "フランチャイズ: franchise@sushiro.co.jp | +81-6-5555-2222"},
    "Coco Ichibanya": {"story": "日本最大のカレーハウス。1,300以上のお店で展開。", "overseas_status": "✅ 積極募集 - 米国、アジア、ヨーロッパ", "history": "1978年に愛知県で創業。カスタマイズ可能なスパイスレベルで日本カレーに革命を起こしました。現在、日本国内に1,300以上、海外に200以上のお店があります。", "requirements": ["最低純資産：50万米ドル", "流動資産：15万米ドル以上", "日本での8週間研修", "スペース：1,500-2,500平方フィート"], "support": ["日本での8週間研修", "出店支援", "店舗デザイン", "設備支援", "継続的なコンサルティング"], "success_story": {"title": "タイでの成功", "story": "2015年にバンコク1号店を出店。3年間で12店舗に拡大。", "metrics": "12店舗 | 平均売上$540k | 18ヶ月でROI"}, "menu_highlights": ["日本カレーライス", "カツカレー", "チーズカレー", "20種類以上のトッピング"], "contact_info": "国際開発: international@coco-curry.com | +81-3-5555-1234"},
    "Pepper Lunch": {"story": "15か国以上に200以上のお店を持つ鉄板ステーキのファストフード。", "overseas_status": "✅ 非常に活発 - 15か国以上", "history": "1994年に市瀬國雄シェフによって創業。熱々の鉄板でお客様自身が調理する革命的なDIYダイニング。15か国以上に展開しています。", "requirements": ["最低純資産：60万米ドル", "流動資産：20万米ドル以上", "飲食店経験必須", "人通りの多い立地"], "support": ["4週間の研修", "店舗デザイン", "鉄板技術", "マーケティング", "R&D支援"], "success_story": {"title": "シンガポールでの成功", "story": "2012年にシンガポールのオーチャードロード1号店を出店。現在、SGとMYに8店舗。", "metrics": "8店舗 | 平均売上$650k | 24ヶ月でROI"}, "menu_highlights": ["鉄板ビーフステーキ", "サーモンムニエール", "スパイシーカレービーフ", "3分調理"], "contact_info": "フランチャイズ: franchise@pepperlunch.com | +81-3-5555-5678"},
    "Kura Sushi": {"story": "米国で展開中のハイテク回転寿司。", "overseas_status": "✅ 米国で展開中", "history": "1999年に奈良で設立。タッチパネル注文、自動回転ベルトシステム、ゲーム性のあるダイニングで知られています。2013年に上場。", "requirements": ["最低純資産：150万米ドル", "流動資産：50万米ドル以上", "複数店舗経験者優遇", "スペース：3,000-5,000平方フィート"], "support": ["12週間の研修", "回転ベルトシステム", "POSテクノロジー", "寿司職人認定", "魚のサプライチェーン"], "success_story": {"title": "カリフォルニア展開", "story": "2019年にアーバイン1号店を出店。テクノロジーに精通したミレニアル世代とファミリーに支持されています。", "metrics": "3店舗 | 平均売上$1.2M | 36ヶ月でROI"}, "menu_highlights": ["プレミアム回転寿司", "タッチパネル注文", "抽選システム", "日本酒セレクション"], "contact_info": "米国: usa@kurasushi.com | +1-949-555-0123"},
    "Sukiya": {"story": "日本最大の牛丼チェーン。2,000以上のお店で展開。", "overseas_status": "✅ 厳選 - アジア中心", "history": "1982年に創業。2,000以上のお店を持つ日本最大の牛丼チェーン。ゼンリングループの一員。24時間営業で知られています。", "requirements": ["最低純資産：80万米ドル", "流動資産：30万米ドル以上", "複数店舗QSR経験", "マスターフランチャイズ優遇"], "support": ["マスターフランチャイズ支援", "研修プログラム", "牛肉サプライチェーン", "店舗レイアウト", "マーケティング"], "success_story": {"title": "香港での支配力", "story": "2010年以来のマスターフランチャイジー。現在、香港とマカオに35店舗。", "metrics": "35店舗 | 平均売上$850k | 20ヶ月でROI"}, "menu_highlights": ["牛丼", "各種サイズ", "サイドディッシュ", "24時間営業"], "contact_info": "国際: overseas@sukiya.co.jp | +81-45-555-9876"},
    "Hoshino Coffee": {"story": "パンケーキで有名な名古屋発のプレミアムコーヒーショップ。", "overseas_status": "✅ アジアで活動中", "history": "1978年に名古屋で設立。ふわふわのパンケーキとレトロな昭和時代の雰囲気で有名。アジア全域に展開中。", "requirements": ["最低純資産：60万米ドル", "流動資産：25万米ドル以上", "カフェ経験者優遇", "プレミアム立地", "スペース：1,200-2,000平方フィート"], "support": ["バリスタ研修", "パンケーキ調理", "インテリアデザイン", "設備調達", "メニュー開発"], "success_story": {"title": "台湾プレミアム成功", "story": "2016年に台北1号店を出店。レトロな雰囲気が即座に話題を呼びました。", "metrics": "6店舗 | 平均売上$420k | 28ヶ月でROI"}, "menu_highlights": ["ふわふわパンケーキ", "ハンドドリップコーヒー", "モーニングセット", "レトロな雰囲気"], "contact_info": "アジア: asia@hoshino-coffee.com | +81-52-555-4321"},
    "Ootoya": {"story": "500以上のお店を持つプレミアム定食レストラン。", "overseas_status": "✅ 確立 - 米国、アジア", "history": "1983年に東京で創業。定食（伝統的な日本食セット）を専門としています。世界中に500以上のお店があり、米国での存在感が強いです。", "requirements": ["最低純資産：70万米ドル", "流動資産：30万米ドル以上", "フルサービス飲食店経験", "スペース：1,500-2,500平方フィート"], "support": ["料理研修", "食材調達", "メニュー計画", "店舗デザイン", "スタッフトレーニング"], "success_story": {"title": "カリフォルニア成功", "story": "2015年にサンマテオに出店。日系アメリカ人と健康志向のダイナーをターゲットにしています。", "metrics": "4店舗 | 平均売上$680k | 30ヶ月でROI"}, "menu_highlights": ["定食セット", "焼き魚", "天ぷら", "ヘルシーオプション"], "contact_info": "フランチャイズ: franchise@otoya.co.jp | +81-3-5555-7890"}
}

# --- CONTENT HELPERS ---
def get_brand(brand):
    base = FRANCHISES.get(brand, {})
    if st.session_state.language == "日本語" and brand in FRANCHISES_JA:
        return {**base, **FRANCHISES_JA[brand]}
    return base

ABOUT_EN = """### A Personal Journey with Japanese Culture\n\nI'm a passionate advocate of Japanese culture and cuisine. Over the years, I've had the privilege of witnessing the remarkable growth and spread of Japanese culinary culture across Asia, Europe, and the United States.\n\nThe numbers tell an incredible story:\n\nThis **8x growth** in less than two decades is unprecedented in global food culture history.\n\n### Our Mission\n\nAs a personal project, I started JXPerience to:\n\n1. **📊 Aggregate Information** - Bring together comprehensive data on Japanese franchises\n2. **🤝 Connect Investors** - Help serious global investors discover authentic Japanese franchise opportunities\n3. **🌍 Support Expansion** - Contribute to the continued global growth of Japanese cuisine\n4. **🍱 Cultural Exchange** - Enable more people worldwide to discover authentic Japanese cuisine\n\n### The Vision\n\nBy making franchise information more accessible, we hope to:\n- Support more people in discovering authentic Japanese cuisine\n- Facilitate meaningful cultural exchanges through food\n- Create shared experiences that bring people together\n- Help Japanese brands find the right partners for global expansion\n\n---\n\n*This platform is a labor of love, built to support the continued growth and appreciation of Japanese culinary excellence worldwide.*"""

ABOUT_JA = """### 日本文化との個人的な旅\n\n私は日本文化と日本料理の熱心な支持者です。長年にわたり、アジア、ヨーロッパ、そして米国全体で日本料理文化の驚くべき成長と普及を目撃する特権を得てきました。\n\n数字が驚くべき物語を語っています：\n\nこの20年未満での**8倍の成長**は、世界の食文化史上前例のないものです。\n\n### 私たちのミッション\n\n個人的なプロジェクトとして、JXPerienceを始めました：\n\n1. **📊 情報集約** - 日本のフランチャイズに関する包括的なデータを集める\n2. **🤝 投資家をつなぐ** - 真剣なグローバル投資家が本物の日本のフランチャイズ機会を発見するのを支援する\n3. **🌍 展開を支援する** - 日本料理の継続的な世界的成長に貢献する\n4. **🍱 文化交流** - 世界中のより多くの人々が本物の日本料理を発見できるようにする\n\n### ビジョン\n\nフランチャイズ情報をよりアクセスしやすくすることで、私たちは以下を希望しています：\n- より多くの人々が本物の日本料理を発見するのを支援する\n- 食を通じた意味のある文化交流を促進する\n- 人々を結びつける共有体験を創造する\n- 日本のブランドがグローバル展開のための適切なパートナーを見つけるのを支援する\n\n---\n\n*このプラットフォームは、世界中での日本料理の卓越性の継続的な成長と Appreciation を支援するために構築された、愛情のこもったプロジェクトです。*"""

def get_about():
    return ABOUT_JA if st.session_state.language == "日本語" else ABOUT_EN

FAQ_EN = [
    {"q": "Is there a fee to use this platform?", "a": "No, browsing and submitting enquiries is completely free for investors."},
    {"q": "How do I know these brands are legitimate?", "a": "We verify overseas expansion status using public data, JETRO reports, and official franchise disclosures."},
    {"q": "What happens after I submit an enquiry?", "a": "Your details are securely sent to our team. We will pre-screen your profile and connect you with the franchise's international development team."},
    {"q": "Can I franchise a brand not listed here?", "a": "Yes! Use the email link above to suggest a brand. We are always adding new opportunities."}
]

FAQ_JA = [
    {"q": "このプラットフォームの利用に料金はかかりますか？", "a": "いいえ、投資家様の閲覧およびお問い合わせ送信は完全に無料です。"},
    {"q": "これらのブランドが正当であることをどうやって知ることができますか？", "a": "公開データ、JETROレポート、および公式フランチャイズ開示情報を使用して海外展開ステータスを確認しています。"},
    {"q": "お問い合わせを送信した後、どうなりますか？", "a": "お客様の詳細は安全に私たちのチームに送信されます。プロフィールを事前審査し、フランチャイズの国際開発チームと接続します。"},
    {"q": "ここにリストされていないブランドをフランチャイズできますか？", "a": "はい！上記のメールリンクを使用してブランドを提案してください。私たちは常に新しい機会を追加しています。"}
]

def get_faqs():
    return FAQ_JA if st.session_state.language == "日本語" else FAQ_EN

FRANCHISOR_EN = '<div style="margin-bottom: 25px;"><h3 style="color: #1a1a2e; margin-top: 0;">Why Register as a Franchisor?</h3><p style="font-size: 1.1em; line-height: 1.6;">As a Japanese franchise brand, you have unique access to the global market. Our platform connects you directly with qualified international investors.</p></div><div class="benefit-card"><h4>✅ What You\'ll Get as a Verified Partner</h4><ul style="padding-left: 20px; margin: 15px 0;"><li><strong>Real-time qualified leads</strong> - See genuine investor applications as they come in</li><li><strong>Pre-screened investors</strong> - All applicants are vetted for serious investment capacity</li><li><strong>Dedicated dashboard</strong> - Track your leads and review applications in one place</li><li><strong>CSV export</strong> - Download your leads in spreadsheet format</li><li><strong>Direct connection</strong> - Contact investors directly through our secure platform</li></ul></div>'

FRANCHISOR_JA = '<div style="margin-bottom: 25px;"><h3 style="color: #1a1a2e; margin-top: 0;">なぜフランチャイザーとして登録するのか？</h3><p style="font-size: 1.1em; line-height: 1.6;">日本のフランチャイズブランドとして、グローバル市場へのユニークなアクセス権を持っています。私たちのプラットフォームは、資格のある国際投資家と直接接続します。</p></div><div class="benefit-card"><h4>✅ 認定パートナーの特典</h4><ul style="padding-left: 20px; margin: 15px 0;"><li><strong>リアルタイムの qualified リード</strong> - 投資家アプリケーションが届き次第確認</li><li><strong>事前審査済みの投資家</strong> - すべての応募者は真剣な投資能力について審査済み</li><li><strong>専用ダッシュボード</strong> - リードを追跡し、アプリケーションを一つの場所で確認</li><li><strong>CSVエクスポート</strong> - リードをスプレッドシート形式でダウンロード</li><li><strong>直接接続</strong> - 安全なプラットフォームを通じて投資家と直接連絡</li></ul></div>'

def get_franchisor_text():
    return FRANCHISOR_JA if st.session_state.language == "日本語" else FRANCHISOR_EN

# --- FUNCTIONS ---
def send_email(subject, body, to_email=None):
    if not to_email: to_email = YOUR_GMAIL
    msg = MIMEText(body)
    msg["Subject"] = subject; msg["From"] = YOUR_GMAIL; msg["To"] = to_email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(YOUR_GMAIL, YOUR_APP_PASSWORD); server.send_message(msg)
        return True
    except Exception as e:
        print(f"Email error: {e}"); return False

def save_to_sheet(franchise, name, email, capital, experience, industry, location, timeline):
    payload = {"franchise": franchise, "name": name, "email": email, "capital": capital, "experience": experience, "industry": industry, "location": location, "timeline": timeline}
    try:
        requests.post(SHEET_WEBHOOK_URL, json=payload); return True
    except Exception as e:
        print(f"Sheet error: {e}"); return False

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
        st.error("Could not load data"); return
    
    st.subheader(t("found_brands"))
    st.sidebar.subheader(t("search_header"))
    search = st.sidebar.text_input(t("search_placeholder"), "")
    categories = st.session_state.get("categories", [])
    selected_cat = st.sidebar.multiselect(t("filter_category"), categories, default=[], help=t("choose_options"))
    
    filtered = df.copy()
    if search: filtered = filtered[filtered["brand_name"].str.contains(search, case=False, na=False) | filtered["category"].str.contains(search, case=False, na=False)]
    if selected_cat: filtered = filtered[filtered["category"].isin(selected_cat)]
    
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
            <div class="brand-logo-wrapper">{first_letter}<img src="{logo_url}" class="brand-logo-img"></div>
            <div class="brand-info"><p class="brand-name">{brand}</p><p class="brand-category">{category} | {stores} {t('stores')}</p></div>
            <div class="brand-stats"><p class="brand-investment">${investment}</p><p class="brand-royalty">{t('royalty')}: {royalty}%</p></div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
        
        if has_dd:
            col1, col2 = st.columns([2, 1])
            with col1:
                if st.button(t("view_details"), key=f"detail_{idx}"):
                    st.session_state.selected_franchise = brand; st.session_state.page = "details"; st.rerun()
            with col2:
                if st.button(t("enquiry"), key=f"enq_{idx}"):
                    st.session_state.selected_franchise = brand; st.session_state.page = "quiz"; st.rerun()
        else:
            if st.button(t("enquiry"), key=idx):
                st.session_state.selected_franchise = brand; st.session_state.page = "quiz"; st.rerun()

    st.markdown(f"""<div class="footer"><p>{t('footer_text')}</p><p>{t('footer_contact')}</p></div>""", unsafe_allow_html=True)

def show_brand_details():
    brand = st.session_state.selected_franchise
    if not brand or brand not in FRANCHISES:
        st.session_state.page = "home"; st.rerun()
    
    data = get_brand(brand) # Uses helper to get correct language
    
    if st.button(t("back_brands")):
        st.session_state.page = "home"; st.rerun()
    
    st.title(f"🗾 {brand}")
    st.markdown(f'<div class="status-badge">{data["overseas_status"]}</div>', unsafe_allow_html=True)
    
    st.markdown(f"""<div class="detail-section"><h2 style="margin-top:0;">{t('company_history')}</h2></div>""", unsafe_allow_html=True)
    st.write(data["history"])
    
    st.markdown(f"""<div class="detail-section"><h2 style="margin-top:0;">{t('menu_highlights')}</h2></div>""", unsafe_allow_html=True)
    st.write(", ".join(data["menu_highlights"]))
    
    st.markdown(f"""<div class="detail-section"><h2 style="margin-top:0;">{t('investment_overview')}</h2></div>""", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Investment", data["investment"]); col2.metric("Royalty", data["royalty"]); col3.metric("Avg. Sales", data["sales"])
    
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
            st.session_state.page = "quiz"; st.rerun()
    with col2:
        youtube_url = f"https://www.youtube.com/results?search_query={quote(data['youtube_search'])}"
        st.markdown(f"[{t('watch_videos')}]({youtube_url})")

def show_quiz():
    brand = st.session_state.selected_franchise or "General"
    st.title(t("enquiry_title", brand=brand))
    if st.button(t("back")):
        st.session_state.page = "home"; st.rerun()
    with st.form("quiz"):
        name = st.text_input(t("name")); email = st.text_input(t("email"))
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
    st.markdown(get_franchisor_text(), unsafe_allow_html=True) # Uses helper
    
    if not st.session_state.franchisor_logged_in:
        st.markdown(f'<div style="margin-bottom: 25px;"><h3 style="color: #1a1a2e; margin-top: 0;">{t("access_dashboard")}</h3><p style="font-size: 1.1em; line-height: 1.6;">If your brand is already approved as a partner, enter your access code to see your leads.</p></div>', unsafe_allow_html=True)
        pwd = st.text_input(t("password"), type="password")
        if st.button(t("login")):
            if pwd == "jfa2026":
                st.session_state.franchisor_logged_in = True; st.rerun()
            else:
                st.error(t("wrong_password"))
        st.markdown(f'<div style="margin-top: 30px;"><h3 style="color: #1a1a2e; margin-top: 0;">{t("new_to_jx")}</h3><p style="font-size: 1.1em; line-height: 1.6;">If you\'re a Japanese franchise brand looking to expand internationally, you can request access to our platform.</p></div>', unsafe_allow_html=True)
        with st.form("request"):
            company = st.text_input(t("company")); email = st.text_input(t("email"))
            if st.form_submit_button(t("request_access")):
                send_email("Partner Request", f"{company}: {email}"); st.success(t("request_sent"))
        return
    
    st.success(t("logged_in"))
    if st.button(t("logout")):
        st.session_state.franchisor_logged_in = False; st.rerun()
    tab1, tab2 = st.tabs([t("leads"), t("settings")])
    with tab1:
        leads = get_leads()
        if leads:
            df = pd.DataFrame(leads); st.write(t("found_leads", count=len(leads))); st.dataframe(df)
            csv = df.to_csv(index=False); st.download_button(t("download_csv"), csv, "leads.csv")
        else:
            st.info(t("no_leads"))
    with tab2:
        st.info(t("settings_soon"))

def show_about():
    st.title(t("about_title")); st.caption(t("about_caption")); st.markdown("---")
    st.subheader(t("why_started"))
    st.markdown(get_about(), unsafe_allow_html=True) # Uses helper
    
    st.markdown("""
    <div class="beta-banner">
        <h4> This is a Beta Site — Help Us Build It Together!</h4>
        <p style="color: #78350f; margin-bottom: 10px;">JXPerience is currently in <strong>beta</strong>. We are actively improving the platform and would love your input.</p>
        <p style="color: #78350f; margin-bottom: 10px;"><strong> Co-Create With Us</strong> — Have suggestions, spotted a bug, or want to recommend a franchise brand to add? We invite you to share your comments and improvement ideas directly with us.</p>
        <p style="color: #78350f; margin: 0;">📧 <strong>Email us at:</strong> <a href="mailto:jxperience.info@gmail.com?subject=JXPerience Feedback">jxperience.info@gmail.com</a></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---"); st.subheader(t("faq_title"))
    for faq in get_faqs(): # Uses helper
        st.markdown(f"""
        <div class="faq-item">
            <p style="font-weight: bold; color: #1a1a2e; margin-bottom: 5px;">{faq["q"]}</p>
            <p style="color: #666; margin: 0;">{faq["a"]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider(); st.subheader(t("ready_explore"))
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button(t("browse"), use_container_width=True):
            st.session_state.page = "home"; st.rerun()
    with col_b:
        st.markdown(f"{t('contact_label')} [jxperience.info@gmail.com](mailto:jxperience.info@gmail.com)")

# --- SIDEBAR ---
st.sidebar.title(t("sidebar_title")); st.sidebar.markdown("---")
st.sidebar.subheader(t("language"))
language = st.sidebar.radio("Select Language / 言語を選択", ["English", "日本語"], index=0 if st.session_state.language == "English" else 1, horizontal=True)
if language != st.session_state.language:
    st.session_state.language = language; st.rerun()

st.sidebar.markdown("---"); st.sidebar.subheader(t("nav_header"))
if st.sidebar.button(t("home"), use_container_width=True): st.session_state.page = "home"; st.rerun()
if st.sidebar.button(t("about"), use_container_width=True): st.session_state.page = "about"; st.rerun()
if st.sidebar.button(t("franchisor"), use_container_width=True): st.session_state.page = "franchisor"; st.rerun()
st.sidebar.markdown("---")

# --- ROUTER ---
if st.session_state.page == "quiz": show_quiz()
elif st.session_state.page == "franchisor": show_franchisor()
elif st.session_state.page == "profile": show_brand_details()
elif st.session_state.page == "details": show_brand_details()
elif st.session_state.page == "about": show_about()
else: show_home()
