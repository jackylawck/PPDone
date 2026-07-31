import streamlit as st
import google.generativeai as genai

# 頁面基本設定
st.set_page_config(
    page_title="P.P.Done | AI Presentation Builder", 
    page_icon="✅", 
    layout="wide"
)

# -------------------------
# 1. 語言設定與 UI 字典
# -------------------------
with st.sidebar:
    st.markdown("### 🌐 界面與報告語言 (UI & Output Language)")
    lang_choice = st.selectbox(
        "",
        ["繁體中文 (Traditional Chinese)", "English (Full)"],
        label_visibility="collapsed"
    )

is_en = "English" in lang_choice

# 根據選擇的語言設定 UI 文字
ui = {
    "main_title": "✅ P.P.Done Generator" if is_en else "✅ 稿定 P.P.Done",
    "sub_title": '"Nail the Outline & Prompt, Get your PPT Done!"' if is_en else "「稿定大綱同 Prompt，PPT 輕鬆 Done！」",
    "caption": "Built-in consultant-grade frameworks & design aesthetics! Generate precise outlines and tailored AI prompts to build high-quality presentations instantly." if is_en else "內建管顧級大綱原則與專業排版美學！先為你打磨精準簡報架構，產生專屬 Prompt，複製貼上即可一鍵生成高品質 PPT。",
    
    "sys_settings": "⚙️ System Settings" if is_en else "⚙️ 系統設定",
    "api_mode_title": "Select API Key Mode:" if is_en else "選擇 AI 金鑰模式：",
    "api_mode_opts": ["🔴 Public Free Quota (1 outline/run)", "⚪ Own AI API Key (Unlimited & Private)"] if is_en else ["🔴 使用公共免費額度 (單次 1 份大綱)", "⚪ 使用自備 AI API Key (無限制 & 高隱私)"],
    "pub_success": "🌱 **Public Resource Loaded (Trial).**" if is_en else "🌱 **公共資源已載入 (免費體驗)。**",
    "pub_warn": "⚠️ **Security Notice:** This mode is for demonstration only. For boardroom-level or highly sensitive corporate data, please switch to 'Own Key' for zero data retention." if is_en else "⚠️ **資安提示**：此模式僅供演示。處理包含高度機密、董事會級別或企業內部敏感數據時，強烈建議切換為「自備 Key」以落實零數據留存。",
    "own_key_label": "🔑 Enter your Gemini API Key" if is_en else "🔑 請輸入你的 Gemini API Key",
    "own_key_info": "💡 **Privacy Guarantee:** Your key runs only in this browser session. The system retains absolutely zero data." if is_en else "💡 **隱私保證**：自備 Key 僅會於當前瀏覽器 Session 運行，系統不會作任何儲存或紀錄，確保資料 100% 留存在你的掌控中。",
    
    "target_tool_title": "### 🎯 Target AI Tool" if is_en else "### 🎯 目標 AI 工具",
    "tools": [
        "Gamma App (Card-by-Card / Markdown)", 
        "ChatGPT / Claude (VBA Code -> PowerPoint)", 
        "ChatGPT / Claude (Marp / Markdown Slides)",
        "Microsoft Copilot (Native PowerPoint AI)",
        "Tome / Mindshow (Visual Storytelling)",
        "Canva AI / SlidesAI (Design-centric)"
    ],
    
    "topic_label": "Presentation Topic / Core Message" if is_en else "簡報主題 / 核心訊息",
    "topic_ph": "e.g., ISO 42001 AI Management System Implementation" if is_en else "例如：ISO 42001 AI 管理系統導入計畫",
    "audience_label": "Target Audience" if is_en else "目標聽眾",
    "audience_ph": "e.g., Board of Directors, C-Suite, HR Team" if is_en else "例如：董事會成員、高階管理層、HR 團隊",
    "purpose_label": "Presentation Purpose" if is_en else "簡報目的",
    "purpose_opts": ["Inform (Status/Sync)", "Persuade (Pitch/Resource Request)", "Facilitate (Workshop/Brainstorming)"] if is_en else ["傳達資訊 (資訊同步/進度報告)", "說服他人 (提案 Pitch/爭取資源)", "引導討論 (工作坊/腦力激盪)"],
    
    "time_label": "Expected Duration (Minutes)" if is_en else "預計演講時間 (分鐘)",
    "pace_label": "Pace (Auto-calculates slides)" if is_en else "簡報節奏 (自動推算頁數)",
    "pace_opts": [
        "Moderate: 1 slide/min (Balanced)" if is_en else "中節奏：1頁/分鐘 (適合平衡視覺與內容吸收)", 
        "Slow: <1 slide/min (Deep dive)" if is_en else "慢節奏：<1頁/分鐘 (適合詳細解說與深度探討)", 
        "Fast: 2-3 slides/min (Highly visual)" if is_en else "快節奏：2-3頁/分鐘 (適合高度視覺化、快速抓住目光)"
    ],
    "tone_label": "Presentation Tone" if is_en else "簡報風格",
    "tone_opts": ["Boardroom / Executive", "Risk & Compliance Report", "Educational / Training", "High-Impact Pitch"] if is_en else ["專業商務 (Boardroom / Executive)", "風險評估與合規報告", "培訓教學 (Educational)", "提案 Pitch (高說服力)"],
    "add_info_label": "Additional Context (Optional)" if is_en else "補充資料或重點內容 (選填)",
    "add_info_ph": "e.g., Must cover AI governance frameworks, risk metrics..." if is_en else "例如：需涵蓋 AI 治理框架、風險管理標準，並提供企業落地案例...",
    
    "btn_generate": "🚀 Generate Outline & Prompt" if is_en else "🚀 開始生成大綱與專屬 Prompt",
    "err_key": "❌ Please enter your API Key in the sidebar." if is_en else "❌ 系統未能讀取 API Key。請確保已在左側輸入。",
    "err_topic": "Please enter a topic!" if is_en else "請填寫簡報主題！",
    "err_aud": "Please specify the audience! (Audience-centric approach requires this)" if is_en else "請填寫目標聽眾！(以人為本的簡報需要明確聽眾)",
    "sp_loading": "Applying presentation frameworks..." if is_en else "AI 正在融合專業排版與各平台特色，為你打磨大綱與 Prompt...",
    "success_msg": "🎉 Done! Your outline and prompt are ready." if is_en else "🎉 搞定！已為你規劃好大綱與專屬 Prompt。"
}

# -------------------------
# 2. 頁面渲染
# -------------------------
st.title(ui["main_title"])
st.subheader(ui["sub_title"])
st.caption(ui["caption"])

with st.sidebar:
    st.divider()
    st.header(ui["sys_settings"])
    
    api_mode = st.radio(ui["api_mode_title"], ui["api_mode_opts"], index=0, label_visibility="collapsed")
    api_key = None

    if "🔴" in api_mode:
        api_key = st.secrets.get("GEMINI_API_KEY", None)
        st.success(ui["pub_success"])
        st.warning(ui["pub_warn"])
        st.markdown("*(Engine: Gemini 1.5 Flash)*")
    else:
        api_key = st.text_input(ui["own_key_label"], type="password")
        st.info(ui["own_key_info"])
        st.markdown("*(Engine: Gemini 1.5 Flash)*")

    st.divider()
    st.markdown(ui["target_tool_title"])
    target_tool = st.selectbox("", ui["tools"], label_visibility="collapsed")

col1, col2 = st.columns(2)
with col1:
    topic = st.text_input(ui["topic_label"], placeholder=ui["topic_ph"])
    audience = st.text_input(ui["audience_label"], placeholder=ui["audience_ph"])
    purpose = st.selectbox(ui["purpose_label"], ui["purpose_opts"])
    
with col2:
    time_minutes = st.number_input(ui["time_label"], min_value=1, max_value=120, value=10)
    pace = st.selectbox(ui["pace_label"], ui["pace_opts"])
    tone = st.selectbox(ui["tone_label"], ui["tone_opts"])

additional_info = st.text_area(ui["add_info_label"], placeholder=ui["add_info_ph"])

# -------------------------
# 3. 邏輯處理與 AI 生成
# -------------------------
if st.button(ui["btn_generate"], type="primary"):
    if not api_key:
        st.error(ui["err_key"])
    elif not topic:
        st.warning(ui["err_topic"])
    elif not audience:
        st.warning(ui["err_aud"])
    else:
        # 計算頁數
        if "1" in pace or "中" in pace:
            slides_count = time_minutes
        elif "<1" in pace or "慢" in pace:
            slides_count = max(3, int(time_minutes * 0.4))  
        else:
            slides_count = time_minutes * 2  

        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner(ui["sp_loading"]):
                
                # 輸出語言控制
                lang_instruction = "IMPORTANT: Please output ALL content (including the outline, bullet points, speaker notes, and the prompt itself) entirely in English." if is_en else "重要提示：請使用繁體中文 (Traditional Chinese) 輸出所有內容（包括大綱、重點、演講備註及 Prompt 指令）。"

                prompt = f"""
                You are a senior presentation architect and management consultant. 
                {lang_instruction}

                【Context】
                - Topic: {topic}
                - Audience: {audience}
                - Purpose: {purpose}
                - Duration: {time_minutes} minutes (Target slides: ~{slides_count})
                - Tone: {tone}
                - Extra Info: {additional_info}
                - Target AI Tool: {target_tool}

                【Rules (Strictly follow consulting-grade principles)】
                1. Audience-Centric: Focus ONLY on what '{audience}' needs to hear and decide.
                2. Extreme Conciseness (No Text Wrapping): Eliminate filler words. Keep every bullet point strictly under ONE line.
                3. Rule of Three: MAXIMUM 3 bullet points per slide.
                4. Don't Read Slides: Provide specific 🗣️ Speaker Notes (2-3 sentences) for each slide.

                Please output the following two sections:
                
                ### Part 1: Slide-by-Slide Outline
                For each of the ~{slides_count} slides, provide:
                1. Slide Title (Very short & impactful)
                2. Core Takeaways (Max 3 bullet points, extreme conciseness)
                3. 🗣️ Speaker Notes (What the presenter should actually say)

                ---

                ### Part 2: Tailored AI Prompt for {target_tool}
                Generate a specific prompt for the user to copy-paste into {target_tool} to build this presentation.
                - If Gamma: Demand Card-by-Card logic, 40% translucent text backing, high contrast, and include specific Image Prompts.
                - If VBA/Copilot: Demand Arial/Calibri font >=18pt, high contrast background, center-aligned titles, and no text wrapping.
                Put this prompt inside a Markdown Code Block.
                """
                
                response = model.generate_content(prompt)
                
                st.success(ui["success_msg"])
                st.markdown("---")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Error: {e}" if is_en else f"生成失敗，錯誤訊息：{e}")
