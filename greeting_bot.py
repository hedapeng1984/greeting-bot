import random
import time
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
    # Windows 控制台编码处理 - 移除所有 emoji 和特殊符号
    import re
    # 移除常见 emoji 范围
    safe_msg = re.sub(r'[\U0001F000-\U0001F9FF]', '', msg)
    safe_msg = re.sub(r'[☀-⛿]', '', safe_msg)  # 其他符号
    # 也替换一些常见的符号
    safe_msg = safe_msg.replace('\U00002705', '[OK]')
    safe_msg = safe_msg.replace('\U0000274c', '[FAIL]')
    safe_msg = safe_msg.replace('⚠️', '[WARN]')
    print(f"[{timestamp}] {safe_msg}")


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
                    "content": "你是一位充满智慧的人生导师，擅长用名人名言激励他人行动。只输出一句名言，不要输出思考过程。"
                },
                {
                    "role": "user",
                    "content": f"""今天是{today}。请生成一句送给何达鹏的励志金句。

要求：
1. 内容要能激励他积极向上、扎实理清思路、推动行动
2. 可以是中文或英文名人金句
3. 格式："【名人】——名言内容"
   示例：【马云】——今天很残酷，明天更残酷，后天很美好，但绝大多数人死在明天晚上。
4. 只输出金句本身，不要有多余的解释"""
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
        # 励志金句备用文案
        fallback_greetings = [
            "【马云】——今天很残酷，明天更残酷，后天很美好，但绝大多数人死在明天晚上。",
            "【稻盛和夫】——付出不亚于任何人的努力。",
            "【曾国藩】——天下古今之庸人，皆以一惰字致败。",
        ]
        fallback = random.choice(fallback_greetings)
        log_message(f"🔄 使用备用金句: {fallback}")
        return fallback


def send_to_wechat(message, max_retries=3):
    """通过 Server 酱发送到微信（支持重试）"""
    # 尝试新旧两种 API
    api_endpoints = [
        f"https://sctapi.ftqq.com/{SERVERCHAN_KEY}.send",  # 新版 API
        f"https://sc.ftqq.com/{SERVERCHAN_KEY}.send",       # 旧版 API（兼容）
    ]

    for attempt in range(max_retries):
        for url in api_endpoints:
            try:
                params = {
                    "text": "💪 每日励志金句",
                    "desp": message
                }
                log_message(f"🔧 尝试推送 (尝试 {attempt + 1}/{max_retries}): {url[:40]}...")
                response = requests.get(url, params=params, timeout=15)
                result = response.json()

                # 新旧 API 都返回 code=0 表示成功
                if result.get("code") == 0:
                    log_message("✅ 微信推送成功")
                    return True

                error_msg = result.get("message", "未知错误")
                log_message(f"⚠️ API 返回错误: {error_msg}")

            except Exception as e:
                log_message(f"⚠️ 请求异常: {str(e)[:50]}")

        # 本次尝试失败，等待后重试
        if attempt < max_retries - 1:
            wait_time = (attempt + 1) * 2  # 递增等待时间
            log_message(f"⏳ {wait_time}秒后重试...")
            time.sleep(wait_time)

    log_message("❌ 推送失败，已尝试所有 API 和重试次数")
    return False


def main():
    log_message("=" * 50)
    log_message("🚀 励志金句机器人执行中")

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
