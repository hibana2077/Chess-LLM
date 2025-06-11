#!/usr/bin/env python3
"""
Chess-LLM 主程式
使用兩個不同的 LLM 模型進行西洋棋對弈
"""

import time
import os
from datetime import datetime
from colorama import init, Fore, Style

from chess_core import ChessCore
from llm_inference import LLMInferenceCore
import config

# 初始化 colorama
init()


class ChessLLMGame:
    """西洋棋 LLM 對弈遊戲主類別"""
    
    def __init__(self):
        self.chess = ChessCore()
        self.llm_core = LLMInferenceCore()
        self.game_start_time = datetime.now()
        
        # 檢查 API 金鑰
        if not config.OPENROUTER_API_KEY:
            print(f"{Fore.RED}錯誤: 未設定 OPENROUTER_API_KEY 環境變數{Style.RESET_ALL}")
            print("請在 .env 檔案中設定你的 OpenRouter API 金鑰")
            exit(1)
    
    def print_header(self):
        """印出遊戲標題"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"           西洋棋 LLM 對弈系統")
        print(f"{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}白棋模型: {config.WHITE_MODEL}")
        print(f"黑棋模型: {config.BLACK_MODEL}")
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
    
    def play_turn(self, player_color: str, model_name: str, personality: str) -> bool:
        """
        執行一回合
        
        Args:
            player_color: 玩家顏色 ("White" 或 "Black")
            model_name: 使用的模型名稱
            personality: 玩家個性

        Returns:
            bool: 是否成功執行移動
        """
        print(f"{Fore.MAGENTA}{'='*40}")
        print(f"  {player_color} 的回合 ({model_name})")
        print(f"{'='*40}{Style.RESET_ALL}")
        
        # 獲取當前遊戲狀態
        board_state = self.chess.get_current_position()
        legal_moves = self.chess.get_legal_moves()
        position_analysis = self.chess.get_position_analysis()
        
        print(f"{Fore.YELLOW}正在思考...{Style.RESET_ALL}")
        
        # LLM 思考和決定移動
        move, thinking_process = self.llm_core.think_and_move(
            model_name=model_name,
            board_state=board_state,
            legal_moves=legal_moves,
            move_history=self.chess.move_history,
            player_color=player_color,
            personality=personality,
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
            print(f"{Fore.RED}✗ 無效移動: {move}{Style.RESET_ALL}")
            print(f"合法移動: {', '.join(legal_moves[:5])}{'...' if len(legal_moves) > 5 else ''}")
            return False
    
    def run_game(self):
        """執行完整的遊戲"""
        self.print_header()
        
        # 清空日誌檔案
        if os.path.exists(config.GAME_LOG_FILE):
            open(config.GAME_LOG_FILE, 'w').close()
        
        move_count = 0
        
        while not self.chess.is_game_over() and move_count < config.MAX_MOVES:
            self.print_board()
            
            current_player = self.chess.get_current_player()
            
            if current_player == "White":
                # 白棋回合
                success = self.play_turn("White", config.WHITE_MODEL, config.WHITE_PERSONALITY)
            else:
                # 黑棋回合
                success = self.play_turn("Black", config.BLACK_MODEL, config.BLACK_PERSONALITY)
            
            if not success:
                print(f"{Fore.RED}移動失敗，遊戲結束{Style.RESET_ALL}")
                break
            
            move_count += 1
            
            # 短暫暫停，讓輸出更易讀
            time.sleep(0.1)
        
        # 遊戲結束
        self.print_game_result()
        self.save_game_data()
    
    def print_game_result(self):
        """印出遊戲結果"""
        self.print_board()
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"                遊戲結束")
        print(f"{'='*60}{Style.RESET_ALL}")
        
        result = self.chess.get_game_result()
        status = self.chess.get_game_status()
        
        print(f"{Fore.YELLOW}結果: {result}")
        print(f"狀態: {status}")
        print(f"總移動數: {self.chess.get_move_count()}")
        
        game_duration = datetime.now() - self.game_start_time
        print(f"遊戲時長: {game_duration}{Style.RESET_ALL}")
        
        # 顯示 PGN
        print(f"\n{Fore.GREEN}PGN 記錄:{Style.RESET_ALL}")
        print(self.chess.export_pgn())
    
    def save_game_data(self):
        """保存遊戲資料"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存 PGN
        pgn_filename = f"game_{timestamp}.pgn"
        with open(pgn_filename, "w", encoding="utf-8") as f:
            f.write(self.chess.export_pgn())
        
        # 保存思考記錄
        thinking_filename = f"thinking_logs_{timestamp}.json"
        self.llm_core.save_thinking_logs(thinking_filename)
        
        print(f"\n{Fore.GREEN}遊戲資料已保存:")
        print(f"  PGN 檔案: {pgn_filename}")
        print(f"  思考記錄: {thinking_filename}")
        print(f"  遊戲日誌: {config.GAME_LOG_FILE}{Style.RESET_ALL}")


def main():
    """主函數"""
    try:
        game = ChessLLMGame()
        game.run_game()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}遊戲被使用者中斷{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}發生錯誤: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
