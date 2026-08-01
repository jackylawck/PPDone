import streamlit as st
from openai import OpenAI

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

ui = {
    "main_title": "✅ P.P.Done Generator" if is_en else "✅ 稿定 P.P.Done",
    "sub_title": '"Nail the Outline & Prompt, Get your PPT Done!"' if is_en else "「稿定大綱同 Prompt，PPT 輕鬆 Done！」",
    "caption": "Built-in consultant-grade frameworks & ISO/Governance logic! Generate precise outlines and tailored AI prompts instantly." if is_en else "內建管顧級大綱原則、ISO 管理體系與專業排版美學！先為你打磨精準簡報架構，產生專屬 Prompt，複製貼上即可一鍵生成高品質 PPT。",
    
    "sys_settings": "⚙️ System Settings" if is_en else "⚙️ 系統設定",
    "api_mode_title": "Select API Key Mode:" if is_en else "選擇 AI 金鑰模式：",
    "api_mode_opts": ["🔴 Public Free Quota (1 outline/run)", "⚪ Own OpenRouter Key (Unlimited)"] if is_en else ["🔴 使用公共免費額度 (單次 1 份大綱)", "⚪ 使用自備 OpenRouter Key (無限制)"],
    "pub_success": "🌱 **Public Resource Loaded (Trial).**" if is_en else "🌱 **公共資源已載入 (免費體驗)。**",
    "pub_warn": "⚠️ **Security Notice:** This mode is for demonstration only. For boardroom-level data, please switch to 'Own Key'." if is_en else "⚠️ **資安提示**：此模式僅供演示。處理包含高度機密數據時，強烈建議切換為「自備 Key」。",
    
    "own_key_label": "🔑 Enter OpenRouter API Key" if is_en else "🔑 請輸入 OpenRouter API Key",
    "own_key_info": "💡 **Privacy:** Key runs only in this session.\n\n🔗 [Get FREE OpenRouter Key](https://openrouter.ai/keys)" if is_en else "💡 **隱私保證**：Key 僅於當前 Session 運行，系統絕不儲存。\n\n🔗 **未有 Key？** [👉 按此免費獲取](https://openrouter.ai/keys) *(香港直連免 VPN)*",
    
    "target_tool_title": "🎯 Target AI Tool" if is_en else "🎯 目標 AI 工具",
    "tools": [
        "Gamma App (Card-by-Card / Markdown)", 
        "ChatGPT / Claude (VBA Code -> PowerPoint)", 
        "ChatGPT / Claude (Marp / Markdown Slides)",
        "Microsoft Copilot (Native PowerPoint AI)",
        "Tome / Mindshow (Visual Storytelling)",
        "Canva AI / SlidesAI (Design-centric)"
    ],
    
    "topic_label": "Presentation Topic / Core Message" if is_en else "簡報主題 / 核心訊息",
    "topic_ph": "e.g., ISO 42001 AI Management System Implementation Plan" if is_en else "例如：ISO 42001 AI 管理系統導入計畫與合規框架",
    "audience_label": "Target Audience" if is_en else "目標聽眾",
    "audience_ph": "e.g., Board of Directors, Audit Committee, C-Suite, HR Team" if is_en else "例如：董事會成員、審計委員會、高階管理層、HR 團隊",
    "purpose_label": "Presentation Purpose" if is_en else "簡報目的",
    "purpose_opts": ["Inform (Status/Sync)", "Persuade (Pitch/Resource Request)", "Facilitate (Workshop/Brainstorming)"] if is_en else ["傳達資訊 (資訊同步/進度報告)", "說服他人 (提案 Pitch/爭取資源)", "引導討論 (工作坊/腦力激盪)"],
    
    "time_label": "Expected Duration (Minutes)" if is_en else "預計演講時間 (分鐘)",
    "pace_label": "Pace (Auto-calculates slides)" if is_en else "簡報節奏 (自動推算頁數)",
    "pace_opts": [
        "Moderate: 1 slide/min (Balanced)" if is_en else "中節奏：1頁/分鐘 (適合平衡視覺與內容吸收)", 
        "Slow: <1 slide/min (Deep dive)" if is_en else "慢節奏：<1頁/分鐘 (適合詳細解說與深度探討)", 
        "Fast: 2-3 slides/min (Highly visual)" if is_en else "快節奏：2-3頁/分鐘 (適合高度視覺化、快速抓住目光)"
    ],
    "tone_label": "Presentation Tone / Framework" if is_en else "簡報風格與框架",
    "tone_opts": [
        "ISO 42001 / AI Governance & Risk Management" if is_en else "ISO 42001 / AI 治理與合規 (PDCA 框架)",
        "Boardroom / Executive Summary" if is_en else "董事會匯報 (Boardroom / Executive)",
        "ISO 31000 Risk Assessment & Internal Audit" if is_en else "ISO 31000 風險評估與內部稽核報告",
        "Mediation & Conflict Resolution / Professional Training" if is_en else "專業調解與溝通 (Mediation & Conflict Resolution)",
        "Educational / Training" if is_en else "培訓教學 (Educational / Training)",
        "High-Impact Pitch" if is_en else "商業提案 Pitch (高說服力)"
    ],
    "add_info_label": "Additional Context (Optional)" if is_en else "補充資料或重點內容 (選填)",
    "add_info_ph": "e.g., Must incorporate NIST AI RMF, mediation frameworks..." if is_en else "例如：需涵蓋調解技巧、溝通框架或 ISO 標準...",
    
    "btn_generate": "🚀 Generate Outline & Prompt" if is_en else "🚀 開始生成大綱與專屬 Prompt",
    "err_key": "❌ Unable to read OPENROUTER_API_KEY. Please check Secrets or sidebar." if is_en else "❌ 系統未能讀取 Key。請確保 Secrets 正確設定或已喺左側輸入。",
    "err_topic": "Please enter a topic!" if is_en else "請填寫簡報主題！",
    "err_aud": "Please specify the audience!" if is_en else "請填寫目標聽眾！",
    "sp_loading": "Integrating frameworks & presentation logic..." if is_en else "AI 正在融合專業架構與排版，打磨大綱與 Prompt...",
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
    openrouter_key = None

    if "🔴" in api_mode:
        openrouter_key = st.secrets.get("OPENROUTER_API_KEY", None)
        st.success(ui["pub_success"])
        st.warning(ui["pub_warn"])
        st.markdown("*(Engine: OpenRouter Auto Free Models)*")
    else:
        openrouter_key = st.text_input(ui["own_key_label"], type="password")
        st.info(ui["own_key_info"])
        st.markdown("*(Engine: OpenRouter Auto Free Models)*")

st.divider()

col1, col2 = st.columns(2)
with col1:
    topic = st.text_input(ui["topic_label"], placeholder=ui["topic_ph"])
    audience = st.text_input(ui["audience_label"], placeholder=ui["audience_ph"])
    purpose = st.selectbox(ui["purpose_label"], ui["purpose_opts"])
    
with col2:
    target_tool = st.selectbox(ui["target_tool_title"], ui["tools"])
    time_minutes = st.number_input(ui["time_label"], min_value=1, max_value=120, value=10)
    pace = st.selectbox(ui["pace_label"], ui["pace_opts"])
    tone = st.selectbox(ui["tone_label"], ui["tone_opts"])

additional_info = st.text_area(ui["add_info_label"], placeholder=ui["add_info_ph"])

# -------------------------
# 3. 邏輯處理與 AI 生成 (OpenRouter API)
# -------------------------
if st.button(ui["btn_generate"], type="primary"):
    if not openrouter_key:
        st.error(ui["err_key"])
    elif not topic:
        st.warning(ui["err_topic"])
    elif not audience:
        st.warning(ui["err_aud"])
    else:
        clean_token = str(openrouter_key).strip().strip('"').strip("'")
        
        if "1" in pace or "中" in pace:
            slides_count = time_minutes
        elif "<1" in pace or "慢" in pace:
            slides_count = max(3, int(time_minutes * 0.4))  
        else:
            slides_count = time_minutes * 2  

        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=clean_token,
            )
            
            with st.spinner(ui["sp_loading"]):
                
                lang_instruction = "IMPORTANT: Please output ALL content entirely in English." if is_en else "重要提示：請使用繁體中文 (Traditional Chinese) 輸出所有內容（包括大綱、重點、演講備註及 Prompt 指令）。"

                iso_prompt_rule = ""
                if "ISO" in tone or "Governance" in tone:
                    iso_prompt_rule = """
                    【ISO Management System & Governance Rules】
                    1. Apply the PDCA (Plan-Do-Check-Act) logic or Risk-based Thinking across the slide flow.
                    2. Include Risk Identification & Mitigation Controls where appropriate.
                    3. Ensure professional ISO/Governance terminology is used (with English terms in brackets if in Chinese).
                    """

                prompt = f"""
                You are a senior presentation architect, management consultant, and governance expert. 
                {lang_instruction}

                【Context】
                - Topic: {topic}
                - Audience: {audience}
                - Purpose: {purpose}
                - Duration: {time_minutes} minutes (Target slides: ~{slides_count})
                - Framework/Tone: {tone}
                - Extra Info: {additional_info}
                - Target AI Tool: {target_tool}

                {iso_prompt_rule}

                【Core Rules】
                1. Audience-Centric: Focus ONLY on what '{audience}' needs to hear, decide, or learn.
                2. Extreme Conciseness: Keep every bullet point strictly under ONE line.
                3. Rule of Three: MAXIMUM 3 bullet points per slide.
                4. Speaker Notes: Provide specific 🗣️ Speaker Notes (2-3 sentences) for each slide.

                Please output:
                ### Part 1: Slide-by-Slide Outline (~{slides_count} slides)
                For each slide:
                1. Slide Title (Short & Impactful)
                2. Core Takeaways (Max 3 bullet points, concise)
                3. 🗣️ Speaker Notes (Executive narrative)

                ---

                ### Part 2: Tailored AI Prompt for {target_tool}
                Generate a specific prompt for {target_tool}. Wrap it in a Markdown Code Block.
                """
                
                # 使用 OpenRouter 動態免費路由 (Auto Free Route) 及當前高可用免費模型列表
                free_models = [
                    "openrouter/auto",
                    "meta-llama/llama-3.3-70b-instruct:free",
                    "mistralai/mistral-7b-instruct:free"
                ]
                
                response = None
                last_err = None

                for m in free_models:
                    try:
                        response = client.chat.completions.create(
                            extra_headers={
                                "HTTP-Referer": "https://ppdone.streamlit.app", 
                                "X-Title": "PPDone Generator",
                            },
                            messages=[
                                {"role": "system", "content": "You are an expert presentation consultant and governance auditor."},
                                {"role": "user", "content": prompt}
                            ],
                            model=m,
                            temperature=0.7,
                        )
                        if response:
                            break
                    except Exception as err:
                        last_err = err
                        continue

                if response:
                    st.success(ui["success_msg"])
                    st.markdown("---")
                    st.markdown(response.choices[0].message.content)
                else:
                    st.error(f"生成失敗：{last_err}")
                
        except Exception as e:
            st.error(f"Error: {e}" if is_en else f"生成失敗，錯誤訊息：{e}")
