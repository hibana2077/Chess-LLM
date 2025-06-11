#!/usr/bin/env python3
"""
Chess-LLM 系統測試腳本
"""

import sys
import os

def test_imports():
    """測試模組導入"""
    print("測試模組導入...")
    
    try:
        import chess
        print("✓ python-chess 導入成功")
    except ImportError as e:
        print(f"✗ python-chess 導入失敗: {e}")
        return False
    
    try:
        import openai
        print("✓ openai 導入成功")
    except ImportError as e:
        print(f"✗ openai 導入失敗: {e}")
        return False
    
    try:
        from chess_core import ChessCore
        print("✓ ChessCore 導入成功")
    except ImportError as e:
        print(f"✗ ChessCore 導入失敗: {e}")
        return False
    
    try:
        from llm_inference import LLMInferenceCore
        print("✓ LLMInferenceCore 導入成功")
    except ImportError as e:
        print(f"✗ LLMInferenceCore 導入失敗: {e}")
        return False
    
    return True

def test_chess_core():
    """測試西洋棋核心功能"""
    print("\n測試西洋棋核心功能...")
    
    try:
        from chess_core import ChessCore
        
        chess = ChessCore()
        print("✓ ChessCore 初始化成功")
        
        # 測試初始位置
        initial_fen = chess.get_current_position()
        expected_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        if initial_fen == expected_fen:
            print("✓ 初始棋盤位置正確")
        else:
            print(f"✗ 初始棋盤位置錯誤: {initial_fen}")
            return False
        
        # 測試合法移動
        legal_moves = chess.get_legal_moves()
        if len(legal_moves) == 20:  # 初始位置有20個合法移動
            print("✓ 合法移動數量正確")
        else:
            print(f"✗ 合法移動數量錯誤: {len(legal_moves)}")
            return False
        
        # 測試移動
        if chess.make_move("e2e4"):
            print("✓ 移動執行成功")
        else:
            print("✗ 移動執行失敗")
            return False
        
        # 測試當前玩家
        if chess.get_current_player() == "Black":
            print("✓ 玩家輪換正確")
        else:
            print(f"✗ 玩家輪換錯誤: {chess.get_current_player()}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ ChessCore 測試失敗: {e}")
        return False

def test_config():
    """測試配置"""
    print("\n測試配置...")
    
    try:
        import config
        print("✓ config 模組導入成功")
        
        # 檢查必要的配置
        if hasattr(config, 'WHITE_MODEL'):
            print(f"✓ WHITE_MODEL: {config.WHITE_MODEL}")
        else:
            print("✗ 缺少 WHITE_MODEL 配置")
            return False
        
        if hasattr(config, 'BLACK_MODEL'):
            print(f"✓ BLACK_MODEL: {config.BLACK_MODEL}")
        else:
            print("✗ 缺少 BLACK_MODEL 配置")
            return False
        
        if hasattr(config, 'OPENROUTER_API_KEY'):
            if config.OPENROUTER_API_KEY:
                print("✓ API 金鑰已設定")
            else:
                print("⚠ API 金鑰未設定 (需要 .env 檔案)")
        else:
            print("✗ 缺少 OPENROUTER_API_KEY 配置")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ config 測試失敗: {e}")
        return False

def test_llm_core_init():
    """測試 LLM 核心初始化"""
    print("\n測試 LLM 核心初始化...")
    
    try:
        from llm_inference import LLMInferenceCore
        
        llm = LLMInferenceCore()
        print("✓ LLMInferenceCore 初始化成功")
        
        if hasattr(llm, 'client'):
            print("✓ OpenAI 客戶端已建立")
        else:
            print("✗ OpenAI 客戶端建立失敗")
            return False
        
        if hasattr(llm, 'thinking_logs'):
            print("✓ 思考記錄列表已初始化")
        else:
            print("✗ 思考記錄列表初始化失敗")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ LLMInferenceCore 測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("開始系統測試...\n")
    
    tests = [
        test_imports,
        test_config,
        test_chess_core,
        test_llm_core_init
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print(f"\n測試失敗，請檢查錯誤訊息")
    
    print(f"\n測試結果: {passed}/{total} 通過")
    
    if passed == total:
        print("✓ 所有測試通過！系統準備就緒。")
        print("\n要開始遊戲，請執行: python main.py")
        return True
    else:
        print("✗ 部分測試失敗，請先修復問題。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
