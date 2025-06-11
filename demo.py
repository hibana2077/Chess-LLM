#!/usr/bin/env python3
"""
Chess-LLM 示範模式
不需要真實的 API 金鑰，使用模擬的 LLM 回應進行西洋棋對弈示範
"""

import time
import random
from datetime import datetime
from colorama import init, Fore, Style

from chess_core import ChessCore

# 初始化 colorama
init()


class DemoLLMCore:
    """示範用的 LLM 核心，模擬 LLM 回應"""
    
    def __init__(self):
        self.thinking_logs = []
        
        # 預設的開局移動
        self.white_opening_moves = ["e2e4", "d2d4", "g1f3", "c2c4"]
        self.black_opening_moves = ["e7e5", "d7d5", "g8f6", "c7c5"]
        
    def think_and_move(self, model_name, board_state, legal_moves, 
                      move_history, player_color, position_analysis):
        """模擬 LLM 思考和決定移動"""
        
        thinking_start = datetime.now()
        
        # 模擬思考時間
        time.sleep(random.uniform(1, 3))
        
        # 選擇移動策略
        if len(move_history) < 6:  # 開局階段
            move = self._choose_opening_move(legal_moves, player_color)
        else:  # 中局階段
            move = self._choose_strategic_move(legal_moves, position_analysis)
        
        thinking_end = datetime.now()
        thinking_duration = (thinking_end - thinking_start).total_seconds()
        
        # 生成模擬的思考過程
        thinking_process = self._generate_thinking_process(
            move, legal_moves, position_analysis, player_color
        )
        
        # 記錄思考過程
        thinking_log = {
            "timestamp": thinking_start.isoformat(),
            "model": model_name,
            "player": player_color,
            "thinking_duration": thinking_duration,
            "chosen_move": move,
            "thinking_process": thinking_process
        }
        
        self.thinking_logs.append(thinking_log)
        
        return move, thinking_process
    
    def _choose_opening_move(self, legal_moves, player_color):
        """選擇開局移動"""
        if player_color == "White":
            preferred = [move for move in self.white_opening_moves if move in legal_moves]
        else:
            preferred = [move for move in self.black_opening_moves if move in legal_moves]
        
        if preferred:
            return random.choice(preferred)
        else:
            return random.choice(legal_moves)
    
    def _choose_strategic_move(self, legal_moves, position_analysis):
        """選擇戰略性移動"""
        # 簡單的移動選擇邏輯
        # 優先考慮吃子、將軍等
        
        # 這裡可以添加更複雜的邏輯，但為了示範，我們隨機選擇
        return random.choice(legal_moves)
    
    def _generate_thinking_process(self, chosen_move, legal_moves, position_analysis, player_color):
        """生成模擬的思考過程"""
        
        thinking_templates = [
            f"局面分析: 當前是{player_color}的回合，棋盤上的局勢看起來{'有利' if random.choice([True, False]) else '需要謹慎'}。",
            f"候選移動考慮:\n  - {chosen_move}: 這個移動可以{'改善棋子位置' if random.choice([True, False]) else '控制關鍵格子'}",
            f"  - {random.choice(legal_moves)}: 另一個選擇，但{'風險較高' if random.choice([True, False]) else '效果不如第一選擇'}",
            f"最終選擇理由: 選擇 {chosen_move} 是因為它能夠{'鞏固陣地' if random.choice([True, False]) else '增加攻擊機會'}，符合當前的戰略目標。"
        ]
        
        # 根據局面添加特殊考量
        if position_analysis.get('is_check'):
            thinking_templates.insert(1, "⚠️ 目前被將軍，必須優先處理國王安全問題。")
        
        if position_analysis.get('material_balance', 0) > 0:
            thinking_templates.insert(1, "💰 材料優勢在手，應該考慮簡化局面。")
        elif position_analysis.get('material_balance', 0) < 0:
            thinking_templates.insert(1, "⚡ 材料劣勢，需要尋找戰術機會。")
        
        return "\n".join(thinking_templates)
    
    def get_thinking_logs(self):
        """獲取思考記錄"""
        return self.thinking_logs


class ChessLLMDemo:
    """西洋棋 LLM 對弈示範系統"""
    
    def __init__(self):
        self.chess = ChessCore()
        self.llm_core = DemoLLMCore()
        self.game_start_time = datetime.now()
        
        # 示範用的模型名稱
        self.white_model = "Demo-GPT-White"
        self.black_model = "Demo-Claude-Black"
    
    def print_header(self):
        """印出遊戲標題"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"           西洋棋 LLM 對弈示範系統")
        print(f"             (模擬模式 - 無需 API 金鑰)")
        print(f"{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}白棋模型: {self.white_model}")
        print(f"黑棋模型: {self.black_model}")
        print(f"遊戲開始時間: {self.game_start_time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        print()
    
    def print_board(self):
        """印出當前棋盤"""
        print(f"\n{Fore.GREEN}當前棋盤:{Style.RESET_ALL}")
        print(self.chess.get_board_ascii())
        
        analysis = self.chess.get_position_analysis()
        print(f"\n{Fore.BLUE}局面資訊:{Style.RESET_ALL}")
        print(f"  輪到: {analysis['turn']}")
        print(f"  移動次數: {analysis['move_count']}")
        print(f"  狀態: {analysis['status']}")
        print(f"  材料平衡: {analysis['material_balance']}")
        if analysis['is_check']:
            print(f"  {Fore.RED}將軍!{Style.RESET_ALL}")
        print()
    
    def play_turn(self, player_color, model_name):
        """執行一回合"""
        print(f"{Fore.MAGENTA}{'='*40}")
        print(f"  {player_color} 的回合 ({model_name})")
        print(f"{'='*40}{Style.RESET_ALL}")
        
        # 獲取當前遊戲狀態
        board_state = self.chess.get_current_position()
        legal_moves = self.chess.get_legal_moves()
        position_analysis = self.chess.get_position_analysis()
        
        print(f"{Fore.YELLOW}正在思考...{Style.RESET_ALL}")
        
        # 模擬 LLM 思考
        move, thinking_process = self.llm_core.think_and_move(
            model_name=model_name,
            board_state=board_state,
            legal_moves=legal_moves,
            move_history=self.chess.move_history,
            player_color=player_color,
            position_analysis=position_analysis
        )
        
        # 顯示思考過程
        if thinking_process:
            print(f"\n{Fore.CYAN}思考過程:{Style.RESET_ALL}")
            print(thinking_process)
            print()
        
        # 執行移動
        if move and self.chess.make_move(move):
            print(f"{Fore.GREEN}✓ {player_color} 移動: {move}{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}✗ 移動失敗: {move}{Style.RESET_ALL}")
            return False
    
    def run_demo(self, max_moves=20):
        """執行示範遊戲"""
        self.print_header()
        
        move_count = 0
        
        while not self.chess.is_game_over() and move_count < max_moves:
            self.print_board()
            
            current_player = self.chess.get_current_player()
            
            if current_player == "White":
                success = self.play_turn("White", self.white_model)
            else:
                success = self.play_turn("Black", self.black_model)
            
            if not success:
                print(f"{Fore.RED}移動失敗，示範結束{Style.RESET_ALL}")
                break
            
            move_count += 1
            
            # 暫停讓使用者觀看
            time.sleep(0.5)
        
        # 示範結束
        self.print_game_result()
    
    def print_game_result(self):
        """印出遊戲結果"""
        self.print_board()
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"                示範結束")
        print(f"{'='*60}{Style.RESET_ALL}")
        
        if self.chess.is_game_over():
            result = self.chess.get_game_result()
            status = self.chess.get_game_status()
            print(f"{Fore.YELLOW}結果: {result}")
            print(f"狀態: {status}")
        else:
            print(f"{Fore.YELLOW}示範已完成 (遊戲未結束)")
        
        print(f"總移動數: {self.chess.get_move_count()}")
        
        game_duration = datetime.now() - self.game_start_time
        print(f"示範時長: {game_duration}{Style.RESET_ALL}")
        
        # 顯示 PGN
        print(f"\n{Fore.GREEN}PGN 記錄:{Style.RESET_ALL}")
        print(self.chess.export_pgn())


def main():
    """主函數"""
    try:
        demo = ChessLLMDemo()
        demo.run_demo()
        
        print(f"\n{Fore.CYAN}示範完成！{Style.RESET_ALL}")
        print("要使用真實的 LLM 模型，請：")
        print("1. 在 .env 檔案中設定你的 OpenRouter API 金鑰")
        print("2. 執行 python3 main.py")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}示範被中斷{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}發生錯誤: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
