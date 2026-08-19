# sunking 项目配置

## 概述

sunking 是 GitHub Actions 云端机器人，与本地微信机器人 sunbot 独立运行。

---

## sunking（GitHub Actions 机器人）

- **仓库**: https://github.com/hedapeng1984/greeting-bot
- **本地路径**: `C:\Users\dapen\greeting-bot\`
- **运行**: 每天 6:45 北京时间自动执行
- **功能**: 调用 MiniMax API 生成励志名人金句，通过 Server 酱推送到微信
- **推送目标**: 何达鹏（Server 酱绑定你的微信）
- **格式**: "【名人】——名言内容"

## Secrets 配置

| 名称 | 值 |
|------|-----|
| MINIMAX_API_KEY | sk-cp-liesvHO4Qkx5B6bBqyBqcrfgh7bO2Cl37ecR5L1apdXocUypNO_bWhJvAABL9oGt7lHPzMrADWUd9pEGw46h5CQhAnljRCK_sY6btCKi5SjYAHYvvG5VWMQ |
| MINIMAX_BASE_URL | https://api.minimax.chat/v1 |
| SERVERCHAN_KEY | SCT400504TCWQz7L4Op0YKcy0vHrWzOYxy |

## 与 sunbot 的区别

| 机器人 | 路径 | 发送方式 | 推送内容 | 目标 |
|--------|------|----------|----------|------|
| **sunbot** | D:\wechat_auto_bot\ | 微信直接发 | 早安祝福（四字成语） | 小余哥 |
| **sunking** | C:\Users\dapen\greeting-bot\ | Server酱推送 | 每日励志金句 | 何达鹏 |

两个机器人独立运行，互为兜底。
