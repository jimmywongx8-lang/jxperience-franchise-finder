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

# --- TRANSLATIONS ---
TRANSLATIONS = {
    "English": {
        "sidebar_title": "🗾 JP Hub", "nav_header": "Navigation", "home": "🏠 Home", "about": "ℹ️ About Us", "franchisor": "🏢 Franchisor",
        "search_header": " Search & Filter", "search_placeholder": "Search brands", "filter_category": "Filter by Category", "choose_options": "Choose options",
        "hero_title": "🗾 Discover Japanese Franchise Opportunities", "hero_subtitle": "Connecting global investors with 63+ expansion-ready Japanese brands",
        "metric_brands": "Brands", "metric_countries": "Countries", "metric_investment": "Investment",
        "found_brands": "Found 63 Expansion-Ready Brands", "showing_brands": "Showing {count} brands", "stores": "stores", "royalty": "Royalty",
        "view_details": "📋 View Details", "enquiry": "Enquiry →",
        "footer_text": "© 2026 JXPerience. Connecting Japanese brands with global investors.", "footer_contact": "📧 Contact: jxperience.info@gmail.com",
        "back_brands": "← Back to Brands", "company_history": "📖 Company History", "menu_highlights": "🍱 Menu Highlights", "investment_overview": "💰 Investment Overview",
        "requirements": "📋 Franchise Requirements", "support": "🤝 Support Provided", "success_story": "⭐ Success Story", "contact_info": "📞 Contact Information",
        "submit_enquiry": " Submit Enquiry", "watch_videos": "▶️ Watch Videos",
        "enquiry_title": "Enquiry: {brand}", "back": "← Back", "name": "Name", "email": "Email", "capital": "Capital", "experience": "Experience", "industry": "Industry", "location": "Location", "timeline": "Timeline",
        "submit": "Submit Enquiry", "success_msg": "✅ Enquiry submitted!", "error_msg": "Fill in name and email",
        "cap_under": "Under $100k", "cap_100_250": "$100k-$250k", "cap_250_500": "$250k-$500k", "cap_500_1m": "$500k-$1M", "cap_over": "Over $1M",
        "exp_none": "None", "exp_1_3": "1-3 years", "exp_3_5": "3-5 years", "exp_5_plus": "5+ years", "exp_owner": "Franchise Owner",
        "ind_fb": "F&B", "ind_retail": "Retail", "ind_corp": "Corporate", "ind_other": "Other",
        "time_research": "Researching", "time_1_2": "1-2 years", "time_6_12": "6-12 months", "time_asap": "ASAP",
        "about_title": "🗾 About JXPerience", "about_caption": "Our Mission & Story", "why_started": "Why We Started This", "faq_title": "❓ Frequently Asked Questions",
        "ready_explore": "🚀 Ready to Explore?", "browse": "Browse Franchises", "contact_label": "📧 **Contact:**",
        "franchisor_title": "🗾 Franchisor Portal", "why_register": "Why Register as a Franchisor?", "what_you_get": "✅ What You'll Get as a Verified Partner",
        "access_dashboard": "Access Your Franchise Dashboard", "new_to_jx": "New to JXPerience?", "password": "Password", "login": "Login", "wrong_password": "Wrong password",
        "company": "Company", "request_access": "Request Access", "request_sent": "Request sent! We'll contact you within 24-48 hours.", "logged_in": "Logged in", "logout": "Logout",
        "leads": "📊 Leads", "settings": "⚙️ Settings", "found_leads": "✅ Found {count} real leads!", "download_csv": "📥 Download CSV", "no_leads": "No leads yet", "settings_soon": "Settings coming soon",
        "language": "🌐 Language", "beta_title": "🚧 This is a Beta Site — Help Us Build It Together!",
        "beta_text1": "JXPerience is currently in **beta**. We are actively improving the platform and would love your input.",
        "beta_text2": "**🤝 Co-Create With Us** — Have suggestions, spotted a bug, or want to recommend a franchise brand to add? We invite you to share your comments and improvement ideas directly with us.",
        "beta_email": "📧 **Email us at:**",
    },
    "日本語": {
        "sidebar_title": "🗾 JPハブ", "nav_header": "ナビゲーション", "home": " ホーム", "about": "ℹ️ 私たちについて", "franchisor": "🏢 フランチャイザー",
        "search_header": "🔍 検索とフィルター", "search_placeholder": "ブランドを検索", "filter_category": "カテゴリでフィルター", "choose_options": "オプションを選択",
        "hero_title": "🗾 日本のフランチャイズ機会を発見", "hero_subtitle": "63以上の展開-readyな日本ブランドとグローバル投資家をつなぐ",
        "metric_brands": "ブランド", "metric_countries": "国・地域", "metric_investment": "投資額",
        "found_brands": "63の展開-readyブランドを発見", "showing_brands": "{count}ブランドを表示", "stores": "店舗", "royalty": "ロイヤリティ",
        "view_details": "📋 詳細を見る", "enquiry": "お問い合わせ →",
        "footer_text": "© 2026 JXPerience. 日本ブランドとグローバル投資家をつなぐ。", "footer_contact": "📧 お問い合わせ: jxperience.info@gmail.com",
        "back_brands": "← ブランド一覧に戻る", "company_history": " 会社の歴史", "menu_highlights": " メニューの特徴", "investment_overview": "💰 投資概要",
        "requirements": "📋 フランチャイズ要件", "support": "🤝 サポート内容", "success_story": "⭐ 成功事例", "contact_info": " お問い合わせ情報",
        "submit_enquiry": "📝 お問い合わせを送信", "watch_videos": "▶️ 動画を見る",
        "enquiry_title": "お問い合わせ: {brand}", "back": "← 戻る", "name": "お名前", "email": "メールアドレス", "capital": "資金", "experience": "経験", "industry": "業界", "location": "場所", "timeline": "スケジュール",
        "submit": "送信", "success_msg": "✅ お問い合わせを送信しました！", "error_msg": "名前とメールアドレスを入力してください",
        "cap_under": "$100k未満", "cap_100_250": "$100k-$250k", "cap_250_500": "$250k-$500k", "cap_500_1m": "$500k-$1M", "cap_over": "$1M超",
        "exp_none": "なし", "exp_1_3": "1-3年", "exp_3_5": "3-5年", "exp_5_plus": "5年以上", "exp_owner": "フランチャイズオーナー",
        "ind_fb": "飲食", "ind_retail": "小売", "ind_corp": "企業", "ind_other": "その他",
        "time_research": "調査中", "time_1_2": "1-2年", "time_6_12": "6-12ヶ月", "time_asap": " ASAP（できるだけ早く）",
        "about_title": " JXPerienceについて", "about_caption": "私たちのミッションとストーリー", "why_started": "なぜ始めたのか", "faq_title": "❓ よくある質問",
        "ready_explore": "🚀 探索する準備はできましたか？", "browse": "ブランドを見る", "contact_label": "📧 **お問い合わせ:**",
        "franchisor_title": "🗾 フランチャイザーポータル", "why_register": "なぜフランチャイザーとして登録するのか？", "what_you_get": "✅ 認定パートナーの特典",
        "access_dashboard": "フランチャイズダッシュボードにアクセス", "new_to_jx": "JXPerienceが初めてですか？", "password": "パスワード", "login": "ログイン", "wrong_password": "パスワードが違います",
        "company": "会社名", "request_access": "アクセスをリクエスト", "request_sent": "リクエストを送信しました！24-48時間以内にご連絡します。", "logged_in": "ログインしました", "logout": "ログアウト",
        "leads": "📊 リード", "settings": "⚙️ 設定", "found_leads": "✅ {count}件のリアルリードを発見！", "download_csv": "📥 CSVをダウンロード", "no_leads": "リードはまだありません", "settings_soon": "設定は近日公開",
        "language": "🌐 言語", "beta_title": "🚧 これはベータサイトです — 一緒に作り上げましょう！",
        "beta_text1": "JXPerienceは現在**ベータ版**です。プラットフォームを積極的に改善しており、皆様のご意見をお待ちしております。",
        "beta_text2": "**🤝 一緒に作りましょう** — ご提案、バグの報告、または追加したいフランチャイズブランドの推薦はありますか？ご意見や改善アイデアを直接お寄せください。",
        "beta_email": "📧 **メールでのお問い合わせ:**",
    },
    "简体中文": {
        "sidebar_title": "🗾 JP Hub", "nav_header": "导航", "home": "🏠 首页", "about": "ℹ️ 关于我们", "franchisor": "🏢 特许经营商",
        "search_header": "🔍 搜索和筛选", "search_placeholder": "搜索品牌", "filter_category": "按类别筛选", "choose_options": "选择选项",
        "hero_title": "🗾 发现日本特许经营机会", "hero_subtitle": "连接63+个准备扩张的日本品牌与全球投资者",
        "metric_brands": "品牌", "metric_countries": "国家", "metric_investment": "投资",
        "found_brands": "找到63个可扩张品牌", "showing_brands": "显示 {count} 个品牌", "stores": "门店", "royalty": "版税",
        "view_details": "📋 查看详情", "enquiry": "咨询 →",
        "footer_text": "© 2026 JXPerience. 连接日本品牌与全球投资者。", "footer_contact": "📧 联系: jxperience.info@gmail.com",
        "back_brands": "← 返回品牌列表", "company_history": "📖 公司历史", "menu_highlights": "🍱 菜单亮点", "investment_overview": "💰 投资概览",
        "requirements": "📋 特许经营要求", "support": "🤝 支持服务", "success_story": "⭐ 成功案例", "contact_info": "📞 联系信息",
        "submit_enquiry": "📝 提交咨询", "watch_videos": "▶️ 观看视频",
        "enquiry_title": "咨询: {brand}", "back": "← 返回", "name": "姓名", "email": "邮箱", "capital": "资金", "experience": "经验", "industry": "行业", "location": "地点", "timeline": "时间线",
        "submit": "提交咨询", "success_msg": "✅ 咨询已提交！", "error_msg": "请填写姓名和邮箱",
        "cap_under": "低于$100k", "cap_100_250": "$100k-$250k", "cap_250_500": "$250k-$500k", "cap_500_1m": "$500k-$1M", "cap_over": "超过$1M",
        "exp_none": "无", "exp_1_3": "1-3年", "exp_3_5": "3-5年", "exp_5_plus": "5年以上", "exp_owner": "特许经营商",
        "ind_fb": "餐饮", "ind_retail": "零售", "ind_corp": "企业", "ind_other": "其他",
        "time_research": "研究中", "time_1_2": "1-2年", "time_6_12": "6-12个月", "time_asap": "尽快",
        "about_title": "🗾 关于JXPerience", "about_caption": "我们的使命与故事", "why_started": "为什么开始", "faq_title": "❓ 常见问题",
        "ready_explore": "🚀 准备好探索了吗？", "browse": "浏览品牌", "contact_label": "📧 **联系:**",
        "franchisor_title": "🗾 特许经营商门户", "why_register": "为什么注册为特许经营商？", "what_you_get": "✅ 作为认证合作伙伴您将获得",
        "access_dashboard": "访问您的特许经营仪表板", "new_to_jx": "JXPerience新手？", "password": "密码", "login": "登录", "wrong_password": "密码错误",
        "company": "公司名称", "request_access": "请求访问", "request_sent": "请求已发送！我们将在24-48小时内联系您。", "logged_in": "已登录", "logout": "登出",
        "leads": " 线索", "settings": "⚙️ 设置", "found_leads": "✅ 找到 {count} 个真实线索！", "download_csv": "📥 下载CSV", "no_leads": "暂无线索", "settings_soon": "设置即将推出",
        "language": " 语言", "beta_title": " 这是一个测试版网站 — 帮助我们共同打造！",
        "beta_text1": "JXPerience目前处于**测试版**。我们正在积极改进平台，非常期待您的反馈。",
        "beta_text2": "**🤝 与我们共同创建** — 有建议、发现错误，或想推荐要添加的特许经营品牌？我们邀请您直接与我们分享您的意见和改进想法。",
        "beta_email": " **通过电子邮件联系我们：**",
    },
    "繁體中文": {
        "sidebar_title": "🗾 JP Hub", "nav_header": "導航", "home": "🏠 首頁", "about": "ℹ️ 關於我們", "franchisor": "🏢 特許經營商",
        "search_header": "🔍 搜索和篩選", "search_placeholder": "搜索品牌", "filter_category": "按類別篩選", "choose_options": "選擇選項",
        "hero_title": "🗾 發現日本特許經營機會", "hero_subtitle": "連接63+個準備擴張的日本品牌與全球投資者",
        "metric_brands": "品牌", "metric_countries": "國家", "metric_investment": "投資",
        "found_brands": "找到63個可擴張品牌", "showing_brands": "顯示 {count} 個品牌", "stores": "門店", "royalty": "版稅",
        "view_details": "📋 查看詳情", "enquiry": "諮詢 →",
        "footer_text": "© 2026 JXPerience. 連接日本品牌與全球投資者。", "footer_contact": "📧 聯繫: jxperience.info@gmail.com",
        "back_brands": "← 返回品牌列表", "company_history": "📖 公司歷史", "menu_highlights": "🍱 菜單亮點", "investment_overview": "💰 投資概覽",
        "requirements": "📋 特許經營要求", "support": "🤝 支持服務", "success_story": "⭐ 成功案例", "contact_info": "📞 聯繫信息",
        "submit_enquiry": "📝 提交諮詢", "watch_videos": "▶️ 觀看視頻",
        "enquiry_title": "諮詢: {brand}", "back": "← 返回", "name": "姓名", "email": "郵箱", "capital": "資金", "experience": "經驗", "industry": "行業", "location": "地點", "timeline": "時間線",
        "submit": "提交諮詢", "success_msg": "✅ 諮詢已提交！", "error_msg": "請填寫姓名和郵箱",
        "cap_under": "低於$100k", "cap_100_250": "$100k-$250k", "cap_250_500": "$250k-$500k", "cap_500_1m": "$500k-$1M", "cap_over": "超過$1M",
        "exp_none": "無", "exp_1_3": "1-3年", "exp_3_5": "3-5年", "exp_5_plus": "5年以上", "exp_owner": "特許經營商",
        "ind_fb": "餐飲", "ind_retail": "零售", "ind_corp": "企業", "ind_other": "其他",
        "time_research": "研究中", "time_1_2": "1-2年", "time_6_12": "6-12個月", "time_asap": "盡快",
        "about_title": "🗾 關於JXPerience", "about_caption": "我們的使命與故事", "why_started": "為什麼開始", "faq_title": "❓ 常見問題",
        "ready_explore": "🚀 準備好探索了嗎？", "browse": "瀏覽品牌", "contact_label": "📧 **聯繫:**",
        "franchisor_title": "🗾 特許經營商門戶", "why_register": "為什麼註冊為特許經營商？", "what_you_get": "✅ 作為認證合作夥伴您將獲得",
        "access_dashboard": "訪問您的特許經營儀表板", "new_to_jx": "JXPerience新手？", "password": "密碼", "login": "登錄", "wrong_password": "密碼錯誤",
        "company": "公司名稱", "request_access": "請求訪問", "request_sent": "請求已發送！我們將在24-48小時內聯繫您。", "logged_in": "已登錄", "logout": "登出",
        "leads": "📊 線索", "settings": "⚙️ 設置", "found_leads": "✅ 找到 {count} 個真實線索！", "download_csv": "📥 下載CSV", "no_leads": "暫無線索", "settings_soon": "設置即將推出",
        "language": " 語言", "beta_title": "🚧 這是一個測試版網站 — 幫助我們共同打造！",
        "beta_text1": "JXPerience目前處於**測試版**。我們正在積極改進平台，非常期待您的反饋。",
        "beta_text2": "**🤝 與我們共同創建** — 有建議、發現錯誤，或想推薦要添加的特許經營品牌？我們邀請您直接與我們分享您的意見和改進想法。",
        "beta_email": "📧 **通過電子郵件聯繫我們：**",
    },
    "한국어": {
        "sidebar_title": "🗾 JP 허브", "nav_header": "내비게이션", "home": "🏠 홈", "about": "ℹ️ 우리에 대해", "franchisor": "🏢 프랜차이저",
        "search_header": "🔍 검색 및 필터", "search_placeholder": "브랜드 검색", "filter_category": "카테고리별 필터", "choose_options": "옵션 선택",
        "hero_title": "🗾 일본 프랜차이즈 기회 발견", "hero_subtitle": "63+개의 확장 준비된 일본 브랜드와 글로벌 투자자 연결",
        "metric_brands": "브랜드", "metric_countries": "국가", "metric_investment": "투자",
        "found_brands": "63개의 확장 준비 브랜드 발견", "showing_brands": "{count}개 브랜드 표시", "stores": "매장", "royalty": "로열티",
        "view_details": "📋 상세 정보 보기", "enquiry": "문의 →",
        "footer_text": "© 2026 JXPerience. 일본 브랜드와 글로벌 투자자 연결.", "footer_contact": "📧 연락처: jxperience.info@gmail.com",
        "back_brands": "← 브랜드 목록으로 돌아가기", "company_history": "📖 회사 역사", "menu_highlights": "🍱 메뉴 하이라이트", "investment_overview": " 투자 개요",
        "requirements": "📋 프랜차이즈 요구사항", "support": "🤝 지원 제공", "success_story": "⭐ 성공 사례", "contact_info": " 연락 정보",
        "submit_enquiry": "📝 문의 제출", "watch_videos": "▶️ 동영상 보기",
        "enquiry_title": "문의: {brand}", "back": "← 뒤로", "name": "이름", "email": "이메일", "capital": "자본", "experience": "경험", "industry": "업종", "location": "위치", "timeline": "타임라인",
        "submit": "문의 제출", "success_msg": "✅ 문의가 제출되었습니다!", "error_msg": "이름과 이메일을 입력하세요",
        "cap_under": "$100k 미만", "cap_100_250": "$100k-$250k", "cap_250_500": "$250k-$500k", "cap_500_1m": "$500k-$1M", "cap_over": "$1M 초과",
        "exp_none": "없음", "exp_1_3": "1-3년", "exp_3_5": "3-5년", "exp_5_plus": "5년 이상", "exp_owner": "프랜차이즈 소유자",
        "ind_fb": "식음료", "ind_retail": "소매", "ind_corp": "기업", "ind_other": "기타",
        "time_research": "연구 중", "time_1_2": "1-2년", "time_6_12": "6-12개월", "time_asap": "가급적 빠르게",
        "about_title": " JXPerience에 대해", "about_caption": "우리의 미션과 이야기", "why_started": "시작한 이유", "faq_title": "❓ 자주 묻는 질문",
        "ready_explore": "🚀 탐색 준비가 되셨나요?", "browse": "브랜드 둘러보기", "contact_label": "📧 **연락처:**",
        "franchisor_title": "🗾 프랜차이저 포털", "why_register": "왜 프랜차이저로 등록해야 하나요?", "what_you_get": "✅ 인증 파트너로서 얻는 것",
        "access_dashboard": "프랜차이즈 대시보드 액세스", "new_to_jx": "JXPerience가 처음이신가요?", "password": "비밀번호", "login": "로그인", "wrong_password": "잘못된 비밀번호",
        "company": "회사 이름", "request_access": "액세스 요청", "request_sent": "요청이 전송되었습니다! 24-48시간 내에 연락드리겠습니다.", "logged_in": "로그인됨", "logout": "로그아웃",
        "leads": "📊 리드", "settings": "⚙️ 설정", "found_leads": "✅ {count}개의 실제 리드 발견!", "download_csv": " CSV 다운로드", "no_leads": "리드가 없습니다", "settings_soon": "설정 준비 중",
        "language": "🌐 언어", "beta_title": "🚧 이것은 베타 사이트입니다 — 함께 만들어 갑시다!",
        "beta_text1": "JXPerience는 현재 **베 버전**입니다. 우리는 플랫폼을 적극적으로 개선하고 있으며 여러분의 의견을 듣고 싶습니다.",
        "beta_text2": "**🤝 함께 만들어요** — 제안사항, 버그 발견, 또는 추가하고 싶은 프랜차이즈 브랜드가 있으신가요? 의견과 개선 아이디어를 직접 공유해 주세요.",
        "beta_email": "📧 **이메일로 연락하세요:**",
    }
}

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'selected_franchise' not in st.session_state: st.session_state.selected_franchise = None
if 'franchisor_logged_in' not in st.session_state: st.session_state.franchisor_logged_in = False
if 'categories' not in st.session_state: st.session_state.categories = []
if 'language' not in st.session_state: 
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
    .main { background-color: #f8f9fa; }
    h1, h2, h3 { color: #1a1a2e; font-weight: 700; margin-bottom: 1rem; }
    .stButton>button { border-radius: 8px; font-weight: 600; padding: 0.5rem 1.5rem; transition: all 0.3s ease; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
    .metric-card { background: rgba(255,255,255,0.2); padding: 15px 25px; border-radius: 10px; backdrop-filter: blur(10px); }
    .status-badge { display: inline-block; background: #10b981; color: white; padding: 8px 16px; border-radius: 20px; font-weight: 600; margin-bottom: 20px; }
    .benefit-card { background: #f0f7ff; border-left: 4px solid #667eea; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    .benefit-card h4 { color: #1a1a2e; margin-top: 0; }
    
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

# --- FRANCHISES (English base) ---
FRANCHISES = {
    "Yoshinoya": {"story": "World-famous gyudon chain with 1,000+ stores.", "investment": "$150k - $300k", "royalty": "5.0%", "sales": "$400k - $800k", "overseas_status": "✅ ACTIVELY RECRUITING - USA, Asia, Middle East", "youtube_search": "Yoshinoya franchise", "news_search": "Yoshinoya expansion", "financials": {"Metric": ["Fee", "Investment", "Royalty", "Stores"], "Details": ["$30k-$50k", "$150k-$300k", "5%", "1,000+"]}, "pros": ["Global brand", "Simple menu", "Fast service"], "cons": ["Beef regulations", "High competition"], "history": "Founded in 1899 in Tokyo's fish market, Yoshinoya is one of Japan's oldest fast-food chains. Specializing in gyudon (beef bowls), it has grown to over 1,200 locations worldwide.", "requirements": ["Minimum net worth: $400k USD", "Liquid capital: $150k+ USD", "Restaurant experience preferred", "High-traffic location: 800-1,500 sq ft"], "support": ["Initial training (2-4 weeks)", "Site selection assistance", "Store design package", "Supply chain for beef", "Marketing support"], "success_story": {"title": "California Success", "story": "A franchisee in Los Angeles opened in 2018. 'The gyudon concept resonates with health-conscious Americans.'", "metrics": "5 locations | $520k avg revenue | 22-month ROI"}, "menu_highlights": ["Gyudon (Beef Bowl)", "Chicken Teriyaki", "Karaage", "Miso Soup"], "contact_info": "International: overseas@yoshinoya.com | +81-3-5555-1111"},
    "Sushiro": {"story": "Japan's #1 conveyor belt sushi chain with 600+ stores.", "investment": "$200k - $500k", "royalty": "6.0%", "sales": "$600k - $1.2M", "overseas_status": "✅ EXPANDING - Asia, USA", "youtube_search": "Sushiro franchise", "news_search": "Sushiro expansion", "financials": {"Metric": ["Fee", "Investment", "Royalty", "Stores"], "Details": ["$50k-$80k", "$200k-$500k", "6%", "600+"]}, "pros": ["Market leader", "High volume", "Tech integration"], "cons": ["Higher investment", "Complex ops"], "history": "Sushiro was established in 1995 and has become Japan's largest conveyor belt sushi chain. Known for high-quality sushi at affordable prices.", "requirements": ["Minimum net worth: $800k USD", "Liquid capital: $250k+ USD", "Restaurant experience required", "Large space: 2,000-3,500 sq ft"], "support": ["Sushi chef training", "Conveyor belt installation", "Fresh fish supply chain", "Technology systems"], "success_story": {"title": "Hong Kong Expansion", "story": "A master franchisee secured HK rights in 2018. Now 15 locations across HK.", "metrics": "15 stores | $850k avg revenue | 26-month ROI"}, "menu_highlights": ["Conveyor belt sushi", "Fresh fish daily", "Touch-screen ordering", "Seasonal specialties"], "contact_info": "Franchise: franchise@sushiro.co.jp | +81-6-5555-2222"},
    "Coco Ichibanya": {"story": "Japan's #1 curry house with 1,300+ stores.", "investment": "$150k - $300k", "royalty": "5% - 7%", "sales": "¥50M - ¥80M", "overseas_status": "✅ ACTIVELY RECRUITING - USA, Asia, Europe", "youtube_search": "Coco Ichibanya franchise", "news_search": "Coco Ichibanya expansion", "financials": {"Metric": ["Fee", "Investment", "Royalty", "Stores"], "Details": ["¥3M-¥5M", "$150k-$300k", "5-7%", "1,300+"]}, "pros": ["Proven success", "Low complexity", "Customizable"], "cons": ["Curry specialization", "Competition"], "history": "Founded in 1978 in Aichi Prefecture. Revolutionized Japanese curry with customizable spice levels. Now 1,300+ stores in Japan and 200+ internationally.", "requirements": ["Minimum net worth: $500k USD", "Liquid capital: $150k+ USD", "8-week training in Japan", "Space: 1,500-2,500 sq ft"], "support": ["8-week training in Japan", "Site selection", "Store design", "Equipment support", "Ongoing consulting"], "success_story": {"title": "Thailand Success", "story": "First Bangkok location in 2015. Expanded to 12 locations in 3 years.", "metrics": "12 stores | $540k avg revenue | 18-month ROI"}, "menu_highlights": ["Japanese Curry Rice", "Katsu Curry", "Cheese Curry", "20+ toppings"], "contact_info": "International: international@coco-curry.com | +81-3-5555-1234"},
    "Pepper Lunch": {"story": "Fast-steak concept with 200+ stores across 15+ countries.", "investment": "$200k - $400k", "royalty": "5% - 6%", "sales": "$400k - $800k", "overseas_status": "✅ VERY ACTIVE - 15+ countries", "youtube_search": "Pepper Lunch franchise", "news_search": "Pepper Lunch expansion", "financials": {"Metric": ["Fee", "Investment", "Royalty", "Stores"], "Details": ["$30k-$50k", "$200k-$400k", "5-6%", "200+"]}, "pros": ["Proven success", "DIY concept", "Fast service"], "cons": ["Sizzling equipment", "Premium pricing"], "history": "Founded in 1994 by Chef Kunio Ichinose. Revolutionary DIY dining on sizzling iron plates. Expanded to 15+ countries.", "requirements": ["Minimum net worth: $600k USD", "Liquid capital: $200k+ USD", "Restaurant experience required", "High-traffic location"], "support": ["4-week training", "Store design", "Sizzling plate tech", "Marketing", "R&D support"], "success_story": {"title": "Singapore Success", "story": "First Orchard Road location in 2012. Now 8 locations across SG and MY.", "metrics": "8 stores | $650k avg revenue | 24-month ROI"}, "menu_highlights": ["Sizzling Beef Steak", "Salmon Meuniere", "Spicy Curry Beef", "3-minute cooking"], "contact_info": "Franchise: franchise@pepperlunch.com | +81-3-5555-5678"},
    "Kura Sushi": {"story": "High-tech conveyor belt sushi expanding in USA.", "investment": "$500k - $1M", "royalty": "5% - 6%", "sales": "$1M - $2M", "overseas_status": "✅ EXPANDING IN USA", "youtube_search": "Kura Sushi USA", "news_search": "Kura Sushi expansion", "financials": {"Metric": ["Investment", "Royalty", "Locations"], "Details": ["$500k-$1M", "5-6%", "10+"]}, "pros": ["High-tech", "Strong growth", "Premium"], "cons": ["High investment", "Complex ops"], "history": "Established in 1999 in Nara. Known for touch-screen ordering, automated conveyor systems, and gamified dining. Public since 2013.", "requirements": ["Minimum net worth: $1.5M USD", "Liquid capital: $500k+ USD", "Multi-unit experience preferred", "Space: 3,000-5,000 sq ft"], "support": ["12-week training", "Conveyor system", "POS technology", "Sushi chef certification", "Fish supply chain"], "success_story": {"title": "California Expansion", "story": "First Irvine location in 2019. Attracted tech-savvy millennials and families.", "metrics": "3 locations | $1.2M avg revenue | 36-month ROI"}, "menu_highlights": ["Premium conveyor sushi", "Touch-screen ordering", "Prize drawing system", "Sake selection"], "contact_info": "USA: usa@kurasushi.com | +1-949-555-0123"},
    "Sukiya": {"story": "Japan's largest gyudon chain with 2,000+ stores.", "investment": "$300k - $600k", "royalty": "4% - 6%", "sales": "¥100M+", "overseas_status": "✅ SELECTIVE - Asia focus", "youtube_search": "Sukiya franchise", "news_search": "Sukiya expansion", "financials": {"Metric": ["Investment", "Royalty", "Stores"], "Details": ["$300k-$600k", "4-6%", "2,000+"]}, "pros": ["Massive brand", "Simple menu", "High volume"], "cons": ["Selective approval", "Beef regulations"], "history": "Founded in 1982. Japan's largest gyudon chain with 2,000+ locations. Part of Zenrin Group. Known for 24-hour operations.", "requirements": ["Minimum net worth: $800k USD", "Liquid capital: $300k+ USD", "Multi-unit QSR experience", "Master franchise preferred"], "support": ["Master franchise support", "Training programs", "Beef supply chain", "Store layout", "Marketing"], "success_story": {"title": "Hong Kong Dominance", "story": "Master franchisee since 2010. Now 35 locations across HK and Macau.", "metrics": "35 stores | $850k avg revenue | 20-month ROI"}, "menu_highlights": ["Gyudon (Beef Bowl)", "Various sizes", "Side dishes", "24/7 operation"], "contact_info": "International: overseas@sukiya.co.jp | +81-45-555-9876"},
    "Hoshino Coffee": {"story": "Premium Nagoya coffee shop famous for pancakes.", "investment": "$250k - $500k", "royalty": "5% - 6%", "sales": "¥60M - ¥100M", "overseas_status": "✅ ACTIVE IN ASIA", "youtube_search": "Hoshino Coffee", "news_search": "Hoshino Coffee expansion", "financials": {"Metric": ["Investment", "Royalty", "Markets"], "Details": ["$250k-$500k", "5-6%", "HK/TW/TH"]}, "pros": ["Premium", "Unique menu", "Strong branding"], "cons": ["Higher price", "Large space needed"], "history": "Established in 1978 in Nagoya. Famous for fluffy pancakes and retro Showa-era atmosphere. Expanding across Asia.", "requirements": ["Minimum net worth: $600k USD", "Liquid capital: $250k+ USD", "Cafe experience preferred", "Premium location", "Space: 1,200-2,000 sq ft"], "support": ["Barista training", "Pancake preparation", "Interior design", "Equipment sourcing", "Menu development"], "success_story": {"title": "Taiwan Premium Success", "story": "First Taipei location in 2016. Retro atmosphere created instant buzz.", "metrics": "6 stores | $420k avg revenue | 28-month ROI"}, "menu_highlights": ["Fluffy pancakes", "Hand-drip coffee", "Morning sets", "Retro atmosphere"], "contact_info": "Asia: asia@hoshino-coffee.com | +81-52-555-4321"},
    "Ootoya": {"story": "Premium teishoku restaurant with 500+ stores.", "investment": "$300k - $600k", "royalty": "5% - 6%", "sales": "$500k - $1M", "overseas_status": "✅ ESTABLISHED - USA, Asia", "youtube_search": "Ootoya franchise", "news_search": "Ootoya international", "financials": {"Metric": ["Investment", "Royalty", "Stores"], "Details": ["$300k-$600k", "5-6%", "50+"]}, "pros": ["Premium", "Healthy menu", "US success"], "cons": ["Complex menu", "Japanese ingredients"], "history": "Founded in 1983 in Tokyo. Specializes in teishoku (traditional Japanese set meals). 500+ locations globally with strong US presence.", "requirements": ["Minimum net worth: $700k USD", "Liquid capital: $300k+ USD", "Full-service restaurant experience", "Space: 1,500-2,500 sq ft"], "support": ["Culinary training", "Ingredient sourcing", "Menu planning", "Store design", "Staff training"], "success_story": {"title": "California Success", "story": "San Mateo location in 2015. Targets Japanese-American and health-conscious diners.", "metrics": "4 locations | $680k avg revenue | 30-month ROI"}, "menu_highlights": ["Teishoku set meals", "Grilled fish", "Tempura", "Healthy options"], "contact_info": "Franchise: franchise@otoya.co.jp | +81-3-5555-7890"}
}

# --- TRANSLATED ABOUT CONTENT ---
ABOUT_CONTENT = {
    "English": """### A Personal Journey with Japanese Culture

I'm a passionate advocate of Japanese culture and cuisine. Over the years, I've had the privilege of witnessing the remarkable growth and spread of Japanese culinary culture across Asia, Europe, and the United States.

The numbers tell an incredible story:

This **8x growth** in less than two decades is unprecedented in global food culture history.

### Our Mission

As a personal project, I started JXPerience to:

1. **📊 Aggregate Information** - Bring together comprehensive data on Japanese franchises
2. **🤝 Connect Investors** - Help serious global investors discover authentic Japanese franchise opportunities
3. **🌍 Support Expansion** - Contribute to the continued global growth of Japanese cuisine
4. **🍱 Cultural Exchange** - Enable more people worldwide to discover authentic Japanese cuisine

### The Vision

By making franchise information more accessible, we hope to:
- Support more people in discovering authentic Japanese cuisine
- Facilitate meaningful cultural exchanges through food
- Create shared experiences that bring people together
- Help Japanese brands find the right partners for global expansion

---

*This platform is a labor of love, built to support the continued growth and appreciation of Japanese culinary excellence worldwide.*""",
    "日本語": """### 日本文化との個人的な旅

私は日本文化と日本料理の熱心な支持者です。長年にわたり、アジア、ヨーロッパ、そして米国全体で日本料理文化の驚くべき成長と普及を目撃する特権を得てきました。

数字が驚くべき物語を語っています：

この20年未満での**8倍の成長**は、世界の食文化史上前例のないものです。

### 私たちのミッション

個人的なプロジェクトとして、JXPerienceを始めました：

1. **📊 情報集約** - 日本のフランチャイズに関する包括的なデータを集める
2. **🤝 投資家をつなぐ** - 真剣なグローバル投資家が本物の日本のフランチャイズ機会を発見するのを支援する
3. ** 展開を支援する** - 日本料理の継続的な世界的成長に貢献する
4. **🍱 文化交流** - 世界中のより多くの人々が本物の日本料理を発見できるようにする

### ビジョン

フランチャイズ情報をよりアクセスしやすくすることで、私たちは以下を希望しています：
- より多くの人々が本物の日本料理を発見するのを支援する
- 食を通じた意味のある文化交流を促進する
- 人々を結びつける共有体験を創造する
- 日本のブランドがグローバル展開のための適切なパートナーを見つけるのを支援する

---

*このプラットフォームは、世界中での日本料理の卓越性の継続的な成長と Appreciation を支援するために構築された、愛情のこもったプロジェクトです。*""",
    "简体中文": """### 与日本文化的个人旅程

我是日本文化和美食的热心倡导者。多年来，我有幸见证了日本美食文化在亚洲、欧洲和美国的惊人增长和传播。

数字讲述了一个令人难以置信的故事：

**8倍增长**在不到二十年内，这在全球美食文化史上是前所未有的。

### 我们的使命

作为一个个人项目，我创建了JXPerience：

1. **📊 汇总信息** - 汇总关于日本特许经营的全面数据
2. **🤝 连接投资者** - 帮助认真的全球投资者发现真实的日本特许经营机会
3. **🌍 支持扩展** - 为日本美食的持续全球增长做出贡献
4. **🍱 文化交流** - 使世界各地更多人发现真实的日本美食

### 愿景

通过使特许经营信息更易于访问，我们希望：
- 支持更多人发现真实的日本美食
- 促进通过食物进行有意义的文化交流
- 创造将人们联系在一起的共享体验
- 帮助日本品牌找到全球扩展的合适伙伴

---

*这个平台是一个充满爱的项目，旨在支持全球范围内日本美食卓越性的持续增长和欣赏。*""",
    "繁體中文": """### 與日本文化的個人旅程

我是日本文化和美食的熱心倡導者。多年來，我有幸見證了日本美食文化在亞洲、歐洲和美國的驚人增長和傳播。

數字講述了一個令人難以置信的故事：

**8倍增長**在不到二十年內，這在全球美食文化史上是前所未有的。

### 我們的使命

作為一個個人項目，我創建了JXPerience：

1. **📊 匯總信息** - 匯總關於日本特許經營的全面數據
2. **🤝 連接投資者** - 幫助認真的全球投資者發現真實的日本特許經營機會
3. **🌍 支持擴展** - 為日本美食的持續全球增長做出貢獻
4. **🍱 文化交流** - 使世界各地更多人發現真實的日本美食

### 願景

通過使特許經營信息更易於訪問，我們希望：
- 支持更多人發現真實的日本美食
- 促進通過食物進行有意義的文化交流
- 創造將人們聯繫在一起的共享體驗
- 幫助日本品牌找到全球擴展的合適伙伴

---

*這個平台是一個充滿愛的項目，旨在支持全球範圍內日本美食卓越性的持續增長和欣賞。*""",
    "한국어": """### 일본 문화와의 개인적인 여정

나는 일본 문화와 요리에 대한 열정적인 옹호자입니다. 몇 년 동안 아시아, 유럽, 미국 전역에서 일본 요리 문화의 놀라운 성장과 확산을 목격할 기회를 가졌습니다.

숫자는 놀라운 이야기를 전합니다:

이 **8배 성장**은 20년 미만의 기간 동안 전 세계 음식 문화 역사상 전례가 없는 것입니다.

### 우리의 미션

개인 프로젝트로, 저는 JXPerience를 시작했습니다:

1. **📊 정보 통합** - 일본 프랜차이즈에 대한 포괄적인 데이터를 수집
2. **🤝 투자자 연결** - 진지한 글로벌 투자자가 진짜 일본 프랜차이즈 기회를 발견하는 데 도움
3. **🌍 확장 지원** - 일본 요리의 지속적인 글로벌 성장을 기여
4. **🍱 문화 교류** - 전 세계 더 많은 사람들이 진짜 일본 요리를 발견할 수 있도록 지원

### 비전

프랜차이즈 정보를 더 쉽게 접근할 수 있도록 하여, 우리는 다음을 기대합니다:
- 더 많은 사람들이 진짜 일본 요리를 발견하는 것을 지원
- 음식을 통해 의미 있는 문화 교류를 촉진
- 사람들을 together하는 공유 경험을 창조
- 일본 브랜드가 글로벌 확장을 위한 적절한 파트너를 찾는 것을 지원

---

*이 플랫폼은 전 세계에서 일본 요리의 우수성 지속 성장과 감사함을 지원하기 위해 구축된, 사랑이 담긴 프로젝트입니다.*"""
}

# --- TRANSLATED FAQ CONTENT ---
FAQ_CONTENT = {
    "English": [
        {"q": "Is there a fee to use this platform?", "a": "No, browsing and submitting enquiries is completely free for investors."},
        {"q": "How do I know these brands are legitimate?", "a": "We verify overseas expansion status using public data, JETRO reports, and official franchise disclosures."},
        {"q": "What happens after I submit an enquiry?", "a": "Your details are securely sent to our team. We will pre-screen your profile and connect you with the franchise's international development team."},
        {"q": "Can I franchise a brand not listed here?", "a": "Yes! Use the email link above to suggest a brand. We are always adding new opportunities."}
    ],
    "日本語": [
        {"q": "このプラットフォームの利用に料金はかかりますか？", "a": "いいえ、投資家様の閲覧およびお問い合わせ送信は完全に無料です。"},
        {"q": "これらのブランドが正当であることをどうやって知ることができますか？", "a": "公開データ、JETROレポート、および公式フランチャイズ開示情報を使用して海外展開ステータスを確認しています。"},
        {"q": "お問い合わせを送信した後、どうなりますか？", "a": "お客様の詳細は安全に私たちのチームに送信されます。プロフィールを事前審査し、フランチャイズの国際開発チームと接続します。"},
        {"q": "ここにリストされていないブランドをフランチャイズできますか？", "a": "はい！上記のメールリンクを使用してブランドを提案してください。私たちは常に新しい機会を追加しています。"}
    ],
    "简体中文": [
        {"q": "使用此平台是否收费？", "a": "不，投资者的浏览和提交咨询完全免费。"},
        {"q": "如何确认这些品牌的合法性？", "a": "我们使用公开数据、JETRO报告和官方特许经营披露来验证海外扩展状态。"},
        {"q": "提交咨询后会发生什么？", "a": "您的详细信息将安全发送给我们的团队。我们将预先审核您的资料，并将您与特许经营的国际开发团队联系。"},
        {"q": "可以特许经营未列出的品牌吗？", "a": "可以！使用上面的电子邮件链接建议一个品牌。我们一直在添加新的机会。"}
    ],
    "繁體中文": [
        {"q": "使用此平台是否收費？", "a": "不，投資者的瀏覽和提交諮詢完全免費。"},
        {"q": "如何確認這些品牌的合法性？", "a": "我們使用公開數據、JETRO報告和官方特許經營披露來驗證海外擴展狀態。"},
        {"q": "提交諮詢後會發生什麼？", "a": "您的詳細信息將安全發送給我們的團隊。我們將預先審核您的資料，並將您與特許經營的國際開發團隊聯繫。"},
        {"q": "可以特許經營未列出的品牌嗎？", "a": "可以！使用上面的電子郵件鏈接建議一個品牌。我們一直在添加新的機會。"}
    ],
    "한국어": [
        {"q": "이 플랫폼을 사용하는 데 비용이 드나요?", "a": "아니오, 투자자의 탐색 및 문의 제출은 완전히 무료입니다."},
        {"q": "이 브랜드들이 정당한지 어떻게 알 수 있나요?", "a": "우리는 공개 데이터, JETRO 보고서 및 공식 프랜차이즈 공개 정보를 사용하여 해외 확장 상태를 확인합니다."},
        {"q": "문의를 제출한 후 어떻게 되나요?", "a": "귀하의 세부 정보는 우리 팀에게 안전하게 전송됩니다. 우리는 귀하의 프로필을 사전 검토하고 프랜차이즈의 국제 개발 팀과 연결합니다."},
        {"q": "목록에 없는 브랜드를 프랜차이즈할 수 있나요?", "a": "예! 위의 이메일 링크를 사용하여 브랜드를 제안하십시오. 우리는 항상 새로운 기회를 추가하고 있습니다."}
    ]
}

# --- TRANSLATED FRANCHISOR CONTENT ---
FRANCHISOR_CONTENT = {
    "English": '<div style="margin-bottom: 25px;"><h3 style="color: #1a1a2e; margin-top: 0;">Why Register as a Franchisor?</h3><p style="font-size: 1.1em; line-height: 1.6;">As a Japanese franchise brand, you have unique access to the global market. Our platform connects you directly with qualified international investors.</p></div><div class="benefit-card"><h4>✅ What You\'ll Get as a Verified Partner</h4><ul style="padding-left: 20px; margin: 15px 0;"><li><strong>Real-time qualified leads</strong> - See genuine investor applications as they come in</li><li><strong>Pre-screened investors</strong> - All applicants are vetted for serious investment capacity</li><li><strong>Dedicated dashboard</strong> - Track your leads and review applications in one place</li><li><strong>CSV export</strong> - Download your leads in spreadsheet format</li><li><strong>Direct connection</strong> - Contact investors directly through our secure platform</li></ul></div>',
    "日本語": '<div style="margin-bottom: 25px;"><h3 style="color: #1a1a2e; margin-top: 0;">なぜフランチャイザーとして登録するのか？</h3><p style="font-size: 1.1em; line-height: 1.6;">日本のフランチャイズブランドとして、グローバル市場へのユニークなアクセス権を持っています。私たちのプラットフォームは、資格のある国際投資家と直接接続します。</p></div><div class="benefit-card"><h4>✅ 認定パートナーの特典</h4><ul style="padding-left: 20px; margin: 15px 0;"><li><strong>リアルタイムの qualified リード</strong> - 投資家アプリケーションが届き次第確認</li><li><strong>事前審査済みの投資家</strong> - すべての応募者は真剣な投資能力について審査済み</li><li><strong>専用ダッシュボード</strong> - リードを追跡し、アプリケーションを一つの場所で確認</li><li><strong>CSVエクスポート</strong> - リードをスプレッドシート形式でダウンロード</li><li><strong>直接接続</strong> - 安全なプラットフォームを通じて投資家と直接連絡</li></ul></div>',
    "简体中文": '<div style="margin-bottom: 25px;"><h3 style="color: #1a1a2e; margin-top: 0;">为什么注册为特许经营商？</h3><p style="font-size: 1.1em; line-height: 1.6;">作为日本特许经营品牌，您拥有进入全球市场的独特渠道。我们的平台将您直接与合格的国际投资者连接。</p></div><div class="benefit-card"><h4>✅ 作为认证合作伙伴您将获得</h4><ul style="padding-left: 20px; margin: 15px 0;"><li><strong>实时合格的线索</strong> - 查看真实的投资人申请</li><li><strong>预先筛选的投资者</strong> - 所有申请人都经过严格审核，具有认真的投资能力</li><li><strong>专用仪表板</strong> - 在一个地方跟踪您的线索并审查申请</li><li><strong>CSV导出</strong> - 以电子表格格式下载您的线索</li><li><strong>直接连接</strong> - 通过我们的安全平台直接联系投资者</li></ul></div>',
    "繁體中文": '<div style="margin-bottom: 25px;"><h3 style="color: #1a1a2e; margin-top: 0;">為什麼註冊為特許經營商？</h3><p style="font-size: 1.1em; line-height: 1.6;">作為日本特許經營品牌，您擁有進入全球市場的獨特渠道。我們的平台將您直接與合格的國際投資者連接。</p></div><div class="benefit-card"><h4>✅ 作為認證合作夥伴您將獲得</h4><ul style="padding-left: 20px; margin: 15px 0;"><li><strong>即時合格的線索</strong> - 查看真實的投資人申請</li><li><strong>預先篩選的投資者</strong> - 所有申請人都經過嚴格審核，具有認真的投資能力</li><li><strong>專用儀表板</strong> - 在一個地方跟蹤您的線索並審查申請</li><li><strong>CSV導出</strong> - 以電子表格格式下載您的線索</li><li><strong>直接連接</strong> - 通過我們的安全平台直接聯繫投資者</li></ul></div>',
    "한국어": '<div style="margin-bottom: 25px;"><h3 style="color: #1a1a2e; margin-top: 0;">왜 프랜차이저로 등록해야 하나요?</h3><p style="font-size: 1.1em; line-height: 1.6;">일본 프랜차이즈 브랜드로서, 당신은 글로벌 시장에 대한 고유한 접근 권한을 가지고 있습니다. 우리의 플랫폼은 당신을 자격 있는 국제 투자자와 직접 연결합니다.</p></div><div class="benefit-card"><h4>✅ 인증 파트너로서 얻는 것</h4><ul style="padding-left: 20px; margin: 15px 0;"><li><strong>실시간 자격 있는 리드</strong> - 투자자 신청서가 올 때마다 확인</li><li><strong>사전 검토된 투자자</strong> - 모든 지원자는 진지한 투자 능력에 대해 검토됨</li><li><strong>전용 대시보드</strong> - 리드를 추적하고 한 곳에서 신청서를 검토</li><li><strong>CSV 내보내기</strong> - 스프레드시트 형식으로 리드 다운로드</li><li><strong>직접 연결</strong> - 안전한 플랫폼을 통해 투자자와 직접 연락</li></ul></div>'
}

# --- CONTENT HELPERS ---
def get_brand(brand):
    return FRANCHISES.get(brand, {})

def get_about():
    lang = st.session_state.language
    return ABOUT_CONTENT.get(lang, ABOUT_CONTENT["English"])

def get_faqs():
    lang = st.session_state.language
    return FAQ_CONTENT.get(lang, FAQ_CONTENT["English"])

def get_franchisor_text():
    lang = st.session_state.language
    return FRANCHISOR_CONTENT.get(lang, FRANCHISOR_CONTENT["English"])

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
            <p style="font-weight:bold; color:#059669; margin-bottom:0;"> {story["metrics"]}</p>
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
    
    st.markdown(f"""
    <div class="beta-banner">
        <h4>{t('beta_title')}</h4>
        <p style="color: #78350f; margin-bottom: 10px;">{t('beta_text1')}</p>
        <p style="color: #78350f; margin-bottom: 10px;">{t('beta_text2')}</p>
        <p style="color: #78350f; margin: 0;">{t('beta_email')} <a href="mailto:jxperience.info@gmail.com?subject=JXPerience Feedback">jxperience.info@gmail.com</a></p>
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
language = st.sidebar.selectbox("Select Language / 言語を選択 / 选择语言 / 選擇語言 / 선택 언어", 
                           ["English", "日本語", "简体中文", "繁體中文", "한국어"],
                           index=0 if st.session_state.language == "English" else 
                           1 if st.session_state.language == "日本語" else
                           2 if st.session_state.language == "简体中文" else
                           3 if st.session_state.language == "繁體中文" else 4)
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
