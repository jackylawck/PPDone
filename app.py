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

# 側邊欄：系統設定與 API 雙軌模式
with st.sidebar:
    st.header("⚙️ 系統設定")
    
    # 選擇 AI 金鑰模式
    api_mode = st.radio(
        "選擇 AI 金鑰模式：",
        ["🔴 使用系統公共免費額度", "⚪ 使用自備 AI API Key (無限制)"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("選擇 AI 金鑰模式：")
    api_mode = st.radio(
        "",
        ["🔴 使用公共免費額度 (單次 1 份大綱)", "⚪ 使用自備 AI API Key (無限制 & 高隱私)"],
        index=0,
        label_visibility="collapsed"
    )

    api_key = None

    if "公共免費" in api_mode:
        api_key = st.secrets.get("GEMINI_API_KEY", None)
        
        # 復刻截圖中的提示區塊
        st.success("🌱 **公共資源已載入 (免費體驗)。**")
        st.warning("⚠️ **資安提示**：此模式僅供系統功能演示與一般簡報生成。處理包含高度機密、董事會級別或企業內部敏感數據時，強烈建議切換為「自備 Key」以落實零數據留存與風險管理。")
        st.markdown("*(Engine: Gemini 1.5 Flash)*")
        
    else:
        api_key = st.text_input("🔑 請輸入你的 Gemini API Key", type="password")
        st.info("💡 **隱私保證**：自備 Key 僅會於當前瀏覽器 Session 運行，系統不會作任何儲存或紀錄，確保資料 100% 留存在你的掌控中。")
        st.markdown("*(Engine: Gemini 1.5 Flash)*")

    st.divider()

    st.markdown("### 🎯 目標 AI 工具")
    target_tool = st.selectbox(
        "你打算用邊款 AI 工具生成 PPT？",
        [
            "Gamma App (推薦，支援 Markdown / 卡片生成)", 
            "ChatGPT / Claude (生成 VBA 代碼 -> 匯入 PPT)", 
            "ChatGPT / Claude (生成 Marp / Markdown 簡報)",
            "Microsoft Copilot (PowerPoint 原生 AI)",
            "Tome / Mindshow (AI 故事與簡報平台)",
            "Canva AI / SlidesAI (設計類 AI 工具)"
        ]
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
        st.error("❌ 系統未能讀取 API Key。如果你選擇了「自備 Key」，請確保已在左側輸入。")
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
            
            with st.spinner("AI 正在融合專業排版與各平台特色，為你打磨大綱與 Prompt..."):
                
                tool_specific_instruction = ""
                if "Gamma" in target_tool:
                    tool_specific_instruction = """請輸出適合直接貼入 Gamma.app 的 Markdown 格式 Prompt。
                    【Gamma 排版指令】：
                    1. 採用 Card-by-Card 邏輯設計，強調標題與大圖對比。
                    2. 標題加上 40% 透明度色塊襯底。
                    3. 為每頁提供精準的 Image Prompt（英文）供 Gamma 圖像生成使用。"""
                elif "VBA" in target_tool:
                    tool_specific_instruction = """請輸出一個完整的 ChatGPT/Claude Prompt，要求 AI 根據大綱寫出可複製到 PowerPoint 執行的 VBA 程式碼。
                    【VBA 要求】：
                    1. 所有文字設定 Arial 或 Calibri，字體 >= 18pt。
                    2. 設定高對比度底色，標題自動放大置中。"""
                elif "Marp" in target_tool:
                    tool_specific_instruction = "請輸出適合直接複製到 Marp / Markdown 簡報工具的語法，包含 `---` 分頁符號與投影片樣式標籤。"
                elif "Copilot" in target_tool:
                    tool_specific_instruction = "請輸出適合 Microsoft Copilot 的 Prompt，要求其配合企業範本、採用高對比度、1:1 圖文排版及 18pt 以上字體生成。"
                elif "Tome" in target_tool or "Mindshow" in target_tool:
                    tool_specific_instruction = "請輸出適合 Tome / Mindshow 平台的視覺敘事型 Prompt，注重每一頁的故事動線與核心視覺提示。"
                else: 
                    tool_specific_instruction = "請輸出適合 Canva AI / SlidesAI 的條列式大綱與視覺風格提示，強調高對比配色與簡潔版面設計。"

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
                
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"生成失敗，錯誤訊息：{e}")
