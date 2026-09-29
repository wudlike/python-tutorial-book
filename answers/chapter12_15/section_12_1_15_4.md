## 12.1 NumPy 数组操作

### 练习1：5×5 随机矩阵分析

**答案：**

```python
import numpy as np

np.random.seed(42)
matrix = np.random.randint(10, 101, (5, 5))
print("原始矩阵：")
print(matrix)

row_means = matrix.mean(axis=1)
col_maxes = matrix.max(axis=0)

print(f"\n每行平均值：{row_means}")
print(f"每列最大值：{col_maxes}")
```

---

### 练习2：平方和性能对比

**答案：**

```python
import numpy as np
import time

n = 10_000_000

# Python 循环
start = time.perf_counter()
py_sum = sum(x ** 2 for x in range(1, n + 1))
py_time = time.perf_counter() - start
print(f"Python 循环: {py_time:.3f}s")

# NumPy 向量化
start = time.perf_counter()
arr = np.arange(1, n + 1)
np_sum = np.sum(arr ** 2)
np_time = time.perf_counter() - start
print(f"NumPy:       {np_time:.3f}s")
print(f"NumPy 快 {py_time / np_time:.1f} 倍")
print(f"结果一致: {py_sum == np_sum}")
```

---

### 练习3：学生成绩处理

**答案：**

```python
import numpy as np

scores = np.array([78, 45, 92, 88, 55, 67, 95, 40, 73, 84])

passed = scores[scores >= 60]
print(f"及格人数: {len(passed)}, 比例: {len(passed) / len(scores) * 100:.1f}%")

adjusted = np.where(scores < 60, 60, scores)
print(f"调整后成绩: {adjusted}")
print(f"调整后平均分: {adjusted.mean():.1f}")
```


## 12.2 Pandas 数据处理

### 练习1：销售数据分析

**答案：**

```python
import pandas as pd
import numpy as np

np.random.seed(42)
dates = pd.date_range("2024-01-01", periods=24, freq="W")
df = pd.DataFrame({
    "日期": dates,
    "产品": np.random.choice(["手机", "笔记本", "平板", "耳机"], 24),
    "销量": np.random.randint(1, 10, 24),
    "单价": np.random.choice([299, 1299, 3999, 5999], 24),
})
df["销售额"] = df["销量"] * df["单价"]

# 按产品汇总
product_sales = df.groupby("产品")["销售额"].sum().sort_values(ascending=False)
print("各产品总销售额：")
print(product_sales)

print(f"\n销售额 TOP3 产品：{product_sales.head(3).index.tolist()}")

# 按日期汇总
daily = df.groupby("日期")["销售额"].sum()
print(f"\n每日总销售额（前5天）：\n{daily.head()}")
```

---

### 练习2：缺失值处理

**答案：**

```python
import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五", "赵六", "钱七", "孙八"],
    "年龄": [25, np.nan, 28, np.nan, 22, 30],
    "薪资": [15000, 20000, np.nan, 18000, np.nan, 22000],
    "部门": ["研发", "市场", np.nan, "研发", "市场", np.nan],
})

print("缺失值统计：")
print(df.isnull().sum())

# 填充
df_filled = df.copy()
df_filled["年龄"] = df_filled["年龄"].fillna(df_filled["年龄"].mean())
df_filled["薪资"] = df_filled["薪资"].fillna(df_filled["薪资"].mean())
df_filled["部门"] = df_filled["部门"].fillna(df_filled["部门"].mode()[0])

print(f"\n填充后缺失值：\n{df_filled.isnull().sum().sum()}")    # 0
print(df_filled)
```

---

### 练习3：学生与班级合并

**答案：**

```python
import pandas as pd

students = pd.DataFrame({
    "学号": [1, 2, 3, 4, 5],
    "姓名": ["张三", "李四", "王五", "赵六", "钱七"],
    "班级ID": [101, 102, 101, 103, 102],
})

classes = pd.DataFrame({
    "班级ID": [101, 102, 103],
    "班级名": ["计算机1班", "计算机2班", "软件工程1班"],
    "班主任": ["王老师", "李老师", "张老师"],
})

merged = pd.merge(students, classes, on="班级ID", how="left")
print(merged[["学号", "姓名", "班级名", "班主任"]])
```


## 12.3 Matplotlib 数据可视化

### 练习1：收入图表

**答案：**

```python
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

years = [2019, 2020, 2021, 2022, 2023]
revenue = [120, 135, 168, 192, 220]

quarters = ["Q1", "Q2", "Q3", "Q4"]
q_data = {
    2019: [25, 30, 35, 30],
    2020: [30, 28, 38, 39],
    2021: [35, 42, 45, 46],
    2022: [45, 48, 50, 49],
    2023: [50, 55, 58, 57],
}

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

ax1.plot(years, revenue, marker="o", color="#2196F3", linewidth=2.5, markersize=8)
ax1.set_title("年度收入趋势（万元）", fontweight="bold")
ax1.set_ylabel("万元")
ax1.grid(True, alpha=0.3)

bottom = np.zeros(5)
colors = ["#2196F3", "#4CAF50", "#FF9800", "#F44336"]
for i, q in enumerate(quarters):
    values = [q_data[y][i] for y in years]
    ax2.bar(years, values, bottom=bottom, label=q, color=colors[i])
    bottom += values
ax2.set_title("各季度收入分布（万元）", fontweight="bold")
ax2.legend()
ax2.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.show()
```

---

### 练习2：正态分布直方图

**答案：**

```python
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

data = np.random.randn(5000)

plt.figure(figsize=(10, 6))
plt.hist(data, bins=50, color="steelblue", edgecolor="white", alpha=0.8)

mean = data.mean()
std = data.std()
plt.axvline(mean, color="red", linestyle="--", linewidth=2, label=f"均值={mean:.2f}")
plt.axvline(mean + std, color="orange", linestyle=":", linewidth=2, label=f"+1σ={mean+std:.2f}")
plt.axvline(mean - std, color="orange", linestyle=":", linewidth=2, label=f"-1σ={mean-std:.2f}")

plt.title("标准正态分布直方图（n=5000）", fontweight="bold")
plt.xlabel("值")
plt.ylabel("频次")
plt.legend()
plt.show()
```

---

### 练习3：散点图

**答案：**

```python
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

np.random.seed(42)
df = pd.DataFrame({
    "城市": ["北京", "上海", "广州", "深圳", "杭州", "成都", "武汉", "南京"],
    "人口": [2154, 2487, 1530, 1756, 1220, 2093, 1121, 931],
    "GDP":  [3610, 3870, 2500, 2760, 1811, 1992, 1562, 1481],
})

plt.figure(figsize=(10, 6))
scatter = plt.scatter(
    df["人口"], df["GDP"],
    s=df["人口"] / 10,          # 点大小与人口成正比
    c=df["GDP"],                # 颜色与 GDP 成正比
    cmap="YlOrRd",
    edgecolors="black",
    linewidth=0.5,
    alpha=0.8,
)

for _, row in df.iterrows():
    plt.text(row["人口"] + 15, row["GDP"], row["城市"], fontsize=10)

plt.colorbar(scatter, label="GDP（亿元）")
plt.title("中国主要城市人口与 GDP 散点图", fontweight="bold")
plt.xlabel("人口（万人）")
plt.ylabel("GDP（亿元）")
plt.grid(True, alpha=0.3)
plt.show()
```


## 12.4 实战案例

### 练习1：额外分析

**答案：**

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 复用12.4节的数据生成逻辑（略，假设 df 已创建）

# 环比增长率
df["月份"] = df["日期"].dt.month
monthly_product = df.groupby(["产品", "月份"])["金额"].sum().unstack(fill_value=0)
print("各产品月度销售额：")
print(monthly_product)

growth = monthly_product.pct_change(axis=1) * 100
print(f"\n环比增长率（%）：\n{growth.round(1)}")

# 各地区客单价最高/最低产品
region_product = df.groupby(["地区", "产品"]).agg(
    订单数=("金额", "count"),
    总金额=("金额", "sum"),
).reset_index()
region_product["客单价"] = region_product["总金额"] / region_product["订单数"]

for region in region_product["地区"].unique():
    subset = region_product[region_product["地区"] == region]
    highest = subset.loc[subset["客单价"].idxmax()]
    lowest = subset.loc[subset["客单价"].idxmin()]
    print(f"\n{region}: 最高客单价 {highest['产品']} (¥{highest['客单价']:.0f}), "
          f"最低客单价 {lowest['产品']} (¥{lowest['客单价']:.0f})")

# 3×1 图
monthly_sales = df.groupby("月份")["金额"].sum()
monthly_product_stack = df.groupby(["月份", "产品"])["金额"].sum().unstack(fill_value=0)
monthly_region_stack = df.groupby(["月份", "地区"])["金额"].sum().unstack(fill_value=0)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 14))

ax1.plot(monthly_sales.index, monthly_sales.values / 10000, marker="o")
ax1.set_title("月度销量趋势（万元）")
ax1.grid(True, alpha=0.3)

monthly_product_stack.plot(kind="area", ax=ax2, alpha=0.7)
ax2.set_title("产品月度堆叠面积图")
ax2.set_ylabel("万元")

monthly_region_stack.plot(kind="area", ax=ax3, alpha=0.7)
ax3.set_title("地区月度堆叠面积图")
ax3.set_xlabel("月份")
ax3.set_ylabel("万元")

plt.tight_layout()
plt.show()
```


## 13.1 Flask 框架基础

### 练习1：温度转换 API

**答案：**

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/c2f")
def c2f():
    celsius = request.args.get("celsius", type=float)
    if celsius is None:
        return jsonify({"error": "请提供 celsius 参数"}), 400
    fahrenheit = celsius * 9 / 5 + 32
    return jsonify({"celsius": celsius, "fahrenheit": round(fahrenheit, 1)})

@app.route("/f2c")
def f2c():
    fahrenheit = request.args.get("fahrenheit", type=float)
    if fahrenheit is None:
        return jsonify({"error": "请提供 fahrenheit 参数"}), 400
    celsius = (fahrenheit - 32) * 5 / 9
    return jsonify({"fahrenheit": fahrenheit, "celsius": round(celsius, 1)})
```

---

### 练习2：用户列表页

**答案：**

```python
from flask import Flask, abort

app = Flask(__name__)

users = [
    {"name": "张三", "age": 25, "city": "北京"},
    {"name": "李四", "age": 30, "city": "上海"},
    {"name": "王五", "age": 22, "city": "广州"},
    {"name": "赵六", "age": 28, "city": "深圳"},
    {"name": "钱七", "age": 35, "city": "杭州"},
]

@app.route("/users")
def user_list():
    table_rows = ""
    for u in users:
        table_rows += f"<tr><td>{u['name']}</td><td>{u['age']}</td><td>{u['city']}</td></tr>"
    return f"""
    <h1>用户列表</h1>
    <table border="1"><tr><th>姓名</th><th>年龄</th><th>城市</th></tr>
    {table_rows}</table>
    """

@app.route("/users/<name>")
def user_detail(name):
    for u in users:
        if u["name"] == name:
            return f"<h2>{u['name']}</h2><p>年龄: {u['age']}</p><p>城市: {u['city']}</p>"
    abort(404)
```

---

### 练习3：自定义错误页面

**答案：**

```python
from flask import Flask

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return """
    <html><head>
    <link rel="stylesheet" href="/static/style.css">
    </head><body>
    <div class="error-page">
        <h1>404 - 页面不存在</h1>
        <p>你访问的页面可能已经被删除或移动。</p>
        <a href="/">返回首页</a>
    </div>
    </body></html>
    """, 404

@app.errorhandler(500)
def server_error(error):
    return """
    <html><head>
    <link rel="stylesheet" href="/static/style.css">
    </head><body>
    <div class="error-page">
        <h1>500 - 服务器错误</h1>
        <p>服务器遇到了意外情况，请稍后重试。</p>
        <a href="/">返回首页</a>
    </div>
    </body></html>
    """, 500

@app.route("/")
def index():
    return "<h1>首页</h1>"
```


## 13.2 路由与视图函数

### 练习1：博客路由系统

**答案：**

```python
from flask import Flask, url_for

app = Flask(__name__)

posts = [
    {"title": "Python入门", "year": 2024, "month": 6},
    {"title": "Flask学习", "year": 2024, "month": 6},
    {"title": "Django对比", "year": 2024, "month": 5},
    {"title": "前端入门", "year": 2023, "month": 12},
]

@app.route("/blog/")
def blog_index():
    links = "<ul>"
    for p in posts:
        links += (f'<li><a href="{url_for("show_post", title=p["title"])}">'
                  f'{p["title"]}</a> ({p["year"]}-{p["month"]:02d})</li>')
    links += "</ul>"

    years = sorted(set(p["year"] for p in posts), reverse=True)
    years_links = " | ".join(
        f'<a href="{url_for("blog_year", year=y)}">{y}年</a>' for y in years
    )
    return f"<h1>所有文章</h1><nav>{years_links}</nav>{links}"

@app.route("/blog/<int:year>/")
def blog_year(year):
    year_posts = [p for p in posts if p["year"] == year]
    links = "<ul>"
    for p in year_posts:
        links += (f'<li>{p["month"]:02d}月 - <a href="'
                  f'{url_for("blog_year_month", year=year, month=p["month"])}">'
                  f'{p["title"]}</a></li>')
    links += "</ul>"
    return f"<h1>{year}年文章</h1>{links}"

@app.route("/blog/<int:year>/<int:month>/")
def blog_year_month(year, month):
    month_posts = [p for p in posts if p["year"] == year and p["month"] == month]
    return f"<h1>{year}年{month:02d}月</h1><ul>" + \
           "".join(f"<li>{p['title']}</li>" for p in month_posts) + "</ul>"
```

---

### 练习2：商品详情 + abort

**答案：**

```python
from flask import Flask, abort

app = Flask(__name__)

products = {1: "机械键盘", 2: "无线鼠标", 3: "显示器", 4: "耳机"}

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    if product_id not in products:
        abort(404)
    return f"<h1>{products[product_id]}</h1><p>商品 ID: {product_id}</p>"
```

---

### 练习3：请求日志

**答案：**

```python
from flask import Flask, request, g
import time

app = Flask(__name__)

@app.before_request
def log_request():
    g.start_time = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] {request.method} {request.path}")

@app.after_request
def log_response(response):
    elapsed = time.time() - g.start_time
    tag = " [SLOW]" if elapsed > 1 else ""
    print(f"[{time.strftime('%H:%M:%S')}] {response.status_code} "
          f"{request.path} ({elapsed:.3f}s){tag}")
    return response

@app.route("/")
def index():
    return "OK"

@app.route("/slow")
def slow():
    time.sleep(1.5)
    return "slow"
```


## 13.3 模板渲染

### 练习1：书籍展示

**答案：**

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.template_filter("stars")
def stars_filter(rating):
    full = int(rating)
    return "★" * full + "☆" * (5 - full)

@app.route("/")
def books():
    book_list = [
        {"title": "Python入门", "author": "张三", "price": 59.9, "rating": 4.5},
        {"title": "Flask实战", "author": "李四", "price": 79.0, "rating": 3.5},
        {"title": "数据科学", "author": "王五", "price": 89.0, "rating": 5.0},
        {"title": "机器学习", "author": "赵六", "price": 99.0, "rating": 4.0},
    ]
    return render_template("books.html", books=book_list)
```

```html
<!-- templates/books.html -->
<!DOCTYPE html>
<html>
<body>
    <h1>书籍列表</h1>
    <table border="1">
        <tr><th>书名</th><th>作者</th><th>价格</th><th>评分</th></tr>
        {% for book in books %}
        <tr {% if book.rating >= 4 %}style="background:#e8f5e9"{% endif %}>
            <td>{{ book.title }}</td>
            <td>{{ book.author }}</td>
            <td>¥{{ "%.2f" | format(book.price) }}</td>
            <td>{{ book.rating | stars }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
```

---

### 练习2：模板继承多页面

**答案：**

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}我的网站{% endblock %}</title>
</head>
<body>
    <header>
        <h1>我的网站</h1>
        <nav>
            <a href="{{ url_for('home') }}">首页</a> |
            <a href="{{ url_for('about') }}">关于</a> |
            <a href="{{ url_for('contact') }}">联系</a>
        </nav>
    </header>
    <main>{% block content %}{% endblock %}</main>
    <footer><hr><p>© 2024 我的网站</p></footer>
</body>
</html>
```

```html
<!-- templates/index.html (home) -->
{% extends "base.html" %}
{% block title %}首页 - 我的网站{% endblock %}
{% block content %}<h2>欢迎来到我的网站</h2>{% endblock %}
```

```html
<!-- templates/about.html -->
{% extends "base.html" %}
{% block title %}关于我们{% endblock %}
{% block content %}<h2>关于我们</h2><p>我们是一个技术分享平台。</p>{% endblock %}
```

```html
<!-- templates/contact.html -->
{% extends "base.html" %}
{% block title %}联系我们{% endblock %}
{% block content %}<h2>联系我们</h2><p>邮箱：hello@example.com</p>{% endblock %}
```

---

### 练习3：登录模拟

**答案：**

```python
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def index():
    username = request.args.get("username")
    return render_template("login_demo.html", username=username)
```

```html
<!-- templates/login_demo.html -->
<!DOCTYPE html>
<html><body>
    {% if username %}
        <h1>欢迎回来，{{ username }}！</h1>
        <a href="/">退出</a>
    {% else %}
        <h1>请登录</h1>
        <form method="get">
            <input name="username" placeholder="用户名">
            <button type="submit">登录</button>
        </form>
    {% endif %}
</body></html>
```


## 13.4 简单博客系统

### 练习1：文章搜索

**答案：**

在 `app.py` 中添加搜索路由：

```python
@app.route("/search")
def search():
    keyword = request.args.get("q", "").strip()
    if not keyword:
        return redirect(url_for("index"))

    results = [p for p in posts
               if keyword.lower() in p["title"].lower()
               or keyword.lower() in p["tags"].lower()]

    return render_template("search.html", keyword=keyword, posts=results)
```

在 `index.html` 添加搜索框（放在 `<main>` 最上方）：

```html
<form action="{{ url_for('search') }}" method="get" style="margin-bottom:20px;">
    <input type="text" name="q" placeholder="搜索文章..." style="padding:6px; width:300px;">
    <button type="submit" class="btn btn-primary">搜索</button>
</form>
```

搜索结果页 `search.html` 可复用 `index.html` 的循环结构，在标题处显示 `搜索"{keyword}"的结果`。

---

### 练习2：归档页面

**答案：**

```python
from collections import defaultdict

@app.route("/archive")
def archive():
    archives = defaultdict(list)
    for post in posts:
        year_month = post["created_at"][:7]    # "2024-06"
        archives[year_month].append(post)

    sorted_archives = sorted(archives.items(), reverse=True)
    return render_template("archive.html", archives=sorted_archives)
```

```html
<!-- templates/archive.html -->
{% extends "base.html" %}
{% block title %}归档{% endblock %}
{% block content %}
<h2>文章归档</h2>
{% for ym, posts in archives %}
    <details>
        <summary>{{ ym }} ({{ posts|length }} 篇)</summary>
        <ul>
        {% for post in posts %}
            <li><a href="{{ url_for('show_post', post_id=post.id) }}">{{ post.title }}</a></li>
        {% endfor %}
        </ul>
    </details>
{% endfor %}
{% endblock %}
```

---

### 练习3：访问计数

**答案：**

为每篇文章增加 `views` 字段（初始化时为 0），在 `show_post()` 中递增：

```python
# 初始化时添加 views
posts = [
    {"id": 1, "title": "...", "content": "...", "tags": "...",
     "created_at": "...", "views": 0},
]

@app.route("/post/<int:post_id>")
def show_post(post_id):
    post = find_post(post_id)
    if post is None:
        abort(404)
    post["views"] += 1    # 每次访问 +1
    return render_template("post.html", post=post)
```

在 `post.html` 中显示：

```html
<p class="meta">👁️ 已被阅读 {{ post.views }} 次</p>
```


## 14.1 requests 库使用

### 练习1：网站状态检查

**答案：**

```python
import requests
from requests.exceptions import RequestException

def check_website_status(urls):
    results = {}
    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            results[url] = response.status_code
        except RequestException:
            results[url] = None
    return results

urls = [
    "https://httpbin.org/get",
    "https://httpbin.org/status/404",
    "https://invalid.domain.xyz",
]
statuses = check_website_status(urls)
for url, code in statuses.items():
    print(f"{url}: {code}")
```

---

### 练习2：Session 模拟登录

**答案：**

```python
import requests

session = requests.Session()

login_url = "https://httpbin.org/post"
response = session.post(login_url, data={"username": "alice", "password": "secret"})
print("登录响应:", response.json()["form"])

cookie_url = "https://httpbin.org/cookies"
response = session.get(cookie_url)
print("Cookie:", response.json())
```

---

### 练习3：批量图片下载

**答案：**

```python
import requests
import hashlib
import os

def download_images(urls, save_dir="images"):
    os.makedirs(save_dir, exist_ok=True)

    for i, url in enumerate(urls, 1):
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            url_hash = hashlib.md5(url.encode()).hexdigest()
            ext = url.split(".")[-1].split("?")[0] or "jpg"
            filename = f"{url_hash}.{ext}"
            filepath = os.path.join(save_dir, filename)

            total_size = int(response.headers.get("content-length", 0))
            downloaded = 0

            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size:
                        pct = downloaded / total_size * 100
                        print(f"\r[{i}] {filename}: {pct:.0f}%", end="")

            print(f" ✅ ({downloaded} bytes)")
        except requests.RequestException as e:
            print(f"\r[{i}] ❌ {url}: {e}")
```


## 14.2 BeautifulSoup 解析 HTML

### 练习1：产品解析

**答案：**

```python
from bs4 import BeautifulSoup

html = """..."""  # 题目中的 HTML

soup = BeautifulSoup(html, "lxml")
products = []

for item in soup.select("div.product"):
    name = item.select_one("h3.name").text.strip()
    price = item.select_one("span.price").text.strip()
    rating = item.select_one("span.rating").text.strip()
    products.append({"name": name, "price": price, "rating": rating})

print(products)
```

---

### 练习2：链接提取

**答案：**

```python
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_links(html, base_url):
    soup = BeautifulSoup(html, "lxml")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith("javascript:") or href == "#":
            continue
        full_url = urljoin(base_url, href)
        links.append({"text": a.text.strip(), "url": full_url})
    return links
```

---

### 练习3：提取纯文本

**答案：**

```python
def extract_article_text(html):
    soup = BeautifulSoup(html, "lxml")
    article_div = soup.find("div", id="article-content")
    if not article_div:
        return ""
    text = article_div.get_text(separator="\n", strip=True)
    return text

# text = extract_article_text(html_doc)
# print(f"字数: {len(text)}")
```


## 14.3 数据存储

### 练习1：通用保存函数

**答案：**

```python
import csv, json, sqlite3, os

def save_data(data, format, filepath):
    if format == "csv":
        file_exists = os.path.exists(filepath)
        with open(filepath, "a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            if not file_exists:
                writer.writeheader()
            writer.writerows(data)

    elif format == "json":
        existing = []
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                existing = json.load(f)
        existing.extend(data)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)

    elif format == "sqlite":
        conn = sqlite3.connect(filepath)
        conn.execute("""CREATE TABLE IF NOT EXISTS articles
            (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, url TEXT UNIQUE)""")
        for item in data:
            conn.execute("INSERT OR IGNORE INTO articles (title, url) VALUES (?, ?)",
                        (item.get("title"), item.get("url")))
        conn.commit()
        conn.close()
```

---

### 练习2：爬虫数据库

**答案：**

```python
import sqlite3

conn = sqlite3.connect("crawler.db")
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT, url TEXT UNIQUE, author TEXT,
    published_date TEXT, content TEXT, views INTEGER
)""")

c.execute("""CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER, author TEXT, content TEXT, time TEXT,
    FOREIGN KEY(post_id) REFERENCES posts(id)
)""")

# 示例查询
rows = c.execute("""
    SELECT p.title, COUNT(c.id) as comment_count
    FROM posts p LEFT JOIN comments c ON p.id = c.post_id
    GROUP BY p.id
    ORDER BY comment_count DESC
""")
for row in rows.fetchall():
    print(f"{row[0]}: {row[1]} 条评论")

rows = c.execute("SELECT title, views FROM posts ORDER BY views DESC LIMIT 10")
for row in rows.fetchall():
    print(f"{row[0]}: {row[1]} 次阅读")

conn.close()
```

---

### 练习3：存储效率对比

**答案：**

```python
import csv, json, os, time

n = 100_000
data = [{"id": i, "name": f"item_{i}", "value": i * 1.5} for i in range(n)]

# CSV
start = time.perf_counter()
with open("test.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["id", "name", "value"])
    w.writeheader()
    w.writerows(data)
csv_time = time.perf_counter() - start
csv_size = os.path.getsize("test.csv")

# JSON
start = time.perf_counter()
with open("test.json", "w", encoding="utf-8") as f:
    json.dump(data, f)
json_time = time.perf_counter() - start
json_size = os.path.getsize("test.json")

print(f"CSV:  {csv_size / 1024:.1f} KB, {csv_time:.3f}s")
print(f"JSON: {json_size / 1024:.1f} KB, {json_time:.3f}s")
print(f"CSV 比 JSON 小 {json_size / csv_size:.1f} 倍")

# 原因：CSV 每行只有值+分隔符，JSON 每行都有键名重复
```


## 14.4 实战案例：爬取新闻

### 练习1：关键词过滤

**答案：**

```python
# 在 crawl_page() 中添加过滤
KEYWORDS = ["Python", "AI", "Flask"]

def crawl_page(url, conn):
    # ... 原有代码 ...
    for article in articles:
        title = title_tag.text.strip()
        summary = summary_tag.text.strip()

        # 关键词过滤
        if not any(kw.lower() in title.lower() or kw.lower() in summary.lower()
                   for kw in KEYWORDS):
            continue

        # ... 存入数据库 ...
```

---

### 练习2：爬取详情页

**答案：**

```python
def crawl_detail(article_url):
    """爬取单篇文章的详情页内容"""
    try:
        response = requests.get(article_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "lxml")
        content_div = soup.find("div", class_="article-content")
        return content_div.get_text(strip=True) if content_div else ""
    except Exception as e:
        print(f"  ⚠️ 详情页爬取失败: {e}")
        return ""

# 在 crawl_page() 中，存储基本信息后：
# content = crawl_detail(absolute_url)
# conn.execute("UPDATE news SET content = ? WHERE url = ?", (content, absolute_url))
```

---

### 练习3：定时爬取

**答案：**

```python
# pip install schedule

import schedule
import time
from datetime import datetime

def scheduled_crawl():
    print(f"[{datetime.now()}] 开始定时爬取...")
    # 调用 main() 或 crawl_page()
    # 发送邮件通知
    print("爬取完成")

schedule.every().day.at("09:00").do(scheduled_crawl)

print("定时爬虫已启动，等待执行...")
while True:
    schedule.run_pending()
    time.sleep(60)
```


## 15.1 文件批量处理

### 练习1：合并日志文件

**答案：**

```python
import os
from datetime import datetime

def merge_logs(directory, output="merged.log"):
    log_files = sorted(
        [f for f in os.listdir(directory) if f.endswith(".log")])

    with open(output, "w", encoding="utf-8") as out:
        for log_file in log_files:
            filepath = os.path.join(directory, log_file)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            out.write(f"\n=== {log_file} | 合并于 {timestamp} ===\n\n")

            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    out.write(f"[{log_file}] {line}")

    print(f"共合并 {len(log_files)} 个文件 → {output}")
```

---

### 练习2：重复文件查找器

**答案：**

```python
import os
import hashlib
from collections import defaultdict

def find_duplicates(directory):
    hash_to_files = defaultdict(list)

    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                with open(filepath, "rb") as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                hash_to_files[file_hash].append(filepath)
            except (IOError, PermissionError):
                pass

    duplicates = {h: files for h, files in hash_to_files.items() if len(files) > 1}
    total_wasted = 0

    for h, files in duplicates.items():
        size = os.path.getsize(files[0])
        wasted = size * (len(files) - 1)
        total_wasted += wasted
        print(f"\n重复组 ({len(files)} 个文件, 每个 {size} bytes):")
        for f in files:
            print(f"  {f}")
        print(f"  可释放: {wasted} bytes")

    print(f"\n总共可释放: {total_wasted / 1024:.1f} KB")
    return duplicates
```

---

### 练习3：pathlib 重写分类脚本

**答案：**

```python
from pathlib import Path
import shutil

CATEGORIES = {
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "文档": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".txt", ".md"],
    "压缩包": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "代码": [".py", ".js", ".html", ".css", ".java", ".json"],
}

def organize_with_pathlib(directory):
    dir_path = Path(directory)
    moved = 0

    for category in CATEGORIES:
        (dir_path / category).mkdir(exist_ok=True)

    for file in dir_path.iterdir():
        if file.is_dir():
            continue

        ext = file.suffix.lower()
        for category, extensions in CATEGORIES.items():
            if ext in extensions:
                dest = dir_path / category / file.name
                shutil.move(str(file), str(dest))
                print(f"  📁 {category}/ ← {file.name}")
                moved += 1
                break

    print(f"完成！移动了 {moved} 个文件")
```


## 15.2 邮件自动发送

### 练习1：异常监控通知

**答案：**

```python
import sys
import traceback
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

def notify_admin_on_exception(smtp_config, admin_email):
    """装饰器/上下文管理器——发生异常时自动发邮件通知"""
    exc_type, exc_value, exc_tb = sys.exc_info()
    if exc_type is None:
        return

    tb_lines = traceback.format_exception(exc_type, exc_value, exc_tb)
    body = (
        f"异常时间: {datetime.now()}\n"
        f"异常类型: {exc_type.__name__}\n"
        f"异常信息: {exc_value}\n\n"
        f"Traceback:\n{''.join(tb_lines)}"
    )

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = f"🚨 程序异常: {exc_type.__name__}"
    msg["From"] = smtp_config["sender"]
    msg["To"] = admin_email

    with smtplib.SMTP(smtp_config["server"], smtp_config["port"], timeout=10) as s:
        s.starttls()
        s.login(smtp_config["sender"], smtp_config["password"])
        s.sendmail(smtp_config["sender"], [admin_email], msg.as_string())
        print("异常通知邮件已发送")
```

---

### 练习2：定时发送日报

**答案：**

```python
import schedule
import time
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_daily_report(smtp_config, receiver, report_html):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"📊 日报 - {datetime.now().strftime('%Y-%m-%d')}"
    msg["From"] = smtp_config["sender"]
    msg["To"] = receiver
    msg.attach(MIMEText("请使用 HTML 客户端查看", "plain", "utf-8"))
    msg.attach(MIMEText(report_html, "html", "utf-8"))

    with smtplib.SMTP(smtp_config["server"], smtp_config["port"], timeout=10) as s:
        s.starttls()
        s.login(smtp_config["sender"], smtp_config["password"])
        s.sendmail(smtp_config["sender"], [receiver], msg.as_string())
    print(f"[{datetime.now()}] 日报已发送")

schedule.every().day.at("17:30").do(
    send_daily_report, smtp_config, "admin@example.com", "<h1>今日数据</h1>"
)
```

---

### 练习3：退订 + 限流

**答案：**

```python
import time

unsubscribed = set()
sent_count = 0
hour_start = time.time()

def load_unsubscribed(filepath="unsubscribed.txt"):
    if Path(filepath).exists():
        return set(Path(filepath).read_text().splitlines())
    return set()

def save_unsubscribed(email, filepath="unsubscribed.txt"):
    with open(filepath, "a") as f:
        f.write(email + "\n")

def send_one(server, sender, email, name, body, unsub_link):
    global sent_count, hour_start
    if time.time() - hour_start > 3600:
        sent_count = 0
        hour_start = time.time()
    if sent_count >= 50:
        print("⚠️ 达到每小时限制，暂停发送")
        return False

    body_with_unsub = body + f"\n\n不想收到此类邮件？点击退订: {unsub_link}/{email}"
    msg = MIMEText(body_with_unsub, "plain", "utf-8")
    msg["Subject"] = "..."
    msg["From"] = sender
    msg["To"] = email
    server.sendmail(sender, [email], msg.as_string())
    sent_count += 1
    return True
```


## 15.3 微信机器人基础

### 练习1：成语接龙

**答案：**

```python
# 基于模拟微信机器人框架

import json

# 加载成语库（模拟）
idioms = ["一心一意", "意气风发", "发愤图强", "强人所难", "难以置信"]
last_idiom = None

def process_message(text):
    global last_idiom
    text = text.strip()

    if text == "成语接龙":
        last_idiom = "一心一意"
        return f"🏮 成语接龙开始！\n机器人出：{last_idiom}\n请接以'意'字开头的成语"

    if last_idiom:
        if text[0] != last_idiom[-1]:
            return f"❌ 需要以'{last_idiom[-1]}'字开头，你的成语以'{text[0]}'开头"
        if text not in idioms:
            return "❌ 不在成语库中"

        # 机器人接龙——找一个以用户成语末字开头的
        prefix = text[-1]
        next_idiom = next((i for i in idioms if i[0] == prefix), None)
        if next_idiom:
            last_idiom = next_idiom
            return f"✅ 正确！\n机器人接：{next_idiom}\n请接以'{next_idiom[-1]}'字开头的成语"
        else:
            return "🎉 机器人接不上了，你赢了！"

    return f"收到：{text}"
```

---

### 练习2：关键词提醒

**答案：**

```python
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import re

reminders = []

def process_message(text, user_name):
    match = re.match(r"提醒\s+(\d{1,2}:\d{2})\s+(.+)", text)
    if match:
        time_str, content = match.groups()
        hour, minute = map(int, time_str.split(":"))
        reminders.append({"user": user_name, "content": content, "hour": hour, "minute": minute})
        return f"✅ 已设置提醒：{time_str} — {content}"
    return f"收到：{text}"

def check_reminders(send_func):
    now = datetime.now()
    for r in reminders[:]:
        if r["hour"] == now.hour and r["minute"] == now.minute:
            send_func(r["user"], f"⏰ 提醒：{r['content']}")
            reminders.remove(r)

scheduler = BackgroundScheduler()
scheduler.add_job(check_reminders, "interval", minutes=1, args=[send_func])
scheduler.start()
```

---

### 练习3：群消息归档

**答案：**

```python
import sqlite3
from datetime import datetime

conn = sqlite3.connect("chat_archive.db")
conn.execute("""CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_name TEXT, sender TEXT, content TEXT, time TEXT
)""")

def archive_message(room_name, sender, content):
    conn.execute(
        "INSERT INTO messages (room_name, sender, content, time) VALUES (?, ?, ?, ?)",
        (room_name, sender, content, datetime.now().isoformat())
    )
    conn.commit()

def search_messages(keyword, date=None):
    query = "SELECT * FROM messages WHERE content LIKE ?"
    params = [f"%{keyword}%"]
    if date:
        query += " AND time LIKE ?"
        params.append(f"{date}%")
    return conn.execute(query + " ORDER BY time DESC", params).fetchall()
```


## 15.4 系统监控脚本

### 练习1：网络流量异常检测

**答案：**

```python
import psutil
import statistics
from collections import deque

class NetworkMonitor:
    def __init__(self, window_size=10):
        self.samples = deque(maxlen=window_size)

    def check(self):
        current = psutil.net_io_counters().bytes_recv
        self.samples.append(current)

        if len(self.samples) >= 3:
            rates = [self.samples[i] - self.samples[i-1] for i in range(1, len(self.samples))]
            mean = statistics.mean(rates)
            stdev = statistics.stdev(rates) if len(rates) >= 2 else 0
            latest_rate = rates[-1]

            if stdev > 0 and latest_rate > mean + 3 * stdev:
                return f"⚠️ 网络接收流量异常: {latest_rate/1024:.1f} KB/s (均值: {mean/1024:.1f})"
        return None
```

---

### 练习2：进程看门狗

**答案：**

```python
import psutil
import subprocess
import time
from datetime import datetime

def watchdog(process_name, restart_command, check_interval=10):
    print(f"🐕 看门狗启动，监控 '{process_name}'...")

    while True:
        found = False
        for proc in psutil.process_iter(["name"]):
            try:
                if process_name.lower() in proc.info["name"].lower():
                    found = True
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        if not found:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] ⚠️ {process_name} 未运行，尝试重启...")
            try:
                subprocess.Popen(restart_command, shell=True)
                print(f"[{timestamp}] ✅ 重启命令已执行")
            except Exception as e:
                print(f"[{timestamp}] ❌ 重启失败: {e}")

        time.sleep(check_interval)
```

---

### 练习3：监控 → 报告 → 邮件

**答案：**

```python
from system_monitor import SystemMonitor
from email_sender import send_html_email
import schedule
import time

SMTP_CONFIG = { ... }

def on_alert(alerts):
    """异常时发送报告"""
    report_html = generate_health_report()
    send_html_email(
        smtp_server=SMTP_CONFIG["server"], smtp_port=SMTP_CONFIG["port"],
        sender=SMTP_CONFIG["sender"], password=SMTP_CONFIG["password"],
        receiver="admin@example.com",
        subject=f"🚨 系统报警 - {len(alerts)} 项异常",
        html_body=report_html
    )

def daily_report():
    report = generate_health_report()
    send_html_email(..., subject="📊 每日系统健康报告", html_body=report)

# 启动
monitor = SystemMonitor(thresholds={"cpu": 70, "memory": 80, "disk": 85})
schedule.every().day.at("09:00").do(daily_report)

# 在主线程中运行监控，后台线程运行定时器
import threading
t = threading.Thread(target=lambda: schedule.run_pending() or time.sleep(60), daemon=True)
t.start()
monitor.run(interval=30, alert_callback=on_alert)
```