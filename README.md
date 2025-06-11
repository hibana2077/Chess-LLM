# Chess-LLM

使用 OpenRouter API 讓兩個不同的 LLM 模型進行西洋棋對弈的專案。

## 功能特色

- 🤖 支援多種 LLM 模型進行對弈
- ♟️ 完整的西洋棋規則實作
- 🧠 記錄每步棋的思考過程
- 📝 自動生成 PGN 遊戲記錄
- 🎨 彩色終端介面
- 📊 局面分析和統計

## 系統架構

### Chess Core
- 處理棋盤狀態和移動驗證
- 遊戲規則實作
- PGN 匯出功能

### LLM Inference Core
- 與 OpenRouter API 溝通
- 結構化提示詞生成
- 思考過程記錄

### Main
遊戲流程：白棋先行 → 白棋思考 → 白棋移動 → 黑棋思考 → 黑棋移動

## 安裝步驟

1. 克隆專案：
```bash
git clone <repository-url>
cd Chess-LLM
```

2. 安裝依賴：
```bash
pip install -r requirements.txt
```

3. 設定 API 金鑰：
```bash
cp .env.example .env
# 編輯 .env 檔案，填入你的 OpenRouter API 金鑰
```

## 使用方法

```bash
python main.py
```

## 配置選項

在 `config.py` 中可以調整以下設定：

- `WHITE_MODEL`: 白棋使用的模型
- `BLACK_MODEL`: 黑棋使用的模型
- `MAX_MOVES`: 最大回合數
- `THINKING_TIMEOUT`: 思考超時時間

## 輸出檔案

每場遊戲會產生以下檔案：

- `game_YYYYMMDD_HHMMSS.pgn`: PGN 格式的遊戲記錄
- `thinking_logs_YYYYMMDD_HHMMSS.json`: 詳細的思考過程記錄
- `game_log.txt`: 即時遊戲日誌

## 支援的模型

透過 OpenRouter 可以使用的模型包括：
- `anthropic/claude-3.5-sonnet`
- `openai/gpt-4-turbo`
- `google/gemini-pro`
- 等等更多...

## 系統需求

- Python 3.8+
- OpenRouter API 金鑰
- 網路連線