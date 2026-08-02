import streamlit as st
import json
import os

# 1. 頁面基礎設定
st.set_page_config(
    page_title="P.P.Done 簡報內容生成工具",
    page_icon="📄",
    layout="wide"
)

# 2. 簡潔標頭 (Header) - 無誇飾行銷字眼
st.title("📄 P.P.Done 簡報與專案結構簡報生成器")
st.caption("由 Jacky Law 開發 | 涵蓋 23 個管理領域與 53 個實戰模組，提供結構化的簡報大綱與演講備忘錄。")

# 3. 可摺疊的總覽區塊 (預設收起，保持頁面乾淨)
with st.expander("🔍 檢視知識庫概況與模組清單 (點擊展開/收起)", expanded=False):
    st.markdown("""
    ### 系統架構簡介
    本系統整理了 23 個企業管理與專案執行領域，共 53 份結構化簡報範本。包含以下主要範疇：
    * **經營與戰略**：公司治理、企業重整、跨國合資、法說會溝通
    * **營運與管理**：向上管理、壞消息通報、跨部門協調、專案啟動
    * **合規與科技**：AI 治理與風險管理、數據隱私、資安防護、監管回應
    * **分析與思維**：系統思考、賽局應用、行為經濟學、組織權力分析
    """)
    st.info("💡 提示：本工具旨在提供清晰、符合邏輯的簡報結構與 Speaker Notes，適合職場簡報與教案撰寫。")

st.markdown("---")

# 4. 主要操作區 (選擇模組與內容呈現)
st.subheader("🛠️ 選擇簡報主題與生成內容")

# 這裡假設你的 JSON 檔案存在 knowledge_base 資料夾下
KB_DIR = "knowledge_base"

# 模擬模組選擇 (可根據實際資料夾目錄動態讀取)
# 這裡僅列出操作示範結構
col1, col2 = st.columns([1, 2])

with col1:
    selected_domain = st.selectbox(
        "選擇管理領域",
        [
            "Executive_Communication_and_Upward_Management (向上管理與溝通)",
            "AI_Governance_and_Ethics (AI 治理與科技倫理)",
            "Strategy_and_Execution (戰略規劃與執行)",
            "Finance_and_Control (財務與內控)",
            "Mergers_and_Acquisitions (併購與重組)"
        ]
    )
    
    # 範例模組清單 (實際運作時可從資料夾讀取對應 JSON)
    selected_module = st.selectbox(
        "選擇簡報模組",
        [
            "upward_management_resource_pitch (戰略資源爭取)",
            "upward_management_bad_news_delivery (壞消息通報與修復)",
            "matrix_leadership_cross_functional_alignment (跨部門對齊)",
            "aigp_scenario_wargame (AI 專案治理沙盤推演)"
        ]
    )
    
    generate_btn = st.button("生成簡報結構與講稿", type="primary")

with col2:
    if generate_btn:
        st.success("✅ 內容已生成 (範例預覽)")
        
        # 示範平實簡潔的 Slide 顯示格式
        st.markdown("### 📋 簡報結構範例")
        
        tab1, tab2 = st.tabs(["Slide 1: 背景與主要訴求", "Slide 2: 商業論證與效益"])
        
        with tab1:
            st.markdown("#### **Slide 1: 現況說明與主要訴求**")
            st.markdown("""
            **重點標題 (Bullet Points)：**
            * **現狀描述**：本部門目前負責的專案進度符合預期，但現有流程耗費人力，影響 Q4 的交付效率。
            * **面臨瓶頸**：若不進行流程優化，預計於下季度將產生作業延宕與維護成本上升的風險。
            * **主要訴求**：提議導入自動化流程工具，預計申請專案預算與跨部門支援，以解決營運瓶頸。
            """)
            st.warning("""
            🗣️ **演講備忘錄 (Speaker Notes)：**  
            主管好，今天主要想跟各位報告我們部門目前面臨的流程瓶頸。雖然目前進度正常，但如果沒有適當改善，下季度的維護成本會顯著增加。今天的提案是希望能獲得資源進行自動化改善，確保專案能如期高質量的交付。
            """)
            
        with tab2:
            st.markdown("#### **Slide 2: 商業論證與預算回收**")
            st.markdown("""
            **重點標題 (Bullet Points)：**
            * **效益評估**：透過改善流程，預計每年可節省約 15% 的營運時間與人力耗損。
            * **回收週期**：本次專案投入的預算，預估於 12 個月內完成回收。
            * **風險管理**：專案採分階段導入，若第一階段未達指標將即時調整，不影響日常業務運作。
            """)
            st.warning("""
            🗣️ **演講備忘錄 (Speaker Notes)：**  
            這筆預算能為我們帶來實質的效率提升。經精算，回收期約為一年。為了降低風險，我們規劃了階段性驗收，確保不會對現有的日常營運造成干擾。
            """)

# 5. Sidebar 底部資訊 (中英文精簡優雅風)
st.sidebar.markdown("### 關於本工具")
st.sidebar.caption("P.P.Done 提供專案提案、經營報告與管理簡報的結構化範本。")
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-size: 0.85rem; color: #64748B; line-height: 1.6;">
    💡 如有系統使用問題或交流，歡迎聯絡作者。<br>
    <i>For system support or inquiries, feel free to contact the author:</i><br>
    👉 <a href="https://jackylawck.github.io/jackylawck/" target="_blank" style="color: #2563EB; font-weight: 600; text-decoration: underline;">Jacky Law</a>
</div>
""", unsafe_allow_html=True)
