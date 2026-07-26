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

# --- TRANSLATIONS (Phase 3: 4 Languages) ---
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
    },
    "简体中文": {
        "sidebar_title": " JP Hub", "nav_header": "导航", "home": "🏠 首页", "about": "ℹ️ 关于我们", "franchisor": "🏢 特许经营商",
        "search_header": "🔍 搜索和筛选", "search_placeholder": "搜索品牌", "filter_category": "按类别筛选", "choose_options": "选择选项",
        "hero_title": " 发现日本特许经营机会", "hero_subtitle": "连接63+个准备扩张的日本品牌与全球投资者",
        "metric_brands": "品牌", "metric_countries": "国家", "metric_investment": "投资",
        "found_brands": "找到63个可扩张品牌", "showing_brands": "显示 {count} 个品牌", "stores": "门店", "royalty": "版税",
        "view_details": " 查看详情", "enquiry": "咨询 →",
        "footer_text": "© 2026 JXPerience. 连接日本品牌与全球投资者。", "footer_contact": "📧 联系: jxperience.info@gmail.com",
        "back_brands": "← 返回品牌列表", "company_history": " 公司历史", "menu_highlights": "🍱 菜单亮点", "investment_overview": "💰 投资概览",
        "requirements": "📋 特许经营要求", "support": "🤝 支持服务", "success_story": "⭐ 成功案例", "contact_info": "📞 联系信息",
        "submit_enquiry": "📝 提交咨询", "watch_videos": "▶️ 观看视频",
        "enquiry_title": "咨询: {brand}", "back": "← 返回", "name": "姓名", "email": "邮箱", "capital": "资金", "experience": "经验", "industry": "行业", "location": "地点", "timeline": "时间线",
        "submit": "提交咨询", "success_msg": "✅ 咨询已提交！", "error_msg": "请填写姓名和邮箱",
        "cap_under": "低于$100k", "cap_100_250": "$100k-$250k", "cap_250_500": "$250k-$500k", "cap_500_1m": "$500k-$1M", "cap_over": "超过$1M",
        "exp_none": "无", "exp_1_3": "1-3年", "exp_3_5": "3-5年", "exp_5_plus": "5年以上", "exp_owner": "特许经营商",
        "ind_fb": "餐饮", "ind_retail": "零售", "ind_corp": "企业", "ind_other": "其他",
        "time_research": "研究中", "time_1_2": "1-2年", "time_6_12": "6-12个月", "time_asap": "尽快",
        "about_title": " 关于JXPerience", "about_caption": "我们的使命与故事", "why_started": "为什么开始", "faq_title": "❓ 常见问题",
        "ready_explore": " 准备好探索了吗？", "browse": "浏览品牌", "contact_label": "📧 **联系:**",
        "franchisor_title": " 特许经营商门户", "why_register": "为什么注册为特许经营商？", "what_you_get": "✅ 作为认证合作伙伴您将获得",
        "access_dashboard": "访问您的特许经营仪表板", "new_to_jx": "JXPerience新手？", "password": "密码", "login": "登录", "wrong_password": "密码错误",
        "company": "公司名称", "request_access": "请求访问", "request_sent": "请求已发送！我们将在24-48小时内联系您。", "logged_in": "已登录", "logout": "登出",
        "leads": "📊 线索", "settings": "⚙️ 设置", "found_leads": "✅ 找到 {count} 个真实线索！", "download_csv": "📥 下载CSV", "no_leads": "暂无线索", "settings_soon": "设置即将推出",
        "language": "🌐 语言",
    },
    "한국어": {
        "sidebar_title": " JP 허브", "nav_header": "내비게이션", "home": "🏠 홈", "about": "ℹ️ 우리에 대해", "franchisor": "🏢 프랜차이저",
        "search_header": "🔍 검색 및 필터", "search_placeholder": "브랜드 검색", "filter_category": "카테고리별 필터", "choose_options": "옵션 선택",
        "hero_title": " 일본 프랜차이즈 기회 발견", "hero_subtitle": "63+개의 확장 준비된 일본 브랜드와 글로벌 투자자 연결",
        "metric_brands": "브랜드", "metric_countries": "국가", "metric_investment": "투자",
        "found_brands": "63개의 확장 준비 브랜드 발견", "showing_brands": "{count}개 브랜드 표시", "stores": "매장", "royalty": "로열티",
        "view_details": " 상세 정보 보기", "enquiry": "문의 →",
        "footer_text": "© 2026 JXPerience. 일본 브랜드와 글로벌 투자자 연결.", "footer_contact": "📧 연락처: jxperience.info@gmail.com",
        "back_brands": "← 브랜드 목록으로 돌아가기", "company_history": " 회사 역사", "menu_highlights": "🍱 메뉴 하이라이트", "investment_overview": "💰 투자 개요",
        "requirements": "📋 프랜차이즈 요구사항", "support": "🤝 지원 제공", "success_story": "⭐ 성공 사례", "contact_info": "📞 연락 정보",
        "submit_enquiry": "📝 문의 제출", "watch_videos": "▶️ 동영상 보기",
        "enquiry_title": "문의: {brand}", "back": "← 뒤로", "name": "이름", "email": "이메일", "capital": "자본", "experience": "경험", "industry": "업종", "location": "위치", "timeline": "타임라인",
        "submit": "문의 제출", "success_msg": "✅ 문의가 제출되었습니다!", "error_msg": "이름과 이메일을 입력하세요",
        "cap_under": "$100k 미만", "cap_100_250": "$100k-$250k", "cap_250_500": "$250k-$500k", "cap_500_1m": "$500k-$1M", "cap_over": "$1M 초과",
        "exp_none": "없음", "exp_1_3": "1-3년", "exp_3_5": "3-5년", "exp_5_plus": "5년 이상", "exp_owner": "프랜차이즈 소유자",
        "ind_fb": "식음료", "ind_retail": "소매", "ind_corp": "기업", "ind_other": "기타",
        "time_research": "연구 중", "time_1_2": "1-2년", "time_6_12": "6-12개월", "time_asap": "가급적 빠르게",
        "about_title": " JXPerience에 대해", "about_caption": "우리의 미션과 이야기", "why_started": "시작한 이유", "faq_title": "❓ 자주 묻는 질문",
        "ready_explore": " 탐색 준비가 되셨나요?", "browse": "브랜드 둘러보기", "contact_label": "📧 **연락처:**",
        "franchisor_title": " 프랜차이저 포털", "why_register": "왜 프랜차이저로 등록해야 하나요?", "what_you_get": "✅ 인증 파트너로서 얻는 것",
        "access_dashboard": "프랜차이즈 대시보드 액세스", "new_to_jx": "JXPerience가 처음이신가요?", "password": "비밀번호", "login": "로그인", "wrong_password": "잘못된 비밀번호",
        "company": "회사 이름", "request_access": "액세스 요청", "request_sent": "요청이 전송되었습니다! 24-48시간 내에 연락드리겠습니다.", "logged_in": "로그인됨", "logout": "로그아웃",
        "leads": "📊 리드", "settings": "⚙️ 설정", "found_leads": "✅ {count}개의 실제 리드 발견!", "download_csv": "📥 CSV 다운로드", "no_leads": "리드가 없습니다", "settings_soon": "설정 준비 중",
        "language": "🌐 언어",
    },
    "ไทย": {
        "sidebar_title": " JP Hub", "nav_header": "การนำทาง", "home": "🏠 หน้าหลัก", "about": "ℹ️ เกี่ยวกับเรา", "franchisor": "🏢 ผู้ให้สิทธิ์",
        "search_header": "🔍 ค้นหาและกรอง", "search_placeholder": "ค้นหาแบรนด์", "filter_category": "กรองตามประเภท", "choose_options": "เลือกตัวเลือก",
        "hero_title": " ค้นพบโอกาสแฟรนไชส์ญี่ปุ่น", "hero_subtitle": "เชื่อมต่อนักลงทุนทั่วโลกกับแบรนด์ญี่ปุ่น 63+ ที่พร้อมขยายตัว",
        "metric_brands": "แบรนด์", "metric_countries": "ประเทศ", "metric_investment": "การลงทุน",
        "found_brands": "พบแบรนด์ที่พร้อมขยายตัว 63 แบรนด์", "showing_brands": "แสดง {count} แบรนด์", "stores": "สาขา", "royalty": "ค่าลิขสิทธิ์",
        "view_details": " ดูรายละเอียด", "enquiry": "สอบถาม →",
        "footer_text": "© 2026 JXPerience. เชื่อมต่อแบรนด์ญี่ปุ่นกับนักลงทุนทั่วโลก", "footer_contact": "📧 ติดต่อ: jxperience.info@gmail.com",
        "back_brands": "← กลับไปที่รายการแบรนด์", "company_history": " ประวัติบริษัท", "menu_highlights": "🍱 จุดเด่นเมนู", "investment_overview": "💰 ภาพรวมการลงทุน",
        "requirements": "📋 ข้อกำหนดแฟรนไชส์", "support": "🤝 การสนับสนุน", "success_story": "⭐ กรณีศึกษาความสำเร็จ", "contact_info": "📞 ข้อมูลการติดต่อ",
        "submit_enquiry": "📝 ส่งคำถาม", "watch_videos": "▶️ ดูวิดีโอ",
        "enquiry_title": "สอบถาม: {brand}", "back": "← กลับ", "name": "ชื่อ", "email": "อีเมล", "capital": "เงินทุน", "experience": "ประสบการณ์", "industry": "อุตสาหกรรม", "location": "สถานที่", "timeline": "ช่วงเวลา",
        "submit": "ส่งคำถาม", "success_msg": "✅ ส่งคำถามแล้ว!", "error_msg": "กรุณากรอกชื่อและอีเมล",
        "cap_under": "ต่ำกว่า $100k", "cap_100_250": "$100k-$250k", "cap_250_500": "$250k-$500k", "cap_500_1m": "$500k-$1M", "cap_over": "เกิน $1M",
        "exp_none": "ไม่มี", "exp_1_3": "1-3 ปี", "exp_3_5": "3-5 ปี", "exp_5_plus": "5+ ปี", "exp_owner": "ผู้ให้สิทธิ์",
        "ind_fb": "อาหารและเครื่องดื่ม", "ind_retail": "ค้าปลีก", "ind_corp": "องค์กร", "ind_other": "อื่นๆ",
        "time_research": "กำลังศึกษา", "time_1_2": "1-2 ปี", "time_6_12": "6-12 เดือน", "time_asap": "โดยเร็วที่สุด",
        "about_title": " เกี่ยวกับ JXPerience", "about_caption": "ภารกิจและเรื่องราวของเรา", "why_started": "ทำไมเราจึงเริ่มต้น", "faq_title": "❓ คำถามที่พบบ่อย",
        "ready_explore": " พร้อมที่จะสำรวจหรือยัง?", "browse": "ดูแบรนด์", "contact_label": "📧 **ติดต่อ:**",
        "franchisor_title": " พอร์ทัลผู้ให้สิทธิ์", "why_register": "ทำไมต้องลงทะเบียนเป็นผู้ให้สิทธิ์?", "what_you_get": "✅ สิ่งที่คุณจะได้รับเป็นพันธมิตรที่ได้รับการรับรอง",
        "access_dashboard": "เข้าถึงแดชบอร์ดแฟรนไชส์ของคุณ", "new_to_jx": "JXPerience สำหรับผู้เริ่มต้น?", "password": "รหัสผ่าน", "login": "เข้าสู่ระบบ", "wrong_password": "รหัสผ่านไม่ถูกต้อง",
        "company": "ชื่อบริษัท", "request_access": "ขอสิทธิ์เข้าถึง", "request_sent": "ส่งคำขอแล้ว! เราจะติดต่อกลับภายใน 24-48 ชั่วโมง", "logged_in": "เข้าสู่ระบบแล้ว", "logout": "ออกจากระบบ",
        "leads": "📊 ลูกค้า", "settings": "⚙️ ตั้งค่า", "found_leads": "✅ พบ {count} ลูกค้าจริง!", "download_csv": "📥 ดาวน์โหลด CSV", "no_leads": "ยังไม่มีลูกค้า", "settings_soon": "ตั้งค่าเร็วๆ นี้",
        "language": "🌐 ภาษา",
    }
}

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'selected_franchise' not in st.session_state: st.session_state.selected_franchise = None
if 'franchisor_logged_in' not in st.session_state: st.session_state.franchisor_logged_in = False
if 'categories' not in st.session_state: st.session_state.categories = []
if 'language' not in st.session_state: 
    # Detect browser language
    st.session_state.language = 'English'
    try:
        browser_lang = st.query_params.get('language') or st.query_params.get('lang')
        if browser_lang and browser_lang in TRANSLATIONS.keys():
            st.session_state.language = browser_lang
    except:
        pass

# --- TRANSLATION HELPER ---
def t(key, **kwargs):
    lang = st.session_state.language
    text = TRANSLATIONS.get(lang, TRANSLATIONS["English"]).get(key, key)
    return text.format(**kwargs) if kwargs else text

# --- MOBILE-READY CSS ---
st.markdown("""
<style>
    /* Base styles */
    .main { background-color: #f8f9fa; }
    h1, h2, h3 { color: #1a1a2e; font-weight: 700; margin-bottom: 1rem; }
    .stButton>button { border-radius: 8px; font-weight: 600; padding: 0.5rem 1.5rem; transition: all 0.3s ease; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
    .metric-card { background: rgba(255,255,255,0.2); padding: 15px 25px; border-radius: 10px; backdrop-filter: blur(10px); }
    .status-badge { display: inline-block; background: #10b981; color: white; padding: 8px 16px; border-radius: 20px; font-weight: 600; margin-bottom: 20px; }
    .benefit-card { background: #f0f7ff; border-left: 4px solid #667eea; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    .benefit-card h4 { color: #1a1a2e; margin-top: 0; }
    
    /* Mobile-specific */
    @media (max-width: 768px) {
        .main { padding: 0 10px; }
        h1 { font-size: 1.8em; }
        h2 { font-size: 1.5em; }
        h3 { font-size: 1.3em; }
        .stButton>button { padding: 0.5rem 1rem; font-size: 0.9em; }
        .metric-card { padding: 10px 15px; }
        .brand-row { padding: 15px 10px; }
        .brand-logo-wrapper { width: 50px; height: 50px; font-size: 1.4em; }
        .brand-name { font-size: 1.0em; }
        .brand-category { font-size: 0.8em; }
        .brand-stats { text-align: left; }
        .brand-royalty, .brand-investment { font-size: 0.8em; }
        .detail-section { padding: 15px; }
        .footer { padding: 10px; }
    }
    
    /* Card styling */
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
    
    /* Beta banner */
    .beta-banner {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .beta-banner h4 { color: #92400e; margin-top: 0; margin-bottom: 10px; }
    
    /* FAQ items */
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

# --- TRANSLATED CONTENT (Phase 3: 4 Languages) ---
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

FRANCHISES_ZH = {
    "Yoshinoya": {"story": "世界知名的牛丼连锁店，拥有1,000多家门店。", "overseas_status": "✅ 积极招募 - 美国、亚洲、中东", "history": "1899年创立于东京鱼市场，吉野家是日本最古老的快餐连锁之一。专注于牛丼（牛肉碗），目前已在全球1,200多家门店运营。", "requirements": ["最低净资产：40万美元", "流动资金：15万美元以上", "餐饮经验优先", "人流量大的位置：800-1,500平方英尺"], "support": ["初期培训（2-4周）", "选址协助", "店铺设计包", "牛肉供应链", "营销支持"], "success_story": {"title": "加利福尼亚成功", "story": "2018年在洛杉矶开设。'牛丼概念深受健康意识强的美国人欢迎。'", "metrics": "5家门店 | 平均收入$520k | 22个月ROI"}, "menu_highlights": ["牛丼（牛肉碗）", "鸡肉照烧", "炸鸡", "味噌汤"], "contact_info": "国际：overseas@yoshinoya.com | +81-3-5555-1111"},
    "Sushiro": {"story": "日本最大的回转寿司连锁店，拥有600多家门店。", "overseas_status": "✅ 拓展中 - 亚洲、美国", "history": "1995年成立，已成为日本最大的回转寿司连锁店。以提供价格实惠的高品质寿司而闻名。", "requirements": ["最低净资产：80万美元", "流动资金：25万美元以上", "必须有餐饮经验", "宽敞空间：2,000-3,500平方英尺"], "support": ["寿司师傅培训", "回转带安装", "新鲜鱼类供应链", "技术系统"], "success_story": {"title": "香港拓展", "story": "2018年获得香港特许经营权。现已在香港各地开设15家门店。", "metrics": "15家门店 | 平均收入$850k | 26个月ROI"}, "menu_highlights": ["回转寿司", "每日新鲜鱼类", "触摸屏点餐", "季节性特色菜"], "contact_info": "特许经营：franchise@sushiro.co.jp | +81-6-5555-2222"},
    "Coco Ichibanya": {"story": "日本最大的咖喱屋，拥有1,300多家门店。", "overseas_status": "✅ 积极招募 - 美国、亚洲、欧洲", "history": "1978年创立于爱知县。通过可定制的香料水平革新了日本咖喱。现已有1,300多家日本门店和200多家国际门店。", "requirements": ["最低净资产：50万美元", "流动资金：15万美元以上", "日本8周培训", "空间：1,500-2,500平方英尺"], "support": ["日本8周培训", "选址", "店铺设计", "设备支持", "持续咨询"], "success_story": {"title": "泰国成功", "story": "2015年在曼谷开设首家门店。3年内扩展至12家门店。", "metrics": "12家门店 | 平均收入$540k | 18个月ROI"}, "menu_highlights": ["日本咖喱饭", "炸猪排咖喱", "芝士咖喱", "20多种配料"], "contact_info": "国际：international@coco-curry.com | +81-3-5555-1234"},
    "Pepper Lunch": {"story": "拥有200多家门店的铁板牛排快餐概念，在15多个国家。", "overseas_status": "✅ 非常活跃 - 15多个国家", "history": "1994年由市濑国雄厨师创立。革命性的DIY用餐体验，顾客在热铁板上自己烹饪。已拓展到15多个国家。", "requirements": ["最低净资产：60万美元", "流动资金：20万美元以上", "必须有餐饮经验", "人流量大的位置"], "support": ["4周培训", "店铺设计", "铁板技术", "营销", "R&D支持"], "success_story": {"title": "新加坡成功", "story": "2012年在新加坡乌节路开设首家门店。现已在SG和MY开设8家门店。", "metrics": "8家门店 | 平均收入$650k | 24个月ROI"}, "menu_highlights": ["铁板牛排", "三文鱼", "辣味咖喱牛排", "3分钟烹饪"], "contact_info": "特许经营：franchise@pepperlunch.com | +81-3-5555-5678"},
    "Kura Sushi": {"story": "在美国拓展的高科技回转寿司。", "overseas_status": "✅ 美国拓展中", "history": "1999年在奈良成立。以触摸屏点餐、自动回转带系统和游戏化用餐体验而闻名。2013年上市。", "requirements": ["最低净资产：150万美元", "流动资金：50万美元以上", "多家门店经验优先", "空间：3,000-5,000平方英尺"], "support": ["12周培训", "回转带系统", "POS技术", "寿司师傅认证", "鱼类供应链"], "success_story": {"title": "加利福尼亚拓展", "story": "2019年在欧文开设首家门店。吸引了精通技术的千禧一代和家庭。", "metrics": "3家门店 | 平均收入$1.2M | 36个月ROI"}, "menu_highlights": ["高级回转寿司", "触摸屏点餐", "抽奖系统", "清酒选择"], "contact_info": "美国：usa@kurasushi.com | +1-949-555-0123"},
    "Sukiya": {"story": "日本最大的牛丼连锁店，拥有2,000多家门店。", "overseas_status": "✅ 严格筛选 - 亚洲重点", "history": "1982年创立。日本最大的牛丼连锁店，拥有2,000多家门店。作为Zenrin集团一员。以24小时营业而闻名。", "requirements": ["最低净资产：80万美元", "流动资金：30万美元以上", "多家门店QSR经验", "优先考虑特许经营"], "support": ["特许经营支持", "培训计划", "牛肉供应链", "店铺布局", "营销"], "success_story": {"title": "香港支配力", "story": "2010年以来的特许经营者。现已在香港和澳门开设35家门店。", "metrics": "35家门店 | 平均收入$850k | 20个月ROI"}, "menu_highlights": ["牛丼", "各种尺寸", "配菜", "24/7营业"], "contact_info": "国际：overseas@sukiya.co.jp | +81-45-555-9876"},
    "Hoshino Coffee": {"story": "以煎饼闻名的名古屋高级咖啡店。", "overseas_status": "✅ 亚洲活跃中", "history": "1978年在名古屋成立。以松软煎饼和复古昭和时代氛围而闻名。正在亚洲各地拓展。", "requirements": ["最低净资产：60万美元", "流动资金：25万美元以上", "咖啡店经验优先", "高级位置", "空间：1,200-2,000平方英尺"], "support": ["咖啡师培训", "煎饼制作", "室内设计", "设备采购", "菜单开发"], "success_story": {"title": "台湾高级成功", "story": "2016年在台北开设首家门店。复古氛围立即引起轰动。", "metrics": "6家门店 | 平均收入$420k | 28个月ROI"}, "menu_highlights": ["松软煎饼", "手冲咖啡", "早餐套餐", "复古氛围"], "contact_info": "亚洲：asia@hoshino-coffee.com | +81-52-555-4321"},
    "Ootoya": {"story": "拥有500多家门店的高级定食餐厅。", "overseas_status": "✅ 已确立 - 美国、亚洲", "history": "1983年在东京创立。专注于定食（传统日本套餐）。在全球拥有500多家门店，美国市场影响力强大。", "requirements": ["最低净资产：70万美元", "流动资金：30万美元以上", "全方位餐饮店经验", "空间：1,500-2,500平方英尺"], "support": ["烹饪培训", "食材采购", "菜单规划", "店铺设计", "员工培训"], "success_story": {"title": "加利福尼亚成功", "story": "2015年在圣马特奥开业。针对日裔美国人和注重健康的顾客。", "metrics": "4家门店 | 平均收入$680k | 30个月ROI"}, "menu_highlights": ["定食套餐", "烤鱼", "天妇罗", "健康选择"], "contact_info": "特许经营：franchise@otoya.co.jp | +81-3-5555-7890"}
}

FRANCHISES_KO = {
    "Yoshinoya": {"story": "세계적으로 유명한 규동 체인. 일본에 1,000개 이상, 해외에 200개 이상의 매장 보유.", "overseas_status": "✅ 적극 모집 - 미국, 아시아, 중동", "history": "1899년 도쿄 어시장에서 창업한 요시노야는 일본에서 가장 오래된 패스트푸드 체인 중 하나입니다. 규동(소고기 덮밥) 전문으로, 현재 전 세계 1,200개 이상의 매장에서 운영되고 있습니다.", "requirements": ["최소 순자산: 40만 달러", "유동 자본: 15만 달러 이상", "음식점 경험 우선", "고객이 많은 위치: 800-1,500 제곱피트"], "support": ["초기 교육(2-4주)", "출점 지원", "매장 디자인 패키지", "소고기 공급망", "마케팅 지원"], "success_story": {"title": "캘리포니아 성공", "story": "2018년 로스앤젤레스에 개점. '규동 컨셉트는 건강 의식이 높은 미국인들에게 호응을 얻고 있습니다.'", "metrics": "5개 매장 | 평균 매출 $520k | 22개월 ROI"}, "menu_highlights": ["규동(소고기 덮밥)", "치킨 테리야끼", "가라아게", "미소스프"], "contact_info": "국제 프랜차이즈: overseas@yoshinoya.com | +81-3-5555-1111"},
    "Sushiro": {"story": "일본 최대 회전 초밥 체인. 600개 이상의 매장 보유.", "overseas_status": "✅ 확장 중 - 아시아, 미국", "history": "1995년 설립되어 일본 최대 회전 초밥 체인으로 성장했습니다. 합리적인 가격으로 고품질 초밥을 제공함으로써 유명합니다.", "requirements": ["최소 순자산: 80만 달러", "유동 자본: 25만 달러 이상", "음식점 경험 필수", "넓은 공간: 2,000-3,500 제곱피트"], "support": ["초밥 셰프 교육", "회전 벨트 설치", "신선한 생선 공급망", "테크놀로지 시스템"], "success_story": {"title": "홍콩 확장", "story": "2018년 홍콩 마스터 프랜차이즈 권한을 획득. 현재 홍콩 전역에 15개 매장 보유.", "metrics": "15개 매장 | 평균 매출 $850k | 26개월 ROI"}, "menu_highlights": ["회전 초밥", "매일 신선한 생선", "터치스크린 주문", "계절별 특별 메뉴"], "contact_info": "프랜차이즈: franchise@sushiro.co.jp | +81-6-5555-2222"},
    "Coco Ichibanya": {"story": "일본 최대 카레 하우스. 1,300개 이상의 매장 보유.", "overseas_status": "✅ 적극 모집 - 미국, 아시아, 유럽", "history": "1978년 아이치현에서 창업. 사용자 정의 가능한 스파이스 레벨로 일본 카레에 혁명을 일으켰습니다. 현재 일본 내 1,300개 이상, 해외 200개 이상의 매장이 있습니다.", "requirements": ["최소 순자산: 50만 달러", "유동 자본: 15만 달러 이상", "일본 8주 교육", "공간: 1,500-2,500 제곱피트"], "support": ["일본 8주 교육", "출점 지원", "매장 디자인", "설비 지원", "지속적인 컨설팅"], "success_story": {"title": "태국 성공", "story": "2015년 방콕 1호점 개점. 3년 내 12개 매장으로 확대.", "metrics": "12개 매장 | 평균 매출 $540k | 18개월 ROI"}, "menu_highlights": ["일본 카레 라이스", "카츠 카레", "치즈 카레", "20가지 이상의 토핑"], "contact_info": "국제 개발: international@coco-curry.com | +81-3-5555-1234"},
    "Pepper Lunch": {"story": "15개 이상의 국가에 200개 이상의 매장을 보유한 철판 스테이크 패스트푸드.", "overseas_status": "✅ 매우 활발 - 15개 이상의 국가", "history": "1994년 시내국웅 셰프에 의해 창업. 뜨거운 철판에서 고객이 직접 요리하는 혁명적인 DIY 다이닝. 15개 이상의 국가로 확장되었습니다.", "requirements": ["최소 순자산: 60만 달러", "유동 자본: 20만 달러 이상", "음식점 경험 필수", "고객이 많은 위치"], "support": ["4주 교육", "매장 디자인", "철판 기술", "마케팅", "R&D 지원"], "success_story": {"title": "싱가포르 성공", "story": "2012년 싱가포르 오차드로드 1호점 개점. 현재 SG와 MY에 8개 매장 보유.", "metrics": "8개 매장 | 평균 매출 $650k | 24개월 ROI"}, "menu_highlights": ["철판 비프 스테이크", "サーモン 무니에르", "스파이시 카레 비프", "3분 조리"], "contact_info": "프랜차이즈: franchise@pepperlunch.com | +81-3-5555-5678"},
    "Kura Sushi": {"story": "미국에서 확장 중인 하이테크 회전 초밥.", "overseas_status": "✅ 미국 확장 중", "history": "1999년 나라에서 설립. 터치스크린 주문, 자동 회전 벨트 시스템, 게임화된 다이닝으로 유명합니다. 2013년 상장.", "requirements": ["최소 순자산: 150만 달러", "유동 자본: 50만 달러 이상", "다수 매장 경험 우선", "공간: 3,000-5,000 제곱피트"], "support": ["12주 교육", "회전 벨트 시스템", "POS 테크놀로지", "초밥 셰프 인증", "생선 공급망"], "success_story": {"title": "캘리포니아 확장", "story": "2019년 어바인 1호점 개점. 기술에 능통한 밀레니엄 세대와 가족에게 호응을 얻고 있습니다.", "metrics": "3개 매장 | 평균 매출 $1.2M | 36개월 ROI"}, "menu_highlights": ["프리미엄 회전 초밥", "터치스크린 주문", "추첨 시스템", "사케 선택"], "contact_info": "미국: usa@kurasushi.com | +1-949-555-0123"},
    "Sukiya": {"story": "일본 최대 규동 체인. 2,000개 이상의 매장 보유.", "overseas_status": "✅ 엄선 - 아시아 중점", "history": "1982년 창업. 2,000개 이상의 매장을 보유한 일본 최대 규동 체인. 젠린 그룹의 일원입니다. 24시간 영업으로 유명합니다.", "requirements": ["최소 순자산: 80만 달러", "유동 자본: 30만 달러 이상", "다수 매장 QSR 경험", "마스터 프랜차이즈 우선"], "support": ["마스터 프랜차이즈 지원", "교육 프로그램", "소고기 공급망", "매장 레이아웃", "마케팅"], "success_story": {"title": "홍콩 지배력", "story": "2010년 이래 마스터 프랜차이지. 현재 홍콩과 마카오에 35개 매장 보유.", "metrics": "35개 매장 | 평균 매출 $850k | 20개월 ROI"}, "menu_highlights": ["규동", "다양한 크기", "사이드 디쉬", "24/7 영업"], "contact_info": "국제: overseas@sukiya.co.jp | +81-45-555-9876"},
    "Hoshino Coffee": {"story": "팬케이크로 유명한 나고야 프리미엄 커피숍.", "overseas_status": "✅ 아시아 활동 중", "history": "1978년 나고야에서 설립. 부드러운 팬케이크와 레트로 쇼와 시대 분위기로 유명합니다. 아시아 전역에 확장 중입니다.", "requirements": ["최소 순자산: 60만 달러", "유동 자본: 25만 달러 이상", "카페 경험 우선", "프리미엄 위치", "공간: 1,200-2,000 제곱피트"], "support": ["바리스타 교육", "팬케이크 조리", "인테리어 디자인", "설비 조달", "메뉴 개발"], "success_story": {"title": "타이완 프리미엄 성공", "story": "2016년 타이페이 1호점 개점. 레트로 분위기가 즉시 화제를 불러일으켰습니다.", "metrics": "6개 매장 | 평균 매출 $420k | 28개월 ROI"}, "menu_highlights": ["부드러운 팬케이크", "핸드 드립 커피", "모닝 세트", "레트로 분위기"], "contact_info": "아시아: asia@hoshino-coffee.com | +81-52-555-4321"},
    "Ootoya": {"story": "500개 이상의 매장을 보유한 프리미엄 정식 레스토랑.", "overseas_status": "✅ 확립 - 미국, 아시아", "history": "1983년 도쿄에서 창업. 정식(전통 일본 세트 식사) 전문입니다. 전 세계 500개 이상의 매장과 미국 시장에서 강한 존재감을 가지고 있습니다.", "requirements": ["최소 순자산: 70만 달러", "유동 자본: 30만 달러 이상", "풀 서비스 음식점 경험", "공간: 1,500-2,500 제곱피트"], "support": ["요리 교육", "재료 조달", "메뉴 계획", "매장 디자인", "스태프 교육"], "success_story": {"title": "캘리포니아 성공", "story": "2015년 샌 매트오 개점. 일계 미국인과 건강 의식이 높은 고객을 대상으로 합니다.", "metrics": "4개 매장 | 평균 매출 $680k | 30개월 ROI"}, "menu_highlights": ["정식 세트 식사", "구이 물고기", "텐푸라", "건강한 옵션"], "contact_info": "프랜차이즈: franchise@otoya.co.jp | +81-3-5555-7890"}
}

FRANCHISES_TH = {
    "Yoshinoya": {"story": "แบรนด์ gyudon ระดับโลกที่มีมากกว่า 1,000 สาขา", "overseas_status": "✅ รับสมัครอย่างกระตือรือร้น - สหรัฐอเมริกา, เอเชีย, ตะวันออกกลาง", "history": "ก่อตั้งในปี 1899 ที่ตลาดปลาโตเกียว โยชิโนยะเป็นหนึ่งในร้านอาหารฟาสต์ฟูดด์เก่าแก่ที่สุดของญี่ปุ่น ให้บริการ gyudon (ข้าวหน้าเนื้อ) ปัจจุบันมีกว่า 1,200 สาขาทั่วโลก", "requirements": ["มูลค่าสุทธิขั้นต่ำ: 400,000 ดอลลาร์", "เงินทุนหมุนเวียน: 150,000 ดอลลาร์ขึ้นไป", "ประสบการณ์ร้านอาหารเป็นที่ต้องการ", "ทำเลที่มีผู้คนพลุกพล่าน: 800-1,500 ตารางฟุต"], "support": ["การฝึกอบรมเบื้องต้น (2-4 สัปดาห์)", "การช่วยเหลือในการเลือกสถานที่", "แพ็กเกจออกแบบร้าน", "ระบบซัพพลายเชนเนื้อ", "การสนับสนุนการตลาด"], "success_story": {"title": "ความสำเร็จที่แคลิฟอร์เนีย", "story": "ร้านแรกที่ลอสแอนเจลิสเปิดในปี 2018 'แนวคิด gyudon ได้รับความนิยมจากชาวอเมริกันที่ใส่ใจสุขภาพ'", "metrics": "5 สาขา | รายได้เฉลี่ย $520k | ROI 22 เดือน"], "menu_highlights": ["Gyudon (ข้าวหน้าเนื้อ)", "ไก่เทริยากิ", "คาเร็กเกะ", "ซุปมิโสะ"], "contact_info": "สากล: overseas@yoshinoya.com | +81-3-5555-1111"},
    "Sushiro": {"story": "ร้านซูชิสายพานยี่ปุ่นที่ใหญ่ที่สุด 600+ สาขา", "overseas_status": "✅ ขยายตัว - เอเชีย, สหรัฐอเมริกา", "history": "ก่อตั้งในปี 1995 จนกลายเป็นร้านซูชิสายพานที่ใหญ่ที่สุดในญี่ปุ่น ให้บริการซูชิคุณภาพสูงในราคาที่เหมาะสม", "requirements": ["มูลค่าสุทธิขั้นต่ำ: 800,000 ดอลลาร์", "เงินทุนหมุนเวียน: 250,000 ดอลลาร์ขึ้นไป", "ต้องมีประสบการณ์ร้านอาหาร", "พื้นที่กว้าง: 2,000-3,500 ตารางฟุต"], "support": ["การฝึกอบรมพ่อครัวซูชิ", "การติดตั้งสายพาน", "ระบบซัพพลายเชนปลาสด", "ระบบเทคโนโลยี"], "success_story": {"title": "การขยายตัวที่ฮ่องกง", "story": "ได้รับสิทธิ์มาร์เตอร์ฟรานไชส์ในฮ่องกงในปี 2018 ปัจจุบันมี 15 สาขาทั่วฮ่องกง", "metrics": "15 สาขา | รายได้เฉลี่ย $850k | ROI 26 เดือน"], "menu_highlights": ["ซูชิสายพาน", "ปลาสดทุกวัน", "ระบบสั่งอาหารแบบสัมผัส", "เมนูพิเศษตามฤดูกาล"], "contact_info": "ฟรานไชส์: franchise@sushiro.co.jp | +81-6-5555-2222"},
    "Coco Ichibanya": {"story": "ร้านคารีญี่ปุ่นที่ใหญ่ที่สุด 1,300+ สาขา", "overseas_status": "✅ รับสมัครอย่างกระตือรือร้น - สหรัฐอเมริกา, เอเชีย, ยุโรป", "history": "ก่อตั้งในปี 1978 ในจังหวัดไอจิ ปฏิวัติการบริโภคคารีญี่ปุ่นด้วยระดับเครื่องปรุงที่ปรับได้ ปัจจุบันมี 1,300+ สาขาในญี่ปุ่นและ 200+ สาขาต่างประเทศ", "requirements": ["มูลค่าสุทธิขั้นต่ำ: 500,000 ดอลลาร์", "เงินทุนหมุนเวียน: 150,000 ดอลลาร์ขึ้นไป", "การฝึกอบรม 8 สัปดาห์ในญี่ปุ่น", "พื้นที่: 1,500-2,500 ตารางฟุต"], "support": ["การฝึกอบรม 8 สัปดาห์ในญี่ปุ่น", "การช่วยเลือกสถานที่", "การออกแบบร้าน", "การสนับสนุนอุปกรณ์", "การให้คำปรึกษาต่อเนื่อง"], "success_story": {"title": "ความสำเร็จที่ไทย", "story": "สาขาแรกในกรุงเทพฯ เปิดในปี 2015 ขยายเป็น 12 สาขาใน 3 ปี", "metrics": "12 สาขา | รายได้เฉลี่ย $540k | ROI 18 เดือน"], "menu_highlights": ["ข้าวหน้าคารีญี่ปุ่น", "คารีหมูกรอบ", "คารีชีส", "เครื่องปรุงมากกว่า 20 ชนิด"], "contact_info": "สากล: international@coco-curry.com | +81-3-5555-1234"},
    "Pepper Lunch": {"story": "ร้านสเต็กที่ลูกค้าทำเอง 200+ สาขาใน 15+ ประเทศ", "overseas_status": "✅ คึกคักมาก - 15+ ประเทศ", "history": "ก่อตั้งในปี 1994 โดยเชฟคุณ Kunio Ichinose แนวคิดการรับประทานอาหารแบบทำเองบนเหล็กร้อน ขยายตัวไป 15+ ประเทศ", "requirements": ["มูลค่าสุทธิขั้นต่ำ: 600,000 ดอลลาร์", "เงินทุนหมุนเวียน: 200,000 ดอลลาร์ขึ้นไป", "ต้องมีประสบการณ์ร้านอาหาร", "ทำเลที่มีผู้คนพลุกพล่าน"], "support": ["การฝึกอบรม 4 สัปดาห์", "การออกแบบร้าน", "เทคโนโลยีเหล็ก", "การตลาด", "การสนับสนุน R&D"], "success_story": {"title": "ความสำเร็จที่สิงคโปร์", "story": "สาขาแรกที่ออร์ชาร์ดโรดเปิดในปี 2012 ปัจจุบันมี 8 สาขาทั่วสิงคโปร์และมาเลเซีย", "metrics": "8 สาขา | รายได้เฉลี่ย $650k | ROI 24 เดือน"], "menu_highlights": ["สเต็กเนื้อที่เหล็ก", "แซลมอน", "คารีเนื้อเผ็ด", "ปรุง 3 นาที"], "contact_info": "ฟรานไชส์: franchise@pepperlunch.com | +81-3-5555-5678"},
    "Kura Sushi": {"story": "ซูชิสายพานเทคโนโลยีสูงที่ขยายตัวในสหรัฐอเมริกา", "overseas_status": "✅ ขยายตัวในสหรัฐอเมริกา", "history": "ก่อตั้งในปี 1999 ที่นารา รู้จักด้วยการสั่งอาหารแบบสัมผัส ระบบสายพานอัตโนมัติ และประสบการณ์การรับประทานอาหารแบบเกมส์ ขึ้นตลาดในปี 2013", "requirements": ["มูลค่าสุทธิขั้นต่ำ: 1.5 ล้านดอลลาร์", "เงินทุนหมุนเวียน: 500,000 ดอลลาร์ขึ้นไป", "ประสบการณ์หลายสาขาเป็นที่ต้องการ", "พื้นที่: 3,000-5,000 ตารางฟุต"], "support": ["การฝึกอบรม 12 สัปดาห์", "ระบบสายพาน", "เทคโนโลยี POS", "การรับรองพ่อครัวซูชิ", "ระบบซัพพลายเชนปลา"], "success_story": {"title": "การขยายตัวที่แคลิฟอร์เนีย", "story": "สาขาแรกที่ไอร์วินเปิดในปี 2019 ดึงดูดกลุ่มมิลเลนเนียลและครอบครัวที่เชี่ยวชาญด้านเทคโนโลยี", "metrics": "3 สาขา | รายได้เฉลี่ย $1.2M | ROI 36 เดือน"], "menu_highlights": ["ซูชิสายพานพรีเมียม", "ระบบสั่งอาหารแบบสัมผัส", "ระบบจับรางวัล", "เมนูสาเก"], "contact_info": "สหรัฐอเมริกา: usa@kurasushi.com | +1-949-555-0123"},
    "Sukiya": {"story": "ร้าน gyudon ที่ใหญ่ที่สุดในญี่ปุ่น 2,000+ สาขา", "overseas_status": "✅ เลือกสรร - เน้นเอเชีย", "history": "ก่อตั้งในปี 1982 ร้าน gyudon ที่ใหญ่ที่สุดในญี่ปุ่นที่มี 2,000+ สาขา เป็นส่วนหนึ่งของกลุ่ม Zenrin รู้จักด้วยการเปิด 24 ชั่วโมง", "requirements": ["มูลค่าสุทธิขั้นต่ำ: 800,000 ดอลลาร์", "เงินทุนหมุนเวียน: 300,000 ดอลลาร์ขึ้นไป", "ประสบการณ์หลายสาขา QSR", "มาร์เตอร์ฟรานไชส์เป็นที่ต้องการ"], "support": ["การสนับสนุนมาร์เตอร์ฟรานไชส์", "โปรแกรมการฝึกอบรม", "ระบบซัพพลายเชนเนื้อ", "การจัดวางร้าน", "การตลาด"], "success_story": {"title": "อำนาจที่ฮ่องกง", "story": "มาร์เตอร์ฟรานไชส์ตั้งแต่ปี 2010 ปัจจุบันมี 35 สาขาทั่วฮ่องกงและมาเก๊า", "metrics": "35 สาขา | รายได้เฉลี่ย $850k | ROI 20 เดือน"], "menu_highlights": ["Gyudon (ข้าวหน้าเนื้อ)", "ขนาดต่างๆ", "เมนูข้าง", "เปิด 24/7"], "contact_info": "สากล: overseas@sukiya.co.jp | +81-45-555-9876"},
    "Hoshino Coffee": {"story": "ร้านกาแฟพรีเมียมจากนาโกยาที่มีชื่อเสียงเรื่องแพนเค้ก", "overseas_status": "✅ ทำงานในเอเชีย", "history": "ก่อตั้งในปี 1978 ที่นาโกยา มีชื่อเสียงจากแพนเค้กนุ่มและบรรยากาศยุคโชวะที่ย้อนยุค ขยายตัวทั่วเอเชีย", "requirements": ["มูลค่าสุทธิขั้นต่ำ: 600,000 ดอลลาร์", "เงินทุนหมุนเวียน: 250,000 ดอลลาร์ขึ้นไป", "ประสบการณ์ร้านกาแฟเป็นที่ต้องการ", "ทำเลพรีเมียม", "พื้นที่: 1,200-2,000 ตารางฟุต"], "support": ["การฝึกอบรมบาริสต้า", "การปรุงแพนเค้ก", "การออกแบบภายใน", "การจัดหาอุปกรณ์", "การพัฒนาเมนู"], "success_story": {"title": "ความสำเร็จพรีเมียมที่ไต้หวัน", "story": "สาขาแรกที่ไทเปอเปิดในปี 2016 บรรยากาศย้อนยุคสร้างกระแสทันที", "metrics": "6 สาขา | รายได้เฉลี่ย $420k | ROI 28 เดือน"], "menu_highlights": ["แพนเค้กนุ่ม", "กาแฟแบบดรอป", "เมนูเช้า", "บรรยากาศย้อนยุค"], "contact_info": "เอเชีย: asia@hoshino-coffee.com | +81-52-555-4321"},
    "Ootoya": {"story": "ร้านอาหารเซตส์แบบดั้งเดิมพรีเมียมที่มี 500+ สาขา", "overseas_status": "✅ ตั้งรากฐาน - สหรัฐอเมริกา, เอเชีย", "history": "ก่อตั้งในปี 1983 ที่โตเกียว ให้บริการ teishoku (อาหารเซตแบบดั้งเดิมของญี่ปุ่น) มี 500+ สาขาทั่วโลกและมีอิทธิพลในตลาดสหรัฐอเมริกา", "requirements": ["มูลค่าสุทธิขั้นต่ำ: 700,000 ดอลลาร์", "เงินทุนหมุนเวียน: 300,000 ดอลลาร์ขึ้นไป", "ประสบการณ์ร้านอาหารเต็มรูปแบบ", "พื้นที่: 1,500-2,500 ตารางฟุต"], "support": ["การฝึกอบรมด้านการทำอาหาร", "การจัดหาวัตถุดิบ", "การวางแผนเมนู", "การออกแบบร้าน", "การฝึกอบรมพนักงาน"], "success_story": {"title": "ความสำเร็จที่แคลิฟอร์เนีย", "story": "สาขาที่ซานมาเทโอเปิดในปี 2015 เจาะกลุ่มชาวญี่ปุ่น-อเมริกันและผู้ที่ใส่ใจสุขภาพ", "metrics": "4 สาขา | รายได้เฉลี่ย $680k | ROI 30 เดือน"], "menu_highlights": ["เมนูเซต teishoku", "ปลาที่ย่าง", "เทมปุระ", "ตัวเลือกเพื่อสุขภาพ"], "contact_info": "ฟรานไชส์: franchise@otoya.co.jp | +81-3-5555-7890"}
}

# --- CONTENT HELPERS ---
def get_brand(brand):
    base = FRANCHISES.get(brand, {})
    lang = st.session_state.language
    
    if lang == "日本語" and brand in FRANCHISES_JA:
        return {**base, **FRANCHISES_JA[brand]}
    elif lang == "简体中文" and brand in FRANCHISES_ZH:
        return {**base, **FRANCHISES_ZH[brand]}
    elif lang == "한국어" and brand in FRANCHISES_KO:
        return {**base, **FRANCHISES_KO[brand]}
    elif lang == "ไทย" and brand in FRANCHISES_TH:
        return {**base, **FRANCHISES_TH[brand]}
    
    return base

ABOUT_EN = """### A Personal Journey with Japanese Culture\n\nI'm a passionate advocate of Japanese culture and cuisine. Over the years, I've had the privilege of witnessing the remarkable growth and spread of Japanese culinary culture across Asia, Europe, and the United States.\n\nThe numbers tell an incredible story:\n\nThis **8x growth** in less than two decades is unprecedented in global food culture history.\n\n### Our Mission\n\nAs a personal project, I started JXPerience to:\n\n1. **📊 Aggregate Information** - Bring together comprehensive data on Japanese franchises\n2. **🤝 Connect Investors** - Help serious global investors discover authentic Japanese franchise opportunities\n3. **🌍 Support Expansion** - Contribute to the continued global growth of Japanese cuisine\n4. **🍱 Cultural Exchange** - Enable more people worldwide to discover authentic Japanese cuisine\n\n### The Vision\n\nBy making franchise information more accessible, we hope to:\n- Support more people in discovering authentic Japanese cuisine\n- Facilitate meaningful cultural exchanges through food\n- Create shared experiences that bring people together\n- Help Japanese brands find the right partners for global expansion\n\n---\n\n*This platform is a labor of love, built to support the continued growth and appreciation of Japanese culinary excellence worldwide.*"""

ABOUT_JA = """### 日本文化との個人的な旅\n\n私は日本文化と日本料理の熱心な支持者です。長年にわたり、アジア、ヨーロッパ、そして米国全体で日本料理文化の驚くべき成長と普及を目撃する特権を得てきました。\n\n数字が驚くべき物語を語っています：\n\nこの20年未満での**8倍の成長**は、世界の食文化史上前例のないものです。\n\n### 私たちのミッション\n\n個人的なプロジェクトとして、JXPerienceを始めました：\n\n1. **📊 情報集約** - 日本のフランチャイズに関する包括的なデータを集める\n2. **🤝 投資家をつなぐ** - 真剣なグローバル投資家が本物の日本のフランチャイズ機会を発見するのを支援する\n3. **🌍 展開を支援する** - 日本料理の継続的な世界的成長に貢献する\n4. **🍱 文化交流** - 世界中のより多くの人々が本物の日本料理を発見できるようにする\n\n### ビジョン\n\nフランチャイズ情報をよりアクセスしやすくすることで、私たちは以下を希望しています：\n- より多くの人々が本物の日本料理を発見するのを支援する\n- 食を通じた意味のある文化交流を促進する\n- 人々を結びつける共有体験を創造する\n- 日本のブランドがグローバル展開のための適切なパートナーを見つけるのを支援する\n\n---\n\n*このプラットフォームは、世界中での日本料理の卓越性の継続的な成長と Appreciation を支援するために構築された、愛情のこもったプロジェクトです。*"""

ABOUT_ZH = """### 与日本文化的个人旅程\n\n我是日本文化和美食的热心倡导者。多年来，我有幸见证了日本美食文化在亚洲、欧洲和美国的惊人增长和传播。\n\n数字讲述了一个令人难以置信的故事：\n\n**8倍增长**在不到二十年内，这在全球美食文化史上是前所未有的。\n\n### 我们的使命\n\n作为一个个人项目，我创建了JXPerience：\n\n1. **📊 汇总信息** - 汇总关于日本特许经营的全面数据\n2. **🤝 连接投资者** - 帮助认真的全球投资者发现真实的日本特许经营机会\n3. **🌍 支持扩展** - 为日本美食的持续全球增长做出贡献\n4. **🍱 文化交流** - 使世界各地更多人发现真实的日本美食\n\n### 愿景\n\n通过使特许经营信息更易于访问，我们希望：\n- 支持更多人发现真实的日本美食\n- 促进通过食物进行有意义的文化交流\n- 创造将人们联系在一起的共享体验\n- 帮助日本品牌找到全球扩展的合适伙伴\n\n---\n\n*这个平台是一个充满爱的项目，旨在支持全球范围内日本美食卓越性的持续增长和欣赏。*"""

ABOUT_KO = """### 일본 문화와의 개인적인 여정\n\n나는 일본 문화와 요리에 대한 열정적인 옹호자입니다. 몇 년 동안 아시아, 유럽, 미국 전역에서 일본 요리 문화의 놀라운 성장과 확산을 목격할 기회를 가졌습니다.\n\n숫자는 놀라운 이야기를 전합니다:\n\n이 **8배 성장**은 20년 미만의 기간 동안 전 세계 음식 문화 역사상 전례가 없는 것입니다.\n\n### 우리의 미션\n\n개인 프로젝트로, 저는 JXPerience를 시작했습니다:\n\n1. **📊 정보 통합** - 일본 프랜차이즈에 대한 포괄적인 데이터를 수집\n2. **🤝 투자자 연결** - 진지한 글로벌 투자자가 진짜 일본 프랜차이즈 기회를 발견하는 데 도움\n3. **🌍 확장 지원** - 일본 요리의 지속적인 글로벌 성장을 기여\n4. **🍱 문화 교류** - 전 세계 더 많은 사람들이 진짜 일본 요리를 발견할 수 있도록 지원\n\n### 비전\n\n프랜차이즈 정보를 더 쉽게 접근할 수 있도록 하여, 우리는 다음을 기대합니다:\n- 더 많은 사람들이 진짜 일본 요리를 발견하는 것을 지원\n- 음식을 통해 의미 있는 문화 교류를 촉진\n- 사람들을 together하는 공유 경험을 창조\n- 일본 브랜드가 글로벌 확장을 위한 적절한 파트너를 찾는 것을 지원\n\n---\n\n*이 플랫폼은 전 세계에서 일본 요리의 우수성 지속 성장과 감사함을 지원하기 위해 구축된, 사랑이 담긴 프로젝트입니다.*"""

ABOUT_TH = """### การเดินทางส่วนตัวกับวัฒนธรรมญี่ปุ่น\n\nฉันเป็นผู้สนับสนุนวัฒนธรรมและอาหารญี่ปุ่นอย่างจริงใจ ตลอดหลายปีที่ผ่านมา ฉันได้รับเกียรติในการสังเกตการเติบโตและขยายตัวของวัฒนธรรมอาหารญี่ปุ่นทั่วเอเชีย ยุโรป และสหรัฐอเมริกา\n\nตัวเลขบอกเล่าเรื่องราวที่น่าทึ่ง:\n\n**การเติบโต 8 เท่า** ในช่วงเวลาไม่ถึงสองทศวรรษ เป็นเรื่องที่ไม่เคยมีมาก่อนในประวัติศาสตร์วัฒนธรรมอาหารโลก\n\n### ภารกิจของเรา\n\nเป็นโครงการส่วนตัว ฉันเริ่ม JXPerience เพื่อ:\n\n1. **📊 รวบรวมข้อมูล** - รวมข้อมูลที่ครอบคลุมเกี่ยวกับแฟรนไชส์ญี่ปุ่น\n2. **🤝 สร้างความเชื่อมโยงกับนักลงทุน** - ช่วยนักลงทุนทั่วโลกที่จริงจังค้นหาโอกาสแฟรนไชส์ญี่ปุ่นที่แท้จริง\n3. **🌍 สนับสนุนการขยายตัว** - มีส่วนร่วมในการเติบโตของอาหารญี่ปุ่นทั่วโลกอย่างต่อเนื่อง\n4. **🍱 การแลกเปลี่ยนวัฒนธรรม** - ช่วยให้ผู้คนทั่วโลกค้นพบอาหารญี่ปุ่นที่แท้จริงมากขึ้น\n\n### วิสัยทัศน์\n\nด้วยการทำให้ข้อมูลแฟรนไชส์เข้าถึงได้ง่ายขึ้น เราหวังว่า:\n- จะสนับสนุนผู้คนให้ค้นพบอาหารญี่ปุ่นที่แท้จริงมากขึ้น\n- จะส่งเสริมการแลกเปลี่ยนวัฒนธรรมที่มีความหมายผ่านอาหาร\n- จะสร้างประสบการณ์ร่วมที่เชื่อมโยงผู้คนเข้าด้วยกัน\n- จะช่วยให้แบรนด์ญี่ปุ่นหาพันธมิตรที่เหมาะสมสำหรับการขยายตัวระดับโลก\n\n---\n\n*แพลตฟอร์มนี้เป็นโครงการที่เต็มไปด้วยความรัก สร้างขึ้นเพื่อสนับสนุนการเติบโตและความชื่นชมอย่างต่อเนื่องของความเป็นเลิศด้านอาหารญี่ปุ่นทั่วโลก*"""

def get_about():
    lang = st.session_state.language
    if lang == "日本語": return ABOUT_JA
    elif lang == "简体中文": return ABOUT_ZH
    elif lang == "한국어": return ABOUT_KO
    elif lang == "ไทย": return ABOUT_TH
    return ABOUT_EN

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

FAQ_ZH = [
    {"q": "使用此平台是否收费？", "a": "不，投资者的浏览和提交咨询完全免费。"},
    {"q": "如何确认这些品牌的合法性？", "a": "我们使用公开数据、JETRO报告和官方特许经营披露来验证海外扩展状态。"},
    {"q": "提交咨询后会发生什么？", "a": "您的详细信息将安全发送给我们的团队。我们将预先审核您的资料，并将您与特许经营的国际开发团队联系。"},
    {"q": "可以特许经营未列出的品牌吗？", "a": "可以！使用上面的电子邮件链接建议一个品牌。我们一直在添加新的机会。"}
]

FAQ_KO = [
    {"q": "이 플랫폼을 사용하는 데 비용이 드나요?", "a": "아니오, 투자자의 탐색 및 문의 제출은 완전히 무료입니다."},
    {"q": "이 브랜드들이 정당한지 어떻게 알 수 있나요?", "a": "우리는 공개 데이터, JETRO 보고서 및 공식 프랜차이즈 공개 정보를 사용하여 해외 확장 상태를 확인합니다."},
    {"q": "문의를 제출한 후 어떻게 되나요?", "a": "귀하의 세부 정보는 우리 팀에게 안전하게 전송됩니다. 우리는 귀하의 프로필을 사전 검토하고 프랜차이즈의 국제 개발 팀과 연결합니다."},
    {"q": "목록에 없는 브랜드를 프랜차이즈할 수 있나요?", "a": "예! 위의 이메일 링크를 사용하여 브랜드를 제안하십시오. 우리는 항상 새로운 기회를 추가하고 있습니다."}
]

FAQ_TH = [
    {"q": "ใช้แพลตฟอร์มนี้มีค่าใช้จ่ายหรือไม่?", "a": "ไม่ นักลงทุนสามารถดูและส่งคำถามได้ฟรีทั้งหมด"},
    {"q": "จะรู้ได้อย่างไรว่าแบรนด์เหล่านี้ถูกต้องตามกฎหมาย?", "a": "เราตรวจสอบสถานะการขยายตัวต่างประเทศโดยใช้ข้อมูลสาธารณะ รายงาน JETRO และข้อมูลการให้สิทธิ์อย่างเป็นทางการ"},
    {"q": "หลังจากส่งคำถามแล้วจะเกิดอะไรขึ้น?", "a": "ข้อมูลของคุณจะถูกส่งอย่างปลอดภัยถึงทีมของเรา เราจะตรวจสอบโปรไฟล์ของคุณล่วงหน้าและเชื่อมต่อคุณกับทีมพัฒนาระดับสากลของแฟรนไชส์"},
    {"q": "สามารถขอสิทธิ์แฟรนไชส์แบรนด์ที่ไม่ได้ระบุไว้หรือไม่?", "a": "ได้! ใช้ลิงค์อีเมลข้างต้นเพื่อเสนอแบรนด์ เราเพิ่มโอกาสใหม่เสมอ"}
]

def get_faqs():
    lang = st.session_state.language
    if lang == "日本語": return FAQ_JA
    elif lang == "简体中文": return FAQ_ZH
    elif lang == "한국어": return FAQ_KO
    elif lang == "ไทย": return FAQ_TH
    return FAQ_EN

FRANCHISOR_EN = '<div style="margin-bottom: 25px;"><h3 style="color: #1a1a2e; margin-top: 0;">Why Register as a Franchisor?</h3><p style="font-size: 1.1em; line-height: 1.6;">As a Japanese franchise brand, you have unique access to the global market. Our platform connects you directly with qualified international investors.</p></div><div class="benefit-card"><h4>✅ What You\'ll Get as a Verified Partner</h4><ul style="padding-left: 20px; margin: 15px 0;"><li><strong>Real-time qualified leads</strong> - See genuine investor applications as they come in</li><li><strong>Pre-screened investors</strong> - All applicants are vetted for serious investment capacity</li><li><strong>Dedicated dashboard</strong> - Track your leads and review applications in one place</li><li><strong>CSV export</strong> - Download your leads in spreadsheet format</li><li><strong>Direct connection</strong> - Contact investors directly through our secure platform</li></ul></div>'

FRANCHISOR_JA = '<div style="margin-bottom: 25px;"><h3 style="color: #1a1a2e; margin-top: 0;">なぜフランチャイザーとして登録するのか？</h3><p style="font-size: 1.1em; line-height: 1.6;">日本のフランチャイズブランドとして、グローバル市場へのユニークなアクセス権を持っています。私たちのプラットフォームは、資格のある国際投資家と直接接続します。</p></div><div class="benefit-card"><h4>✅ 認定パートナーの特典</h4><ul style="padding-left: 20px; margin: 15px 0;"><li><strong>リアルタイムの qualified リード</strong> - 投資家アプリケーションが届き次第確認</li><li><strong>事前審査済みの投資家</strong> - すべての応募者は真剣な投資能力について審査済み</li><li><strong>専用ダッシュボード</strong> - リードを追跡し、アプリケーションを一つの場所で確認</li><li><strong>CSVエクスポート</strong> - リードをスプレッドシート形式でダウンロード</li><li><strong>直接接続</strong> - 安全なプラットフォームを通じて投資家と直接連絡</li></ul></div>'

FRANCHISOR_ZH = '<div style="margin-bottom: 25px;"><h3 style="color: #1a1a2e; margin-top: 0;">为什么注册为特许经营商？</h3><p style="font-size: 1.1em; line-height: 1.6;">作为日本特许经营品牌，您拥有进入全球市场的独特渠道。我们的平台将您直接与合格的国际投资者连接。</p></div><div class="benefit-card"><h4>✅ 作为认证合作伙伴您将获得</h4><ul style="padding-left: 20px; margin: 15px 0;"><li><strong>实时合格的线索</strong> - 查看真实的投资人申请</li><li><strong>预先筛选的投资者</strong> - 所有申请人都经过严格审核，具有认真的投资能力</li><li><strong>专用仪表板</strong> - 在一个地方跟踪您的线索并审查申请</li><li><strong>CSV导出</strong> - 以电子表格格式下载您的线索</li><li><strong>直接连接</strong> - 通过我们的安全平台直接联系投资者</li></ul></div>'

FRANCHISOR_KO = '<div style="margin-bottom: 25px;"><h3 style="color: #1a1a2e; margin-top: 0;">왜 프랜차이저로 등록해야 하나요?</h3><p style="font-size: 1.1em; line-height: 1.6;">일본 프랜차이즈 브랜드로서, 당신은 글로벌 시장에 대한 고유한 접근 권한을 가지고 있습니다. 우리의 플랫폼은 당신을 자격 있는 국제 투자자와 직접 연결합니다.</p></div><div class="benefit-card"><h4>✅ 인증 파트너로서 얻는 것</h4><ul style="padding-left: 20px; margin: 15px 0;"><li><strong>실시간 자격 있는 리드</strong> - 투자자 신청서가 올 때마다 확인</li><li><strong>사전 검토된 투자자</strong> - 모든 지원자는 진지한 투자 능력에 대해 검토됨</li><li><strong>전용 대시보드</strong> - 리드를 추적하고 한 곳에서 신청서를 검토</li><li><strong>CSV 내보내기</strong> - 스프레드시트 형식으로 리드 다운로드</li><li><strong>직접 연결</strong> - 안전한 플랫폼을 통해 투자자와 직접 연락</li></ul></div>'

FRANCHISOR_TH = '<div style="margin-bottom: 25px;"><h3 style="color: #1a1a2e; margin-top: 0;">ทำไมต้องลงทะเบียนเป็นผู้ให้สิทธิ์?</h3><p style="font-size: 1.1em; line-height: 1.6;">ในฐานะแบรนด์แฟรนไชส์ญี่ปุ่น คุณมีโอกาสเข้าถึงตลาดโลกที่ไม่เหมือนใคร แพลตฟอร์มของเราเชื่อมต่อคุณโดยตรงกับนักลงทุนต่างประเทศที่มีคุณสมบัติ</p></div><div class="benefit-card"><h4>✅ สิ่งที่คุณจะได้รับเป็นพันธมิตรที่ได้รับการรับรอง</h4><ul style="padding-left: 20px; margin: 15px 0;"><li><strong>ลูกค้าจริงทันที</strong> - ดูการสมัครของนักลงทุนจริงเมื่อมาถึง</li><li><strong>นักลงทุนที่ได้รับการตรวจสอบแล้ว</strong> - ผู้สมัครทั้งหมดได้รับการตรวจสอบเพื่อความสามารถในการลงทุนจริง</li><li><strong>แดชบอร์ดเฉพาะ</strong> - ติดตามลูกค้าและทบทวนการสมัครในที่เดียว</li><li><strong>ส่งออก CSV</strong> - ดาวน์โหลดลูกค้าในรูปแบบสเปรดชีต</li><li><strong>การเชื่อมต่อโดยตรง</strong> - ติดต่อนักลงทุนโดยตรงผ่านแพลตฟอร์มที่ปลอดภัยของเรา</li></ul></div>'

def get_franchisor_text():
    lang = st.session_state.language
    if lang == "日本語": return FRANCHISOR_JA
    elif lang == "简体中文": return FRANCHISOR_ZH
    elif lang == "한국어": return FRANCHISOR_KO
    elif lang == "ไทย": return FRANCHISOR_TH
    return FRANCHISOR_EN

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
    
    data = get_brand(brand)
    
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
    st.markdown(get_franchisor_text(), unsafe_allow_html=True)
    
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
    st.markdown(get_about(), unsafe_allow_html=True)
    
    st.markdown("""
    <div class="beta-banner">
        <h4> This is a Beta Site — Help Us Build It Together!</h4>
        <p style="color: #78350f; margin-bottom: 10px;">JXPerience is currently in <strong>beta</strong>. We are actively improving the platform and would love your input.</p>
        <p style="color: #78350f; margin-bottom: 10px;"><strong> Co-Create With Us</strong> — Have suggestions, spotted a bug, or want to recommend a franchise brand to add? We invite you to share your comments and improvement ideas directly with us.</p>
        <p style="color: #78350f; margin: 0;">📧 <strong>Email us at:</strong> <a href="mailto:jxperience.info@gmail.com?subject=JXPerience Feedback">jxperience.info@gmail.com</a></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---"); st.subheader(t("faq_title"))
    for faq in get_faqs():
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
language = st.sidebar.selectbox("Select Language / 言語を選択 / 选择语言 / 선택 언어 / เลือกภาษา", 
                           ["English", "日本語", "简体中文", "한국어", "ไทย"],
                           index=0 if st.session_state.language == "English" else 
                           1 if st.session_state.language == "日本語" else
                           2 if st.session_state.language == "简体中文" else
                           3 if st.session_state.language == "한국어" else 4)
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
