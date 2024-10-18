import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from cachetools import TTLCache

# 配置
TELEGRAM_BOT_TOKEN = 'your_telegram_bot_token'
DIFY_API_KEY = 'your_dify_api_key'
DIFY_API_URL = 'https://api.dify.ai/v1/chat-messages'

# 使用 TTLCache 來模擬緩存服務
cache = TTLCache(maxsize=1000, ttl=3600)

async def call_dify_chat_messages_api(request_data):
    headers = {
        'Authorization': f'Bearer {DIFY_API_KEY}',
        'Content-Type': 'application/json'
    }
    response = requests.post(DIFY_API_URL, headers=headers, json=request_data)
    return response.json()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('你好！我是一個由 Dify AI 驅動的聊天機器人。請隨意與我聊天！')

async def forget(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    cache.pop(str(user_id), None)
    await update.message.reply_text("對話歷史已清除。")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    user_message = update.message.text
    conversation_id = cache.get(user_id, "")

    request_data = {
        "inputs": {},
        "query": user_message,
        "response_mode": "blocking",
        "conversation_id": conversation_id,
        "user": user_id
    }

    response = await call_dify_chat_messages_api(request_data)
    response_msg = response.get('answer', '抱歉，我無法處理您的請求。')
    cache[user_id] = response.get('conversation_id', '')

    await update.message.reply_text(response_msg)

def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("forget", forget))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()


# 這個版本的主要特點：
# 1. 使用 python-telegram-bot 庫來處理 Telegram Bot API。
# 2. 保留了使用 Dify API 和緩存對話 ID 的邏輯。
# 3. 新增了 /start 和 /forget 命令處理器。
# 4. 主要邏輯保持不變：
#     . 處理用戶消息
#     . 調用 Dify API 獲取回應
#     . 存儲對話 ID
#     . 回覆消息給用戶

# 使用說明：
# 1. 安裝必要的庫：
# pip install python-telegram-bot requests cachetools
# 2. 替換配置中的佔位符為實際的 Telegram Bot Token 和 Dify API 密鑰。
# 3. 運行腳本：
# python telegram_bot.py
# 4. 在 Telegram 中與您的機器人開始對話。
# 主要變化：
# 1. 使用 Telegram 的命令系統，新增了 /start 和 /forget 命令。
# 2. 使用 Telegram 的更新處理系統，不需要設置 Webhook。
# 3. 消息處理邏輯適應了 Telegram 的 API 結構。