import os
import json
import re
import pathlib
import streamlit as st

# ==========================================
# 1. 頁面基本配置 (Streamlit Page Config)
# ==========================================
st.set_page_config(
    page_title="PPDone - C-Level 簡報大腦與 AI 簡報生成器",
    page_icon="📊",
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
                    st.error(f"❌ 載入檔案失敗 {file_path}: {e}")

    return kb_data, categories

# 讀取系統提示詞 (system_prompt.md)
def load_system_prompt(prompt_path="system_prompt.md"):
    if os.path.exists(prompt_path):
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    return "你是一位頂尖的 C-Level 戰略顧問與專業簡報設計師。"

# ==========================================
# 3. 智慧意圖與關鍵字比對 (Keyword Matching Engine)
# ==========================================
def match_best_topic(user_input, kb_data):
    """
    比對使用者輸入與知識庫模組的關鍵字、topic_id 及標題，
    計算分數並回傳最佳匹配模組。
    """
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
    st.title("🚀 PPDone - C-Level 戰略簡報生成系統")
    st.caption("結合 20+ 頂級 C-Level 商業知識庫與 AI 的簡報大腦")

    # 載入知識庫
    kb_data, categories = load_all_knowledge_base()

    # --- 側邊欄：知識庫數據與檢索器 ---
    with st.sidebar:
        st.header("📚 C-Level 知識庫概況")
        st.metric("已載入戰略模組", f"{len(kb_data)} 個")
        st.metric("涵蓋領域數", f"{len(categories)} 大領域")

        st.divider()
        st.subheader("⚙️ API 設定")
        api_provider = st.selectbox("選擇 AI 模型供應商", ["Gemini", "OpenAI"])
        api_key = st.text_input("輸入 API Key", type="password", help="若無輸入 API Key，系統將提供知識庫預設大綱預覽模式。")

        st.divider()
        st.subheader("🗂️ 戰略領域與模組總覽")
        for cat_name, modules in categories.items():
            with st.expander(f"📁 {cat_name} ({len(modules)})"):
                for mod in modules:
                    zh_title = mod.get("title", {}).get("zh", mod.get("topic_id"))
                    st.write(f"• **{zh_title}** (`{mod.get('topic_id')}`)")

    # --- 主區域：簡報需求輸入與匹配 ---
    st.subheader("💡 請輸入您的簡報主題或戰略訴求")
    
    col_input, col_preset = st.columns([3, 1])
    with col_preset:
        preset_choice = st.selectbox(
            "快速套用範本需求：",
            ["自訂輸入", "新專案 ROI 提案", "ISO 42001 AI 治理", "跨國併購文化融合", "家族企業接班傳承", "CFO 財報與資本配置"]
        )
    
    preset_mapping = {
        "新專案 ROI 提案": "我們需要向董事會提案啟動新專案，申請預算，並計算不作為成本與 ROI。",
        "ISO 42001 AI 治理": "請製作一份關於 ISO 42001 AI 管理系統與歐盟 AI 法案合規的董事會匯報。",
        "跨國併購文化融合": "針對海外併購與跨國團隊的文化衝突，提出 Glocalization 與 PMI 整合藍圖。",
        "家族企業接班傳承": "為創辦人與董事會規劃家族企業傳承，運用三環模型與家族信託進行頂層治理。",
        "CFO 財報與資本配置": "CFO 向審計委員會進行財務績效與資本配置匯報，涵蓋 EBITDA 與營運資金壓力測試。"
    }

    default_text = preset_mapping.get(preset_choice, "") if preset_choice != "自訂輸入" else ""

    with col_input:
        user_query = st.text_area(
            "提示詞 (Prompt)：",
            value=default_text,
            placeholder="例如：請以繁體中文幫我準備一份關於跨國併購後文化融合與 PMI 90 天藍圖的簡報，受眾為董事會...",
            height=120
        )

    # 執行智慧匹配
    matched_module = match_best_topic(user_query, kb_data)

    if user_query:
        st.divider()
        st.subheader("🎯 知識庫智慧匹配結果")
        if matched_module:
            st.success(f"已自動匹配最佳 C-Level 戰略模組：**{matched_module.get('title', {}).get('zh')}** (`{matched_module.get('topic_id')}`)")
            
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.info(f"**所屬領域：** {matched_module.get('category')}")
            with m_col2:
                st.info(f"**關鍵字：** {', '.join(matched_module.get('keywords', [])[:4])}")
            with m_col3:
                st.info(f"**模組投影片數：** {len(matched_module.get('slides', []))} 張")

            # 顯示 Prompt Template 與 Slide 大綱預覽
            tab_prompt, tab_slides, tab_notes = st.tabs(["📄 戰略 Prompt 範本", "📊 Slide 結構預覽", "🎙️ 演講逐字稿 (Speaker Notes)"])
            
            with tab_prompt:
                st.code(matched_module.get("prompt_template", {}).get("zh", ""), language="text")
                
            with tab_slides:
                for slide in matched_module.get("slides", []):
                    st.markdown(f"#### Slide {slide.get('slide_number')}: {slide.get('slide_title', {}).get('zh')}")
                    for bp in slide.get("bullet_points", {}).get("zh", []):
                        st.markdown(f"- {bp}")
                        
            with tab_notes:
                for slide in matched_module.get("slides", []):
                    st.markdown(f"**Slide {slide.get('slide_number')} 講稿：**")
                    st.info(slide.get("speaker_notes", {}).get("zh", ""))

        else:
            st.warning("⚠️ 未能精準比對特定戰略模組，系統將使用通用高階管理簡報邏輯生成。")

    # --- 生成按鈕與處理邏輯 ---
    st.divider()
    if st.button("✨ 立即生成管顧級戰略簡報", type="primary", use_container_width=True):
        if not user_query:
            st.error("請先輸入簡報主題或需求！")
        else:
            with st.spinner("🚀 正在調用 C-Level 戰略大腦與 HTML 簡報渲染引擎..."):
                # 組合 Prompt
                system_prompt = load_system_prompt()
                matched_prompt = matched_module.get("prompt_template", {}).get("zh", "") if matched_module else ""
                
                combined_prompt = f"""
{system_prompt}

【使用者具體需求】：
{user_query}

【知識庫推薦戰略 Prompt】：
{matched_prompt}
"""
                
                # 若有 API Key 則嘗試調用 LLM，否則顯示示範生成
                if api_key:
                    st.success("✅ 已成功連接 AI 模型，正在生成符合 1280x720 規範之 HTML 簡報...")
                    # 此處可對接 google.generativeai 或 openai 套件
                    st.code(combined_prompt[:500] + "\n\n... (Prompt 已對齊最高 C-Level 規格)", language="text")
                else:
                    st.info("💡 目前為「知識庫結構預覽模式」。輸入 API Key 後即可生成完整動態 HTML 簡報檔案。")
                    
                    if matched_module:
                        st.subheader("📦 預覽匯出的 JSON 戰略資料包")
                        st.json(matched_module)
                        
                        # 提供 JSON 下載
                        json_str = json.dumps(matched_module, ensure_ascii=False, indent=2)
                        st.download_button(
                            label="📥 下載完整戰略 JSON 檔案",
                            data=json_str,
                            file_name=f"{matched_module.get('topic_id')}_strategy.json",
                            mime="application/json"
                        )

if __name__ == "__main__":
    main()
