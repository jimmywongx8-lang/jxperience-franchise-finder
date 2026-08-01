import streamlit as st
import pandas as pd
from openai import OpenAI
import json
import os

# --- CONFIGURATION ---
# SECURE API KEY - reads from Streamlit Secrets
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

# CSV path - works for both local and Streamlit Cloud
if os.path.exists("C:\\jfa_scraper\\franchise_data.csv"):
    CSV_PATH = "C:\\jfa_scraper\\franchise_data.csv"
else:
    CSV_PATH = "franchise_data.csv"

st.set_page_config(
    page_title="JXPerience | フランチャイズ登録", 
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
        letter-spacing: -0.5px;
    }
    .brand-accent {
        color: #0066cc;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-top: -10px;
    }
    .info-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
        border-left: 4px solid #0066cc;
    }
    .step-badge {
        background: #0066cc;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 8px;
    }
    .inquiry-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 16px;
        padding: 30px;
        margin: 20px 0;
        border: 2px solid #0066cc;
    }
    </style>
""", unsafe_allow_html=True)

# Navigation & Header
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("⬅️ メインページに戻る"):
        st.switch_page("app.py")
with col2:
    st.markdown('<div class="main-header"><span class="brand-accent">JX</span>Perience</div>', unsafe_allow_html=True)

st.markdown('<div class="sub-header">フランチャイズ・オーナー様向け オンボーディング</div>', unsafe_allow_html=True)
st.markdown("日本のブランド紹介文を貼り付けてください。AIが自動的に英訳し、海外投資家向けに最適化します。")

# Check API Key
if not GROQ_API_KEY:
    st.error("️ APIキーが設定されていません。管理者にお問い合わせください。")
    st.stop()

# Initialize AI Client
client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")

# --- INFO BOX ---
st.markdown("""
    <div class="info-box">
        <strong>💡 ご利用方法：</strong><br>
        1. ブランド名と日本語の紹介文（公式サイト、パンフレット、IR資料など）を貼り付けます<br>
        2. 「AIで投資案件概要を生成」ボタンをクリック<br>
        3. 生成された英語データを編集・確認<br>
        4. データベースに保存 → 海外投資家向けプラットフォームに公開されます
    </div>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_data' not in st.session_state:
    st.session_state['generated_data'] = None
if 'ready_to_save' not in st.session_state:
    st.session_state['ready_to_save'] = False

# --- STEP 1: INPUT FORM ---
with st.form("onboarding_form"):
    st.subheader("1. ブランド情報入力")
    brand_name_input = st.text_input("ブランド名（ローマ字または英語）", placeholder="例：Ichiran, Gogo Curry")
    raw_text = st.text_area(
        "日本語の紹介文を貼り付け", 
        height=200, 
        placeholder="貴社のフランチャイズ情報、投資条件、沿革などを日本語で貼り付けてください...",
        help="AIが自動的に英訳し、投資金額・店舗数などの数値データを抽出します。"
    )
    
    submitted = st.form_submit_button("✨ AIで英語の投資案件概要を生成")

    if submitted:
        if not brand_name_input or not raw_text:
            st.error("ブランド名と紹介文の両方を入力してください。")
        else:
            with st.spinner("🤖 AIが翻訳・分析中..."):
                try:
                    prompt = f"""あなたは日本のフランチャイズ専門アナリスト兼翻訳家です。
以下の日本語テキストを読み、海外投資家向けに最適な英語データを抽出・翻訳してください。
数値データ（投資額、ロイヤリティなど）が明確でない場合は、業界標準に基づいて妥当な範囲を推定し、備考に「推定値」と明記してください。

出力は厳密に以下のJSON形式のみで返してください（マークダウンや説明文は不要）：
{{
    "brand_name": "{brand_name_input}",
    "category": "カテゴリ（例：Ramen, Sushi, Cafe, Fast Food）",
    "stores_japan": "日本国内店舗数（例：100+）",
    "stores_overseas": "海外店舗数（例：20+）",
    "investment_usd": "総投資額USD（例：150k-300k）",
    "franchise_fee_usd": "フランチャイズ手数料USD（例：50000）",
    "royalty_pct": "ロイヤリティ％（例：5.0）",
    "target_markets": "対象市場（例：SE Asia, USA, Europe）",
    "website": "公式サイトURL（例：brand.com）",
    "overseas_franchise_confirmed": "海外展開実績（YES / PROBABLE / NEEDS_VERIFICATION のいずれか）",
    "expansion_type": "展開形態（Single-unit / Master Franchise / Joint Venture）",
    "notes": "ブランドの強み・差別化ポイント（英語1文）"
}}

日本語テキスト：
{raw_text}
"""

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.3,
                        response_format={"type": "json_object"}
                    )
                    
                    st.session_state['generated_data'] = json.loads(response.choices[0].message.content)
                    st.session_state['ready_to_save'] = True

                except Exception as e:
                    st.error(f"AI処理エラー: {e}")

# --- STEP 2: REVIEW & SAVE ---
if st.session_state.get('ready_to_save'):
    st.markdown("---")
    st.subheader("2. データの確認・編集")
    st.info("AIが生成した英語データを確認してください。投資家向けに公開される内容です。必要に応じて修正してから保存してください。")
    
    data = st.session_state['generated_data']
    
    col1, col2 = st.columns(2)
    with col1:
        data['category'] = st.text_input("カテゴリ", data.get('category', ''))
        data['stores_japan'] = st.text_input("日本国内店舗数", data.get('stores_japan', ''))
        data['stores_overseas'] = st.text_input("海外店舗数", data.get('stores_overseas', ''))
        data['investment_usd'] = st.text_input("総投資額（USD）", data.get('investment_usd', ''))
        data['franchise_fee_usd'] = st.text_input("フランチャイズ手数料（USD）", data.get('franchise_fee_usd', ''))
        data['royalty_pct'] = st.text_input("ロイヤリティ（％）", data.get('royalty_pct', ''))
    
    with col2:
        data['target_markets'] = st.text_input("対象市場", data.get('target_markets', ''))
        data['website'] = st.text_input("公式サイトURL", data.get('website', ''))
        
        overseas_options = ["YES", "PROBABLE", "NEEDS_VERIFICATION", "NO"]
        current_overseas = str(data.get('overseas_franchise_confirmed', 'NEEDS_VERIFICATION')).upper().strip()
        if current_overseas not in overseas_options:
            current_overseas = 'NEEDS_VERIFICATION'
        data['overseas_franchise_confirmed'] = st.selectbox("海外展開実績", overseas_options, index=overseas_options.index(current_overseas))
        
        expansion_options = ["Single-unit", "Master Franchise", "Joint Venture"]
        current_expansion = str(data.get('expansion_type', 'Single-unit')).strip()
        if 'Single' in current_expansion:
            current_expansion = 'Single-unit'
        elif 'Master' in current_expansion:
            current_expansion = 'Master Franchise'
        elif 'Joint' in current_expansion:
            current_expansion = 'Joint Venture'
        else:
            current_expansion = 'Single-unit'
        
        data['expansion_type'] = st.selectbox("展開形態", expansion_options, index=expansion_options.index(current_expansion))
        data['notes'] = st.text_area("備考・ブランドの強み", data.get('notes', ''))

    if st.button("✅ 確認してデータベースに保存", type="primary"):
        try:
            new_row = pd.DataFrame([data])
            file_exists = os.path.isfile(CSV_PATH)
            new_row.to_csv(CSV_PATH, mode='a', header=not file_exists, index=False, encoding='utf-8')
            
            st.success("✅ 保存完了！貴社ブランドがデータベースに追加されました。")
            st.balloons()
            
            st.session_state['ready_to_save'] = False
            st.session_state['generated_data'] = None
            
            st.info("「メインページに戻る」ボタンをクリックして、追加されたブランドをご確認ください。")
            
        except Exception as e:
            st.error(f"保存エラー: {e}")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888; font-size: 0.85rem;'>© 2026 <span style='color:#0066cc'>JX</span>Perience | 日本フランチャイズ海外展開プラットフォーム</div>", unsafe_allow_html=True)
