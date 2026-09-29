"""模拟新闻网站 —— 用于爬虫练习

运行方式：python serve_news.py
访问地址：http://127.0.0.1:5000
"""

from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>TechNews - 科技资讯</title></head>
<body>
    <header><h1>TechNews 科技资讯</h1></header>
    <main>
        <div class="news-list">
            <article class="news-item">
                <h2><a href="/news/1">Python 3.13 发布：性能提升 50%</a></h2>
                <span class="date">2024-06-25</span>
                <p class="summary">Python 3.13 正式版发布了，JIT 编译器带来显著的性能提升。</p>
                <span class="source">来源：Python官方博客</span>
            </article>
            <article class="news-item">
                <h2><a href="/news/2">AI 大模型的下一个风口：多模态融合</a></h2>
                <span class="date">2024-06-24</span>
                <p class="summary">多位专家认为，文本+图像+语音的多模态融合将成为 AI 的下一个突破口。</p>
                <span class="source">来源：科技日报</span>
            </article>
            <article class="news-item">
                <h2><a href="/news/3">Flask 3.1 发布，带来异步视图支持</a></h2>
                <span class="date">2024-06-23</span>
                <p class="summary">Flask 3.1 引入了原生异步视图函数支持，大幅简化了异步代码的编写。</p>
                <span class="source">来源：Flask 官方</span>
            </article>
            <article class="news-item">
                <h2><a href="/news/4">开源数据库 PostgreSQL 17 性能测试</a></h2>
                <span class="date">2024-06-22</span>
                <p class="summary">最新基准测试显示 PostgreSQL 17 的查询性能比上一代提升了 30%。</p>
                <span class="source">来源：数据库周刊</span>
            </article>
            <article class="news-item">
                <h2><a href="/news/5">2024 年最值得学习的编程语言排名</a></h2>
                <span class="date">2024-06-21</span>
                <p class="summary">Stack Overflow 年度调查出炉，Python 连续第五年蝉联最受欢迎语言。</p>
                <span class="source">来源：Stack Overflow</span>
            </article>
        </div>
        <nav class="pagination">
            <a href="/?page=2">下一页 →</a>
        </nav>
    </main>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True)