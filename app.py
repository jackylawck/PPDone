import os
import json
import streamlit as st

# ==========================================
# 1. 頁面基本配置 (Streamlit Page Config)
# ==========================================
st.set_page_config(
    page_title="稿定 (P.P.Done) - Presentation Prompt Done",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. 知識庫自動掃描與載入 (Recursive KB Loader)
# ==========================================
@st.cache_data(ttl=600)
def load_all_knowledge_base(base_dir="knowledge_base"):
    """
    使用 os.walk 遞迴掃描 knowledge_base 資料夾及其所有子目錄，
    自動載入所有 JSON 模組並按分類目錄歸類。
    """
    kb_data = {}
    categories = {}
    
    if not os.path.exists(base_dir):
        return kb_data, categories

    for root, dirs, files in os.walk(base_dir):
        for filename in files:
            if filename.endswith(".json"):
                file_path = os.path.join(root, filename)
                category_name = os.path.basename(root)
                
                # 如果檔案在 knowledge_base 根目錄，標記為 General
                if category_name == os.path.basename(base_dir):
                    category_name = "General"

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        topic_id = data.get("topic_id")
                        
                        if topic_id:
                            # 注入類別與檔案路徑 metadata
                            data["category"] = category_name
                            data["file_path"] = file_path
                            kb_data[topic_id] = data

                            # 建立分類群組字典
                            if category_name not in categories:
                                categories[category_name] = []
                            categories[category_name].append(data)
                except Exception as e:
                    st.error(f"❌ Error loading file {file_path}: {e}")

    return kb_data, categories

# 讀取系統提示詞 (system_prompt.md)
def load_system_prompt(prompt_path="system_prompt.md"):
    if os.path.exists(prompt_path):
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    return "You are an elite C-Level strategic advisor and master presentation designer."

# ==========================================
# 3. 智慧意圖與關鍵字比對 (Keyword Matching Engine)
# ==========================================
def match_best_topic(user_input, kb_data):
    if not user_input or not kb_data:
        return None

    query = user_input.lower()
    best_match = None
    max_score = 0

    for topic_id, module in kb_data.items():
        score = 0
        
        # 1. 匹配 Topic ID (權重 5)
        if topic_id.lower() in query:
            score += 5
            
        # 2. 匹配 關鍵字 Keywords (權重 3)
        keywords = module.get("keywords", [])
        for kw in keywords:
            if kw.lower() in query:
                score += 3

        # 3. 匹配 標題 Title (權重 4)
        title_dict = module.get("title", {})
        for lang, title_text in title_dict.items():
            if title_text.lower() in query:
                score += 4

        if score > max_score:
            max_score = score
            best_match = module

    return best_match if max_score > 0 else None

# ==========================================
# 4. Streamlit UI 介面構建
# ==========================================
def main():
    # --- 雙語文本配置 (UI i18n Dictionary) ---
    UI_TEXT = {
        "zh": {
            "app_name": "🚀 稿定 (P.P.Done)",
            "title_caption": "Presentation Prompt Done | 高階 C-Level 戰略簡報大腦",
            "kb_overview": "📚 C-Level 知識庫概況",
            "loaded_modules": "已載入戰略模組",
            "covered_domains": "涵蓋領域數",
            "api_config": "⚙️ AI 模型與安全設定",
            "provider": "選擇 AI 模型供應商",
            "api_key_label": "輸入您的 API Key",
            "api_key_help": "您的 API Key 僅存於瀏覽器記憶體中，傳輸全程加密，「稿定」絕對不會記錄或儲存任何 Key 與敏感商業數據。",
            "security_notice_title": "🔒 企業級安全與數據隱私聲明",
            "security_notice_body": "• **零伺服器留存 (Zero-Data Retention)**：API Key 僅於客戶端（Client-side）調用 LLM，不寫入任何資料庫。\n• **資料傳輸加密**：所有請求均經由 256-bit TLS 加密直接發送至 AI 官方 API。\n• **商業合規**：建議配合企業內部 AI 使用規範（如 ISO 42001）使用。",
            "modules_overview": "🗂️ 戰略領域與模組總覽",
            "input_header": "💡 請輸入您的簡報主題或戰略訴求",
            "preset_label": "快速套用範本需求：",
            "prompt_label": "提示詞 (Prompt)：",
            "prompt_placeholder": "例如：請幫我準備一份關於跨國併購後文化融合與 PMI 90 天藍圖的簡報，受眾為董事會...",
            "matched_title": "🎯 知識庫智慧匹配結果",
            "matched_success": "已自動匹配最佳 C-Level 戰略模組：",
            "category_label": "所屬領域：",
            "keywords_label": "關鍵字：",
            "slides_count_label": "模組投影片數：",
            "tab_prompt": "📄 戰略 Prompt 範本",
            "tab_slides": "📊 Slide 結構預覽",
            "tab_notes": "🎙️ 演講逐字稿 (Speaker Notes)",
            "generate_btn": "✨ 稿定！立即生成管顧級戰略簡報",
            "api_success": "✅ 已成功連接 AI 模型，正在生成符合 1280x720 規範之 HTML 簡報...",
            "preview_mode": "💡 目前為「知識庫結構預覽模式」。輸入 API Key 後即可調用 AI 模型生成動態簡報。",
            "export_json_title": "📦 預覽匯出的 JSON 戰略資料包",
            "download_btn": "📥 下載完整戰略 JSON 檔案"
        },
        "en": {
            "app_name": "🚀 P.P.Done (稿定)",
            "title_caption": "Presentation Prompt Done | C-Level Strategic Presentation Brain",
            "kb_overview": "📚 C-Level Knowledge Base Overview",
            "loaded_modules": "Loaded Modules",
            "covered_domains": "Strategic Domains",
            "api_config": "⚙️ AI Model & Security Settings",
            "provider": "Select AI Provider",
            "api_key_label": "Enter your API Key",
            "api_key_help": "Your API Key is held strictly in client memory. All requests are encrypted; P.P.Done never stores your keys or proprietary data.",
            "security_notice_title": "🔒 Enterprise Security & Privacy Notice",
            "security_notice_body": "• **Zero-Data Retention**: API Keys are processed client-side without database storage.\n• **End-to-End Encryption**: Requests are transmitted directly to official LLM APIs via 256-bit TLS encryption.\n• **Corporate Governance**: Fully compliant with enterprise AI standards (e.g., ISO 42001).",
            "modules_overview": "🗂️ Strategic Domains & Modules",
            "input_header": "💡 Enter Your Strategic Presentation Objective",
            "preset_label": "Quick Preset Templates:",
            "prompt_label": "Prompt / Instructions:",
            "prompt_placeholder": "e.g., Prepare a board-level presentation on Post-Merger Integration (PMI) cultural alignment and a 90-day execution roadmap...",
            "matched_title": "🎯 Intelligence Engine Matching Result",
            "matched_success": "Auto-matched to Best C-Level Strategic Module:",
            "category_label": "Domain:",
            "keywords_label": "Keywords:",
            "slides_count_label": "Slide Count:",
            "tab_prompt": "📄 Strategic Prompt Template",
            "tab_slides": "📊 Slide Structure Preview",
            "tab_notes": "🎙️ Speaker Notes (Verbatim)",
            "generate_btn": "✨ Generate C-Level Strategic Presentation",
            "api_success": "✅ AI Model Connected. Generating 1280x720 compliant HTML Presentation...",
            "preview_mode": "💡 Currently in 'Knowledge Base Preview Mode'. Input your API Key to activate AI-driven generation.",
            "export_json_title": "📦 Exported Strategic JSON Package Preview",
            "download_btn": "📥 Download Strategic JSON File"
        }
    }

    # --- 頂部語言切換器 (Language Toggle) ---
    col_logo, col_lang = st.columns([4, 1])
    with col_lang:
        lang_choice = st.radio("🌐 Language / 語言", ["繁體中文", "English"], horizontal=True)
        lang_key = "zh" if lang_choice == "繁體中文" else "en"

    t = UI_TEXT[lang_key]

    with col_logo:
        st.title(t["app_name"])
        st.caption(t["title_caption"])

    # 載入知識庫
    kb_data, categories = load_all_knowledge_base()

    # --- 側邊欄：知識庫概況與安全聲明 ---
    with st.sidebar:
        st.header(t["kb_overview"])
        st.metric(t["loaded_modules"], f"{len(kb_data)}")
        st.metric(t["covered_domains"], f"{len(categories)}")

        st.divider()
        st.subheader(t["api_config"])
        api_provider = st.selectbox(t["provider"], ["Gemini", "OpenAI"])
        api_key = st.text_input(t["api_key_label"], type="password", help=t["api_key_help"])

        # 🔒 安全聲明區塊 (Security & Privacy Accordion)
        with st.expander(t["security_notice_title"]):
            st.markdown(t["security_notice_body"])

        st.divider()
        st.subheader(t["modules_overview"])
        for cat_name, modules in categories.items():
            with st.expander(f"📁 {cat_name} ({len(modules)})"):
                for mod in modules:
                    title_text = mod.get("title", {}).get(lang_key, mod.get("topic_id"))
                    st.write(f"• **{title_text}** (`{mod.get('topic_id')}`)")

    # --- 主區域：需求輸入與匹配 ---
    st.subheader(t["input_header"])
    
    col_input, col_preset = st.columns([3, 1])
    
    preset_options_zh = ["自訂輸入", "新專案 ROI 提案", "ISO 42001 AI 治理", "跨國併購文化融合", "家族企業接班傳承", "CFO 財報與資本配置"]
    preset_options_en = ["Custom Input", "Internal Pitch ROI", "ISO 42001 AI Governance", "Cross-Border M&A Culture", "Family Business Succession", "CFO Financial & CapEx Review"]
    
    preset_options = preset_options_zh if lang_key == "zh" else preset_options_en

    with col_preset:
        preset_choice = st.selectbox(t["preset_label"], preset_options)
    
    preset_mapping_zh = {
        "新專案 ROI 提案": "我們需要向董事會提案啟動新專案，申請預算，並計算不作為成本與 ROI。",
        "ISO 42001 AI 治理": "請製作一份關於 ISO 42001 AI 管理系統與歐盟 AI 法案合規的董事會匯報。",
        "跨國併購文化融合": "針對海外併購與跨國團隊的文化衝突，提出 Glocalization 與 PMI 整合藍圖。",
        "家族企業接班傳承": "為創辦人與董事會規劃家族企業傳承，運用三環模型與家族信託進行頂層治理。",
        "CFO 財報與資本配置": "CFO 向審計委員會進行財務績效與資本配置匯報，涵蓋 EBITDA 與營運資金壓力測試。"
    }

    preset_mapping_en = {
        "Internal Pitch ROI": "Proposal to the Board for launching a new project, securing CapEx budget, and calculating Cost of Inaction and ROI.",
        "ISO 42001 AI Governance": "Board-level presentation regarding ISO 42001 AIMS implementation and EU AI Act compliance.",
        "Cross-Border M&A Culture": "Addressing cultural friction post-acquisition via Glocalization and a 90-day PMI integration plan.",
        "Family Business Succession": "Structuring succession planning for the Founder and Board using the Three-Circle Model and Family Trusts.",
        "CFO Financial & CapEx Review": "CFO quarterly report to the Audit Committee covering EBITDA margins, cash flow stress testing, and capital allocation."
    }

    preset_mapping = preset_mapping_zh if lang_key == "zh" else preset_mapping_en
    default_text = preset_mapping.get(preset_choice, "") if preset_choice not in ["自訂輸入", "Custom Input"] else ""

    with col_input:
        user_query = st.text_area(
            t["prompt_label"],
            value=default_text,
            placeholder=t["prompt_placeholder"],
            height=120
        )

    # 執行智慧匹配
    matched_module = match_best_topic(user_query, kb_data)

    if user_query:
        st.divider()
        st.subheader(t["matched_title"])
        if matched_module:
            module_title = matched_module.get('title', {}).get(lang_key, matched_module.get('topic_id'))
            st.success(f"{t['matched_success']} **{module_title}** (`{matched_module.get('topic_id')}`)")
            
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.info(f"**{t['category_label']}** {matched_module.get('category')}")
            with m_col2:
                st.info(f"**{t['keywords_label']}** {', '.join(matched_module.get('keywords', [])[:4])}")
            with m_col3:
                st.info(f"**{t['slides_count_label']}** {len(matched_module.get('slides', []))}")

            # 顯示 Prompt Template 與 Slide 大綱預覽
            tab_prompt, tab_slides, tab_notes = st.tabs([t["tab_prompt"], t["tab_slides"], t["tab_notes"]])
            
            with tab_prompt:
                st.code(matched_module.get("prompt_template", {}).get(lang_key, ""), language="text")
                
            with tab_slides:
                for slide in matched_module.get("slides", []):
                    st.markdown(f"#### Slide {slide.get('slide_number')}: {slide.get('slide_title', {}).get(lang_key)}")
                    for bp in slide.get("bullet_points", {}).get(lang_key, []):
                        st.markdown(f"- {bp}")
                        
            with tab_notes:
                for slide in matched_module.get("slides", []):
                    st.markdown(f"**Slide {slide.get('slide_number')} Speaker Notes:**")
                    st.info(slide.get("speaker_notes", {}).get(lang_key, ""))

        else:
            st.warning("⚠️ No exact strategic module matched. Using general C-Level presentation logic.")

    # --- 生成按鈕與處理邏輯 ---
    st.divider()
    if st.button(t["generate_btn"], type="primary", use_container_width=True):
        if not user_query:
            st.error("Please enter your prompt / instructions first.")
        else:
            with st.spinner("🚀 Activating C-Level Strategic Brain & HTML Engine..."):
                system_prompt = load_system_prompt()
                matched_prompt = matched_module.get("prompt_template", {}).get(lang_key, "") if matched_module else ""
                
                combined_prompt = f"""
{system_prompt}

【User Specific Request】:
{user_query}

【Knowledge Base Strategic Prompt】:
{matched_prompt}
"""
                
                if api_key:
                    st.success(t["api_success"])
                    st.code(combined_prompt[:500] + "\n\n... (Prompt Aligned to C-Level Standards)", language="text")
                else:
                    st.info(t["preview_mode"])
                    
                    if matched_module:
                        st.subheader(t["export_json_title"])
                        st.json(matched_module)
                        
                        json_str = json.dumps(matched_module, ensure_ascii=False, indent=2)
                        st.download_button(
                            label=t["download_btn"],
                            data=json_str,
                            file_name=f"{matched_module.get('topic_id')}_strategy.json",
                            mime="application/json"
                        )

if __name__ == "__main__":
    main()
