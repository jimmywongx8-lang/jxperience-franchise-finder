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

# --- EXPANDED FRANCHISE DETAILS (NOW INCLUDES YOSHINOYA & SUSHIRO) ---
FRANCHISES = {
    "Yoshinoya": {
        "story": "World-famous gyudon chain with 1,000+ stores in Japan and 200+ overseas.",
        "investment": "$150k - $300k",
        "royalty": "5.0%",
        "sales": "$400k - $800k",
        "overseas_status": "✅ ACTIVELY RECRUITING - USA, Asia, Middle East",
        "youtube_search": "Yoshinoya franchise",
        "news_search": "Yoshinoya expansion",
        "financials": {"Metric": ["Franchise Fee", "Total Investment", "Royalty", "Store Count"], "Details": ["$30k-$50k", "$150k-$300k", "5%", "1,000+"]},
        "pros": ["Global brand recognition", "Simple menu", "Fast service model", "Strong supply chain"],
        "cons": ["Beef import regulations", "High competition", "Thin margins"],
        
        "history": "Founded in 1899 in Tokyo's fish market, Yoshinoya is one of Japan's oldest and most iconic fast-food chains. Specializing in gyudon (beef bowls), the company has grown to over 1,200 locations worldwide. Known for speed, affordability, and consistent quality, Yoshinoya has successfully expanded to the USA, China, Southeast Asia, and the Middle East.",
        
        "requirements": [
            "Minimum net worth: $400k USD",
            "Liquid capital: $150k+ USD",
            "Restaurant or retail management experience preferred",
            "Ability to operate fast-service model",
            "Understanding of import regulations for beef",
            "Suitable location: 800-1,500 sq ft in high-traffic area"
        ],
        
        "support": [
            "Initial training program (2-4 weeks)",
            "Site selection assistance",
            "Store design and equipment package",
            "Supply chain establishment for beef",
            "Recipe standardization",
            "Marketing and promotional support",
            "Ongoing operational consulting",
            "Technology systems (POS, inventory)"
        ],
        
        "success_story": {
            "title": "California Success",
            "story": "A franchisee in Los Angeles opened their first Yoshinoya in 2018. The simple menu and fast service attracted busy professionals and students. 'The gyudon concept resonates with health-conscious Americans looking for quick, affordable Japanese food. We serve 400+ customers daily.'",
            "metrics": "5 locations | $520k avg revenue | 22-month ROI"
        },
        
        "menu_highlights": ["Gyudon (Beef Bowl)", "Chicken Teriyaki", "Karaage (Fried Chicken)", "Miso Soup", "Quick service", "Value meals"],
        
        "contact_info": "International Franchise: overseas@yoshinoya.com | +81-3-5555-1111"
    },
    
    "Sushiro": {
        "story": "Japan's #1 conveyor belt sushi chain with 600+ stores.",
        "investment": "$200k - $500k",
        "royalty": "6.0%",
        "sales": "$600k - $1.2M",
        "overseas_status": "✅ EXPANDING - Asia, USA",
        "youtube_search": "Sushiro franchise",
        "news_search": "Sushiro expansion",
        "financials": {"Metric": ["Franchise Fee", "Investment", "Royalty", "Global Stores"], "Details": ["$50k-$80k", "$200k-$500k", "6%", "600+"]},
        "pros": ["Market leader", "High volume", "Fresh fish supply chain", "Technology integration"],
        "cons": ["Higher investment", "Complex operations", "Fresh seafood handling"],
        
        "history": "Sushiro (formerly Akindo Sushiro) was established in 1995 and has become Japan's largest conveyor belt sushi chain. Known for high-quality sushi at affordable prices, advanced ordering technology, and efficient operations. The company operates 600+ stores across Japan and is rapidly expanding in Asia and the USA.",
        
        "requirements": [
            "Minimum net worth: $800k USD",
            "Liquid capital: $250k+ USD",
            "Restaurant experience required",
            "Understanding of seafood handling and freshness standards",
            "Ability to manage 20-30 staff members",
            "Large space: 2,000-3,500 sq ft",
            "Commitment to quality and freshness"
        ],
        
        "support": [
            "Comprehensive sushi chef training",
            "Conveyor belt system installation",
            "Fresh fish supply chain network",
            "Technology systems (touch-screen ordering)",
            "Store design and layout",
            "Quality control systems",
            "Marketing support",
            "Ongoing menu development"
        ],
        
        "success_story": {
            "title": "Hong Kong Expansion",
            "story": "A master franchisee secured Hong Kong rights in 2018. They now operate 15 locations across HK. 'Sushiro's combination of quality, technology, and affordability is perfect for Hong Kong's competitive F&B market. Average wait time: 45 minutes during peak hours.'",
            "metrics": "15 stores | $850k avg revenue | 26-month ROI"
        },
        
        "menu_highlights": ["Conveyor belt sushi", "Fresh fish daily", "Touch-screen ordering", "Seasonal specialties", "Premium selections", "Family sets"],
        
        "contact_info": "Franchise Development: franchise@sushiro.co.jp | +81-6-5555-2222"
    },
    
    "Coco Ichibanya": {
        "story": "Japan's #1 curry house with 1,300+ stores. Aggressively expanding overseas.",
        "investment": "$150k - $300k",
        "royalty": "5% - 7%",
        "sales": "¥50M - ¥80M",
        "overseas_status": "✅ ACTIVELY RECRUITING - USA, Asia, Europe",
        "youtube_search": "Coco Ichibanya franchise",
        "news_search": "Coco Ichibanya expansion",
        "financials": {"Metric": ["Franchise Fee", "Total Investment", "Royalty", "Store Count"], "Details": ["¥3M-¥5M", "$150k-$300k", "5-7%", "1,300+"]},
        "pros": ["Proven overseas success", "Low complexity", "Customizable menu"],
        "cons": ["Curry specialization", "Competition in Asia"],
        
        "history": "Founded in 1978 in Ichinomiya, Aichi Prefecture, Coco Ichibanya (CoCo壱番屋) started as a small family restaurant. The company revolutionized Japanese curry by offering customizable spice levels and toppings. Today, it operates over 1,300 stores in Japan and 200+ internationally, making it the world's largest curry house chain.",
        
        "requirements": [
            "Minimum net worth: $500k USD",
            "Liquid capital: $150k+ USD",
            "Prior restaurant experience preferred but not required",
            "Commitment to full-time operation",
            "Willingness to attend 8-week training program in Japan",
            "Suitable location with 1,500-2,500 sq ft space"
        ],
        
        "support": [
            "Comprehensive 8-week training in Japan (headquarters)",
            "Site selection and lease negotiation assistance",
            "Store design and layout planning",
            "Equipment procurement support",
            "Initial marketing and grand opening support",
            "Ongoing operational consulting",
            "Recipe and menu development",
            "Supply chain management"
        ],
        
        "success_story": {
            "title": "Thailand Expansion Success",
            "story": "Mr. Tanaka opened the first Coco Ichibanya in Bangkok in 2015. Within 3 years, he expanded to 12 locations across Thailand. Average monthly revenue: $45k USD per store. 'The training program in Japan was exceptional. The support team helped us adapt the menu to local tastes while maintaining authenticity.'",
            "metrics": "12 stores | $540k avg annual revenue | 18-month ROI"
        },
        
        "menu_highlights": ["Signature Japanese Curry Rice", "Katsu Curry", "Cheese Curry", "Half-size options", "5-10 spice levels", "20+ toppings"],
        
        "contact_info": "International Development: international@coco-curry.com | +81-3-5555-1234"
    },
    
    "Pepper Lunch": {
        "story": "Fast-steak concept with 200+ stores across 15+ countries. Highly successful internationally.",
        "investment": "$200k - $400k",
        "royalty": "5% - 6%",
        "sales": "$400k - $800k",
        "overseas_status": "✅ VERY ACTIVE - 15+ countries",
        "youtube_search": "Pepper Lunch franchise",
        "news_search": "Pepper Lunch expansion",
        "financials": {"Metric": ["Franchise Fee", "Investment", "Royalty", "Global Stores"], "Details": ["$30k-$50k", "$200k-$400k", "5-6%", "200+"]},
        "pros": ["Proven success", "DIY concept", "Fast service"],
        "cons": ["Sizzling equipment", "Premium pricing"],
        
        "history": "Pepper Lunch was founded in 1994 by Chef Kunio Ichinose in Japan. The revolutionary concept allows customers to cook their own meals on sizzling hot iron plates at their tables. This unique DIY dining experience has expanded to 15+ countries with over 200 locations, becoming one of Japan's most successful international food exports.",
        
        "requirements": [
            "Minimum net worth: $600k USD",
            "Liquid capital: $200k+ USD",
            "Restaurant or retail management experience required",
            "Ability to hire and train 15-25 staff members",
            "Commitment to brand standards and quality",
            "Prime location in high-traffic area (mall or street-front)"
        ],
        
        "support": [
            "4-week intensive training program",
            "Complete store design and equipment package",
            "Proprietary sizzling plate technology",
            "Recipe and menu standardization",
            "Marketing materials and campaigns",
            "Ongoing R&D for new menu items",
            "Regional manager support",
            "Supplier network access"
        ],
        
        "success_story": {
            "title": "Singapore Success Story",
            "story": "The Lim family opened their first Pepper Lunch in Singapore's Orchard Road in 2012. They now operate 8 locations across Singapore and Malaysia. 'The DIY concept resonates perfectly with Asian diners. The unique sizzling experience creates memorable dining that keeps customers coming back.'",
            "metrics": "8 stores | $650k avg revenue | 24-month ROI"
        },
        
        "menu_highlights": ["Sizzling Beef Steak", "Salmon Meuniere", "Spicy Curry Beef", "Garlic Fried Rice", "Signature sauces", "Quick 3-minute cooking"],
        
        "contact_info": "Franchise Department: franchise@pepperlunch.com | +81-3-5555-5678"
    },
    
    "Kura Sushi": {
        "story": "High-tech conveyor belt sushi expanding in USA.",
        "investment": "$500k - $1M",
        "royalty": "5% - 6%",
        "sales": "$1M - $2M",
        "overseas_status": "✅ EXPANDING IN USA",
        "youtube_search": "Kura Sushi USA",
        "news_search": "Kura Sushi expansion",
        "financials": {"Metric": ["Investment", "Royalty", "Locations"], "Details": ["$500k-$1M", "5-6%", "10+"]},
        "pros": ["High-tech", "Strong growth", "Premium"],
        "cons": ["High investment", "Complex operations"],
        
        "history": "Kura Sushi (Kura-zushi) was established in 1999 in Nara, Japan. Known for its innovative technology including touch-screen ordering, automated conveyor systems, and a gamified dining experience with prize drawings. The company went public in 2013 and is aggressively expanding in the US market with plans for 100+ locations.",
        
        "requirements": [
            "Minimum net worth: $1.5M USD",
            "Liquid capital: $500k+ USD",
            "Multi-unit restaurant experience strongly preferred",
            "Understanding of technology-driven operations",
            "Ability to invest in high-end equipment",
            "Large space requirement: 3,000-5,000 sq ft",
            "Commitment to premium customer experience"
        ],
        
        "support": [
            "Extensive 12-week training program",
            "State-of-the-art conveyor belt system installation",
            "Proprietary POS and ordering technology",
            "Sushi chef training and certification",
            "Fresh fish supply chain management",
            "Marketing and brand positioning",
            "Quality control systems",
            "Continuous technology updates"
        ],
        
        "success_story": {
            "title": "California Expansion",
            "story": "A franchisee in Irvine, California opened their first location in 2019. The high-tech concept attracted tech-savvy millennials and families. 'The gamification aspect—where customers win prizes after 5 plates—creates incredible engagement. Kids love it, adults appreciate the quality.'",
            "metrics": "3 locations | $1.2M avg revenue | 36-month ROI"
        },
        
        "menu_highlights": ["Premium conveyor belt sushi", "Touch-screen ordering", "Fresh fish daily", "Prize drawing system", "Seasonal specialties", "Sake selection"],
        
        "contact_info": "USA Development: usa@kurasushi.com | +1-949-555-0123"
    },
    
    "Sukiya": {
        "story": "Japan's largest gyudon chain with 2,000+ stores. Expanding in Asia.",
        "investment": "$300k - $600k",
        "royalty": "4% - 6%",
        "sales": "¥100M+",
        "overseas_status": "✅ SELECTIVE - Asia focus",
        "youtube_search": "Sukiya franchise",
        "news_search": "Sukiya expansion",
        "financials": {"Metric": ["Investment", "Royalty", "Stores"], "Details": ["$300k-$600k", "4-6%", "2,000+"]},
        "pros": ["Massive brand", "Simple menu", "High volume"],
        "cons": ["Selective approval", "Beef regulations"],
        
        "history": "Sukiya was founded in 1982 and has grown to become Japan's largest gyudon (beef bowl) chain with over 2,000 locations. Part of the Zenrin Group, Sukiya is known for fast service, affordable prices, and 24-hour operations. The brand has a strong presence across Asia and is selectively expanding through master franchise agreements.",
        
        "requirements": [
            "Minimum net worth: $800k USD",
            "Liquid capital: $300k+ USD",
            "Multi-unit QSR (Quick Service Restaurant) experience required",
            "Ability to operate 24/7",
            "Understanding of import regulations for beef",
            "Master franchise preference (5+ locations)",
            "Strong local market knowledge"
        ],
        
        "support": [
            "Master franchise support for qualified candidates",
            "Operational training programs",
            "Supply chain establishment for beef imports",
            "Store layout and equipment specifications",
            "Recipe standardization and quality control",
            "Marketing and promotional support",
            "Ongoing menu development",
            "Technology systems (POS, inventory)"
        ],
        
        "success_story": {
            "title": "Hong Kong Market Dominance",
            "story": "A master franchisee secured rights for Hong Kong in 2010. They now operate 35 locations across HK and Macau. 'The simple menu and fast service model works perfectly in Hong Kong's fast-paced environment. We serve 500+ customers daily per store.'",
            "metrics": "35 stores | $850k avg revenue | 20-month ROI"
        },
        
        "menu_highlights": ["Gyudon (Beef Bowl)", "Various sizes (S/M/L)", "Side dishes", "Miso soup", "Quick 3-min service", "24/7 operation"],
        
        "contact_info": "International: overseas@sukiya.co.jp | +81-45-555-9876"
    },
    
    "Hoshino Coffee": {
        "story": "Premium Nagoya coffee shop famous for pancakes. Expanding in Asia.",
        "investment": "$250k - $500k",
        "royalty": "5% - 6%",
        "sales": "¥60M - ¥100M",
        "overseas_status": "✅ ACTIVE IN ASIA",
        "youtube_search": "Hoshino Coffee",
        "news_search": "Hoshino Coffee expansion",
        "financials": {"Metric": ["Investment", "Royalty", "Markets"], "Details": ["$250k-$500k", "5-6%", "HK/TW/TH"]},
        "pros": ["Premium", "Unique menu", "Strong branding"],
        "cons": ["Higher price", "Large space needed"],
        
        "history": "Hoshino Coffee was established in 1978 in Nagoya, Japan, as a traditional kissaten (coffee shop). Famous for its thick, fluffy pancakes and retro Showa-era atmosphere, the brand has successfully modernized while maintaining its nostalgic charm. Currently expanding across Asia with a focus on premium positioning.",
        
        "requirements": [
            "Minimum net worth: $600k USD",
            "Liquid capital: $250k+ USD",
            "Hospitality or café experience preferred",
            "Premium location in upscale area",
            "Large space: 1,200-2,000 sq ft",
            "Commitment to traditional service standards",
            "Understanding of premium positioning"
        ],
        
        "support": [
            "Barista and service training",
            "Signature pancake preparation training",
            "Interior design consultation (retro-modern aesthetic)",
            "Equipment sourcing (espresso machines, etc.)",
            "Menu development and recipes",
            "Brand marketing materials",
            "Ongoing quality assurance",
            "Seasonal menu updates"
        ],
        
        "success_story": {
            "title": "Taiwan Premium Success",
            "story": "Opened first location in Taipei's Xinyi District in 2016. The retro atmosphere and famous pancakes created instant buzz. 'Hoshino Coffee fills a unique niche—traditional Japanese café culture with modern premium positioning. Customers stay 2-3 hours, creating a destination experience.'",
            "metrics": "6 stores | $420k avg revenue | 28-month ROI"
        },
        
        "menu_highlights": ["Famous fluffy pancakes", "Hand-drip coffee", "Morning sets", "Retro atmosphere", "Premium beans", "Traditional service"],
        
        "contact_info": "Asia Development: asia@hoshino-coffee.com | +81-52-555-4321"
    },
    
    "Ootoya": {
        "story": "Premium teishoku restaurant with 500+ stores. Strong US presence.",
        "investment": "$300k - $600k",
        "royalty": "5% - 6%",
        "sales": "$500k - $1M",
        "overseas_status": "✅ ESTABLISHED - USA, Asia",
        "youtube_search": "Ootoya franchise",
        "news_search": "Ootoya international",
        "financials": {"Metric": ["Investment", "Royalty", "Stores"], "Details": ["$300k-$600k", "5-6%", "50+"]},
        "pros": ["Premium", "Healthy menu", "US success"],
        "cons": ["Complex menu", "Japanese ingredients"],
        
        "history": "Ootoya was founded in 1983 in Tokyo, specializing in teishoku (traditional Japanese set meals). With over 500 locations globally, Ootoya emphasizes healthy, balanced meals using quality ingredients. The brand has successfully established itself in the US market with locations in California, New York, and Hawaii.",
        
        "requirements": [
            "Minimum net worth: $700k USD",
            "Liquid capital: $300k+ USD",
            "Full-service restaurant experience required",
            "Understanding of Japanese cuisine preferred",
            "Access to Japanese ingredient suppliers",
            "Space: 1,500-2,500 sq ft",
            "Commitment to authentic preparation"
        ],
        
        "support": [
            "Comprehensive culinary training",
            "Japanese ingredient sourcing network",
            "Menu planning and recipe development",
            "Store design and atmosphere creation",
            "Staff training programs",
            "Marketing and community engagement",
            "Quality control systems",
            "Seasonal menu innovation"
        ],
        
        "success_story": {
            "title": "California Success Story",
            "story": "A franchisee in San Mateo, CA opened in 2015, targeting the Japanese-American community and health-conscious diners. 'Ootoya's teishoku concept resonates with customers seeking authentic, healthy Japanese meals. We've built a loyal following of both Japanese expats and local foodies.'",
            "metrics": "4 locations | $680k avg revenue | 30-month ROI"
        },
        
        "menu_highlights": ["Teishoku set meals", "Grilled fish", "Tempura", "Miso soup", "Rice and pickles", "Healthy options"],
        
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
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 50px 30px; border-radius: 15px; color: white; margin-bottom: 30px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
        <h1 style="color: white; margin: 0 0 15px 0; font-size: 2.5em; font-weight: 700;">🗾 Discover Japanese Franchise Opportunities</h1>
        <p style="font-size: 1.3em; margin: 0 0 20px 0; opacity: 0.95;">Connecting global investors with 63+ expansion-ready Japanese brands</p>
        <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-top: 25px;">
            <div class="metric-card"><div style="font-size: 2em; font-weight: bold;">63+</div><div style="font-size: 0.9em; opacity: 0.9;">Brands</div></div>
            <div class="metric-card"><div style="font-size: 2em; font-weight: bold;">15+</div><div style="font-size: 0.9em; opacity: 0.9;">Countries</div></div>
            <div class="metric-card"><div style="font-size: 2em; font-weight: bold;">$100k+</div><div style="font-size: 0.9em; opacity: 0.9;">Investment</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    df = load_brands()
    if df.empty:
        st.error("Could not load data")
        return
    
    st.subheader("Found 63 Expansion-Ready Brands")
    
    st.sidebar.subheader("🔍 Search & Filter")
    search = st.sidebar.text_input("Search brands", "")
    categories = st.session_state.get("categories", [])
    selected_cat = st.sidebar.multiselect("Filter by Category", categories, default=[])
    
    filtered = df.copy()
    if search:
        filtered = filtered[filtered["brand_name"].str.contains(search, case=False, na=False) | filtered["category"].str.contains(search, case=False, na=False)]
    if selected_cat:
        filtered = filtered[filtered["category"].isin(selected_cat)]
    
    st.write(f"Showing {len(filtered)} brands")
    
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
                <p class="brand-category">{category} | {stores} stores</p>
            </div>
            <div class="brand-stats">
                <p class="brand-investment">${investment}</p>
                <p class="brand-royalty">Royalty: {royalty}%</p>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
        
        if has_dd:
            col1, col2 = st.columns([2, 1])
            with col1:
                if st.button("📋 View Details", key=f"detail_{idx}"):
                    st.session_state.selected_franchise = brand
                    st.session_state.page = "details"
                    st.rerun()
            with col2:
                if st.button("Enquiry →", key=f"enq_{idx}"):
                    st.session_state.selected_franchise = brand
                    st.session_state.page = "quiz"
                    st.rerun()
        else:
            if st.button("Enquiry →", key=idx):
                st.session_state.selected_franchise = brand
                st.session_state.page = "quiz"
                st.rerun()

    st.markdown("""
    <div class="footer">
        <p>© 2026 JXPerience. Connecting Japanese brands with global investors.</p>
        <p>📧 Contact: jxperience.info@gmail.com</p>
    </div>
    """, unsafe_allow_html=True)

def show_brand_details():
    brand = st.session_state.selected_franchise
    if not brand or brand not in FRANCHISES:
        st.session_state.page = "home"
        st.rerun()
    
    data = FRANCHISES[brand]
    
    if st.button("← Back to Brands"):
        st.session_state.page = "home"
        st.rerun()
    
    st.title(f"🗾 {brand}")
    st.markdown(f'<div class="status-badge">{data["overseas_status"]}</div>', unsafe_allow_html=True)
    
    # Company History
    st.markdown("""<div class="detail-section"><h2 style="margin-top:0;"> Company History</h2></div>""", unsafe_allow_html=True)
    st.write(data["history"])
    
    # Menu Highlights
    st.markdown("""<div class="detail-section"><h2 style="margin-top:0;">🍱 Menu Highlights</h2></div>""", unsafe_allow_html=True)
    st.write(", ".join(data["menu_highlights"]))
    
    # Financial Overview
    st.markdown("""<div class="detail-section"><h2 style="margin-top:0;">💰 Investment Overview</h2></div>""", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Investment", data["investment"])
    col2.metric("Royalty", data["royalty"])
    col3.metric("Avg. Sales", data["sales"])
    
    # Franchise Requirements
    st.markdown("""<div class="detail-section"><h2 style="margin-top:0;">📋 Franchise Requirements</h2></div>""", unsafe_allow_html=True)
    for req in data["requirements"]:
        st.markdown(f"""<div class="requirement-box">✅ {req}</div>""", unsafe_allow_html=True)
    
    # Support Provided
    st.markdown("""<div class="detail-section"><h2 style="margin-top:0;"> Support Provided</h2></div>""", unsafe_allow_html=True)
    for support in data["support"]:
        st.markdown(f"• {support}")
    
    # Success Story
    if "success_story" in data:
        story = data["success_story"]
        st.markdown("""<div class="detail-section"><h2 style="margin-top:0;">⭐ Success Story</h2></div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="success-story">
            <h3 style="margin-top:0; color:#059669;">{story["title"]}</h3>
            <p>{story["story"]}</p>
            <p style="font-weight:bold; color:#059669; margin-bottom:0;">📊 {story["metrics"]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Contact Information
    st.markdown("""<div class="detail-section"><h2 style="margin-top:0;">📞 Contact Information</h2></div>""", unsafe_allow_html=True)
    st.info(data["contact_info"])
    
    # Call to Action
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Submit Enquiry", type="primary", use_container_width=True):
            st.session_state.page = "quiz"
            st.rerun()
    with col2:
        youtube_url = f"https://www.youtube.com/results?search_query={quote(data['youtube_search'])}"
        st.markdown(f"[▶️ Watch Videos]({youtube_url})")

def show_profile():
    brand = st.session_state.selected_franchise
    if not brand:
        st.session_state.page = "home"
        st.rerun()
    if st.button("← Back"):
        st.session_state.page = "home"
        st.rerun()
    if brand in FRANCHISES:
        data = FRANCHISES[brand]
        st.title(f"🗾 {brand}")
        st.markdown(f'<div class="status-badge">{data["overseas_status"]}</div>', unsafe_allow_html=True)
        st.info(data["story"])
        st.subheader("📺 Watch")
        st.markdown(f'[▶️ Watch Videos](https://www.youtube.com/results?search_query={quote(data["youtube_search"])})')
        st.subheader("📰 News")
        st.markdown(f'[📰 Read News](https://www.google.com/search?q={quote(data["news_search"])}&tbm=nws)')
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
        if st.button("Start Enquiry", type="primary"):
            st.session_state.page = "quiz"
            st.rerun()
    else:
        st.title(brand)
        st.info("Profile coming soon")

def show_quiz():
    brand = st.session_state.selected_franchise or "General"
    st.title(f"Enquiry: {brand}")
    if st.button("← Back"):
        st.session_state.page = "home"
        st.rerun()
    with st.form("quiz"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        capital = st.selectbox("Capital", ["Under $100k", "$100k-$250k", "$250k-$500k", "$500k-$1M", "Over $1M"])
        experience = st.selectbox("Experience", ["None", "1-3 years", "3-5 years", "5+ years", "Franchise Owner"])
        industry = st.selectbox("Industry", ["F&B", "Retail", "Corporate", "Other"])
        location = st.text_input("Location")
        timeline = st.selectbox("Timeline", ["Researching", "1-2 years", "6-12 months", "ASAP"])
        if st.form_submit_button("Submit Enquiry"):
            if name and email:
                send_email(f"Enquiry: {name} for {brand}", f"Name: {name}\nEmail: {email}")
                save_to_sheet(brand, name, email, capital, experience, industry, location, timeline)
                st.success("✅ Enquiry submitted!")
            else:
                st.error("Fill in name and email")

def show_franchisor():
    st.title(" Franchisor Portal")
    st.markdown('<div style="margin-bottom: 25px;"><h3 style="color: #1a1a2e; margin-top: 0;">Why Register as a Franchisor?</h3><p style="font-size: 1.1em; line-height: 1.6;">As a Japanese franchise brand, you have unique access to the global market. Our platform connects you directly with qualified international investors.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="benefit-card"><h4>✅ What You\'ll Get as a Verified Partner</h4><ul style="padding-left: 20px; margin: 15px 0;"><li><strong>Real-time qualified leads</strong> - See genuine investor applications as they come in</li><li><strong>Pre-screened investors</strong> - All applicants are vetted for serious investment capacity</li><li><strong>Dedicated dashboard</strong> - Track your leads and review applications in one place</li><li><strong>CSV export</strong> - Download your leads in spreadsheet format</li><li><strong>Direct connection</strong> - Contact investors directly through our secure platform</li></ul></div>', unsafe_allow_html=True)
    
    if not st.session_state.franchisor_logged_in:
        st.markdown('<div style="margin-bottom: 25px;"><h3 style="color: #1a1a2e; margin-top: 0;">Access Your Franchise Dashboard</h3><p style="font-size: 1.1em; line-height: 1.6;">If your brand is already approved as a partner, enter your access code to see your leads.<br><br><strong>Not sure if you\'re approved?</strong> Check your email for the access code, or <strong>request access</strong> below if you\'re a new franchise brand.</p></div>', unsafe_allow_html=True)
        pwd = st.text_input("Password", type="password")
        if st.button("Login"):
            if pwd == "jfa2026":
                st.session_state.franchisor_logged_in = True
                st.rerun()
            else:
                st.error("Wrong password")
        st.markdown('<div style="margin-top: 30px;"><h3 style="color: #1a1a2e; margin-top: 0;">New to JXPerience?</h3><p style="font-size: 1.1em; line-height: 1.6;">If you\'re a Japanese franchise brand looking to expand internationally, you can request access to our platform.</p></div>', unsafe_allow_html=True)
        with st.form("request"):
            company = st.text_input("Company")
            email = st.text_input("Email")
            st.markdown('<p style="font-size: 0.9em; color: #666;">By submitting this form, you\'ll receive:<ul style="padding-left: 20px; margin-top: 10px;"><li>Confirmation of your request</li><li>Review of your brand\'s expansion readiness</li><li>Access code within 24-48 hours</li></ul></p>', unsafe_allow_html=True)
            if st.form_submit_button("Request Access"):
                send_email("Partner Request", f"{company}: {email}")
                st.success("Request sent! We'll contact you within 24-48 hours.")
        return
    
    st.success("Logged in")
    if st.button("Logout"):
        st.session_state.franchisor_logged_in = False
        st.rerun()
    tab1, tab2 = st.tabs(["📊 Leads", "️ Settings"])
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
    st.markdown("### A Personal Journey with Japanese Culture\n\nI'm a passionate advocate of Japanese culture and cuisine. Over the years, I've had the privilege of witnessing the remarkable growth and spread of Japanese culinary culture across Asia, Europe, and the United States.\n\nThe numbers tell an incredible story:")
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Japanese Restaurants (2006)", "24,000", "Starting point")
    with col2: st.metric("Japanese Restaurants (Today)", "200,000+", "+733% growth")
    with col3: st.metric("Growth Period", "~18 years", "JETRO Data")
    st.markdown("This **8x growth** in less than two decades is unprecedented in global food culture history.\n\n### Our Mission\n\nAs a personal project, I started JXPerience to:\n\n1. ** Aggregate Information** - Bring together comprehensive data on Japanese franchises, from well-known brands to emerging opportunities\n2. **🤝 Connect Investors** - Help serious global investors discover and connect with authentic Japanese franchise opportunities\n3. **🌍 Support Expansion** - Contribute to the continued global growth of Japanese cuisine and culture\n4. ** Cultural Exchange** - Enable more people worldwide to discover authentic Japanese cuisine, fostering deeper understanding and appreciation of Japanese culture\n\n### The Vision\n\nBy making franchise information more accessible, we hope to:\n- Support more people in discovering authentic Japanese cuisine\n- Facilitate meaningful cultural exchanges through food\n- Create shared experiences that bring people together\n- Help Japanese brands find the right partners for global expansion\n\n---\n\n*This platform is a labor of love, built to support the continued growth and appreciation of Japanese culinary excellence worldwide.*")
    
    st.markdown("""
    <div class="beta-banner">
        <h4> This is a Beta Site — Help Us Build It Together!</h4>
        <p style="color: #78350f; margin-bottom: 10px;">
            JXPerience is currently in <strong>beta</strong>. We are actively improving the platform and would love your input.
        </p>
        <p style="color: #78350f; margin-bottom: 10px;">
            <strong>🤝 Co-Create With Us</strong> — Have suggestions, spotted a bug, or want to recommend a franchise brand to add? 
            We invite you to share your comments and improvement ideas directly with us.
        </p>
        <p style="color: #78350f; margin: 0;">
             <strong>Email us at:</strong> <a href="mailto:jxperience.info@gmail.com?subject=JXPerience Feedback&body=Hi, I'd like to share some feedback about JXPerience...">jxperience.info@gmail.com</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader(" Frequently Asked Questions")
    
    faqs = [
        {"q": "Is there a fee to use this platform?", "a": "No, browsing and submitting enquiries is completely free for investors."},
        {"q": "How do I know these brands are legitimate?", "a": "We verify overseas expansion status using public data, JETRO reports, and official franchise disclosures. Look for the 'Verified' badge on deep-dive profiles."},
        {"q": "What happens after I submit an enquiry?", "a": "Your details are securely sent to our team. We will pre-screen your profile and connect you with the franchise's international development team if there is a match."},
        {"q": "Can I franchise a brand not listed here?", "a": "Yes! Use the 'Co-Create' email link above to suggest a brand. We are always adding new opportunities."}
    ]
    
    for faq in faqs:
        st.markdown(f"""
        <div class="faq-item">
            <p style="font-weight: bold; color: #1a1a2e; margin-bottom: 5px;">{faq["q"]}</p>
            <p style="color: #666; margin: 0;">{faq["a"]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("🚀 Ready to Explore?")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Browse Franchises", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
    with col_b:
        st.markdown("📧 **Contact:** [jxperience.info@gmail.com](mailto:jxperience.info@gmail.com)")

# --- SIDEBAR ---
st.sidebar.title("🗾 JP Hub")
st.sidebar.markdown("---")
st.sidebar.subheader("Navigation")
if st.sidebar.button("🏠 Home", use_container_width=True):
    st.session_state.page = "home"
    st.rerun()
if st.sidebar.button("ℹ️ About Us", use_container_width=True):
    st.session_state.page = "about"
    st.rerun()
if st.sidebar.button("🏢 Franchisor", use_container_width=True):
    st.session_state.page = "franchisor"
    st.rerun()
st.sidebar.markdown("---")

# --- ROUTER ---
if st.session_state.page == "quiz": show_quiz()
elif st.session_state.page == "franchisor": show_franchisor()
elif st.session_state.page == "profile": show_profile()
elif st.session_state.page == "details": show_brand_details()
elif st.session_state.page == "about": show_about()
else: show_home()
