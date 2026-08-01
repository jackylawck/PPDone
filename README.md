# 📊 稿定 P.P.Done | AI Presentation Outline & Prompt Generator

> **「稿定大綱同 Prompt，PPT 輕鬆 Done！」**
> 
> *Nail the Outline & Prompt, Get your PPT Done with Zero Token Waste!*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ppdone.streamlit.app/)
![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)

---

## 💡 專案理念 (Concept)

市面上的 AI PPT 工具（如 Gamma、Copilot 等）往往需要消耗大量 Token 或付費點數，且直接產出的內容容易流於套話。**稿定 P.P.Done** 採取「知識庫優先 + AI 備援」雙軌策略：

1. **⚡ 專家知識庫快取 (Zero Token Cost)**：內建 ISO 治理、高階 HR 談判、管理學與月報等管顧級範本，精準命中時 **0.1 秒秒出，完全零 Token 消耗**。
2. **🎯 專屬 Prompt 一鍵複製**：針對你的目標 AI 工具（Gamma, ChatGPT VBA, Copilot, Marp 等），自動生成結構化提示詞與特化格式指令，貼上即可生成高品質簡報。
3. **🚀 智能極簡 UX**：支援「無腦生成模式」，只需輸入主題即可由 AI 自動推斷聽眾與商業框架。

---

## ✨ 核心特色 (Key Features)

- 💼 **管顧級與 ISO 治理邏輯 (Consultant & ISO Frameworks)**：
  - 內建 PDCA 循環、ISO 42001 AI 治理、ISO 31000 風險評估、董事會 Executive Summary、職場調解溝通及管理原理（MGT B240C）等多種專業框架。
- 🎯 **跨平台 AI 工具 Prompt 特化 (Tailored AI Prompts)**：
  - 支援 **Gamma App** (Card-by-Card 邏輯與 Markdown 分隔)
  - 支援 **ChatGPT / Claude** (可直接執行的 PowerPoint VBA Code / Marp Markdown)
  - 支援 **Microsoft Copilot**、**Tome**、**Canva AI** 等平台。
- ⚡ **極簡輸入與智能自動補全 (Minimalist UX)**：
  - 懶人模式：僅需填寫主題即可一鍵生成；專家模式：預設折疊進階設定（聽眾、節奏、風格框架），滿足細粒度控制。
- 🗣️ **預備講稿備註 (Speaker Notes)**：
  - 遵循「Don't Read Slides」原則，每頁提供 2-3 句講者口述備註。
- 🔒 **雙軌金鑰與資安防護 (Dual API Key & Privacy)**：
  - 提供公共免費體驗額度，同時支援使用者自備 OpenRouter Key（Session 級別留存，不儲存任何企業機密數據）。
- 🌐 **全中英雙語 UI (Full Bilingual UI)**：
  - 一鍵切換繁體中文或 Full English 介面與輸出內容。

---

## 🛠️ 開發套件與架構 (Tech Stack)

- **UI Framework**: [Streamlit](https://streamlit.io/)
- **Architecture**: Knowledge Base JSON Cache + OpenRouter AI Fallback Engine
- **Deployment**: Streamlit Community Cloud

---

## 📄 授權條款 (License)

本專案採用 [Apache License 2.0](LICENSE) 授權釋出 - 保留專利授權與品牌商標保護，歡迎自由使用、修改與二次開發。
