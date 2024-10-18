from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests
import json
from cachetools import TTLCache

app = Flask(__name__)

# 配置
LINE_CHANNEL_SECRET = 'your_line_channel_secret'
LINE_CHANNEL_ACCESS_TOKEN = 'your_line_channel_access_token'
DIFY_API_KEY = 'your_dify_api_key'
DIFY_API_URL = 'https://api.dify.ai/v1/chat-messages'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 使用 TTLCache 來模擬緩存服務
cache = TTLCache(maxsize=1000, ttl=3600)

def call_dify_chat_messages_api(request_data):
    headers = {
        'Authorization': f'Bearer {DIFY_API_KEY}',
        'Content-Type': 'application/json'
    }
    response = requests.post(DIFY_API_URL, headers=headers, json=request_data)
    return response.json()

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_message = event.message.text
    conversation_id = cache.get(user_id, "")

    if user_message.lower().strip() == "/forget":
        cache.pop(user_id, None)
        response_msg = "對話歷史已清除。"
    else:
        request_data = {
            "inputs": {},
            "query": user_message,
            "response_mode": "blocking",
            "conversation_id": conversation_id,
            "user": user_id
        }

        response = call_dify_chat_messages_api(request_data)
        response_msg = response.get('answer', '抱歉，我無法處理您的請求。')
        cache[user_id] = response.get('conversation_id', '')

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response_msg)
    )

if __name__ == "__main__":
    app.run(debug=True)
