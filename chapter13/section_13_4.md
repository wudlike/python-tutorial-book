## 13.4 简单博客系统开发——串联 Flask 的全部知识

前面三节分别学习了 Flask 的基础、路由和模板。这一节将它们串联起来，开发一个完整的**个人博客系统**——虽然功能精简，但它包含了 Web 开发中最核心的模式：路由设计、数据模型、模板渲染、表单处理、CRUD 操作（增删改查）。完成这个项目后，你将有能力开发任何简单的 Web 应用。

### 13.4.1 项目规划

我们的博客系统包含以下功能：
- 首页：显示所有文章的标题、摘要和发布日期
- 文章详情页：显示单篇文章的完整内容
- 新建文章：通过表单提交标题、内容和标签
- 编辑文章：修改已有文章
- 删除文章：删除指定文章

数据结构用 Python 列表和字典存储（简化版——真实场景会用数据库），每篇文章是一个字典：

```python
{
    "id": 1,
    "title": "我的第一篇博客",
    "content": "这是正文内容...",
    "tags": "Python, Flask",
    "created_at": "2024-06-29 14:30:00"
}
```

### 13.4.2 项目文件结构

```text
blog_project/
    app.py                   # Flask 应用主文件
    templates/
        base.html            # 基模板（页头 + 页脚）
        index.html           # 首页——文章列表
        post.html            # 文章详情页
        create.html          # 新建 / 编辑文章表单
    static/
        style.css            # 全局样式
```

### 13.4.3 完整代码

> 💡 **完整项目代码**已放入 `projects/blog_system/` 目录，包含以下文件：
>
> | 文件 | 说明 |
> |------|------|
> | `app.py` | Flask 应用主文件（路由、数据模型、视图函数） |
> | `templates/base.html` | 基模板（页头 + 导航 + 页脚） |
> | `templates/index.html` | 首页模板（文章列表） |
> | `templates/post.html` | 文章详情页模板 |
> | `templates/create.html` | 新建/编辑文章的表单模板 |
> | `static/style.css` | 全局样式表 |
>
> 你可以进入该目录直接运行 `python app.py` 启动博客系统，浏览器访问 `http://127.0.0.1:5000` 即可体验。

下面逐段讲解 `app.py` 中的核心代码结构：

#### 数据模型

```python
posts = [
    {
        "id": 1,
        "title": "Python Flask 入门指南",
        "content": "...",
        "tags": "Python, Flask, Web",
        "created_at": "2024-06-01 10:00:00"
    },
]
next_id = 3
```

#### 路由设计

```python
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
    """新建文章——GET显示表单，POST保存数据"""
    ...

@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    """编辑文章"""
    ...

@app.route("/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    """删除文章"""
    ...
```

#### 辅助函数

```python
def find_post(post_id):
    """根据 id 查找文章，找不到返回 None"""
    for post in posts:
        if post["id"] == post_id:
            return post
    return None
```

> 📂 **以上代码的完整可运行版本参见**：`projects/blog_system/app.py`

### 13.4.4 模板设计思路

模板采用 Jinja2 的**继承机制**——`base.html` 定义页面骨架，各子模板通过 `{% block %}` 填充内容区域。全部模板文件见 `projects/blog_system/templates/`。

以 `base.html` 为例，它定义了所有页面共享的结构：

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}我的技术博客{% endblock %}</title>
</head>
<body>
    <header>
        <h1><a href="{{ url_for('index') }}">📝 我的技术博客</a></h1>
        <nav>
            <a href="{{ url_for('index') }}">首页</a>
            <a href="{{ url_for('create_post') }}">✏️ 写文章</a>
        </nav>
    </header>
    <main>{% block content %}{% endblock %}</main>
    <footer><p>© 2024 My Tech Blog. Powered by Flask.</p></footer>
</body>
</html>
```

子模板如 `index.html` 通过 `{% extends "base.html" %}` 继承这个骨架，然后重写 `title` 和 `content` 两个 block。其他模板（`post.html`、`create.html`）同理。

> 📂 **完整模板文件**参见 `projects/blog_system/templates/`

### 13.4.5 样式文件

完整的 CSS 样式文件位于 `projects/blog_system/static/style.css`。核心要点：

- `max-width: 800px` + `margin: 0 auto` 实现内容居中
- `.post-card` 用 `box-shadow` 和 `border-radius` 制作卡片效果
- `.btn` 类提供统一的按钮样式，`.btn-primary` / `.btn-danger` 区分不同语义

### 13.4.6 代码导读——理解架构模式

1. **路由设计遵循 RESTful 风格**：`/post/1` 显示文章、`/create` 新建、`/edit/1` 编辑、`/delete/1` 删除——URL 清晰表达了资源的操作
2. **PRG 模式**（Post-Redirect-Get）：新建和编辑在 POST 提交成功后执行 `redirect()` 而不是直接返回 HTML。这防止了用户刷新页面时重复提交表单
3. **模板复用的巧思**：`create.html` 同时服务于"新建"和"编辑"两个场景——通过 `post` 变量是否为空来判断是哪种模式，避免了写两个几乎相同的模板
4. **删除用 POST 而非 GET**：`/delete/<id>` 只接受 POST 请求，配合 `onsubmit` 确认对话框——防止搜索引擎爬虫或浏览器预加载意外触发删除

### 13.4.7 后续可扩展的方向

这个博客系统是"麻雀虽小，五脏俱全"的起点。你可以沿着以下方向升级它：
- **数据库**：用 SQLAlchemy + SQLite 替代内存列表，使数据持久化
- **用户认证**：添加 Flask-Login 实现注册、登录、权限控制
- **Markdown**：支持用 Markdown 语法写文章，渲染为 HTML
- **评论系统**：为每篇文章添加评论功能
- **部署上线**：用 gunicorn + nginx 部署到云服务器

### 13.4.8 实战练习

1. 在本节的博客系统基础上添加"文章搜索"功能——在首页添加一个搜索框，提交后按"标题"和"标签"两个字段筛选文章，并高亮匹配的关键词。

2. 为博客添加"归档"页面（`/archive`），按年月分组显示所有文章（如"2024-06（3 篇）"），点击月份展开显示该月的文章列表。

3. 实现"文章访问计数"功能——每篇文章详情页显示"已被阅读 X 次"，每次有人访问文章详情页，计数器就加 1。提示：在 `posts` 列表中为每篇文章增加一个 `views` 字段。