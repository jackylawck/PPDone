import streamlit as st
import json
import os

# 1. 頁面基礎設定
st.set_page_config(
    page_title="P.P.Done 簡報與專案內容生成器",
    page_icon="📄",
    layout="wide"
)

# 2. 側邊欄：語言切換與聯絡資訊
with st.sidebar:
    lang = st.radio("Language / 語言", ["繁體中文", "English"], index=0)
    st.markdown("---")
    
    # 方案 B：精簡優雅風 (中英文對照)
    st.markdown("""
    <div style="font-size: 0.85rem; color: #64748B; line-height: 1.6;">
        💡 如有系統使用問題或交流，歡迎聯絡作者。<br>
        <i>For system support or inquiries, feel free to contact the author:</i><br>
        👉 <a href="https://jackylawck.github.io/jackylawck/" target="_blank" style="color: #2563EB; font-weight: 600; text-decoration: underline;">Jacky Law</a>
    </div>
    """, unsafe_allow_html=True)

# 3. 根據語言設定雙語字典
if lang == "繁體中文":
    TEXTS = {
        "title": "📄 P.P.Done 簡報與專案內容生成器",
        "subtitle": "由 Jacky Law 開發。輸入主題即可自動生成結構化簡報大綱與演講備忘錄。",
        "expander_overview": "🔍 檢視知識庫概況 (點擊展開/收起)",
        "overview_content": """
        ### 知識庫涵蓋範疇
        本系統整理了 23 個管理與專案執行領域，共 53 份結構化簡報範本：
        * **經營與戰略**：公司治理、企業重整、合資企業、法說會溝通
        * **營運與管理**：向上管理、壞消息通報、跨部門協調、專案啟動
        * **合規與科技**：AI 治理與風險管理、數據隱私、資安防護、監管回應
        * **分析與思維**：系統思考、賽局應用、行為經濟學、組織權力分析
        """,
        "input_label": "請輸入簡報主題或想解決的問題（簡易選擇）：",
        "input_placeholder": "例如：向 CFO 爭取自動化系統預算、通報專案延宕與修復計畫、AI 專案風險評估...",
        "expander_advanced": "⚙️ 精細選擇：手動指定領域與模組 (有需要才展開)",
        "domain_label": "選擇管理領域：",
        "module_label": "選擇簡報模組：",
        "btn_generate": "生成簡報結構與講稿",
        "success_msg": "✅ 已成功生成簡報大綱與演講備忘錄",
        "tab_slide1": "Slide 1: 現況說明與主要訴求",
        "tab_slide2": "Slide 2: 效益評估與風險管理",
        "slide1_title": "Slide 1: 現況說明與主要訴求",
        "slide1_bullets": """
        **重點標題 (Bullet Points)：**
        * **現狀描述**：本部門目前負責的專案進度符合預期，但現有流程耗費人力，影響下季度的交付效率。
        * **面臨瓶頸**：若不進行流程優化，預計將產生作業延宕與維護成本上升的風險。
        * **主要訴求**：提議導入自動化流程工具，預計申請專案預算與跨部門支援，以解決營運瓶頸。
        """,
        "slide1_notes": """
        🗣️ **演講備忘錄 (Speaker Notes)：**  
        主管好，今天主要想跟各位報告我們部門目前面臨的流程瓶頸。雖然目前進度正常，但如果沒有適當改善，下季度的維護成本會顯著增加。今天的提案是希望能獲得資源進行自動化改善，確保專案能如期高質量的交付。
        """,
        "slide2_title": "Slide 2: 效益評估與風險管理",
        "slide2_bullets": """
        **重點標題 (Bullet Points)：**
        * **效益評估**：透過改善流程，預計每年可節省約 15% 的營運時間與人力耗損。
        * **回收週期**：本次專案投入的預算，預估於 12 個月內完成回收。
        * **風險管理**：專案採分階段導入，若第一階段未達指標將即時調整，不影響日常業務運作。
        """,
        "slide2_notes": """
        🗣️ **演講備忘錄 (Speaker Notes)：**  
        這筆預算能為我們帶來實質的效率提升。經精算，回收期約為一年。為了降低風險，我們規劃了階段性驗收，確保不會對現有的日常營運造成干擾。
        """
    }
else:
    TEXTS = {
        "title": "📄 P.P.Done Presentation & Project Content Generator",
        "subtitle": "Developed by Jacky Law. Enter a topic to generate structured slide outlines and speaker notes.",
        "expander_overview": "🔍 View Knowledge Base Overview (Click to expand/collapse)",
        "overview_content": """
        ### Knowledge Base Scope
        This system aggregates 23 management domains and 53 structured presentation templates:
        * **Governance & Strategy**: Corporate Governance, Restructuring, Joint Ventures, Earnings Calls
        * **Operations & Leadership**: Managing Up, Delivering Bad News, Cross-Functional Alignment, Project Kickoffs
        * **Compliance & Tech**: AI Governance & Risk Management, Data Privacy, Cybersecurity, Regulatory Response
        * **Analytics & Thinking**: Systems Thinking, Game Theory, Behavioral Economics, Power Dynamics
        """,
        "input_label": "Enter your presentation topic or goal (Quick Selection):",
        "input_placeholder": "e.g., Pitching an automation budget to CFO, Reporting project delay & recovery, AI risk assessment...",
        "expander_advanced": "⚙️ Fine-Grained Selection: Specify Domain & Module (Optional)",
        "domain_label": "Select Management Domain:",
        "module_label": "Select Presentation Module:",
        "btn_generate": "Generate Outline & Speaker Notes",
        "success_msg": "✅ Presentation outline and speaker notes successfully generated",
        "tab_slide1": "Slide 1: Context & Core Proposal",
        "tab_slide2": "Slide 2: Business Case & Risk Management",
        "slide1_title": "Slide 1: Current Context & Core Proposal",
        "slide1_bullets": """
        **Bullet Points:**
        * **Current Context**: Our department's current deliverables meet expectations, but legacy workflows consume excessive bandwidth, threatening Q4 efficiency.
        * **Operational Bottleneck**: Without process optimization, we project operational delays and rising maintenance overhead next quarter.
        * **Core Proposal**: Recommending the deployment of automated workflow tools, requesting project budget and cross-functional bandwidth to resolve the bottleneck.
        """,
        "slide1_notes": """
        🗣️ **Speaker Notes:**  
        Good morning. Today I want to address an operational bottleneck in our current workflow. While current milestones are on track, maintaining this legacy process will significantly inflate maintenance costs next quarter. This proposal seeks budget approval for workflow automation to ensure long-term delivery quality.
        """,
        "slide2_title": "Slide 2: Business Case & Risk Management",
        "slide2_bullets": """
        **Bullet Points:**
        * **Value Capture**: Process optimization is projected to reduce operational cycle time and manual effort by 15% annually.
        * **Payback Period**: Capital expenditure for this initiative is estimated to achieve full payback within 12 months.
        * **Risk Mitigation**: Deployment will follow a phased approach; failure to hit Phase 1 milestones will trigger a stop-loss without disrupting daily business operations.
        """,
        "slide2_notes": """
        🗣️ **Speaker Notes:**  
        This budget request drives tangible efficiency gains. Based on our calculations, the payback period is 12 months. To mitigate downside risk, we have built in milestone validation gates to guarantee zero disruption to core daily business operations.
        """
    }

# 4. 主頁面內容
st.title(TEXTS["title"])
st.caption(TEXTS["subtitle"])

# 5. 可摺疊的知識庫概況 (預設收起)
with st.expander(TEXTS["expander_overview"], expanded=False):
    st.markdown(TEXTS["overview_content"])

st.markdown("---")

# 6. 簡易選擇 (最主要的操作區域)
user_topic = st.text_input(
    TEXTS["input_label"],
    placeholder=TEXTS["input_placeholder"]
)

# 7. 精細選擇 (預設收起，有需要才選)
with st.expander(TEXTS["expander_advanced"], expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        domain = st.selectbox(
            TEXTS["domain_label"],
            [
                "Executive_Communication_and_Upward_Management",
                "AI_Governance_and_Ethics",
                "Strategy_and_Execution",
                "Finance_and_Control",
                "Mergers_and_Acquisitions"
            ]
        )
    with col2:
        module = st.selectbox(
            TEXTS["module_label"],
            [
                "upward_management_resource_pitch",
                "upward_management_bad_news_delivery",
                "matrix_leadership_cross_functional_alignment",
                "aigp_scenario_wargame"
            ]
        )

# 8. 生成按鈕
if st.button(TEXTS["btn_generate"], type="primary"):
    st.success(TEXTS["success_msg"])
    
    # 頁籤輸出
    tab1, tab2 = st.tabs([TEXTS["tab_slide1"], TEXTS["tab_slide2"]])
    
    with tab1:
        st.markdown(f"#### **{TEXTS['slide1_title']}**")
        st.markdown(TEXTS["slide1_bullets"])
        st.info(TEXTS["slide1_notes"])
        
    with tab2:
        st.markdown(f"#### **{TEXTS['slide2_title']}**")
        st.markdown(TEXTS["slide2_bullets"])
        st.info(TEXTS["slide2_notes"])
