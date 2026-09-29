## 14.1 requests 库使用——HTTP 的世界语

在第 13 章中，我们站在服务器的角度处理 HTTP 请求——当浏览器访问某个 URL 时，Flask 负责返回响应。现在换个视角：你作为**客户端**，用 Python 代码去访问别人的网站，获取页面内容。这就是 requests 库的职责——它把复杂的 HTTP 协议封装成直观的 Python 调用，让你像"用浏览器访问网页"一样简单。

requests 是 Python 生态中下载量最高的第三方库之一，GitHub 上有超过 50k 的 star。它的设计哲学是"HTTP for Humans"——能一行代码搞定的事，绝不用两行。

### 14.1.1 安装与第一个请求

```python
# pip install requests

import requests

# GET 请求——最基础的操作，获取网页内容
response = requests.get("https://httpbin.org/get")
print(f"状态码: {response.status_code}")        # 200
print(f"编码: {response.encoding}")              # utf-8
print(f"响应头: {dict(response.headers)}")
print(f"内容前 200 字符:\n{response.text[:200]}")
```

### 14.1.2 HTTP 方法——GET、POST、PUT、DELETE

```python
import requests

# GET —— 获取资源（可带查询参数）
params = {"q": "python tutorial", "page": 1}
response = requests.get("https://httpbin.org/get", params=params)
print(f"实际请求 URL: {response.url}")
# https://httpbin.org/get?q=python+tutorial&page=1

# POST —— 提交数据
# 方式 1：表单数据（application/x-www-form-urlencoded）
data = {"username": "alice", "password": "secret123"}
response = requests.post("https://httpbin.org/post", data=data)
print(response.json()["form"])

# 方式 2：JSON 数据（application/json）
import json
json_data = {"name": "Alice", "age": 25, "skills": ["Python", "SQL"]}
response = requests.post("https://httpbin.org/post", json=json_data)
print(response.json()["json"])         # 服务端收到的 JSON

# 方式 3：直接发送 JSON 字符串
response = requests.post(
    "https://httpbin.org/post",
    data=json.dumps(json_data),
    headers={"Content-Type": "application/json"}
)

# PUT —— 更新资源（全部替换）
response = requests.put("https://httpbin.org/put", json={"name": "Bob"})

# DELETE —— 删除资源
response = requests.delete("https://httpbin.org/delete")

# 总结四种方法的语义
print(f"GET     — 获取：{requests.get('https://httpbin.org/get').status_code}")
print(f"POST    — 创建：{requests.post('https://httpbin.org/post').status_code}")
print(f"PUT     — 更新：{requests.put('https://httpbin.org/put').status_code}")
print(f"DELETE  — 删除：{requests.delete('https://httpbin.org/delete').status_code}")
```

`json=` 参数和 `data=` 参数的关键区别：`json=` 会自动设置 `Content-Type: application/json` 并将 Python 对象序列化为 JSON 字符串；`data=` 需要你手动设置 Content-Type 头并自行序列化。

### 14.1.3 请求头与 Cookie——"伪装"成浏览器

很多网站会检查 `User-Agent` 请求头来判断访问者是不是浏览器。直接用 requests 的默认 `User-Agent`（像 `python-requests/2.x`）很容易被网站拦截：

```python
import requests

# 设置请求头——模仿浏览器
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://www.google.com/",
}

response = requests.get("https://httpbin.org/headers", headers=headers)
print(response.json()["headers"]["User-Agent"])

# Cookie 管理——requests 自动处理（像浏览器一样）
session = requests.Session()    # 创建会话——自动保存 Cookie

# 登录（模拟）
session.post("https://httpbin.org/post",
             data={"username": "alice", "password": "secret"})

# 访问需要登录的页面——Cookie 自动带上
response = session.get("https://httpbin.org/cookies")
print(response.json())

# 手动设置 Cookie
cookies = {"token": "abc123", "user_id": "42"}
response = requests.get("https://httpbin.org/cookies", cookies=cookies)
print(response.json())
```

`requests.Session()` 是爬虫开发中的关键工具——它不仅自动管理 Cookie，还复用了底层的 TCP 连接池（对同一主机的多次请求共享连接），大幅提升性能。需要登录后才能访问的网站几乎都依赖 Session 来保持登录状态。

### 14.1.4 超时、重试与错误处理

网络请求是"不可靠的"——服务器可能宕机、网络可能中断、响应可能超时。健壮的爬虫必须处理这些异常：

```python
import requests
from requests.exceptions import (
    Timeout, ConnectionError, HTTPError, RequestException
)

url = "https://httpbin.org/delay/3"    # 这个 URL 会故意延迟 3 秒

try:
    # timeout=5：连接超时 + 读取超时合计不超过 5 秒
    response = requests.get(url, timeout=5)
    response.raise_for_status()         # 状态码不是 2xx 时抛出 HTTPError
    print(f"成功：{response.status_code}")
except Timeout:
    print("请求超时——服务器太慢了")
except ConnectionError:
    print("连接错误——检查网络或 URL 是否正确")
except HTTPError as e:
    print(f"HTTP 错误：{e}")
except RequestException as e:
    print(f"其他请求错误：{e}")

# 带重试的健壮请求
import time

def robust_get(url, max_retries=3, delay=1):
    """带重试的 GET 请求"""
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except (Timeout, ConnectionError) as e:
            if attempt == max_retries:
                raise    # 最后一次也失败，抛出异常
            print(f"第 {attempt} 次失败（{e}），{delay} 秒后重试...")
            time.sleep(delay)
            delay *= 2   # 指数退避——每次等待时间翻倍
```

### 14.1.5 响应内容的多种处理方式

```python
import requests

response = requests.get("https://httpbin.org/json")

# text —— 字符串形式
print(type(response.text))               # <class 'str'>
print(response.text[:50])

# content —— 字节形式（用于下载图片、文件等二进制数据）
print(type(response.content))             # <class 'bytes'>

# json() —— 自动解析 JSON（省去 json.loads() 这一步）
data = response.json()
print(type(data))                         # <class 'dict'>
print(data)

# 编码处理——确保中文不乱码
response = requests.get("https://www.baidu.com")
print(f"检测到的编码: {response.encoding}")     # ISO-8859-1（可能不准）
response.encoding = "utf-8"                     # 手动设置正确的编码
print(f"修复后: {response.text[:50]}")

# 下载文件——逐块写入，避免大文件撑爆内存
url = "https://httpbin.org/image/jpeg"
response = requests.get(url, stream=True)
with open("image.jpg", "wb") as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
print("图片下载完成")
```

### 14.1.6 实战练习

1. 编写一个函数 `check_website_status(urls)`，接收一个 URL 列表，依次用 requests 访问每个 URL，返回一个字典 `{url: status_code}`。对于超时（timeout=5 秒）或连接失败的 URL，状态码记录为 `None`。处理可能出现的所有异常，不让单个 URL 的失败影响其他 URL 的检查。

2. 使用 `requests.Session()` 模拟一个"登录-访问"的流程：先访问一个 POST 接口提交用户名和密码（使用 `https://httpbin.org/post` 模拟），然后使用同一个 Session 访问一个"需要登录"的页面（`https://httpbin.org/cookies`），验证 Cookie 是否被自动携带。

3. 编写一个图片批量下载工具：给定一个包含 10 个图片 URL 的列表，使用 `stream=True` 逐块下载每张图片，以 URL 的 MD5 哈希值命名保存。显示每张图片的下载进度（文件大小）。