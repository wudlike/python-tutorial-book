## 15.3 微信机器人基础——把 Python 接入日常聊天

微信是中国使用最广泛的即时通讯工具。能用 Python 控制微信——自动回复消息、定时发送提醒、把群聊消息转发到邮箱——是无数自动化需求的起点。本节介绍一个开源的微信机器人方案，帮你快速搭建一个可运行的微信自动化助手。

---

\begin{warningbox}
**合规性声明**
微信官方不允许第三方程序控制微信客户端，自动化的微信操作有**封号风险**。本节内容仅供**技术学习**使用，请遵守微信的用户协议，不要用于商业用途、批量营销或骚扰他人。建议使用**小号**测试。
\end{warningbox}

---

### 15.3.1 方案选择——itchat 与 WeChaty

Python 控制微信主要有两种思路：
- **itchat**：模拟 Web 微信协议，纯 Python 实现，最适合学习。缺点是新注册的微信号通常没有 Web 微信权限
- **WeChaty + Python**：基于 Puppet 协议，支持多种协议适配器，更稳定但配置更复杂

本节基于 itchat 进行讲解（如果有 Web 微信权限的话）。如果你没有 Web 微信权限，本节也提供一个用 Flask 搭建的"模拟微信机器人"方案，同样覆盖了核心的编程模式和概念。

### 15.3.2 itchat 基础——登录与消息接收

```python
# 安装
# pip install itchat

import itchat

# 登录——扫描二维码
itchat.auto_login(hotReload=True)    # hotReload=True 短期内免扫二维码

# 获取好友列表
friends = itchat.get_friends(update=True)
print(f"共有 {len(friends)} 位好友")

# 给自己发送一条消息
itchat.send("Hello, 这是我用 Python 发送的消息！", toUserName="filehelper")

# 获取所有群聊
chatrooms = itchat.get_chatrooms(update=True)
for room in chatrooms[:5]:
    print(f"群名: {room['NickName']} | 人数: {len(room['MemberList'])}")

# 退出登录
itchat.logout()
```

### 15.3.3 消息自动回复——最核心的功能

`@itchat.msg_register` 装饰器是 itchat 的灵魂——它注册一个函数来处理特定类型的消息：

```python
import itchat
import time
from datetime import datetime

# 全局变量——记录消息统计数据
stats = {"received": 0, "replied": 0, "start_time": time.time()}

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    """处理所有收到的文本消息"""
    stats["received"] += 1
    from_user = msg["User"]["NickName"]
    content = msg["Text"]
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {from_user}: {content}")

    # 根据内容回复——关键词匹配
    reply = None
    content_lower = content.lower().strip()

    if "帮助" in content or "help" in content_lower:
        reply = (
            "🤖 我是 Python 机器人小助手\n"
            "支持的命令：\n"
            "  • 帮助/help — 显示此菜单\n"
            "  • 时间 — 查看当前时间\n"
            "  • 天气 — 查询天气（示例）\n"
            "  • 统计 — 查看机器人运行状态\n"
            "  • 笑话 — 随机讲个笑话"
        )
    elif "时间" in content:
        reply = f"🕐 当前时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    elif "天气" in content:
        reply = "🌤 今天天气不错（具体功能需要接入天气 API）"
    elif "笑话" in content:
        import random
        jokes = [
            "为什么程序员不喜欢出门？因为外面的世界没有 Git。",
            "老婆给程序员打电话：下班买一斤包子回来，如果看到卖西瓜的，买一个。"
            "结果程序员只买了一个包子回来——因为他看到了卖西瓜的。",
            "程序员最讨厌康熙的哪个儿子？——胤禩，因为他是八阿哥（bug）。",
        ]
        reply = random.choice(jokes)
    elif "统计" in content:
        uptime = time.time() - stats["start_time"]
        reply = (
            f"📊 运行状态\n"
            f"运行时间：{uptime/3600:.1f} 小时\n"
            f"收到消息：{stats['received']} 条\n"
            f"回复消息：{stats['replied']} 条"
        )
    else:
        reply = f'收到你的消息："{content}"\n回复"帮助"查看我能做什么'

    if reply:
        stats["replied"] += 1
        msg.user.send(reply)

# 启动机器人
print("🤖 微信机器人启动中...")
itchat.auto_login(hotReload=True)
itchat.run()    # 阻塞运行，持续监听消息
```

### 15.3.4 定时发送——早安提醒与天气预报

结合 `apscheduler` 库实现定时任务：

```python
# pip install apscheduler

import itchat
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

def send_morning_greeting():
    """每天早上 8 点发送早安消息给出差群"""
    today = datetime.now().strftime("%Y年%m月%d日")
    weekday = ["一", "二", "三", "四", "五", "六", "日"][datetime.now().weekday()]
    message = (
        f"☀️ 早安！今天是 {today} 星期{weekday}\n"
        f"今日待办：\n"
        f"  • 10:00 团队站会\n"
        f"  • 14:00 项目评审\n"
        f"  • 提交周报\n\n"
        f"新的一天，加油！💪"
    )

    # 找到指定群聊
    rooms = itchat.search_chatrooms(name="工作群")
    if rooms:
        rooms[0].send(message)
        print(f"[定时任务] 早安消息已发送到 {rooms[0]['NickName']}")

# 启动定时器
scheduler = BackgroundScheduler()
scheduler.add_job(send_morning_greeting, "cron", hour=8, minute=0)
scheduler.start()

# itchat.auto_login(hotReload=True)
# itchat.run()
```

### 15.3.5 模拟微信机器人——无需 Web 微信权限

如果 itchat 不可用，这里提供一个基于 Flask 的模拟方案——通过 HTTP 接口收发消息，覆盖了相同的编程概念：

```python
# 保存为 fake_wechat_bot.py，运行后访问 http://127.0.0.1:5000
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
import random

app = Flask(__name__)

# 模拟的消息存储
messages = []
BOT_NAME = "🤖 小助手"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>模拟微信机器人</title>
    <style>
        body { font-family: "Microsoft YaHei"; max-width: 600px; margin: 20px auto; }
        .chat-box { border: 1px solid #ddd; height: 400px; overflow-y: auto;
                    padding: 10px; border-radius: 8px; background: #f5f5f5; }
        .msg { margin: 8px 0; padding: 6px 12px; border-radius: 12px; max-width: 80%; }
        .user { background: #95ec69; float: right; clear: both; }
        .bot { background: white; float: left; clear: both; }
        .input-area { margin-top: 10px; display: flex; gap: 8px; }
        input { flex: 1; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        button { padding: 8px 20px; background: #07c160; color: white;
                 border: none; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <h2>模拟微信机器人</h2>
    <div class="chat-box" id="chat">
        {% for msg in messages %}
        <div class="msg {{ 'user' if msg.role == 'user' else 'bot' }}">
            <b>{{ '你' if msg.role == 'user' else BOT_NAME }}</b><br>
            {{ msg.text }}
        </div>
        <div style="clear:both"></div>
        {% endfor %}
    </div>
    <form method="post" class="input-area">
        <input name="text" placeholder="输入消息..." autofocus>
        <button type="submit">发送</button>
    </form>
</body>
</html>
"""

def process_message(text):
    """处理消息并返回回复——核心逻辑"""
    text_lower = text.lower().strip()
    if "帮助" in text or "help" in text_lower:
        return "支持的命令：帮助 | 时间 | 天气 | 笑话 | 统计"
    elif "时间" in text:
        return f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    elif "笑话" in text:
        return random.choice([
            "为什么程序员总在深夜工作？因为 Bug 是夜行动物。",
            "一个 QA 走进酒吧，要了 1 杯酒...999 杯酒...0 杯酒...-1 杯酒。",
        ])
    elif "天气" in text:
        return "🌤 晴天 25°C（模拟数据）"
    else:
        return f"收到：{text}（回复'帮助'查看菜单）"

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_text = request.form["text"]
        messages.append({"role": "user", "text": user_text})
        reply = process_message(user_text)
        messages.append({"role": "bot", "text": reply})
    return render_template_string(HTML, messages=messages, BOT_NAME=BOT_NAME)

@app.route("/api/send", methods=["POST"])
def api_send():
    """API 接口——可供外部脚本调用"""
    data = request.json
    user_text = data.get("text", "")
    reply = process_message(user_text)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
```

### 15.3.6 实战练习

1. 在 itchat 或模拟微信机器人中，实现一个"成语接龙"游戏——机器人先出一个成语，用户接的成语必须以前一个成语的最后一个字开头，机器人检查是否合法并继续接龙。

2. 为微信机器人添加"关键词提醒"功能：用户可以发送"提醒 14:00 开会"，机器人在指定时间向该用户发送提醒消息。使用 `apscheduler` 实现定时调度。

3. 实现"群消息归档"功能——将指定群聊的所有消息（包括发送者、时间、内容）实时记录到 SQLite 数据库中，支持按日期和关键词检索。