## 14.3 数据存储——把爬虫的"战利品"保存下来

爬虫抓取了数据，下一步就是把它存起来。对于几十条数据，存成 CSV 或 JSON 文件就够用；对于几万条以上，SQLite 或 MySQL 数据库是更专业的选择；对于更复杂的场景（如新闻文章的全文搜索），还可能用到 MongoDB 等 NoSQL 数据库。本节介绍三种最常用的存储方案，并给出"怎么选"的决策标准。

### 14.3.1 CSV 存储——最通用的表格格式

CSV 的优势是"任何数据分析工具都能打开"——Excel、Pandas、R、甚至记事本。对于大多数爬虫项目，CSV 是首选：

```python
import csv
import os
from datetime import datetime

data = [
    {"title": "Python入门指南", "author": "张三", "date": "2024-06-01", "views": 1500},
    {"title": "Flask Web开发", "author": "李四", "date": "2024-06-15", "views": 2300},
    {"title": "数据科学基础", "author": "王五", "date": "2024-06-20", "views": 1800},
]

# 写入 CSV
filepath = "articles.csv"
file_exists = os.path.exists(filepath)

with open(filepath, "a", encoding="utf-8", newline="") as f:
    fieldnames = ["title", "author", "date", "views"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    if not file_exists:
        writer.writeheader()          # 文件不存在才写表头
    writer.writerows(data)

print(f"数据已追加至 {filepath}")

# 读取 CSV 验证
with open(filepath, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['title']} — {row['views']} 次阅读")

# 使用 Pandas 读写（数据量大时更高效）
# import pandas as pd
# df = pd.DataFrame(data)
# df.to_csv("articles.csv", index=False, encoding="utf-8")
# df = pd.read_csv("articles.csv")
```

### 14.3.2 JSON 存储——结构灵活的"万能格式"

当数据包含嵌套结构（如文章有多个标签、评论列表等），CSV 的扁平表格结构就力不从心了。JSON 可以自然地表达嵌套数据：

```python
import json
import os

articles = [
    {
        "title": "Python入门指南",
        "author": {"name": "张三", "email": "zhangsan@example.com"},
        "tags": ["Python", "入门", "教程"],
        "comments": [
            {"user": "小明", "text": "写得很棒！", "time": "2024-06-02"},
            {"user": "小红", "text": "学到了", "time": "2024-06-03"},
        ],
        "stats": {"views": 1500, "likes": 128},
    }
]

# 写入 JSON
filepath = "articles.json"
existing = []
if os.path.exists(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        existing = json.load(f)

existing.extend(articles)

with open(filepath, "w", encoding="utf-8") as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)

print(f"数据已保存至 {filepath}，共 {len(existing)} 篇文章")

# 读取 JSON
with open(filepath, "r", encoding="utf-8") as f:
    loaded = json.load(f)
    for article in loaded:
        print(f"{article['title']} — {len(article['tags'])} 个标签, "
              f"{len(article['comments'])} 条评论")
```

### 14.3.3 SQLite 数据库——本地的关系型数据库

当数据量超过几万条、需要多表关联查询、或者需要持久化存储时，SQLite 是比 CSV/JSON 更好的选择。它无需安装服务器，数据库就是一个 `.db` 文件，Python 标准库自带 `sqlite3` 模块：

```python
import sqlite3

# 连接数据库（文件不存在会自动创建）
conn = sqlite3.connect("crawler.db")
cursor = conn.cursor()

# 建表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT,
        content TEXT,
        url TEXT UNIQUE,
        published_date TEXT,
        crawled_date TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id INTEGER,
        tag TEXT,
        FOREIGN KEY (article_id) REFERENCES articles(id)
    )
""")

# 插入数据——使用参数化查询防止 SQL 注入
article = ("Python入门指南", "张三", "文章内容...",
           "https://example.com/post/1", "2024-06-01", "2024-06-29")
cursor.execute(
    "INSERT OR IGNORE INTO articles (title, author, content, url, published_date, crawled_date) "
    "VALUES (?, ?, ?, ?, ?, ?)",
    article
)

# 批量插入
many_articles = [
    ("Flask Web开发", "李四", "内容...",
     "https://example.com/post/2", "2024-06-15", "2024-06-29"),
    ("数据科学基础", "王五", "内容...",
     "https://example.com/post/3", "2024-06-20", "2024-06-29"),
]
cursor.executemany(
    "INSERT OR IGNORE INTO articles (title, author, content, url, published_date, crawled_date) "
    "VALUES (?, ?, ?, ?, ?, ?)",
    many_articles
)

conn.commit()

# 查询数据
print("\n=== 所有文章 ===")
rows = cursor.execute("SELECT id, title, author, published_date FROM articles")
for row in rows.fetchall():
    print(f"  #{row[0]} {row[1]} by {row[2]} ({row[3]})")

# 统计查询
print(f"\n文章总数: {cursor.execute('SELECT COUNT(*) FROM articles').fetchone()[0]}")

# ORM 方式（推荐大型项目使用 SQLAlchemy）
# pip install sqlalchemy
# from sqlalchemy import create_engine
# engine = create_engine("sqlite:///crawler.db")
# df = pd.read_sql("SELECT * FROM articles", engine)

conn.close()
```

### 14.3.4 选择策略——哪种存储适合你？

| 场景 | 推荐方案 | 原因 |
|:-----|:---------|:-----|
| 几百条数据，结构简单 | CSV | 任何工具都能打开，方便分享 |
| 数据有嵌套结构 | JSON | 自然表达嵌套关系 |
| 几万条以上，需要查询 | SQLite | 支持 SQL 查询，索引，事务 |
| 需要全文搜索 | MongoDB / Elasticsearch | 专业搜索引擎 |
| 数据需要"版本控制" | CSV / JSON | 文本文件可以直接 git diff |
| 多节点分布式爬虫 | MySQL / PostgreSQL | 支持并发读写 |

### 14.3.5 实战练习

1. 编写一个通用的数据保存函数 `save_data(data, format, filepath)`，支持 `format` 为 `"csv"`、`"json"` 和 `"sqlite"` 三种格式。函数应自动判断文件是否存在以决定是新建还是追加，并对 SQLite 做去重处理（同 URL 不重复插入）。

2. 创建一个小型爬虫数据库：设计两张表——`posts`（标题、URL、作者、发布时间、正文、阅读量）和 `comments`（所属文章 ID、评论者、评论内容、时间）。编写建表语句和几个示例查询（JOIN 查询每篇文章的评论数、按阅读量排名）。

3. 对比 CSV 和 JSON 的存储效率：生成 10 万条同样的模拟数据，分别存为 CSV 和 JSON 文件，比较两个文件的大小。思考为什么会有差异。