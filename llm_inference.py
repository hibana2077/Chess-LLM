import openai
import json
import time
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
from prompt_lib import RESPONSE_FORMAT_THINK, RESPONSE_FORMAT_WITHOUT_THINK
import config


class LLMInferenceCore:
    """LLM 推理核心類別，處理與 OpenRouter API 的溝通"""
    
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=config.OPENROUTER_API_KEY,
            base_url=config.OPENROUTER_BASE_URL
        )
        self.thinking_logs: list = []
    
    def think_and_move(self, 
                      model_name: str,
                      board_state: str,
                      legal_moves: list,
                      move_history: list,
                      player_color: str,
                      personality: str,
                      position_analysis: dict) -> Tuple[str, str]:
        """
        讓 LLM 思考並決定下一步移動
        
        Args:
            model_name: 使用的模型名稱
            board_state: 當前棋盤狀態 (FEN)
            legal_moves: 合法移動列表
            move_history: 移動歷史
            player_color: 玩家顏色 ("White" 或 "Black")
            position_analysis: 位置分析資訊
            
        Returns:
            Tuple[str, str]: (選擇的移動, 思考過程)
        """
        
        # 建構提示詞
        prompt = self._build_chess_prompt(
            board_state, legal_moves, move_history, 
            player_color, position_analysis
        )
        
        thinking_start_time = datetime.now()
        
        try:
            # 呼叫 LLM API
            response = self.client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a {personality} professional chess master. respond in JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1000,
                timeout=config.THINKING_TIMEOUT
            )
            
            thinking_end_time = datetime.now()
            thinking_duration = (thinking_end_time - thinking_start_time).total_seconds()
            
            # 解析回應
            response_content = response.choices[0].message.content
            move, thinking_process = self._parse_llm_response(response_content)
            
            # 記錄思考過程
            thinking_log = {
                "timestamp": thinking_start_time.isoformat(),
                "model": model_name,
                "player": player_color,
                "thinking_duration": thinking_duration,
                "board_state": board_state,
                "legal_moves": legal_moves,
                "thinking_process": thinking_process,
                "chosen_move": move,
                "raw_response": response_content
            }
            
            self.thinking_logs.append(thinking_log)
            
            if config.LOG_THINKING_PROCESS:
                self._log_thinking_process(thinking_log)
            
            return move, thinking_process
            
        except Exception as e:
            error_msg = f"LLM 推理錯誤: {str(e)}"
            print(f"錯誤: {error_msg}")
            
            # 錯誤時隨機選擇一個合法移動
            import random
            fallback_move = random.choice(legal_moves) if legal_moves else None
            
            return fallback_move, f"錯誤回退: {error_msg}"
    
    def _build_chess_prompt(self, 
                           board_state: str,
                           legal_moves: list,
                           move_history: list,
                           player_color: str,
                           position_analysis: dict) -> str:
        """建構西洋棋分析提示詞"""
        response_format = RESPONSE_FORMAT_THINK if config.RESPONSE_WITH_THINKING else RESPONSE_FORMAT_WITHOUT_THINK
        prompt = f"""
Please analyze the following chess position and choose the best move:

**Game Information:**
- You are playing as {player_color}
- Current position: {board_state}
- Move count: {position_analysis.get('move_count', 0)}
- Game status: {position_analysis.get('status', 'Active')}
- In check: {position_analysis.get('is_check', False)}
- Material balance: {position_analysis.get('material_balance', 0)} (positive means White is ahead)

**Available legal moves:**
{', '.join(legal_moves)}

{response_format}
```

Please ensure that the chosen move is within the legal moves list.
"""
        return prompt
    
    def _parse_llm_response(self, response_content: str) -> Tuple[str, str]:
        """解析 LLM 回應並提取移動和思考過程"""
        try:
            # 尋找 JSON 部分
            start_idx = response_content.find('{')
            end_idx = response_content.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_content[start_idx:end_idx]
                response_data = json.loads(json_str)
                
                move = response_data.get("chosen_move", "")
                
                # 組合思考過程
                thinking_parts = []
                if "analysis" in response_data:
                    thinking_parts.append(f"局面分析: {response_data['analysis']}")
                
                if "candidate_moves" in response_data:
                    thinking_parts.append("候選移動:")
                    for candidate in response_data["candidate_moves"]:
                        thinking_parts.append(f"  - {candidate.get('move', '')}: {candidate.get('evaluation', '')}")
                
                if "reasoning" in response_data:
                    thinking_parts.append(f"最終選擇理由: {response_data['reasoning']}")
                
                thinking_process = "\n".join(thinking_parts)
                
                return move, thinking_process
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"解析 LLM 回應時發生錯誤: {e}")
        
        # 解析失敗時的回退處理
        return "", f"解析失敗，原始回應: {response_content[:500]}..."
    
    def _log_thinking_process(self, thinking_log: dict):
        """記錄思考過程到檔案"""
        try:
            with open(config.GAME_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"\n{'='*50}\n")
                f.write(f"時間: {thinking_log['timestamp']}\n")
                f.write(f"模型: {thinking_log['model']}\n")
                f.write(f"玩家: {thinking_log['player']}\n")
                f.write(f"思考時間: {thinking_log['thinking_duration']:.2f} 秒\n")
                f.write(f"選擇移動: {thinking_log['chosen_move']}\n")
                f.write(f"\n思考過程:\n{thinking_log['thinking_process']}\n")
                f.write(f"{'='*50}\n")
        except Exception as e:
            print(f"記錄思考過程時發生錯誤: {e}")
    
    def get_thinking_logs(self) -> list:
        """獲取所有思考記錄"""
        return self.thinking_logs
    
    def save_thinking_logs(self, filename: str):
        """將思考記錄保存到 JSON 檔案"""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.thinking_logs, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存思考記錄時發生錯誤: {e}")
