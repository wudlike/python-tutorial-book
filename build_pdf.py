"""Markdown → 精美PDF 生成脚本
方案：Python Markdown → HTML → Edge浏览器渲染PDF（中文完美支持）
自动发现并合并 chapter*.md 生成完整书籍PDF
"""

import markdown
import re
import os
import glob
import subprocess
import shutil

# ===== 1. 自动发现并读取所有章节目录中的 .md 文件 =====
def _chapter_sort_key(dirname):
    m = re.search(r'chapter(\d+)', dirname)
    return int(m.group(1)) if m else 0

chapter_dirs = sorted(
    [d for d in glob.glob('chapter*') if os.path.isdir(d)],
    key=_chapter_sort_key
)
if not chapter_dirs:
    print("❌ 未找到任何章节目录（chapter*/）！")
    exit(1)

print(f"📚 发现 {len(chapter_dirs)} 个章节目录:")
md_content = ""
for d in chapter_dirs:
    md_files = sorted(glob.glob(os.path.join(d, '*.md')))
    if not md_files:
        print(f"   ⚠️  {d}/ （空目录，跳过）")
        continue
    for mf in md_files:
        with open(mf, 'r', encoding='utf-8') as f:
            chapter_text = f.read()
        md_content += chapter_text + "\n\n"
        print(f"   ✅ {mf}")

# ===== 2. 加载 Pygments CSS（代码语法高亮） =====
from pygments.formatters import HtmlFormatter
PYGMENTS_CSS = HtmlFormatter(style='tango').get_style_defs('.highlight')

# ===== 3. CSS 样式（删除了 xhtml2pdf 特有语法，使用标准 CSS） =====
CSS_STYLE = """
/* ===== 页面设置 ===== */
@page {
    size: A4;
    margin: 2.2cm;
}

body {
    font-family: "SimSun", "宋体", "Noto Serif SC", serif;
    font-size: 10.5pt;
    line-height: 1.35;
    color: #333333;
    max-width: 100%;
}

p {
    margin: 0 0 4pt 0;
}

/* ===== 标题颜色 ===== */
h1 {
    color: #1565C0;
    font-size: 18pt;
    border-bottom: 3px solid #1565C0;
    padding-bottom: 6pt;
    margin-top: 20pt;
    margin-bottom: 10pt;
    page-break-before: always;
}

h1:first-of-type {
    page-break-before: avoid;
}

h2 {
    color: #2E7D32;
    font-size: 14pt;
    margin-top: 14pt;
    margin-bottom: 8pt;
    padding-left: 10pt;
    border-left: 4px solid #2E7D32;
}

h3 {
    color: #E65100;
    font-size: 11.5pt;
    margin-top: 12pt;
    margin-bottom: 6pt;
}

h4 {
    color: #7B1FA2;
    font-size: 11pt;
    margin-top: 10pt;
    margin-bottom: 4pt;
    padding-left: 6pt;
    border-left: 3px solid #CE93D8;
}

/* ===== 定义框（蓝色） ===== */
.definitionbox {
    background: #E3F2FD;
    border-left: 5px solid #1565C0;
    border-radius: 5px;
    padding: 10pt 14pt;
    margin: 10pt 0;
    page-break-inside: avoid;
    break-inside: avoid;
}
.definitionbox .box-title {
    color: #1565C0;
    font-size: 11.5pt;
    font-weight: bold;
    margin-bottom: 4pt;
}

/* ===== 提示框（绿色） ===== */
.tipbox {
    background: #E8F5E9;
    border-left: 5px solid #2E7D32;
    border-radius: 5px;
    padding: 10pt 14pt;
    margin: 10pt 0;
    page-break-inside: avoid;
    break-inside: avoid;
}
.tipbox .box-title {
    color: #2E7D32;
    font-size: 11.5pt;
    font-weight: bold;
    margin-bottom: 4pt;
}

/* ===== 警告框（橙色） ===== */
.warningbox {
    background: #FFF3E0;
    border-left: 5px solid #E65100;
    border-radius: 5px;
    padding: 10pt 14pt;
    margin: 10pt 0;
    page-break-inside: avoid;
    break-inside: avoid;
}
.warningbox .box-title {
    color: #E65100;
    font-size: 11.5pt;
    font-weight: bold;
    margin-bottom: 4pt;
}

/* ===== 补充知识框（紫色） ===== */
.notebox {
    background: #F3E5F5;
    border-left: 5px solid #7B1FA2;
    border-radius: 5px;
    padding: 10pt 14pt;
    margin: 10pt 0;
    page-break-inside: avoid;
    break-inside: avoid;
}
.notebox .box-title {
    color: #7B1FA2;
    font-size: 11.5pt;
    font-weight: bold;
    margin-bottom: 4pt;
}

/* ===== 代码块 ===== */
pre {
    background: #FAFAFA;
    border: 1px solid #E0E0E0;
    border-left: 4px solid #1976D2;
    border-radius: 5px;
    padding: 10pt 12pt;
    font-family: "Consolas", "Courier New", "Source Code Pro", monospace;
    font-size: 9pt;
    line-height: 1.4;
    overflow-x: auto;
    margin: 10pt 0;
    white-space: pre-wrap;
    word-break: break-all;
    page-break-inside: avoid;
    break-inside: avoid;
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
    margin: 10pt 0;
    font-size: 10pt;
    page-break-inside: avoid;
    break-inside: avoid;
}

thead {
    background: #1976D2;
    color: white;
}

th {
    padding: 8pt 10pt;
    text-align: left;
    font-weight: bold;
}

td {
    padding: 6pt 10pt;
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
    margin: 12pt auto;
    border-radius: 5px;
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
    padding-left: 24pt;
    margin: 4pt 0;
}

li {
    margin: 2pt 0;
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

# ===== 3.5 生成目录页 =====
def _slugify(text):
    """将标题转换为 Python Markdown 兼容的锚点 ID"""
    import unicodedata
    text = text.lower().strip()
    text = ''.join(c for c in text if c.isalnum() or c in '-_ ')
    text = text.replace(' ', '-')
    return text.strip('-')

def _build_toc_html(md_text):
    """从 markdown 文本中提取标题并生成目录 HTML
    
    生成结构：
        第一部分：Python基础入门            （居中加粗）
        第1章：...                        （# 一级标题）
        1.1 ...                           （## 二级标题）
    """
    # 先用正则从全文提取各分部标题（可能跨多行）
    # 在文本中插入行内标记，后续逐行扫描时就能识别
    marked_text = md_text
    
    # 处理多行 div（第一部分~第三部分）
    multi_part = re.compile(
        r'<div[^>]*>\s*\n\s*(第[一二三四五]部分[：:]\S+)\s*\n\s*</div>',
        re.MULTILINE
    )
    marked_text = multi_part.sub(r'<!--PART_MARKER::\1-->', marked_text)
    
    # 处理单行 div（第四部分、第五部分、附录）
    single_part = re.compile(
        r'<div[^>]*>(第[一二三四五]部分[：:]\S+)</div>'
    )
    marked_text = single_part.sub(r'<!--PART_MARKER::\1-->', marked_text)
    
    single_appendix = re.compile(
        r'<div[^>]*>(附录)</div>'
    )
    marked_text = single_appendix.sub(r'<!--PART_MARKER::\1-->', marked_text)
    
    # 扫描结果
    entries = []
    
    for line in marked_text.split('\n'):
        line_stripped = line.strip()
        
        # 检查分部标题标记
        pm = re.match(r'<!--PART_MARKER::(.+)-->', line_stripped)
        if pm:
            entries.append(('part', pm.group(1), None))
            continue
        
        # 检查 markdown 标题（只取 # 和 ##）
        m = re.match(r'^(#{1,2})\s+(.+)$', line_stripped)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            
            if level == 1:
                # 章标题判断
                is_chapter = False
                if re.match(r'^(第\d+章|附录[A-Z])', title):
                    is_chapter = True
                elif title in ('2. 第一个Python程序', '3. Python基础语法'):
                    is_chapter = True
                
                if is_chapter:
                    anchor = _slugify(title)
                    entries.append(('chapter', title, anchor))
            elif level == 2:
                # 节标题：以 "N.N" 开头（如 1.1, 12.3）
                if re.match(r'^\d+\.\d+\s', title):
                    anchor = _slugify(title)
                    entries.append(('section', title, anchor))
    
    return entries

toc_entries = _build_toc_html(md_content)

# 生成带锚点链接的目录 HTML
toc_html_parts = []
toc_html_parts.append('<div style="page-break-after: always;">')
toc_html_parts.append('<h1 style="text-align: center; border-bottom: none; font-size: 22pt;">目  录</h1>')
toc_html_parts.append('<div style="margin-top: 20pt;">')

for entry_type, title, anchor in toc_entries:
    if entry_type == 'part':
        # 分部标题——居中、加粗、蓝色
        toc_html_parts.append(
            f'<p style="text-align: center; font-size: 13pt; font-weight: bold; color: #1565C0; '
            f'margin: 18pt 0 10pt 0; padding: 8pt 0; '
            f'border-top: 2px solid #BBDEFB; border-bottom: 2px solid #BBDEFB;">{title}</p>'
        )
    elif entry_type == 'chapter':
        # 章标题——加粗，可点击跳转
        toc_html_parts.append(
            f'<p style="font-size: 11pt; font-weight: bold; margin: 10pt 0 4pt 0;">'
            f'<a href="#{anchor}" style="color: #333; text-decoration: none;">{title}</a></p>'
        )
    elif entry_type == 'section':
        # 节标题——缩进，可点击跳转
        toc_html_parts.append(
            f'<p style="font-size: 10pt; margin: 2pt 0 2pt 24pt; color: #555;">'
            f'<a href="#{anchor}" style="color: #555; text-decoration: none;">{title}</a></p>'
        )

toc_html_parts.append('</div></div>')
TOC_HTML = '\n'.join(toc_html_parts)

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
<title>Python：2周从入门到精通</title>
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
{TOC_HTML}
{html_body}
</body>
</html>"""

OUTPUT_NAME = '极简Python_从入门到精通'

# ===== 8. 输出 HTML 文件 =====
html_path = f'{OUTPUT_NAME}.html'
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(FULL_HTML)
print(f"✅ HTML 已生成: {html_path}")

# ===== 9. 用 Edge/Chrome 无头模式打印 PDF =====
pdf_path = os.path.abspath(f'{OUTPUT_NAME}.pdf')
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
    print(f"   请手动用浏览器打开 {html_path}，然后 Ctrl+P 另存为 PDF")
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
        print(f"✅ PDF 已生成: {OUTPUT_NAME}.pdf ({file_size / 1024:.1f} KB)")
        print("   请打开查看，中文应该完美显示！")
    else:
        print(f"❌ PDF 生成失败 (exit code: {result.returncode})")
        if result.stderr:
            print(f"   错误: {result.stderr[:500]}")
        print(f"   请手动用浏览器打开 {html_abs}，然后 Ctrl+P → 另存为 PDF")