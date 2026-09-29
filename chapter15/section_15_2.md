## 15.2 邮件自动发送——让程序替你"跑腿"

你是否需要在每天下班前给领导发日报？或者在监控脚本检测到异常时自动通知自己？Python 的 `smtplib` 和 `email` 模块可以帮你实现这一切——用代码发送邮件，可以是简单的纯文本，也可以是图文并茂的 HTML 邮件，甚至可以带上附件。

### 15.2.1 SMTP 基础——邮件是怎么发出去的？

发送邮件依赖 **SMTP**（Simple Mail Transfer Protocol，简单邮件传输协议）。Python 的 `smtplib` 模块封装了 SMTP 协议，你只需要提供：
- SMTP 服务器地址和端口（如 QQ 邮箱是 `smtp.qq.com:587`）
- 你的邮箱账号和**授权码**（不是登录密码！）
- 发件人、收件人、主题和正文

**获取授权码**（以 QQ 邮箱为例）：登录 QQ 邮箱 → 设置 → 账户 → POP3/IMAP/SMTP 服务 → 开启并获取授权码。**千万不要把授权码硬编码在代码中**——用环境变量存储（参见 11.1 节）。

### 15.2.2 发送纯文本邮件

```python
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_text_email(smtp_server, smtp_port, sender, password, receiver, subject, body):
    """
    发送纯文本邮件
    smtp_server: SMTP 服务器地址（如 smtp.qq.com）
    smtp_port: 端口号（QQ: 587, 163: 465）
    sender: 发件人邮箱
    password: SMTP 授权码（不是登录密码！）
    receiver: 收件人邮箱
    subject: 邮件主题
    body: 邮件正文
    """
    # 构造邮件对象
    msg = MIMEText(body, "plain", "utf-8")    # plain = 纯文本
    msg["From"] = Header(f"发件人<{sender}>")
    msg["To"] = Header(f"收件人<{receiver}>")
    msg["Subject"] = Header(subject, "utf-8")

    try:
        # 连接 SMTP 服务器
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        server.starttls()                        # 启用 TLS 加密
        server.login(sender, password)
        server.sendmail(sender, [receiver], msg.as_string())
        print(f"✅ 邮件已发送至 {receiver}")
    except smtplib.SMTPAuthenticationError:
        print("❌ 认证失败——检查邮箱地址和授权码是否正确")
    except smtplib.SMTPConnectError:
        print("❌ 连接失败——检查 SMTP 服务器地址和端口")
    except Exception as e:
        print(f"❌ 发送失败: {e}")
    finally:
        try:
            server.quit()
        except:
            pass

# 使用示例——请替换为你的真实邮箱信息
# import os
# send_text_email(
#     smtp_server="smtp.qq.com",
#     smtp_port=587,
#     sender=os.environ.get("EMAIL_USER"),
#     password=os.environ.get("EMAIL_PASS"),
#     receiver="friend@example.com",
#     subject="来自 Python 的问候",
#     body="你好！这是我用 Python 自动发送的邮件。\n祝你今天愉快！"
# )
```

### 15.2.3 发送 HTML 邮件——图文并茂

HTML 邮件可以包含格式、颜色、图片和链接，适合发送报告、通知等需要美观排版的内容：

```python
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def send_html_email(smtp_server, smtp_port, sender, password, receiver,
                    subject, html_body):
    """发送 HTML 格式的邮件"""
    msg = MIMEMultipart("alternative")    # alternative = 同时提供纯文本和 HTML
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject

    # 纯文本版本——邮件客户端不支持 HTML 时的降级方案
    text_body = "请使用支持 HTML 的邮件客户端查看此邮件。"

    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, [receiver], msg.as_string())
        print("✅ HTML 邮件已发送")

# HTML 模板——模拟每日工作报告
daily_report = """
<html>
<body style="font-family: 'Microsoft YaHei', sans-serif; max-width: 600px;">
    <h2 style="color: #1565C0;">📊 每日工作报告 — 2024-06-29</h2>

    <h3>✅ 今日完成</h3>
    <ul>
        <li>完成用户登录模块的开发（3h）</li>
        <li>修复订单列表页的排序 Bug（1h）</li>
        <li>参与代码评审会议（1h）</li>
    </ul>

    <h3>📋 明日计划</h3>
    <ul>
        <li>开始支付模块集成</li>
        <li>编写用户模块的单元测试</li>
    </ul>

    <h3>⚠️ 遇到的问题</h3>
    <p style="background: #fff3e0; padding: 10px; border-left: 4px solid #ff9800;">
        支付 API 文档不完整，已发邮件沟通，预计明天收到回复。
    </p>

    <hr>
    <p style="color: #888; font-size: 12px;">
        此邮件由 Python 自动化脚本自动发送 | 回复此邮件将不被处理
    </p>
</body>
</html>
"""
```

### 15.2.4 发送带附件的邮件

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_email_with_attachment(smtp_server, smtp_port, sender, password,
                               receiver, subject, body, filepath):
    """发送带附件的邮件"""
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject

    # 正文
    msg.attach(MIMEText(body, "plain", "utf-8"))

    # 附件
    filename = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        attachment = MIMEBase("application", "octet-stream")
        attachment.set_payload(f.read())
    encoders.encode_base64(attachment)
    attachment.add_header(
        "Content-Disposition",
        f"attachment; filename*=UTF-8''{filename}"
    )
    msg.attach(attachment)

    with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, [receiver], msg.as_string())
        print(f"✅ 邮件已发送（附件: {filename}）")

# 使用示例
# send_email_with_attachment(
#     ...,  # smtp 配置同上
#     subject="数据分析报告",
#     body="请查收附件中的本月销售数据分析报告。",
#     filepath="./sales_report.pdf"
# )
```

### 15.2.5 群发邮件——尊重每一位收件人

```python
import smtplib
from email.mime.text import MIMEText
import time

def send_bulk_email(smtp_server, smtp_port, sender, password, receivers,
                    subject_template, get_body):
    """
    群发邮件——每封独立发送，收件人互不可见
    receivers: 收件人列表 [(邮箱, 姓名), ...]
    get_body: 函数，接收 (email, name) 返回邮件正文（可做个性化）
    """
    with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
        server.starttls()
        server.login(sender, password)

        success, failed = 0, 0
        for email, name in receivers:
            msg = MIMEText(get_body(email, name), "plain", "utf-8")
            msg["From"] = sender
            msg["To"] = email
            msg["Subject"] = subject_template.replace("{name}", name)

            try:
                server.sendmail(sender, [email], msg.as_string())
                print(f"  ✅ {name} <{email}>")
                success += 1
            except Exception as e:
                print(f"  ❌ {name} <{email}>: {e}")
                failed += 1

            time.sleep(1)    # 间隔 1 秒，避免被 SMTP 服务器限流

    print(f"\n发送完成：成功 {success}，失败 {failed}")

# 使用示例
# receivers = [
#     ("alice@example.com", "Alice"),
#     ("bob@example.com", "Bob"),
# ]
# send_bulk_email(
#     ...,  # smtp 配置
#     receivers=receivers,
#     subject_template="{name}，你好！最新课程已上线",
#     get_body=lambda email, name: f"亲爱的{name}：\n\n新课程《Python自动化》已上线..."
# )
```

### 15.2.6 实战练习

1. 编写一个"异常监控邮件通知"函数：当程序发生未捕获的异常时，自动发送一封邮件到管理员邮箱，邮件内容包含异常类型、异常信息、发生时间和完整的 traceback 栈信息。

2. 实现"定时发送日报"——编写一个脚本，每天下午 5:30 自动从数据库/CSV 文件中读取当天的数据（模拟），生成一份 HTML 格式的日报并发送到指定邮箱。使用 `schedule` 库实现定时触发。

3. 改进群发邮件程序——添加"退订"功能：在邮件末尾附上退订链接（模拟），将退订请求记录到文件中。同时限制每小时最多发送 50 封邮件，防止触发邮件服务商的每日限额。