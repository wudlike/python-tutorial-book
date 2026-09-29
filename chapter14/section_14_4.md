## 14.4 实战案例：爬取新闻数据——从网页到数据库的完整流水线

前面三节分别学习了 requests 获取网页、BeautifulSoup 解析 HTML、多种方式存储数据。这一节将它们串联成一个完整的爬虫项目——从真实的新闻网站抓取新闻信息，解析出标题、时间、摘要和链接，清洗后存入 SQLite 数据库，最后用 Pandas 做快速分析。

### 14.4.1 项目目标与免责声明

**目标**：爬取新闻列表页，提取新闻标题、发布日期、摘要和链接，存入数据库。

**重要声明**：爬虫是一把双刃剑。在使用爬虫之前，请务必：
1. 检查网站的 `robots.txt`（如 `https://example.com/robots.txt`），确认目标页面允许爬取
2. 遵守网站的"服务条款"（Terms of Service）
3. 控制请求频率（添加延时），不对目标服务器造成压力
4. 仅用于个人学习和研究，不侵犯版权

本节使用一个自己搭建的模拟新闻页面来进行演示——你可以在本地用 Flask 运行它，或者直接使用下面的静态 HTML 做验证。

### 14.4.2 准备模拟的新闻页面

> 💡 **完整项目代码**已放入 `projects/news_crawler/` 目录。你可以在该目录下按以下步骤运行：
>
> 1. 先启动模拟网站：`python serve_news.py`
> 2. 再运行爬虫：`python crawler.py`

模拟网站的核心是使用 Flask 渲染一个包含多条新闻的静态 HTML 页面，每条新闻是一个 `<article class="news-item">` 元素，包含标题、日期、摘要和来源。完整代码见 `projects/news_crawler/serve_news.py`。

### 14.4.3 爬虫代码结构

整个爬虫由几个核心模块组成，完整代码见 `projects/news_crawler/crawler.py`。下面讲解关键部分：

#### 数据库初始化

```python
import sqlite3

def init_db():
    conn = sqlite3.connect("news.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            summary TEXT,
            source TEXT,
            date TEXT,
            crawled_at TEXT DEFAULT (datetime('now', 'localtime'))
        )
    """)
    conn.commit()
    return conn
```

其中 `url TEXT UNIQUE` 约束配合后面的 `INSERT OR IGNORE`，天然实现了去重——重复爬取同一页面不会产生重复数据。

#### 爬取单页

核心提取逻辑——BeautifulSoup 找到所有 `article.news-item`，逐一提取标题、日期、摘要、来源：

```python
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawl_page(url, conn):
    response = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(response.text, "lxml")
    articles = soup.find_all("article", class_="news-item")

    for article in articles:
        title = article.find("h2").find("a").text.strip()
        absolute_url = urljoin(url, article.find("h2").find("a")["href"])
        date = article.find("span", class_="date").text.strip()
        summary = article.find("p", class_="summary").text.strip()

        conn.execute(
            "INSERT OR IGNORE INTO news (title, url, summary, source, date) "
            "VALUES (?, ?, ?, ?, ?)", (title, absolute_url, summary, source, date)
        )
```

#### 主流程

```python
def main():
    conn = init_db()
    for page in range(1, 4):
        url = BASE_URL if page == 1 else f"{BASE_URL}/?page={page}"
        crawl_page(url, conn)
        time.sleep(REQUEST_DELAY)  # 请求间隔，尊重服务器
    conn.close()
```

> 📂 **完整可运行代码**参见 `projects/news_crawler/crawler.py`（约 120 行），包含请求头伪装、异常处理、数据分析、CSV 导出等完整功能。

这个爬虫项目展示了几个重要模式：

**1. 模块化设计**——`init_db()`、`crawl_page()`、`main()` 各司其职。修改任何一个部分（如更换存储方案、调整解析逻辑）都不影响其他部分。

**2. `urljoin()` 拼接绝对 URL**——爬取到的链接可能是相对路径（如 `/news/1`），`urljoin(url, relative_url)` 会自动拼接为完整 URL。这比手动字符串拼接更可靠，能正确处理各种边界情况（`../`、`./`、协议相对路径等）。

**3. 请求间隔**——在分页爬取之间加入 `time.sleep()` 是对目标服务器最基本的尊重。对于生产环境，建议将间隔设置在 1-5 秒之间，具体取决于网站的负载能力。

**4. `INSERT OR IGNORE` 去重**——设计数据库表时给 `url` 字段加了 `UNIQUE` 约束，配合 `INSERT OR IGNORE`，重复爬取同一页面不会产生重复数据。这是爬虫"幂等性"的标准实践。

**5. 异常处理的层次**——网络异常（requests.exceptions）在 `crawl_page()` 中捕获，这样一个页面的失败不会导致整个爬虫崩溃。数据库异常单独捕获，避免因一条数据的格式问题影响其他数据的保存。

### 14.4.5 扩展方向

这个基础爬虫可以从以下方向升级：

- **增量爬取**：只爬取比数据库中最新记录更新的文章，避免重复工作
- **并发爬取**：使用 `concurrent.futures.ThreadPoolExecutor`（参见 10.4 节）并行爬取多个页面
- **动态页面**：对于用 JavaScript 渲染的页面（如 React/Vue 单页应用），使用 Selenium 或 Playwright
- **反反爬虫**：实现 User-Agent 轮换、IP 代理池、验证码识别
- **数据可视化**：用 Matplotlib（参见 12.3 节）分析新闻的发布趋势、来源分布

### 14.4.6 实战练习

1. 修改本节的爬虫，增加一个"关键词过滤"功能——爬取的所有新闻中，只保存标题或摘要中包含指定关键词（如"Python""AI"）的文章到数据库。

2. 为本节的爬虫添加"爬取详情页"功能——在获取新闻列表后，进一步访问每条新闻的详情页 URL，提取完整的正文内容，并在数据库中增加一个 `content` 列存储正文。

3. 使用 `schedule` 库（需安装 `pip install schedule`）实现定时爬取——每天上午 9 点自动执行一次爬虫，将新爬取的新闻数量通过邮件发送给自己（邮件发送的代码可参考 15.2 节的内容）。