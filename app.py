import os
import json
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
    "caption": "Built-in consultant-grade frameworks & Knowledge Base! Generate precise outlines instantly with zero token waste." if is_en else "內建管顧級大綱原則、ISO 管理體系與本土職場生存知識庫！先為你打磨精準簡報架構，產生專屬 Prompt，複製貼上即可一鍵生成高品質 PPT。",
    
    "sys_settings": "⚙️ System Settings" if is_en else "⚙️ 系統設定",
    "api_mode_title": "Select API Key Mode:" if is_en else "選擇 AI 金鑰模式：",
    "api_mode_opts": ["🔴 Public Free Quota (Auto Cache / Free Models)", "⚪ Own OpenRouter Key"] if is_en else ["🔴 使用公共免費額度 (知識庫優先 / 自動免費模型)", "⚪ 使用自備 OpenRouter Key"],
    "pub_success": "🌱 **Public Resource Loaded.**" if is_en else "🌱 **公共資源已載入 (知識庫秒出 / AI 備援)。**",
    "pub_warn": "⚠️ **Security Notice:** For boardroom-level confidential data, please switch to 'Own Key'." if is_en else "⚠️ **資安提示**：處理高度機密數據時，強烈建議切換為「自備 Key」。",
    
    "own_key_label": "🔑 Enter OpenRouter API Key" if is_en else "🔑 請輸入 OpenRouter API Key",
    "own_key_info": "💡 **Privacy:** Key runs only in this session.\n\n🔗 [Get FREE OpenRouter Key](https://openrouter.ai/keys)" if is_en else "💡 **隱私保證**：Key 僅於當前 Session 運行，系統絕不儲存。\n\n🔗 **未有 Key？** [👉 按此免費獲取](https://openrouter.ai/keys)",
    
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
    "topic_ph": "e.g., Monthly Review, ISO 42001 AI Governance, Incident Post-mortem" if is_en else "例如：月度工作進度匯報、ISO 42001 導入計畫、跨部門協調...",
    "audience_label": "Target Audience" if is_en else "目標聽眾",
    "audience_ph": "e.g., Line Manager, Board of Directors, Students, Team" if is_en else "例如：直屬主管、董事會成員、學生、跨部門團隊",
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
    "add_info_ph": "e.g., Key KPIs, risks, resource requirements..." if is_en else "例如：重點 KPI、主要風險、具體資源需求...",
    
    "btn_generate": "🚀 Generate Outline & Prompt" if is_en else "🚀 開始生成大綱與專屬 Prompt",
    "err_key": "❌ Unable to read API Key." if is_en else "❌ 系統未能讀取 Key。請檢查 Secrets 或左側輸入。",
    "err_topic": "Please enter a topic!" if is_en else "請填寫簡報主題！",
    "err_aud": "Please specify the audience!" if is_en else "請填寫目標聽眾！",
    "sp_loading": "Searching Knowledge Base & Running AI Engine..." if is_en else "正在檢索專屬知識庫與 AI 引擎，打磨大綱與 Prompt...",
    "success_kb": "⚡ **Hit Knowledge Base Template! Generated instantly (Zero Token Used).**" if is_en else "⚡ **成功命中專家知識庫範本！秒速完成生成（零耗能 / 免 Token）。**",
    "success_ai": "🎉 **Generated via AI Engine.**" if is_en else "🎉 **已由 AI 引擎成功生成專屬大綱與 Prompt。**"
}

# -------------------------
# 2. 知識庫檢索邏輯 (Knowledge Base Router)
# -------------------------
def search_knowledge_base(user_topic):
    kb_dir = "knowledge_base"
    if not os.path.exists(kb_dir):
        return None
    
    user_topic_lower = user_topic.lower()
    for filename in os.listdir(kb_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(kb_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    kb_data = json.load(f)
                    keywords = kb_data.get("keywords", [])
                    for kw in keywords:
                        if kw.lower() in user_topic_lower:
                            return kb_data
            except Exception:
                continue
    return None

# -------------------------
# 3. 頁面渲染
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
    else:
        openrouter_key = st.text_input(ui["own_key_label"], type="password")
        st.info(ui["own_key_info"])

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
# 4. 邏輯處理與生成 (KB First -> AI Fallback)
# -------------------------
if st.button(ui["btn_generate"], type="primary"):
    if not topic:
        st.warning(ui["err_topic"])
    elif not audience:
        st.warning(ui["err_aud"])
    else:
        with st.spinner(ui["sp_loading"]):
            
            # 第一階段：嘗試從知識庫比對 JSON
            matched_kb = search_knowledge_base(topic)
            
            if matched_kb:
                st.success(ui["success_kb"])
                st.markdown("---")
                
                # 渲染 Part 1：大綱
                st.markdown(f"### Part 1: 逐頁大綱（{matched_kb.get('title', topic)}）")
                for slide in matched_kb.get("slides", []):
                    st.markdown(f"#### 投影片 {slide.get('slide_number')}｜{slide.get('slide_title')}")
                    for bp in slide.get("bullet_points", []):
                        st.markdown(f"- {bp}")
                    st.markdown(f"🗣️ **Speaker Notes**：{slide.get('speaker_notes')}\n")
                
                # 渲染 Part 2：專屬 Prompt
                st.markdown("---")
                st.markdown(f"### Part 2: {target_tool} 專用 AI Prompt")
                prompt_content = f"""請以繁體中文製作一份簡報：
【簡報主題】{topic}
【目標聽眾】{audience}
【簡報目的】{purpose}
【提示詞範本】{matched_kb.get('prompt_template', '')}
【補充內容】{additional_info}"""
                st.code(prompt_content, language="markdown")
                
            else:
                # 第二階段：未命中知識庫，降級使用 OpenRouter AI 引擎
                if not openrouter_key:
                    st.error(ui["err_key"])
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
                        
                        lang_instruction = "IMPORTANT: Please output ALL content entirely in English." if is_en else "重要提示：請使用繁體中文 (Traditional Chinese) 輸出所有內容。"

                        prompt = f"""
                        You are a senior presentation consultant and governance expert.
                        {lang_instruction}

                        【Context】
                        - Topic: {topic}
                        - Audience: {audience}
                        - Purpose: {purpose}
                        - Duration: {time_minutes} minutes (Target slides: ~{slides_count})
                        - Framework/Tone: {tone}
                        - Extra Info: {additional_info}
                        - Target AI Tool: {target_tool}

                        【Rules】
                        1. Adapt tone to '{audience}'. If students/staff, avoid bureaucratic jargon.
                        2. Keep every bullet point under ONE line, max 3 bullet points per slide.
                        3. Provide 🗣️ Speaker Notes (2-3 sentences) for each slide.

                        Please output:
                        ### Part 1: Slide-by-Slide Outline (~{slides_count} slides)
                        ### Part 2: Tailored AI Prompt for {target_tool} (Wrap in a Markdown Code Block)
                        """
                        
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
                                        {"role": "system", "content": "You are an expert presentation consultant."},
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
                            st.success(ui["success_ai"])
                            st.markdown("---")
                            st.markdown(response.choices[0].message.content)
                        else:
                            st.error(f"生成失敗：{last_err}")
                            
                    except Exception as e:
                        st.error(f"Error: {e}" if is_en else f"生成失敗，錯誤訊息：{e}")
