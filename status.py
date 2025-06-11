#!/usr/bin/env python3
"""
專案狀態檢查和資訊顯示
"""

import os
from datetime import datetime

def print_project_status():
    """顯示專案狀態"""
    print("=" * 60)
    print("           Chess-LLM 專案狀態報告")
    print("=" * 60)
    print(f"生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 檢查檔案狀態
    files_status = [
        ("chess_core.py", "西洋棋核心邏輯"),
        ("llm_inference.py", "LLM 推理引擎"),
        ("main.py", "主程式"),
        ("demo.py", "示範程式"),
        ("config.py", "配置設定"),
        ("test_system.py", "系統測試"),
        ("requirements.txt", "依賴套件"),
        ("README.md", "專案說明"),
        ("QUICKSTART.md", "快速開始指南"),
        (".env", "環境變數設定"),
        (".env.example", "環境變數範例")
    ]
    
    print("📁 檔案狀態:")
    for filename, description in files_status:
        status = "✅" if os.path.exists(filename) else "❌"
        print(f"  {status} {filename:<20} - {description}")
    
    print()
    
    # 檢查配置
    print("⚙️ 系統配置:")
    try:
        import config
        print(f"  白棋模型: {config.WHITE_MODEL}")
        print(f"  黑棋模型: {config.BLACK_MODEL}")
        print(f"  最大移動數: {config.MAX_MOVES}")
        print(f"  思考超時: {config.THINKING_TIMEOUT}秒")
        
        if config.OPENROUTER_API_KEY:
            print("  API 金鑰: ✅ 已設定")
        else:
            print("  API 金鑰: ⚠️ 未設定")
    except Exception as e:
        print(f"  配置載入失敗: {e}")
    
    print()
    
    # 功能特色
    print("🎯 實作功能:")
    features = [
        "完整的西洋棋規則引擎",
        "支援多種 LLM 模型對弈",
        "詳細的思考過程記錄",
        "PGN 格式棋譜匯出", 
        "彩色終端介面",
        "局面分析和統計",
        "示範模式 (無需 API)",
        "完整的系統測試"
    ]
    
    for feature in features:
        print(f"  ✅ {feature}")
    
    print()
    
    # 使用指南
    print("🚀 使用方式:")
    print("  1. 體驗示範:     python3 demo.py")
    print("  2. 系統測試:     python3 test_system.py")
    print("  3. 真實對弈:     python3 main.py (需要 API 金鑰)")
    print()
    
    print("📖 詳細說明請參考:")
    print("  - README.md      - 完整專案說明")
    print("  - QUICKSTART.md  - 快速開始指南")
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    print_project_status()
