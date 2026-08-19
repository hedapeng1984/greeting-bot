# sunbot & sunking 项目配置

## 概述

两个独立的早安问候机器人：
1. **sunbot** - 本地微信机器人
2. **sunking** - GitHub Actions 云端机器人

---

## sunbot（本地微信机器人）

- **路径**: `D:\wechat_auto_bot\greeting_bot.py`
- **运行**: `python D:\wechat_auto_bot\greeting_bot.py --once`
- **功能**: 调用 MiniMax API 生成早安祝福，通过 Windows GUI 自动化发送到微信"小余哥"
- **格式**: "小余哥，早上好☀️☀️☀️，[四字祝福语]，[四字祝福语]"
- **依赖**: Windows + 微信客户端 + pywin32

---

## sunking（GitHub Actions 机器人）

- **仓库**: https://github.com/hedapeng1984/greeting-bot
- **运行**: 每天 6:45 北京时间自动执行
- **功能**: 调用 MiniMax API 生成励志名人金句，通过 Server 酱推送到微信
- **推送目标**: 何达鹏（Server 酱绑定的是你的微信）
- **格式**: "【名人】——名言内容"
- **Secrets 配置**:
  - MINIMAX_API_KEY
  - MINIMAX_BASE_URL: https://api.minimax.chat/v1
  - SERVERCHAN_KEY

---

## 定时任务

- **sunbot**: Windows 任务计划，每天 6:45 启动
- **sunking**: GitHub Actions cron: 45 22 * * * (UTC = 6:45 北京时间)

---

## 使用场景

- sunking 作为兜底方案，电脑不开机也能收到推送
- sunbot 作为主要方案，微信直接发给小余哥
