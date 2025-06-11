# Chess-LLM 快速開始指南

## 🚀 快速體驗

### 1. 立即試用示範模式（無需 API 金鑰）
```bash
python3 demo.py
```
這將展示系統如何運作，使用模擬的 AI 回應。

### 2. 測試系統功能
```bash
python3 test_system.py
```
檢查所有組件是否正常工作。

## 📋 完整設定步驟

### 1. 安裝依賴
```bash
pip3 install -r requirements.txt
```

### 2. 設定 API 金鑰
編輯 `.env` 檔案：
```
OPENROUTER_API_KEY=你的_openrouter_api_金鑰
```

### 3. 執行真實對弈
```bash
python3 main.py
```

## 🎯 系統架構說明

```
Chess-LLM/
├── chess_core.py      # 西洋棋核心邏輯
├── llm_inference.py   # LLM 推理引擎
├── main.py           # 主程式 (真實 LLM 對弈)
├── demo.py           # 示範程式 (模擬對弈)
├── config.py         # 配置設定
├── test_system.py    # 系統測試
└── requirements.txt  # 依賴套件
```

## 🔧 自訂設定

在 `config.py` 中修改：
- `WHITE_MODEL`: 白棋使用的模型
- `BLACK_MODEL`: 黑棋使用的模型
- `MAX_MOVES`: 最大回合數
- `THINKING_TIMEOUT`: 思考超時時間

## 📊 遊戲記錄

每場遊戲會產生：
- `game_YYYYMMDD_HHMMSS.pgn` - 標準棋譜格式
- `thinking_logs_YYYYMMDD_HHMMSS.json` - 完整思考記錄
- `game_log.txt` - 即時遊戲日誌

## 🤝 支援的模型

透過 OpenRouter 支援：
- Anthropic Claude 系列
- OpenAI GPT 系列  
- Google Gemini 系列
- Meta Llama 系列
- 更多模型...
