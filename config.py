import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter API 設定
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# 模型設定
WHITE_MODEL = "meta-llama/llama-4-maverick"  # 白棋使用的模型
BLACK_MODEL = "meta-llama/llama-3.3-70b-instruct" # 黑棋使用的模型

# 遊戲設定
MAX_MOVES = 200  # 最大回合數
THINKING_TIMEOUT = 30  # 思考超時時間（秒）

# 日誌設定
LOG_THINKING_PROCESS = True
GAME_LOG_FILE = "game_log.txt"
