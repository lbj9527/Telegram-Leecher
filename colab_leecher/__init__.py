# copyright 2023 © Xron Trix | https://github.com/Xrontrix10

import logging, json, platform, os
from pyrogram.client import Client

# 处理uvloop在Windows系统的兼容性问题
if platform.system() != "Windows":
    try:
        from uvloop import install
        install()
        print("✅ uvloop已启用")
    except ImportError:
        print("⚠️ uvloop未安装，使用默认事件循环")
else:
    print("ℹ️ Windows系统检测到，跳过uvloop（不支持）")

# 适配不同系统的配置文件路径
if os.path.exists("credentials.json"):
    config_path = "credentials.json"
elif os.path.exists("/content/Telegram-Leecher/credentials.json"):
    config_path = "/content/Telegram-Leecher/credentials.json"
else:
    raise FileNotFoundError("找不到credentials.json配置文件")

# Read the dictionary from the config file
with open(config_path, "r") as file:
    credentials = json.loads(file.read())

API_ID = credentials["API_ID"]
API_HASH = credentials["API_HASH"]
BOT_TOKEN = credentials["BOT_TOKEN"]
OWNER = credentials["USER_ID"]
DUMP_ID = credentials["DUMP_ID"]

# 检查是否配置了代理
PROXY = credentials.get("PROXY", {})

logging.basicConfig(level=logging.INFO)

# 创建Client时支持代理
if PROXY:
    print(f"🌐 使用代理: {PROXY['hostname']}:{PROXY['port']}")
    colab_bot = Client(
        "my_bot", 
        api_id=API_ID, 
        api_hash=API_HASH, 
        bot_token=BOT_TOKEN,
        proxy=PROXY
    )
else:
    print("🌐 未配置代理，直接连接")
    colab_bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
