#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Leecher Bot 启动脚本
"""

import sys
import os

def main():
    print("🚀 启动 Telegram Leecher Bot...")
    print("=" * 50)
    
    # 检查配置文件是否存在
    if not os.path.exists("credentials.json"):
        print("❌ 错误: 找不到 credentials.json 配置文件")
        print("请参考 credentials.json.example 创建配置文件")
        return
    
    # 导入并运行bot
    try:
        import colab_leecher
        print("✅ 配置加载成功")
        print("🤖 Bot正在启动...")
        colab_leecher.colab_bot.run()
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保已安装所有依赖包")
    except Exception as e:
        print(f"❌ 运行错误: {e}")

if __name__ == "__main__":
    main() 