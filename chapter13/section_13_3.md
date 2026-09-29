## 13.3 模板渲染——HTML 的动态生成引擎

在 13.1 节中，我们直接把 HTML 字符串写在 Python 代码里——这在演示时没问题，但对于一个真实的网站来说是不可接受的。模板引擎解决了"Python 逻辑"和"HTML 表现"的分离问题：你在 HTML 文件中写结构和样式，用特殊的占位符标记动态内容的位置，Flask 在运行时把这些占位符替换成实际数据。

Flask 内置的 **Jinja2** 模板引擎功能强大且学习曲线平缓——如果你了解 Python 的语法，Jinja2 就像一个"被限制在 HTML 中的 Python 子集"。

### 13.3.1 第一个模板——变量插值

模板文件必须放在项目根目录的 `templates/` 文件夹中：

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{{ title }} - 我的网站</title>
</head>
<body>
    <h1>{{ heading }}</h1>
    <p>当前时间：{{ current_time }}</p>
    <p>欢迎你，{{ user.name }}！你的等级是 {{ user.level }}</p>
</body>
</html>
```

在视图函数中渲染模板：

```python
from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template(
        "index.html",
        title="首页",
        heading="欢迎来到我的博客",
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M"),
        user={"name": "Alice", "level": "VIP会员"},
    )

if __name__ == "__main__":
    app.run(debug=True)
```

`render_template()` 的第一步参数是模板文件名，后面的命名参数会作为变量传递给模板。Jinja2 使用 `{{ 变量名 }}` 语法来插值——变量名和 Python 变量名规则一致，支持 `.` 访问属性（如 `user.name`）和 `[]` 索引（如 `user["level"]`）。

### 13.3.2 控制结构——条件判断与循环

Jinja2 支持 `{% %}` 语法包裹控制结构（if / for / block / extends 等）：

```html
<!-- templates/products.html -->
<!DOCTYPE html>
<html>
<body>
    <h1>{{ title }}</h1>

    {% if products %}
        <table border="1">
            <tr><th>名称</th><th>价格</th><th>状态</th></tr>
            {% for p in products %}
            <tr>
                <td>{{ p.name }}</td>
                <td>¥{{ "%.2f" | format(p.price) }}</td>
                <td>
                    {% if p.stock > 10 %}
                        <span style="color:green">充足</span>
                    {% elif p.stock > 0 %}
                        <span style="color:orange">紧张</span>
                    {% else %}
                        <span style="color:red">售罄</span>
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
        </table>
    {% else %}
        <p>暂无商品。</p>
    {% endif %}

    <p>共 {{ products | length }} 件商品</p>
</body>
</html>
```

视图函数：

```python
@app.route("/products")
def products():
    product_list = [
        {"name": "Python教程", "price": 59.9, "stock": 50},
        {"name": "机械键盘", "price": 299.0, "stock": 3},
        {"name": "无线鼠标", "price": 129.0, "stock": 0},
        {"name": "显示器支架", "price": 199.0, "stock": 15},
    ]
    return render_template("products.html", title="商品列表", products=product_list)
```

### 13.3.3 过滤器——数据格式化

过滤器（Filter）在变量后面用 `|` 管道符调用，类似于 Unix 管道——数据从左流到右，经过一层层转换：

```html
<!-- 常用过滤器 -->
<p>{{ name | upper }}</p>                    <!-- 大写：ALICE -->
<p>{{ name | capitalize }}</p>               <!-- 首字母大写：Alice -->
<p>{{ price | round(1) }}</p>                <!-- 保留一位小数 -->
<p>{{ "%.2f" | format(price) }}</p>          <!-- 格式化：59.90 -->
<p>{{ items | first }}</p>                   <!-- 列表第一项 -->
<p>{{ items | last }}</p>                    <!-- 列表最后一项 -->
<p>{{ items | length }}</p>                  <!-- 列表长度 -->
<p>{{ items | join(", ") }}</p>              <!-- 用逗号连接 -->
<p>{{ "<script>" | escape }}</p>             <!-- 转义HTML：&lt;script&gt; -->
<p>{{ text | truncate(20) }}</p>             <!-- 截断到20个字符 -->
<p>{{ "你好" | safe }}</p>                    <!-- 不转义（慎用！） -->

<!-- 默认值——变量不存在或为空时使用 -->
<p>{{ bio | default("这个人很懒，什么都没写") }}</p>

<!-- 自定义过滤器 -->
<!-- 在 Python 中注册 -->
@app.template_filter("stars")
def format_stars(rating):
    """将评分转为星星"""
    full = int(rating)
    return "★" * full + "☆" * (5 - full)
```

---

\begin{warningbox}
**`| safe` 过滤器的安全风险**

`| safe` 告诉 Jinja2"不要转义这段 HTML"。这在你确实需要渲染 HTML（比如文章正文包含的格式标签）时有用，但如果内容是用户提交的（评论、留言），使用 `| safe` 就会导致**XSS（跨站脚本攻击）**——恶意用户可以在评论中嵌入 `<script>` 标签来窃取其他用户的信息。除非你确知数据来源是安全的，否则不要使用 `| safe`。
\end{warningbox}

---

### 13.3.4 模板继承——DRY 原则的模板实现

一个真实的网站中，所有页面共享相同的页头、导航栏、页脚。模板继承让你把这些公共部分定义在一个"基模板"（base template）中，然后在子模板中只写不同的内容：

```html
<!-- templates/base.html —— 基模板 -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}我的网站{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <header>
        <h1>我的网站</h1>
        <nav>
            <a href="{{ url_for('index') }}">首页</a>
            <a href="{{ url_for('blog') }}">博客</a>
            <a href="{{ url_for('about') }}">关于</a>
        </nav>
    </header>

    <main>
        {% block content %}
        <!-- 子模板的内容会插在这里 -->
        {% endblock %}
    </main>

    <footer>
        <p>&copy; 2024 我的网站. All rights reserved.</p>
    </footer>
</body>
</html>
```

```html
<!-- templates/index.html —— 首页（继承 base.html） -->
{% extends "base.html" %}

{% block title %}首页 - 我的网站{% endblock %}

{% block content %}
    <h2>欢迎来到我的网站！</h2>
    <p>这里是最新内容...</p>
{% endblock %}
```

```html
<!-- templates/blog.html —— 博客页（继承 base.html） -->
{% extends "base.html" %}

{% block title %}博客 - 我的网站{% endblock %}

{% block content %}
    <h2>最新文章</h2>
    {% for post in posts %}
        <article>
            <h3>{{ post.title }}</h3>
            <p>{{ post.summary }}</p>
        </article>
    {% endfor %}
{% endblock %}
```

`{% block %}` 定义了可以被子模板填充的"槽位"，`{% extends %}` 声明继承关系。子模板中的 `{% block %}` 会覆盖基模板的同名块，未覆盖的块保持基模板的默认内容。这种机制让每个页面只包含自己独特的部分，公共部分集中管理——修改基模板的导航栏，所有页面同步更新。

### 13.3.5 实战练习

1. 创建一个"书籍展示"页面：用 Flask + Jinja2 模板渲染一个书籍列表，每本书包含"书名、作者、价格、评分（1-5星）"。使用过滤器将评分转换为星星符号（★☆），价格保留两位小数。如果书籍评分 ≥ 4 星，用绿色高亮。

2. 使用模板继承搭建一个多页面网站：基模板包含"页头（网站名+导航栏）+ 页脚（版权信息）"，创建至少 3 个子页面（首页、关于、联系），每个页面继承基模板并填充自己的内容。

3. 实现一个"用户登录模拟"页面：如果 URL 参数中有 `?username=xxx`，在页面上显示"欢迎回来，xxx！"，并显示一个"退出"链接；如果没有，显示登录表单。用 Jinja2 的 `{% if %}` 判断实现，不依赖 JavaScript。