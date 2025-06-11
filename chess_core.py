import chess
import chess.pgn
from typing import List, Optional
from datetime import datetime


class ChessCore:
    """西洋棋核心類別，處理棋盤狀態、移動驗證和遊戲規則"""
    
    def __init__(self):
        self.board = chess.Board()
        self.move_history: List[chess.Move] = []
        self.game_start_time = datetime.now()
        self.current_turn = "White"
        
    def get_current_position(self) -> str:
        """獲取當前棋盤的 FEN 表示"""
        return self.board.fen()
    
    def get_board_ascii(self) -> str:
        """獲取棋盤的 ASCII 表示"""
        return str(self.board)
    
    def get_legal_moves(self) -> List[str]:
        """獲取當前位置所有合法移動"""
        return [move.uci() for move in self.board.legal_moves]
    
    def make_move(self, move_uci: str) -> bool:
        """
        執行移動
        
        Args:
            move_uci: UCI 格式的移動 (例如: "e2e4")
            
        Returns:
            bool: 移動是否成功
        """
        try:
            move = chess.Move.from_uci(move_uci)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.move_history.append(move)
                self.current_turn = "Black" if self.board.turn == chess.BLACK else "White"
                return True
            else:
                return False
        except (ValueError, chess.InvalidMoveError):
            return False
    
    def is_game_over(self) -> bool:
        """檢查遊戲是否結束"""
        return self.board.is_game_over()
    
    def get_game_result(self) -> str:
        """獲取遊戲結果"""
        if not self.is_game_over():
            return "Game in progress"
        
        result = self.board.result()
        if result == "1-0":
            return "White wins"
        elif result == "0-1":
            return "Black wins"
        else:
            return "Draw"
    
    def get_game_status(self) -> str:
        """獲取當前遊戲狀態描述"""
        if self.board.is_checkmate():
            return "Checkmate"
        elif self.board.is_stalemate():
            return "Stalemate"
        elif self.board.is_check():
            return "Check"
        elif self.board.is_insufficient_material():
            return "Insufficient material"
        elif self.board.is_fifty_moves():
            return "Fifty-move rule"
        elif self.board.is_repetition():
            return "Threefold repetition"
        else:
            return "Active"
    
    def get_move_count(self) -> int:
        """獲取總移動數"""
        return len(self.move_history)
    
    def get_current_player(self) -> str:
        """獲取當前輪到的玩家"""
        return "White" if self.board.turn == chess.WHITE else "Black"
    
    def export_pgn(self) -> str:
        """匯出 PGN 格式的遊戲記錄"""
        game = chess.pgn.Game()
        game.headers["Event"] = "LLM Chess Battle"
        game.headers["Date"] = self.game_start_time.strftime("%Y.%m.%d")
        game.headers["White"] = "LLM White"
        game.headers["Black"] = "LLM Black"
        game.headers["Result"] = self.board.result()
        
        # 建立移動樹
        node = game
        board = chess.Board()
        for move in self.move_history:
            node = node.add_variation(move)
            board.push(move)
        
        return str(game)
    
    def get_position_analysis(self) -> dict:
        """獲取當前位置的基本分析"""
        return {
            "turn": self.get_current_player(),
            "move_count": self.get_move_count(),
            "status": self.get_game_status(),
            "legal_moves_count": len(list(self.board.legal_moves)),
            "is_check": self.board.is_check(),
            "material_balance": self._calculate_material_balance()
        }
    
    def _calculate_material_balance(self) -> int:
        """計算材料平衡（正數表示白棋優勢）"""
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        
        white_material = 0
        black_material = 0
        
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                value = piece_values[piece.piece_type]
                if piece.color == chess.WHITE:
                    white_material += value
                else:
                    black_material += value
        
        return white_material - black_material
