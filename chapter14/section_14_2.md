## 14.2 BeautifulSoup 解析 HTML——从"网页字符串"到"结构化数据"

requests 帮你拿到了网页的 HTML 源代码，但它只是一串字符串——你需要从中提取出标题、正文、链接、图片等结构化信息。这就是 **BeautifulSoup** 的职责：它把 HTML/XML 文档解析成一棵**文档树**，让你用类似"CSS 选择器"或"遍历树节点"的方式精准定位和提取数据。

BeautifulSoup（简称 BS4）配合 requests，构成了 Python 爬虫开发中最经典的组合。

### 14.2.1 安装与解析器选择

```python
# pip install beautifulsoup4 lxml

from bs4 import BeautifulSoup
import requests

# 获取一个真实的 HTML 页面进行演示
html_doc = """
<html>
<head>
    <title>我的博客 - 首页</title>
    <meta charset="utf-8">
</head>
<body>
    <div id="header">
        <h1 class="site-title">📝 我的技术博客</h1>
    </div>
    <div id="content">
        <div class="post" data-id="1">
            <h2><a href="/post/1">Python 入门指南</a></h2>
            <p class="summary">这是一篇关于 Python 入门的文章。</p>
            <span class="date">2024-06-01</span>
            <span class="tags">Python, 入门</span>
        </div>
        <div class="post" data-id="2">
            <h2><a href="/post/2">Flask Web 开发</a></h2>
            <p class="summary">从零开始学习 Flask Web 框架。</p>
            <span class="date">2024-06-15</span>
            <span class="tags">Flask, Web</span>
        </div>
    </div>
    <div id="footer">
        <p>© 2024 My Blog</p>
    </div>
</body>
</html>
"""

soup = BeautifulSoup(html_doc, "lxml")    # lxml 是最快的解析器
```

BeautifulSoup 支持多种底层解析器。推荐 `lxml`——它比内置的 `html.parser` 快很多，容错性也更好。如果没装 lxml，BeautifulSoup 会自动回退到 `html.parser`，但会打印警告：

```python
# 三种解析器选择
# BeautifulSoup(html, "html.parser")   # Python 内置，无需安装（速度一般）
# BeautifulSoup(html, "lxml")          # 第三方，速度快，容错好（推荐）
# BeautifulSoup(html, "xml")           # 用于解析 XML
```

### 14.2.2 导航文档树——层层深入

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_doc, "lxml")

# 直接访问标签——返回第一个匹配的标签
print(soup.title)                 # <title>我的博客 - 首页</title>
print(soup.title.string)          # 我的博客 - 首页  —— 获取标签内的文本
print(soup.h1)                    # <h1 class="site-title">📝 我的技术博客</h1>
print(soup.h1.text)               # 📝 我的技术博客

# 获取属性——两种方式
print(soup.h1["class"])           # ['site-title']
print(soup.h1.get("class"))       # ['site-title']
# 第一种写法简洁但属性不存在会抛 KeyError；第二种返回 None，更安全

# 父子关系导航
post_div = soup.find("div", class_="post")
print(post_div.name)              # div —— 标签名
print(post_div.h2.a["href"])      # /post/1 —— 像属性一样链式访问
print(post_div.h2.a.text)         # Python 入门指南

# 获取父标签
print(post_div.parent.name)       # div（id="content"）

# 兄弟标签导航
print(post_div.find_next_sibling("div").h2.a.text)    # Flask Web 开发
```

### 14.2.3 搜索文档树——`find()` 与 `find_all()`

导航文档树适合结构简单、路径固定的页面。对于复杂的真实网页，搜索是更强大的方式：

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_doc, "lxml")

# find() —— 返回第一个匹配的标签
first_post = soup.find("div", class_="post")
print(first_post.h2.text)          # Python 入门指南

# find_all() —— 返回所有匹配的标签列表
all_posts = soup.find_all("div", class_="post")
print(f"找到 {len(all_posts)} 篇文章")
for post in all_posts:
    title = post.find("h2").find("a").text
    date = post.find("span", class_="date").text
    summary = post.find("p", class_="summary").text
    print(f"  {title} ({date}): {summary}")

# 按属性搜索
post_1 = soup.find("div", {"data-id": "1"})
print(post_1.h2.text)              # Python 入门指南

# 使用函数作为过滤条件
def has_data_id(tag):
    return tag.has_attr("data-id") and int(tag["data-id"]) > 1

later_posts = soup.find_all(has_data_id)
print([p.h2.text.strip() for p in later_posts])    # ['Flask Web 开发']

# 限制返回数量
first_two = soup.find_all("div", class_="post", limit=2)
```

`find()` 和 `find_all()` 的核心参数表：

| 参数 | 示例 | 功能 |
|:-----|:-----|:-----|
| `name` | `"div"`, `["h1", "h2"]` | 按标签名匹配 |
| `attrs` / `class_` / `id` | `class_="post"`, `id="header"` | 按属性匹配 |
| `string` / `text` | `string="首页"` | 按文本内容匹配 |
| `limit` | `limit=5` | 限制返回数量 |
| `recursive` | `recursive=False` | 是否递归搜索子元素 |

### 14.2.4 CSS 选择器——`select()` 方法

如果你熟悉 CSS 或 jQuery 的选择器语法，`select()` 会让你如鱼得水——它用 CSS 选择器来定位元素，写法紧凑且直观：

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_doc, "lxml")

# CSS 选择器常用模式
print(soup.select("title"))                      # 标签选择器
print(soup.select("#header"))                    # ID 选择器
print(soup.select(".post"))                      # 类选择器
print(soup.select("div.post"))                   # 标签+类组合
print(soup.select("div#content > div.post"))     # 直接子元素
print(soup.select("div.post h2 a"))              # 后代选择器
print(soup.select("div.post:nth-of-type(2)"))    # 第 2 个 .post
print(soup.select("span.tags"))                  # span 标签且 class="tags"
print(soup.select("[data-id]"))                  # 有 data-id 属性的元素
print(soup.select("[data-id='2']"))              # data-id 等于 "2"

# 提取数据
for post in soup.select("div.post"):
    title = post.select_one("h2 a").text         # select_one 只取第一个
    date = post.select_one("span.date").text
    tags = post.select_one("span.tags").text
    print(f"{title} | {date} | {tags}")
```

`select()` vs `find_all()` 的选择建议：
- **select()** 更适合"按路径定位"——如取某个 div 下的第三个 p 标签，CSS 选择器一目了然
- **find_all()** 更适合"按条件筛选"——如找所有包含 `data-id` 属性的元素，`find_all` 的 lambda 过滤更灵活
- 两者可以混用——先用 `find_all` 粗筛，再用 `select` 精取

### 14.2.5 常见爬虫场景实战

```python
from bs4 import BeautifulSoup

# 场景 1：提取页面中所有链接
html = """
<a href="/home">首页</a>
<a href="https://example.com/about">关于</a>
<a href="https://example.com/blog">博客</a>
<a href="javascript:void(0)">无意义链接</a>
"""
soup = BeautifulSoup(html, "lxml")

links = []
for a in soup.find_all("a", href=True):     # href=True 只取有 href 属性的
    href = a["href"]
    if href.startswith("http"):              # 过滤掉 javascript: 和锚点
        links.append({"text": a.text.strip(), "url": href})
print(links)

# 场景 2：提取表格数据
html_table = """
<table>
    <tr><th>姓名</th><th>年龄</th><th>城市</th></tr>
    <tr><td>张三</td><td>25</td><td>北京</td></tr>
    <tr><td>李四</td><td>30</td><td>上海</td></tr>
    <tr><td>王五</td><td>28</td><td>广州</td></tr>
</table>
"""
soup = BeautifulSoup(html_table, "lxml")
rows = soup.find_all("tr")
headers = [th.text.strip() for th in rows[0].find_all("th")]
data = []
for row in rows[1:]:
    cells = [td.text.strip() for td in row.find_all("td")]
    data.append(dict(zip(headers, cells)))
print(data)

# 场景 3：提取 meta 标签中的描述信息
html_meta = """
<head>
    <meta name="description" content="这是一个Python教程网站">
    <meta name="keywords" content="Python, 教程, 编程">
    <meta property="og:title" content="Python入门">
</head>
"""
soup = BeautifulSoup(html_meta, "lxml")
description = soup.find("meta", attrs={"name": "description"})
if description:
    print(description["content"])    # 这是一个Python教程网站
```

### 14.2.6 实战练习

1. 使用 BeautifulSoup 解析以下 HTML，提取"产品名、价格、评分"三个字段，输出为一个字典列表：

```html
<div class="product-list">
    <div class="product">
        <h3 class="name">机械键盘</h3>
        <span class="price">¥299</span>
        <span class="rating">4.8</span>
    </div>
    <div class="product">
        <h3 class="name">无线鼠标</h3>
        <span class="price">¥129</span>
        <span class="rating">4.5</span>
    </div>
    <div class="product">
        <h3 class="name">显示器</h3>
        <span class="price">¥1999</span>
        <span class="rating">4.9</span>
    </div>
</div>
```

2. 编写一个函数 `extract_links(html, base_url)`，从 HTML 中提取所有 `<a>` 标签的 `href` 和文本，处理相对路径（如果 `href` 以 `/` 开头，则拼接 `base_url`），过滤掉 `javascript:` 和 `#` 开头的无效链接。

3. 在一个 HTML 文档中，有一个 `id="article-content"` 的 div 元素，里面包含了多级嵌套的 `<p>`、`<h2>`、`<ul>` 等标签。编写代码提取该 div 中的所有纯文本内容（去除 HTML 标签），并统计字数。