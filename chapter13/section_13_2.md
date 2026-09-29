## 13.2 路由与视图函数——URL 的"调度中心"

路由是 Flask 应用的"交通指挥"——它决定了哪个 URL 由哪个函数处理。在 Web 开发中，一个好的 URL 设计不仅让代码结构清晰，也让用户和搜索引擎更容易理解你的网站。本节将深入路由的高级用法：动态 URL、URL 转换器、重定向、自定义错误处理以及在模板中生成 URL。

### 13.2.1 动态路由——URL 中的变量

在 13.1 节中我们看到了 `<name>` 这种动态路由的简单用法。Flask 支持更精细的变量规则：

```python
from flask import Flask

app = Flask(__name__)

@app.route("/post/<int:post_id>")
def show_post(post_id):
    """显示指定 ID 的文章——post_id 自动转为 int 类型"""
    return f"<h1>文章 #{post_id}</h1>"

@app.route("/user/<username>")
def user_profile(username):
    """默认是 string 类型（不接受斜杠）"""
    return f"<h1>{username} 的个人主页</h1>"

@app.route("/file/<path:filepath>")
def serve_file(filepath):
    """path 类型接受斜杠——如 /file/docs/manual.pdf"""
    return f"<p>请求文件：{filepath}</p>"

@app.route("/price/<float:amount>")
def show_price(amount):
    return f"<p>价格：¥{amount:.2f}</p>"

@app.route("/uuid/<uuid:uid>")
def show_uuid(uid):
    return f"<p>UUID: {uid}</p>"
```

Flask 内置的变量转换器：

| 转换器 | 匹配规则 | 示例 URL |
|:-------|:---------|:---------|
| `string` | 不含斜杠的文本（默认） | `/user/alice` |
| `int` | 整数 | `/post/42` |
| `float` | 浮点数 | `/price/29.9` |
| `path` | 含斜杠的路径 | `/file/docs/report.pdf` |
| `uuid` | UUID 格式的字符串 | `/uuid/550e8400-e29b-41d4-a716-446655440000` |

### 13.2.2 `url_for()`——生成 URL 的"正确姿势"

在视图函数中硬编码 URL（如 `"/user/alice"`）是糟糕的做法——一旦路由改变，所有的硬编码都要逐一修改。`url_for()` 函数用"端点名"（endpoint）动态生成 URL，让 URL 和代码解耦：

```python
from flask import Flask, url_for, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>首页</h1>"

@app.route("/about")
def about():
    return "<h1>关于我们</h1>"

@app.route("/user/<username>")
def profile(username):
    return f"<h1>{username} 的主页</h1>"

@app.route("/links")
def show_links():
    """演示 url_for 的用法"""
    links = f"""
        <ul>
            <li><a href="{url_for('index')}">首页</a></li>
            <li><a href="{url_for('about')}">关于</a></li>
            <li><a href="{url_for('profile', username='alice')}">Alice 的主页</a></li>
            <li><a href="{url_for('static', filename='style.css')}">CSS 文件</a></li>
        </ul>
    """
    return links

@app.route("/old-about")
def old_about():
    """旧版 URL——重定向到新版"""
    return redirect(url_for("about"))
```

`url_for()` 的优势：
1. 路由改变时，只要函数名不变，URL 自动更新
2. 自动处理 `SCRIPT_NAME`（当应用部署在子路径时）
3. 支持 `url_for('static', filename='...')` 生成静态文件 URL
4. 自动转义特殊字符，更安全

### 13.2.3 重定向与`abort`——控制请求流向

Flask 提供了两个用于改变请求流程的函数：

```python
from flask import Flask, redirect, url_for, abort

app = Flask(__name__)

@app.route("/admin")
def admin_panel():
    """需要登录才能访问的管理后台"""
    # 模拟未登录状态
    logged_in = False
    if not logged_in:
        return redirect(url_for("login", next="/admin"))
    return "<h1>管理后台</h1>"

@app.route("/login")
def login():
    return "<h1>登录页面</h1>"

@app.route("/secret/<int:id>")
def secret(id):
    """只允许访问 id 小于 100 的秘密"""
    if id >= 100:
        abort(403)                      # 返回 403 Forbidden
    return f"<h1>秘密 #{id}</h1>"

@app.errorhandler(403)
def forbidden(error):
    return "<h1>403 - 你没有权限访问这个资源</h1>", 403
```

`redirect()` —— 发送 302 状态码（临时重定向），浏览器会自动跳转到新 URL。
`abort(code)` —— 立即终止当前请求并返回指定的 HTTP 状态码。Flask 会查找对应的 `errorhandler` 来渲染错误页面。

### 13.2.4 请求钩子——在请求前后插入逻辑

有时你需要在每个请求的处理"之前"或"之后"执行一些通用逻辑——比如检查用户是否登录、记录请求日志、设置响应头：

```python
from flask import Flask, request, g
import time

app = Flask(__name__)

@app.before_request
def before_each_request():
    """在每个请求处理之前执行"""
    g.start_time = time.time()          # 记录开始时间
    print(f"[请求开始] {request.method} {request.path}")

@app.after_request
def after_each_request(response):
    """在每个请求处理之后执行（即使视图函数抛出异常也会执行）"""
    elapsed = time.time() - g.start_time
    print(f"[请求完成] {request.path} 耗时 {elapsed:.4f}s")
    response.headers["X-Process-Time"] = str(elapsed)
    return response

@app.route("/")
def index():
    return "<h1>首页</h1>"

@app.route("/slow")
def slow():
    time.sleep(1.5)                     # 模拟慢请求
    return "<h1>慢页面</h1>"
```

四个常用的请求钩子：

| 钩子 | 执行时机 |
|:-----|:---------|
| `before_request` | 每个请求处理前 |
| `after_request` | 每个请求处理后（需接收和返回 response 对象） |
| `teardown_request` | 响应发送后（即使中途抛异常也会执行） |
| `before_first_request` | 第一个请求到达前（仅执行一次，适合初始化） |

### 13.2.5 实战练习

1. 创建一个"博客文章"路由系统，支持以下 URL 模式：
   - `/blog/` —— 显示所有文章的列表（标题 + 摘要）
   - `/blog/<int:year>/` —— 显示某一年的文章列表
   - `/blog/<int:year>/<int:month>/` —— 显示某年某月的文章列表
   - 使用 `url_for()` 在页面之间生成导航链接

2. 创建一个"商品详情"页面：`/product/<int:product_id>`。如果 `product_id` 不在有效范围内（如不存在该商品），使用 `abort(404)` 返回 404 错误页面。

3. 实现请求日志记录：使用 `before_request` 和 `after_request` 钩子，在每个请求前后打印 `[时间] 方法 路径` 和响应状态码。将耗时超过 1 秒的请求标记为 `[SLOW]`。