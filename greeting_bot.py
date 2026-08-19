import random
import requests
from datetime import datetime
from openai import OpenAI
import os
import json

# 从环境变量获取配置
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY")
MINIMAX_BASE_URL = os.environ.get("MINIMAX_BASE_URL", "https://api.minimax.chat/v1")
SERVERCHAN_KEY = os.environ.get("SERVERCHAN_KEY")


def log_message(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")


def generate_greeting():
    """调用 MiniMax API 生成早安问候语"""
    try:
        client = OpenAI(
            api_key=MINIMAX_API_KEY,
            base_url=MINIMAX_BASE_URL
        )

        today = datetime.now().strftime("%Y年%m月%d日")

        response = client.chat.completions.create(
            model="abab6.5s-chat",
            messages=[
                {
                    "role": "system",
                    "content": "你是一位温暖、贴心的早安问候语生成助手。只输出问候语，不要输出思考过程。"
                },
                {
                    "role": "user",
                    "content": f"""今天是{today}。请生成一句发给好友的早安问候语。

要求：
1. 收件人称呼为"小余哥"
2. 格式："小余哥，早上好☀️☀️☀️，[四字祝福语]，[四字祝福语]。"
   示例："小余哥，早上好☀️☀️☀️，健康富有，平安喜乐。"
3. 必须包含两组不同的四字祝福语
4. 只输出问候语本身，不要有多余的解释"""
                }
            ],
            max_tokens=200,
            temperature=0.9,
            extra_body={"disable_thinking": True}
        )

        raw_content = response.choices[0].message.content.strip()

        import re
        cleaned = re.sub(r'<thinking>.*?</thinking>', '', raw_content, flags=re.DOTALL).strip()

        if not cleaned or len(cleaned) < 10:
            raise ValueError("API返回内容无效")

        log_message(f"✅ API调用成功，生成问候语: {cleaned}")
        return cleaned

    except Exception as e:
        log_message(f"❌ API调用失败: {str(e)}")
        fallback_greetings = [
            "小余哥，早上好☀️☀️☀️，身体健康，万事如意。",
            "小余哥，早上好☀️☀️☀️，前程似锦，幸福美满。",
            "小余哥，早上好☀️☀️☀️，心想事成，吉祥如意。",
        ]
        fallback = random.choice(fallback_greetings)
        log_message(f"🔄 使用备用问候语: {fallback}")
        return fallback


def send_to_wechat(message):
    """通过 Server 酱发送到微信"""
    try:
        # 使用 GET 方式发送
        url = f"https://sct.ftqq.com/{SERVERCHAN_KEY}.send"
        params = {
            "text": "早安问候",
            "desp": message
        }
        log_message(f"🔧 发送请求到: {url}")
        response = requests.get(url, params=params, timeout=15)
        log_message(f"📥 响应状态码: {response.status_code}")
        log_message(f"📥 响应内容: {response.text[:200]}")
        result = response.json()

        if result.get("code") == 0:
            log_message("✅ 微信推送成功")
            return True
        else:
            log_message(f"❌ 推送失败: {result.get('message')}")
            return False

    except Exception as e:
        log_message(f"❌ 推送失败: {str(e)}")
        return False


def main():
    log_message("=" * 50)
    log_message("🚀 早安问候机器人执行中")

    greeting = generate_greeting()
    if not greeting:
        log_message("❌ 无法生成问候语，任务终止")
        return

    success = send_to_wechat(greeting)

    if success:
        log_message("🎉 任务完成")
    else:
        log_message("⚠️ 任务失败")


if __name__ == "__main__":
    main()
