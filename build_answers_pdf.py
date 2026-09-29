"""习题答案 → PDF 生成脚本
扫描 answers/ 目录下的章节文件夹，合并生成答案合集 PDF
"""

import markdown
import os
import glob
import subprocess
import shutil

# ===== 1. 扫描 answers/ 目录 =====
if not os.path.isdir('answers'):
    print("❌ 未找到 answers/ 目录！")
    exit(1)

chapter_dirs = sorted([d for d in glob.glob('answers/*') if os.path.isdir(d)])
if not chapter_dirs:
    print("❌ answers/ 目录下没有章节文件夹！")
    exit(1)

print(f"📚 发现 {len(chapter_dirs)} 个答案章节目录:")
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

if not md_content.strip():
    print("❌ 没有任何答案内容！")
    exit(1)

# ===== 2. Pygments CSS =====
from pygments.formatters import HtmlFormatter
PYGMENTS_CSS = HtmlFormatter(style='tango').get_style_defs('.highlight')

# ===== 3. CSS（与主书一致） =====
CSS_STYLE = """
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

p { margin: 0 0 4pt 0; }

h1 {
    color: #1565C0;
    font-size: 18pt;
    border-bottom: 3px solid #1565C0;
    padding-bottom: 6pt;
    margin-top: 20pt;
    margin-bottom: 10pt;
    page-break-before: always;
}

h1:first-of-type { page-break-before: avoid; }

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

table {
    width: 100%;
    border-collapse: collapse;
    margin: 10pt 0;
    font-size: 10pt;
    page-break-inside: avoid;
    break-inside: avoid;
}

thead { background: #1976D2; color: white; }
th { padding: 8pt 10pt; text-align: left; font-weight: bold; }
td { padding: 6pt 10pt; border-bottom: 1px solid #E0E0E0; }
tbody tr:nth-child(odd) { background: #FAFAFA; }

ul, ol { padding-left: 24pt; margin: 4pt 0; }
li { margin: 2pt 0; }

strong { color: #1565C0; }
em { color: #E65100; }

pre:not(.highlight) {
    border-left: 4px solid #2E7D32;
}
"""

# ===== 4. Markdown → HTML =====
html_body = markdown.markdown(
    md_content,
    extensions=[
        'markdown.extensions.fenced_code',
        'markdown.extensions.tables',
        'markdown.extensions.codehilite',
    ],
    extension_configs={
        'markdown.extensions.codehilite': {
            'css_class': 'highlight',
            'guess_lang': True,
        },
    }
)

# ===== 5. 完整 HTML =====
FULL_HTML = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>极简Python · 习题答案</title>
<style>
{CSS_STYLE}
{PYGMENTS_CSS}
</style>
</head>
<body>
<h1>极简Python：从入门到精通 · 习题答案</h1>
{html_body}
</body>
</html>"""

OUTPUT_NAME = '极简Python_习题答案'

html_path = f'{OUTPUT_NAME}.html'
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(FULL_HTML)
print(f"✅ HTML 已生成: {html_path}")

# ===== 6. 浏览器渲染 PDF =====
pdf_path = os.path.abspath(f'{OUTPUT_NAME}.pdf')
html_abs = os.path.abspath(html_path)
file_url = f'file:///{html_abs.replace(chr(92), "/")}'

print("正在用浏览器渲染 PDF...")

engines = [
    {'paths': [r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
               r'C:\Program Files\Microsoft\Edge\Application\msedge.exe'], 'name': 'Microsoft Edge'},
    {'paths': [r'C:\Program Files\Google\Chrome\Application\chrome.exe',
               r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'], 'name': 'Google Chrome'},
]

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
    for cmd in ['msedge', 'chrome']:
        found = shutil.which(cmd)
        if found:
            browser_path = found
            browser_name = cmd
            break

if not browser_path:
    print(f"❌ 未找到浏览器！请手动打开 {html_abs} → Ctrl+P → 另存为 PDF")
else:
    print(f"   使用 {browser_name}")
    cmd = [
        browser_path, '--headless=new', '--disable-gpu',
        f'--print-to-pdf={pdf_path}', '--no-pdf-header-footer', file_url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=60)
    if result.returncode == 0 and os.path.exists(pdf_path):
        file_size = os.path.getsize(pdf_path)
        print(f"✅ PDF 已生成: {OUTPUT_NAME}.pdf ({file_size / 1024:.1f} KB)")
    else:
        print(f"❌ PDF 生成失败 (exit code: {result.returncode})")
        print(f"   请手动打开 {html_abs} → Ctrl+P → 另存为 PDF")