"""新闻爬虫 —— 从模拟新闻网站爬取新闻数据

运行方式：
  1. 先启动模拟网站：python serve_news.py
  2. 再运行爬虫：python crawler.py

功能：爬取新闻列表 → 解析标题/日期/摘要/来源 → 存入 SQLite → 导出 CSV
"""

import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import pandas as pd
from urllib.parse import urljoin

# ==================== 配置 ====================
BASE_URL = "http://127.0.0.1:5000"
DB_PATH = "news.db"
REQUEST_DELAY = 1.0

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 Chrome/120.0.0.0"
}

# ==================== 数据库初始化 ====================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
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

# ==================== 爬取单页 ====================
def crawl_page(url, conn):
    print(f"正在爬取: {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        response.encoding = "utf-8"
    except requests.RequestException as e:
        print(f"  ❌ 请求失败: {e}")
        return 0

    soup = BeautifulSoup(response.text, "lxml")
    articles = soup.find_all("article", class_="news-item")

    count = 0
    for article in articles:
        title_tag = article.find("h2").find("a")
        if not title_tag:
            continue

        title = title_tag.text.strip()
        relative_url = title_tag.get("href", "")
        absolute_url = urljoin(url, relative_url)

        date_tag = article.find("span", class_="date")
        date = date_tag.text.strip() if date_tag else ""

        summary_tag = article.find("p", class_="summary")
        summary = summary_tag.text.strip() if summary_tag else ""

        source_tag = article.find("span", class_="source")
        source = source_tag.text.replace("来源：", "").strip() if source_tag else ""

        try:
            conn.execute(
                "INSERT OR IGNORE INTO news (title, url, summary, source, date) "
                "VALUES (?, ?, ?, ?, ?)",
                (title, absolute_url, summary, source, date)
            )
            count += 1
            print(f"  ✅ {title[:40]}... ({date})")
        except sqlite3.Error as e:
            print(f"  ⚠️ 数据库错误: {e}")

    conn.commit()
    return count

# ==================== 主流程 ====================
def main():
    print("=" * 60)
    print("新闻爬虫启动")
    print("=" * 60)

    conn = init_db()

    total = 0
    for page in range(1, 4):
        url = BASE_URL if page == 1 else f"{BASE_URL}/?page={page}"
        total += crawl_page(url, conn)
        if page < 3:
            time.sleep(REQUEST_DELAY)

    print(f"\n✅ 爬取完毕，共获取 {total} 条新闻")

    # 数据分析
    print("\n" + "=" * 60)
    print("数据分析")
    print("=" * 60)

    df = pd.read_sql("SELECT * FROM news ORDER BY date DESC", conn)

    print(f"总新闻数: {len(df)}")
    print(f"日期范围: {df['date'].min()} ~ {df['date'].max()}")

    print("\n【按来源统计】")
    source_counts = df["source"].value_counts()
    for source, count in source_counts.items():
        print(f"  {source}: {count} 篇")

    print("\n【每日新闻数】")
    daily = df["date"].value_counts().sort_index()
    for date, count in daily.items():
        bar = "█" * count
        print(f"  {date}: {bar} ({count})")

    df.to_csv("news_export.csv", index=False, encoding="utf-8")
    print(f"\n📁 数据已导出到 news_export.csv")

    conn.close()

if __name__ == "__main__":
    main()