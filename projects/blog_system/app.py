"""简单博客系统 —— Flask 应用主文件

运行方式：python app.py
访问地址：http://127.0.0.1:5000

功能：首页文章列表 / 文章详情 / 新建文章 / 编辑文章 / 删除文章
"""

from flask import Flask, render_template, request, redirect, url_for, abort
from datetime import datetime

app = Flask(__name__)

# 内存数据库——用列表模拟
posts = [
    {
        "id": 1,
        "title": "Python Flask 入门指南",
        "content": "Flask 是一个轻量级的 Web 框架，它的核心设计理念是'微而不弱'——"
                   "核心只包含路由和模板渲染，其他功能通过扩展按需添加。"
                   "这使得 Flask 的学习曲线平缓，非常适合 Web 开发初学者。",
        "tags": "Python, Flask, Web",
        "created_at": "2024-06-01 10:00:00"
    },
    {
        "id": 2,
        "title": "为什么推荐学 Python？",
        "content": "Python 的语法简洁、生态丰富，从数据分析到 Web 开发再到人工智能，"
                   "Python 几乎覆盖了所有热门技术领域。对于编程初学者来说，"
                   "Python 是最友好的入门语言之一。",
        "tags": "Python, 入门",
        "created_at": "2024-06-15 14:30:00"
    },
]
next_id = 3


def find_post(post_id):
    """根据 id 查找文章，找不到返回 None"""
    for post in posts:
        if post["id"] == post_id:
            return post
    return None


# ==================== 路由 ====================

@app.route("/")
def index():
    """首页——显示所有文章（按时间倒序）"""
    sorted_posts = sorted(posts, key=lambda p: p["created_at"], reverse=True)
    return render_template("index.html", posts=sorted_posts)


@app.route("/post/<int:post_id>")
def show_post(post_id):
    """文章详情页"""
    post = find_post(post_id)
    if post is None:
        abort(404)
    return render_template("post.html", post=post)


@app.route("/create", methods=["GET", "POST"])
def create_post():
    """新建文章"""
    global next_id
    if request.method == "POST":
        post = {
            "id": next_id,
            "title": request.form["title"],
            "content": request.form["content"],
            "tags": request.form["tags"],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        posts.append(post)
        next_id += 1
        return redirect(url_for("show_post", post_id=post["id"]))
    return render_template("create.html", post=None, action="新建")


@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    """编辑文章"""
    post = find_post(post_id)
    if post is None:
        abort(404)
    if request.method == "POST":
        post["title"] = request.form["title"]
        post["content"] = request.form["content"]
        post["tags"] = request.form["tags"]
        return redirect(url_for("show_post", post_id=post_id))
    return render_template("create.html", post=post, action="编辑")


@app.route("/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    """删除文章"""
    global posts
    posts = [p for p in posts if p["id"] != post_id]
    return redirect(url_for("index"))


@app.errorhandler(404)
def not_found(error):
    return render_template("base.html", content="<h2>404 - 文章不存在</h2>"), 404


if __name__ == "__main__":
    app.run(debug=True)