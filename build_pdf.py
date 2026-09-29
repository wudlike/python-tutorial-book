"""Markdown → 精美PDF 生成脚本
方案：Python Markdown → HTML → Edge浏览器渲染PDF（中文完美支持）
"""

import markdown
import re
import os
import subprocess
import shutil

# ===== 1. 读取 Markdown =====
with open('demo_chapter.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# ===== 2. 加载 Pygments CSS（代码语法高亮） =====
from pygments.formatters import HtmlFormatter
PYGMENTS_CSS = HtmlFormatter(style='tango').get_style_defs('.highlight')

# ===== 3. CSS 样式（删除了 xhtml2pdf 特有语法，使用标准 CSS） =====
CSS_STYLE = """
/* ===== 页面设置 ===== */
@page {
    size: A4;
    margin: 2.5cm;
}

body {
    font-family: "SimSun", "宋体", "Noto Serif SC", serif;
    font-size: 10.5pt;
    line-height: 1.5;
    color: #333333;
    max-width: 100%;
}

/* ===== 标题颜色 ===== */
h1 {
    color: #1565C0;
    font-size: 19pt;
    border-bottom: 3px solid #1565C0;
    padding-bottom: 8pt;
    margin-top: 26pt;
    page-break-before: always;
}

h1:first-of-type {
    page-break-before: avoid;
}

h2 {
    color: #2E7D32;
    font-size: 14.5pt;
    margin-top: 20pt;
    padding-left: 10pt;
    border-left: 4px solid #2E7D32;
}

h3 {
    color: #E65100;
    font-size: 12pt;
    margin-top: 16pt;
}

/* ===== 定义框（蓝色） ===== */
.definitionbox {
    background: #E3F2FD;
    border-left: 6px solid #1565C0;
    border-radius: 6px;
    padding: 14pt 18pt;
    margin: 16pt 0;
}
.definitionbox .box-title {
    color: #1565C0;
    font-size: 12pt;
    font-weight: bold;
    margin-bottom: 8pt;
}

/* ===== 提示框（绿色） ===== */
.tipbox {
    background: #E8F5E9;
    border-left: 6px solid #2E7D32;
    border-radius: 6px;
    padding: 14pt 18pt;
    margin: 16pt 0;
}
.tipbox .box-title {
    color: #2E7D32;
    font-size: 12pt;
    font-weight: bold;
    margin-bottom: 8pt;
}

/* ===== 警告框（橙色） ===== */
.warningbox {
    background: #FFF3E0;
    border-left: 6px solid #E65100;
    border-radius: 6px;
    padding: 14pt 18pt;
    margin: 16pt 0;
}
.warningbox .box-title {
    color: #E65100;
    font-size: 12pt;
    font-weight: bold;
    margin-bottom: 8pt;
}

/* ===== 补充知识框（紫色） ===== */
.notebox {
    background: #F3E5F5;
    border-left: 6px solid #7B1FA2;
    border-radius: 6px;
    padding: 14pt 18pt;
    margin: 16pt 0;
}
.notebox .box-title {
    color: #7B1FA2;
    font-size: 12pt;
    font-weight: bold;
    margin-bottom: 8pt;
}

/* ===== 代码块 ===== */
pre {
    background: #FAFAFA;
    border: 1px solid #E0E0E0;
    border-left: 4px solid #1976D2;
    border-radius: 6px;
    padding: 12pt 14pt;
    font-family: "Consolas", "Courier New", "Source Code Pro", monospace;
    font-size: 9pt;
    line-height: 1.5;
    overflow-x: auto;
    margin: 12pt 0;
    white-space: pre-wrap;
    word-break: break-all;
}

code {
    font-family: "Consolas", "Courier New", monospace;
    background: #F5F5F5;
    padding: 1pt 4pt;
    border-radius: 3px;
    font-size: 9.5pt;
    color: #C62828;
}

pre code {
    background: transparent;
    padding: 0;
    color: #37474F;
    font-size: 9pt;
}

/* ===== 表格 ===== */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 14pt 0;
    font-size: 10pt;
}

thead {
    background: #1976D2;
    color: white;
}

th {
    padding: 10pt 12pt;
    text-align: left;
    font-weight: bold;
}

td {
    padding: 8pt 12pt;
    border-bottom: 1px solid #E0E0E0;
}

tbody tr:nth-child(odd) {
    background: #FAFAFA;
}

/* ===== 图片 ===== */
img {
    max-width: 95%;
    height: auto;
    display: block;
    margin: 18pt auto;
    border-radius: 6px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}

/* ===== 文本强调 ===== */
strong {
    color: #1565C0;
}

em {
    color: #E65100;
}

/* ===== 列表 ===== */
ul, ol {
    padding-left: 28pt;
}

li {
    margin: 5pt 0;
}

/* ===== 数学公式 ===== */
.MathJax, .math {
    font-size: 110%;
}

/* ===== 页码 ===== */
.page-break {
    page-break-before: always;
}

/* ===== Pygments 高亮微调 ===== */
.highlight .hll { background-color: #ffffcc }
.highlight .c { color: #8f5902; font-style: italic }
.highlight .k { color: #204a87; font-weight: bold }
.highlight .s { color: #4e9a06 }
.highlight .n { color: #000000 }
.highlight .mi { color: #0000cf }
"""

# ===== 4. 预处理：LaTeX盒子 → HTML占位符（避免Markdown跳过HTML块内解析） =====
BOX_PLACEHOLDERS = {
    r'\\begin\{definitionbox\}': '<!--__BOXDEF__-->',
    r'\\end\{definitionbox\}': '<!--__BOXDEF_END__-->',
    r'\\begin\{tipbox\}': '<!--__BOXTIP__-->',
    r'\\end\{tipbox\}': '<!--__BOXTIP_END__-->',
    r'\\begin\{warningbox\}': '<!--__BOXWARN__-->',
    r'\\end\{warningbox\}': '<!--__BOXWARN_END__-->',
    r'\\begin\{notebox\}': '<!--__BOXNOTE__-->',
    r'\\end\{notebox\}': '<!--__BOXNOTE_END__-->',
}

for pattern, placeholder in BOX_PLACEHOLDERS.items():
    md_content = re.sub(pattern, placeholder, md_content)

# ===== 5. 将 $$ 公式替换为 MathJax 兼容格式 =====
# 独立公式 $$...$$ 保持不变，MathJax 原生支持
# 行内公式 $...$ 保持不变

# ===== 6. Markdown → HTML =====
html_body = markdown.markdown(
    md_content,
    extensions=[
        'markdown.extensions.fenced_code',
        'markdown.extensions.tables',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ],
    extension_configs={
        'markdown.extensions.codehilite': {
            'css_class': 'highlight',
            'guess_lang': True,
        },
    }
)

# ===== 6.5 替换占位符为真正的HTML盒子 =====
BOX_HTML = {
    '<!--__BOXDEF__-->': '<div class="definitionbox"><div class="box-title">📖 定义</div>\n',
    '<!--__BOXDEF_END__-->': '\n</div>',
    '<!--__BOXTIP__-->': '<div class="tipbox"><div class="box-title">💡 提示</div>\n',
    '<!--__BOXTIP_END__-->': '\n</div>',
    '<!--__BOXWARN__-->': '<div class="warningbox"><div class="box-title">⚠️ 注意</div>\n',
    '<!--__BOXWARN_END__-->': '\n</div>',
    '<!--__BOXNOTE__-->': '<div class="notebox"><div class="box-title">ℹ️ 补充知识</div>\n',
    '<!--__BOXNOTE_END__-->': '\n</div>',
}

for placeholder, html in BOX_HTML.items():
    html_body = html_body.replace(placeholder, html)

# ===== 7. 完整 HTML 文档（引入 MathJax CDN） =====
FULL_HTML = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>Python：2周从入门到精通 — 示例章节</title>
<script>
MathJax = {{
  tex: {{
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
    processEscapes: true
  }}
}};
</script>
<script id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js">
</script>
<style>
{CSS_STYLE}
{PYGMENTS_CSS}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

# ===== 8. 输出 HTML 文件 =====
html_path = 'demo_output.html'
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(FULL_HTML)
print("✅ HTML 已生成: demo_output.html")

# ===== 9. 用 Edge/Chrome 无头模式打印 PDF =====
pdf_path = os.path.abspath('demo_output.pdf')
html_abs = os.path.abspath(html_path)
file_url = f'file:///{html_abs.replace(chr(92), "/")}'

print("正在用浏览器渲染 PDF（将自动打开浏览器窗口）...")

# 尝试 Edge，失败则尝试 Chrome
engines = [
    {
        'paths': [
            r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
            r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
        ],
        'name': 'Microsoft Edge'
    },
    {
        'paths': [
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        ],
        'name': 'Google Chrome'
    },
]

# 尝试找到 msedge 或 chrome
browser_path = None
browser_name = None
for engine in engines:
    for p in engine['paths']:
        if os.path.exists(p):
            browser_path = p
            browser_name = engine['name']
            break
    if browser_path:
        break

if not browser_path:
    # 最后尝试用 where 命令找
    for cmd in ['msedge', 'chrome']:
        found = shutil.which(cmd)
        if found:
            browser_path = found
            browser_name = cmd
            break

if not browser_path:
    print("❌ 未找到 Edge 或 Chrome 浏览器！")
    print("   请手动用浏览器打开 demo_output.html，然后 Ctrl+P 另存为 PDF")
    print(f"   文件位置: {html_abs}")
else:
    print(f"   使用 {browser_name}: {browser_path}")

    # 使用 headless 模式生成 PDF
    # --headless=new 使用新版headless（与正常模式完全一致）
    cmd = [
        browser_path,
        '--headless=new',
        '--disable-gpu',
        f'--print-to-pdf={pdf_path}',
        '--no-pdf-header-footer',
        file_url
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=60)

    if result.returncode == 0 and os.path.exists(pdf_path):
        file_size = os.path.getsize(pdf_path)
        print(f"✅ PDF 已生成: demo_output.pdf ({file_size / 1024:.1f} KB)")
        print("   请打开查看，中文应该完美显示！")
    else:
        print(f"❌ PDF 生成失败 (exit code: {result.returncode})")
        if result.stderr:
            print(f"   错误: {result.stderr[:500]}")
        print(f"   请手动用浏览器打开 {html_abs}，然后 Ctrl+P → 另存为 PDF")