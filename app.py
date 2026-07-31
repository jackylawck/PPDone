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
st.caption("內建管顧級大綱原則與專業排版美學！先為你打磨精準簡報架構，產生專屬 Prompt，複製貼上即可一鍵生成高品質 PPT。")

# 優先從 Streamlit Secrets 讀取 API Key
api_key = st.secrets.get("GEMINI_API_KEY", None)

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    
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
    purpose = st.selectbox("簡報目的", ["傳達資訊 (資訊同步/進度報告)", "說服他人 (提案 Pitch/爭取資源)", "引導討論 (工作坊/腦力激盪)"])
    
with col2:
    time_minutes = st.number_input("預計演講時間 (分鐘)", min_value=1, max_value=120, value=10)
    pace = st.selectbox("簡報節奏 (自動推算頁數)", [
        "中節奏：1頁/分鐘 (適合平衡視覺與內容吸收)", 
        "慢節奏：<1頁/分鐘 (適合詳細解說與深度探討)", 
        "快節奏：2-3頁/分鐘 (適合高度視覺化、快速抓住目光)"
    ])
    tone = st.selectbox("簡報風格", ["專業商務 (Boardroom / Executive)", "風險評估與合規報告", "培訓教學 (Educational)", "提案 Pitch (高說服力)"])

additional_info = st.text_area("補充資料或重點內容 (選填)", placeholder="例如：需涵蓋 AI 治理框架、風險管理標準，並提供企業落地案例...")

# 生成按鈕
if st.button("🚀 開始生成大綱與專屬 Prompt", type="primary"):
    if not api_key:
        st.error("系統尚未設定 API Key，請在左側邊欄輸入 API Key 後再試！")
    elif not topic:
        st.warning("請填寫簡報主題！")
    elif not audience:
        st.warning("請填寫目標聽眾！(以人為本的簡報需要明確聽眾)")
    else:
        if "中節奏" in pace:
            slides_count = time_minutes
        elif "慢節奏" in pace:
            slides_count = max(3, int(time_minutes * 0.4))  
        else:
            slides_count = time_minutes * 2  

        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner("AI 正在融合專業排版法則，為你打磨大綱與 Prompt..."):
                
                # 針對不同工具融入視覺與排版法則 (加入 18pt, High Contrast, Arial/Calibri 規則)
                tool_specific_instruction = ""
                if "Gamma" in target_tool:
                    tool_specific_instruction = """請輸出適合直接貼入 Gamma.app 的 Markdown 格式 Prompt。
                    【視覺與排版要求】：
                    1. 視覺衝擊：使用滿版的高解析度圖片，但確保圖形不會過多而干擾視覺。
                    2. 高對比度 (High Contrast)：標題文字必須加上 40% 透明度的色塊襯底，確保文字在背景上清晰可見。
                    3. 字體要求：整體設計風格請選用現代簡潔的無襯線字體。"""
                elif "VBA" in target_tool:
                    tool_specific_instruction = """請輸出一個完整的 ChatGPT Prompt，要求 ChatGPT 根據大綱直接寫出可以放入 PowerPoint 執行的 VBA 程式碼。
                    【VBA 排版嚴格要求】：
                    1. 字體與大小：所有文字強制設定為 Arial 或 Calibri，且所有字體大小必須大於或等於 18 pt (>=18pt)。
                    2. 高對比配色：強制設定淺色背景搭配深色文字，或深色背景搭配淺色文字。
                    3. 排版：大標題置中，內文 Bullet points 不要啟動自動換行 (Text wrapping)。"""
                else:
                    tool_specific_instruction = """請輸出一個結構清晰的 Prompt，適合放入 Copilot 中。
                    【排版指令要求】：
                    1. 要求 Copilot 採用高對比度 (High Contrast) 的企業模板。
                    2. 指定使用易讀的簡潔字體（如 Arial 或 Calibri），確保最小字體不低於 18 pt。
                    3. 版面盡量採用 1:1 圖文搭配，並保持背景乾淨不干擾訊息。"""

                prompt = f"""
                你是一位資深的簡報架構師。請根據以下需求，輸出兩個部分：
                
                【需求資訊】
                - 主題：{topic}
                - 目標聽眾：{audience}
                - 簡報目的：{purpose}
                - 演講時間：{time_minutes} 分鐘 (建議頁數約 {slides_count} 頁)
                - 風格：{tone}
                - 補充背景：{additional_info}
                - 目標 AI 工具：{target_tool}

                【大綱撰寫規則（嚴格遵守大師級法則）】
                1. 聽眾本位：提供「{audience}」需要聽到的關鍵資訊，而不是塞滿所有細節。
                2. 去贅字與極簡化：內容必須極度精簡，刪除不必要的冠詞或連接詞（如 a, the）。每個重點必須控制在【一行以內】，絕對不能換行 (No text wrapping)。
                3. 事不過三：每頁投影片【最多只能有 3 個主要重點】。
                4. 不要照稿讀 (Don't read the presentation)：投影片上的文字只是提示 (cue)，請在每一頁額外提供一段【演講備註 (Speaker Notes)】，寫出演講者實際該講的話。

                請輸出以下內容：
                
                ### 第一部分：簡報結構大綱 (Slide-by-Slide Outline)
                總共約 {slides_count} 頁，逐頁列出：
                1. 頁頭主題 (Slide Title - 嚴格限制短標題)
                2. 內容要點 (最多 3 個 Bullet points，符合極簡無贅字原則)
                3. 🗣️ 演講備註 (Speaker Notes - 提供講者在此頁應該口述的完整內容，約 2-3 句)

                ---

                ### 第二部分：專屬 AI 提示詞 (Tailored Prompt for {target_tool})
                {tool_specific_instruction}
                請將這段 Prompt 放在 Markdown 的 Code Block 中，方便使用者一鍵複製。
                """
                
                response = model.generate_content(prompt)
                
                st.success(f"🎉 搞定！已為你規劃約 {slides_count} 頁的大綱與專屬 Prompt。")
                st.markdown("---")
                
                # 顯示結果
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"生成失敗，錯誤訊息：{e}")
