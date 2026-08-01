# -------------------------
# 3. 頁面渲染 (導入極簡 UX 設計)
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
        # 加入 type="password" 保護隱私
        openrouter_key = st.text_input(ui["own_key_label"], type="password")
        st.info(ui["own_key_info"])

st.divider()

# 主輸入區：極簡模式 (只顯示最關鍵的兩個欄位)
topic = st.text_input("💡 " + ui["topic_label"] + " (必填)", placeholder=ui["topic_ph"])
additional_info = st.text_area("📝 " + ui["add_info_label"], placeholder=ui["add_info_ph"])

# 進階設定區：預設折疊，保持畫面清爽
with st.expander("⚙️ 進階設定 (Advanced Settings)", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        audience = st.text_input(ui["audience_label"], placeholder=ui["audience_ph"])
        purpose = st.selectbox(ui["purpose_label"], ui["purpose_opts"], index=0)
        tone = st.selectbox(ui["tone_label"], ["🤖 AI 自動推薦 (Auto)"] + ui["tone_opts"], index=0)
        
    with col2:
        target_tool = st.selectbox(ui["target_tool_title"], ui["tools"], index=0)
        time_minutes = st.number_input(ui["time_label"], min_value=1, max_value=120, value=10)
        pace = st.selectbox(ui["pace_label"], ui["pace_opts"], index=0)

# -------------------------
# 4. 邏輯處理與生成 (KB First -> AI Fallback)
# -------------------------
if st.button(ui["btn_generate"], type="primary"):
    if not topic:
        st.warning(ui["err_topic"]) # 現在只需檢查 Topic，聽眾改為自動補全
    else:
        # 自動補足未填的 Audience 與 Tone
        final_audience = audience if audience.strip() else "一般目標聽眾 (General Audience)"
        final_tone = tone if tone != "🤖 AI 自動推薦 (Auto)" else "根據主題自動選擇最適合的專業框架"

        with st.spinner(ui["sp_loading"]):
            # (後續維持原本的 KB 搜尋與 AI 生成邏輯，但請記得把 prompt 裡的 audience 換成 final_audience)
