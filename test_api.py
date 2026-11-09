import requests
import json
import time

# ⚠️ 【安全提示】请在GitHub公开仓库中隐藏你的真实Token，用占位符代替
API_TOKEN = "pat_xxxxxxxxxxxxxxxxxxxxxxxx" 
BOT_ID = "7705788971410440232"

headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}

print("=== 1. 正在发起对话 ===")
payload = {
    "bot_id": BOT_ID,
    "user_id": "student_test_01",
    "stream": False,
    "auto_save_history": True,
    "additional_messages": [{"role": "user", "content": "什么是存储周期？", "content_type": "text"}]
}

resp = requests.post("https://api.coze.cn/v3/chat", headers=headers, json=payload)
resp_data = resp.json()
print("=== 2. 接口返回结果 ===")
print(json.dumps(resp_data, ensure_ascii=False, indent=2))

if resp_data.get("code") == 0:
    chat_id = resp_data["data"]["id"]
    conv_id = resp_data["data"]["conversation_id"]
    
    print("\n=== 3. 等待 6 秒钟，让 AI 把话说完 ===")
    time.sleep(6) # 停 6 秒，确保豆包大模型生成完毕
    
    print("\n=== 4. 直接拉取最终回答 ===")
    msg_url = f"https://api.coze.cn/v3/chat/message/list?conversation_id={conv_id}&chat_id={chat_id}"
    msg_data = requests.get(msg_url, headers=headers).json()
    
    for msg in msg_data.get("data", []):
        if msg.get("role") == "assistant" and msg.get("type") == "answer":
            print(f"\n👉 最终提取的回答内容: {msg.get('content')}")
else:
    print("❌ 失败:", resp_data.get("msg"))
