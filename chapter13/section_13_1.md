## 13.1 Flask 框架基础——用 10 行代码启动一个网站

前面章节的代码都在命令行中运行——输入、处理、输出。Web 开发将这一切带到了浏览器中：用户在网页上点击按钮，服务器接收到请求，处理后返回结果。Python 的 Web 框架生态极其丰富——Django（大而全）、Flask（微框架）、FastAPI（高性能异步）各有所长。本书选择 **Flask** 入门，因为它的核心理念是"微而不弱"：核心代码极其精简，但通过丰富的扩展生态，你可以逐步添加数据库、表单验证、用户认证等功能。

### 13.1.1 安装与第一个 Flask 应用

```python
# 安装
# pip install flask

from flask import Flask

app = Flask(__name__)         # 创建 Flask 应用实例

@app.route("/")               # 装饰器：将 URL "/" 绑定到这个函数
def home():
    return "<h1>Hello, Flask!</h1><p>欢迎来到我的第一个网站</p>"

if __name__ == "__main__":
    app.run(debug=True)       # debug=True 开启调试模式（代码修改后自动重启）
```

将以上代码保存为 `app.py`，在终端运行 `python app.py`，你会看到：

```text
 * Running on http://127.0.0.1:5000
```

打开浏览器访问 `http://127.0.0.1:5000`，你就会看到自己写的网页。`debug=True` 的好处是：修改代码保存后 Flask 会自动重启，无需手动干预——对于初学者来说这个开关应该始终打开。

### 13.1.2 Flask 的核心概念

Flask 的设计围绕着几个核心概念，理解它们你就能看懂绝大多数的 Flask 代码：

**应用实例** —— `app = Flask(__name__)` 创建了 WSGI（Web Server Gateway Interface）应用对象。`__name__` 让 Flask 知道从哪里加载静态文件和模板。

**路由（Route）** —— 把 URL 路径映射到 Python 函数。`@app.route("/")` 是一种装饰器语法（回顾 10.3 节），实质上是调用 `app.add_url_rule()` 注册 URL 规则。

**视图函数（View Function）** —— 被路由装饰的函数。它处理请求并返回响应（HTML 字符串、JSON、文件等）。

**请求-响应循环** —— 每次浏览器发送一个 HTTP 请求，Flask 就会调用匹配的视图函数，然后把返回值打包成 HTTP 响应发回浏览器。这就是 Web 应用的工作原理。

### 13.1.3 处理 HTTP 方法与请求数据

HTTP 方法定义了客户端对资源的操作意图：`GET`（读取）、`POST`（提交数据）。Flask 默认只响应 `GET` 请求，通过 `methods` 参数可以指定其他方法：

```python
from flask import Flask, request

app = Flask(__name__)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # 在实际项目中，这里应该验证用户凭据
        return f"<h2>欢迎回来，{username}！</h2>"
    else:
        # GET 请求——显示登录表单
        return '''
            <form method="post">
                <input name="username" placeholder="用户名"><br>
                <input name="password" type="password" placeholder="密码"><br>
                <button type="submit">登录</button>
            </form>
        '''

if __name__ == "__main__":
    app.run(debug=True)
```

`request` 对象包含了本次请求的所有信息：
- `request.method` —— HTTP 方法（`GET`、`POST`……）
- `request.form` —— POST 表单数据（字典形式）
- `request.args` —— URL 查询参数（`?key=value` 部分）
- `request.json` —— JSON 请求体（用于 API）

```python
@app.route("/search")
def search():
    keyword = request.args.get("q", default="")
    page = request.args.get("page", default=1, type=int)
    return f"<p>搜索关键词：{keyword}，当前第 {page} 页</p>"

# 访问 http://127.0.0.1:5000/search?q=python&page=2
# 输出：搜索关键词：python，当前第 2 页
```

### 13.1.4 返回 JSON——构建 API 接口

现代 Web 应用中，服务器不一定要返回 HTML 页面——返回 JSON 数据的 API 更为常见，供前端 JavaScript 或移动端 APP 消费：

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/products")
def get_products():
    products = [
        {"id": 1, "name": "Python教程", "price": 59.9},
        {"id": 2, "name": "机械键盘", "price": 299.0},
        {"id": 3, "name": "无线鼠标", "price": 129.0},
    ]
    return jsonify(products)      # 自动设置 Content-Type: application/json

# 访问 http://127.0.0.1:5000/api/products
# 返回：[{"id":1,"name":"Python教程","price":59.9},...]
```

`jsonify()` 不仅将 Python 对象转为 JSON，还会自动设置正确的 `Content-Type` 响应头——这是 API 开发中的标准做法。

### 13.1.5 错误处理与状态码

HTTP 状态码告诉客户端请求的结果：200 成功、404 没找到、500 服务器错误……Flask 可以自定义这些错误页面：

```python
from flask import Flask

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return "<h1>404 - 页面不存在</h1><p>你访问的页面可能已经被删除。</p>", 404

@app.errorhandler(500)
def server_error(error):
    return "<h1>500 - 服务器开小差了</h1><p>请稍后重试。</p>", 500

@app.route("/greet/<name>")
def greet(name):
    if name.lower() == "admin":
        return "<h1>禁止访问</h1>", 403
    return f"<h1>你好，{name}！</h1>"
```

### 13.1.6 静态文件——CSS、JavaScript、图片

把 HTML 代码直接写在视图函数的字符串里很丑、很难维护。Flask 把模板和静态文件分开处理：
- **模板**（HTML 文件）放在 `templates/` 目录中
- **静态文件**（CSS、JS、图片）放在 `static/` 目录中

Flask 自动为 `static/` 目录中的文件提供 URL 路由：

```python
# 假设项目结构为：
# project/
#   app.py
#   static/
#     style.css
#     logo.png

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return '''
        <html>
        <head>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
            <h1>欢迎</h1>
            <img src="/static/logo.png" alt="Logo">
        </body>
        </html>
    '''
```

更推荐的方式是使用 `url_for()` 函数来生成 URL——它自动处理路径前缀，即使应用部署在子路径下也不会出错（下一节会详细介绍）。

### 13.1.7 项目结构建议

随着应用增长，把所有代码放在 `app.py` 中会变得难以维护。以下是 Flask 推荐的渐进式结构：

```text
小型项目（< 10 个路由）：
  project/
    app.py                # 所有代码
    templates/            # HTML 模板
    static/               # CSS/JS/图片

中型项目（10-50 个路由）：
  project/
    app.py                # 应用工厂
    views.py              # 视图函数
    models.py             # 数据模型
    templates/
    static/

大型项目（使用 Blueprint 模块化）：
  project/
    app.py                # 应用工厂
    auth/                 # 认证模块（独立蓝图）
    blog/                 # 博客模块
    templates/
    static/
```

### 13.1.8 实战练习

1. 创建一个 Flask 应用，实现一个简单的"温度转换 API"：访问 `/c2f?celsius=30` 返回 JSON `{"celsius": 30, "fahrenheit": 86.0}`；访问 `/f2c?fahrenheit=86` 返回 JSON `{"fahrenheit": 86, "celsius": 30.0}`。

2. 创建一个"用户列表"页面——用 Python 列表存储 5 个用户的姓名和年龄，访问 `/users` 时返回一个 HTML 表格显示所有用户。当访问 `/users/<name>` 时（如 `/users/张三`），返回该用户的详细信息。

3. 在 Flask 应用中添加一个自定义 404 页面和一个自定义 500 页面，使用 HTML 编写而不是纯文本。确保两个页面的风格一致（可以共用同一个 CSS 文件）。