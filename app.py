import streamlit as st
import google.generativeai as genai

# 頁面基本設定
st.set_page_config(
    page_title="稿定 P.P.Done | AI 簡報大綱與 Prompt 生成器", 
    page_icon="✅", 
    layout="wide"
)

# 標題與標語
st.title("✅ 稿定 P.P.Done")
st.subheader("「稿定大綱同 Prompt，PPT 輕鬆 Done！」")
st.caption("專為慳 Token 打造！先為你打磨精準簡報架構，產生專屬 Prompt，複製貼上即可一鍵生成 PPT。")

# 優先從 Streamlit Secrets (環境變數) 讀取 API Key
api_key = st.secrets.get("GEMINI_API_KEY", None)

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    
    # 如果 Secrets 裡面沒有 Key，才顯示輸入框讓使用者手動輸入
    if not api_key:
        api_key = st.text_input("請輸入 Gemini API Key", type="password", help="可至 Google AI Studio 免費申請")
    else:
        st.success("🟢 系統 API Key 已連線 (免輸入 Key)")
    
    st.divider()
    st.markdown("### 🎯 目標 AI 工具")
    target_tool = st.selectbox(
        "你打算用邊款 AI 工具生成 PPT？",
        ["Gamma App (推薦，支援 Markdown)", "ChatGPT / Claude (生成 VBA 代碼)", "Microsoft Copilot"]
    )

# 主要輸入區
col1, col2 = st.columns(2)

with col1:
    topic = st.text_input("簡報主題 / 核心訊息", placeholder="例如：ISO 42001 AI 管理系統導入計畫")
    audience = st.text_input("目標聽眾", placeholder="例如：董事會成員、高階管理層、HR 團隊")
    
with col2:
    slides_count = st.slider("預計頁數", min_value=3, max_value=20, value=8)
    tone = st.selectbox("簡報風格", ["專業商務 (Boardroom / Executive)", "風險評估與合規報告", "培訓教學 (Educational)", "提案 Pitch (高說服力)"])

additional_info = st.text_area("補充資料或重點內容 (選填)", placeholder="例如：需涵蓋 AI 治理框架、風險管理標準，並提供企業落地案例...")

# 生成按鈕
if st.button("🚀 開始生成大綱與專屬 Prompt", type="primary"):
    if not api_key:
        st.error("系統尚未設定 API Key，請在左側邊欄輸入 API Key 後再試！")
    elif not topic:
        st.warning("請填寫簡報主題！")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner("AI 正在規劃簡報大綱與 Prompt..."):
                
                tool_specific_instruction = ""
                if "Gamma" in target_tool:
                    tool_specific_instruction = "請輸出適合直接貼入 Gamma.app 的 Markdown 格式 Prompt，強調每一頁的標題、圖片建議 (Image Prompt) 以及卡片式排版要求。"
                elif "VBA" in target_tool:
                    tool_specific_instruction = "請輸出一個完整的 ChatGPT Prompt，要求 ChatGPT 根據大綱直接寫出可以放入 PowerPoint 執行的 VBA 程式碼，並自動套用基本排版。"
                else:
                    tool_specific_instruction = "請輸出一個結構清晰的 Prompt，適合放入 Copilot 中，要求它根據大綱逐頁生成 PowerPoint 投影片，並配合企業模板風格。"

                prompt = f"""
                你是一位資深的簡報架構師與 Prompt 專家。請根據以下需求，輸出兩個部分：
                
                【需求資訊】
                - 主題：{topic}
                - 目標聽眾：{audience}
                - 頁數：{slides_count} 頁
                - 風格：{tone}
                - 補充背景：{additional_info}
                - 使用者預計使用的 AI 工具：{target_tool}

                請輸出以下內容：
                
                ### 第一部分：簡報結構大綱 (Slide-by-Slide Outline)
                逐頁列出每頁的：
                1. 頁頭主題 (Slide Title)
                2. 核心觀點 (Key Takeaway - 1句話)
                3. 內容要點 (3-4 個 Bullet points)

                ---

                ### 第二部分：專屬 AI 提示詞 (Tailored Prompt for {target_tool})
                {tool_specific_instruction}
                Prompt 內需包含：角色設定、排版邏輯、視覺風格指導、內容層次結構等。請將這段 Prompt 放在 Markdown 的 Code Block 中，方便使用者一鍵複製。
                """
                
                response = model.generate_content(prompt)
                
                st.success("🎉 搞定！大綱同 Prompt 已經為你準備好。")
                st.markdown("---")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"生成失敗，錯誤訊息：{e}")
