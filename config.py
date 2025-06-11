import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter API 設定
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# 模型設定
WHITE_MODEL = "anthropic/claude-3.5-haiku"  # white 
BLACK_MODEL = "mistralai/mixtral-8x22b-instruct" # black

# Personality 設定
WHITE_PERSONALITY = "Aggressive. Focus on attacking strategies and quick victories."
BLACK_PERSONALITY = "Defensive. Focus on counterattacks and solid positioning."

# 遊戲設定
MAX_MOVES = 200  # 最大回合數
THINKING_TIMEOUT = 30  # 思考超時時間（秒）

# 日誌設定
LOG_THINKING_PROCESS = True
GAME_LOG_FILE = "game_log.txt"
RESPONSE_WITH_THINKING = True  # 是否在回應中包含思考過程