## 11.4 re 正则表达式——文本处理的"瑞士军刀"

如果你曾经手动在一大段文本里找邮箱地址、验证手机号格式、或者从 HTML 中提取数据，你一定体会过"肉眼扫描"的低效。正则表达式（Regular Expression，简称 regex）就是为解决这类问题而生的——它是一种描述字符串模式的微型语言，可以在几行代码内完成"提取、匹配、替换、拆分"等复杂的文本处理任务。

Python 的 `re` 模块提供了完整的正则表达式支持。正则入门有一定陡峭度，但一旦突破，它将成为你文本处理工具箱中最锋利的武器。

### 11.4.1 基础匹配——从字面到元字符

最简单的正则表达式就是普通字符串本身——它只匹配完全相同的文本：

```python
import re

text = "Python is powerful. Python is elegant."

# search —— 找到第一个匹配
match = re.search(r"Python", text)
if match:
    print(f"找到：{match.group()}，位置：{match.start()}-{match.end()}")
    # 找到：Python，位置：0-6

# findall —— 找到所有匹配，返回列表
matches = re.findall(r"Python", text)
print(f"所有匹配：{matches}")                       # ['Python', 'Python']
print(f"出现了 {len(matches)} 次")

# match —— 只从字符串开头匹配（不常用）
print(re.match(r"Python", text))                     # 匹配（开头是 Python）
print(re.match(r"powerful", text))                   # None（开头不是 powerful）
```

真正的威力来自**元字符**——有特殊含义的符号：

```python
import re

# . —— 匹配除换行符外的任意单个字符
print(re.findall(r"P.th.n", "Python Pythan Pythqn"))    # ['Python', 'Pythan', 'Pythqn']

# ^ —— 字符串开头
# $ —— 字符串结尾
print(re.findall(r"^Hello", "Hello World\nHello"))      # ['Hello']（只匹配开头那个）
print(re.findall(r"end$", "the end is the end"))        # ['end']（只匹配结尾那个）

# \d —— 任意数字（等价于 [0-9]）
# \w —— 字母、数字、下划线（等价于 [a-zA-Z0-9_]）
# \s —— 空白字符（空格、tab、换行）
print(re.findall(r"\d+", "房间号 301 和 502"))           # ['301', '502']
print(re.findall(r"\w+", "user_123 你好 ab-cd"))         # ['user_123', '你好', 'ab', 'cd']

# \b —— 单词边界（零宽断言，不消耗字符）
print(re.findall(r"\bcat\b", "cat catalog bobcat cat"))  # ['cat', 'cat']（只匹配独立的 cat）
```

### 11.4.2 量词——控制重复次数

| 符号 | 含义 | 示例 |
|:-----|:-----|:-----|
| `*` | 0 次或多次 | `a*` 匹配 `""`、`"a"`、`"aaa"` |
| `+` | 1 次或多次 | `a+` 匹配 `"a"`、`"aaa"`，但不匹配 `""` |
| `?` | 0 次或 1 次 | `a?` 匹配 `""` 或 `"a"` |
| `{n}` | 恰好 n 次 | `a{3}` 匹配 `"aaa"` |
| `{n,}` | 至少 n 次 | `a{3,}` 匹配 `"aaa"`、`"aaaa"`…… |
| `{n,m}` | n 到 m 次 | `a{2,4}` 匹配 `"aa"`、`"aaa"`、`"aaaa"` |

```python
import re

# 实用：匹配手机号、身份证号等的长度约束
print(re.findall(r"\d{11}", "电话：13800138000，备用：13912345678"))
# ['13800138000', '13912345678']

print(re.findall(r"\d{3,4}", "区号：010 和 0755"))      # ['010', '0755']

# 量词的贪婪匹配 —— 默认尽可能多匹配
print(re.findall(r"<.*>", "<p>段落1</p><p>段落2</p>"))
# ['<p>段落1</p><p>段落2</p>'] —— 整个被吞了！因为 .* 贪婪

# 量词的非贪婪匹配 —— 加 ? 变"尽可能少"
print(re.findall(r"<.*?>", "<p>段落1</p><p>段落2</p>"))
# ['<p>', '</p>', '<p>', '</p>'] —— 每次只匹配最短的标签
```

**贪婪匹配是最常见的坑。** 默认量词 `*` `+` 会尽可能多地"吞噬"字符。在后面加一个 `?` 变成 `*?` `+?`，就切换为"非贪婪模式"——匹配尽可能少的字符。当你发现正则在"吃太多"的时候，第一个想到的就应该是加 `?`。

### 11.4.3 字符类——一组字符中任选一个

```python
import re

# [abc] —— a、b、c 中的任意一个
print(re.findall(r"[aeiou]", "Hello World"))          # ['e', 'o', 'o']

# [a-z] —— 从 a 到 z 的任意字母
# [0-9] —— 从 0 到 9 的任意数字
print(re.findall(r"[a-z]+", "Hello123 World456"))     # ['ello', 'orld']

# [^abc] —— 除了 a、b、c 之外的任意字符
print(re.findall(r"[^0-9]", "a1b2c3"))               # ['a', 'b', 'c']

# 实用：匹配中文
print(re.findall(r"[\u4e00-\u9fff]+", "Hello 你好 世界 World"))
# ['你好', '世界']

# 实用：匹配十六进制颜色代码
print(re.findall(r"#[0-9a-fA-F]{6}", "背景 #FFFFFF，前景 #333333"))
# ['#FFFFFF', '#333333']
```

### 11.4.4 分组与捕获——提取匹配中的"零件"

用括号 `()` 将模式的一部分括起来，就创建了一个"分组"。`findall()` 在有分组时的行为会改变——不再返回完整的匹配，而是返回各组捕获内容的元组：

```python
import re

text = "姓名：张三，电话：13800138000；姓名：李四，电话：13912345678"

# 分组捕获——提取姓名和电话
pattern = r"姓名：(\w+)，电话：(\d{11})"
matches = re.findall(pattern, text)
print(matches)    # [('张三', '13800138000'), ('李四', '13912345678')]

# 分别取出
for name, phone in matches:
    print(f"{name} 的电话是 {phone}")

# search() + group() —— 更精确的控制
match = re.search(r"姓名：(\w+)，电话：(\d{11})", text)
if match:
    print(f"完整匹配：{match.group(0)}")    # 姓名：张三，电话：13800138000
    print(f"姓名：{match.group(1)}")         # 张三
    print(f"电话：{match.group(2)}")         # 13800138000

# 命名分组 —— (?P<name>...)
pattern = r"姓名：(?P<name>\w+)，电话：(?P<phone>\d{11})"
match = re.search(pattern, text)
if match:
    print(f"姓名：{match.group('name')}")
    print(f"电话：{match.group('phone')}")
```

### 11.4.5 `re.sub()`——查找并替换

```python
import re

text = "我的电话是 138-0013-8000，请勿外传"

# 将电话号码中间四位替换为 ****
masked = re.sub(r"(\d{3})-(\d{4})-(\d{4})", r"\1-****-\3", text)
print(masked)    # 我的电话是 138-****-8000，请勿外传

# \1 \2 \3 分别引用第 1、2、3 个捕获组的内容

# 使用函数作为替换内容——更灵活
def mask_phone(match):
    """把中间四位替换为 *"""
    return f"{match.group(1)}-****-{match.group(3)}"

masked2 = re.sub(r"(\d{3})-(\d{4})-(\d{4})", mask_phone, text)
print(masked2)    # 我的电话是 138-****-8000，请勿外传

# 实用：清理多余空白
dirty = "这   是   一段   混乱的  文本"
clean = re.sub(r"\s+", " ", dirty).strip()
print(clean)    # 这 是 一段 混乱的 文本

# 实用：移除 HTML 标签
html = "<p>这是<b>粗体</b>文本</p>"
plain = re.sub(r"<[^>]+>", "", html)
print(plain)    # 这是粗体文本
```

### 11.4.6 `re.split()`——比 `str.split()` 更强大的拆分

```python
import re

# str.split() 只能按一个固定字符串拆分
text = "苹果, 香蕉; 橘子  葡萄|西瓜"
print(text.split(","))    # ['苹果', ' 香蕉; 橘子  葡萄|西瓜'] —— 只拆了逗号

# re.split() 可以按模式拆分——多种分隔符一次搞定
result = re.split(r"[,;|\s]+", text)
result = [x for x in result if x]    # 过滤空字符串
print(result)    # ['苹果', '香蕉', '橘子', '葡萄', '西瓜']

# 实用：按句子拆分英文文本
paragraph = "Hello! How are you? I'm fine. Thanks."
sentences = re.split(r"[.!?]\s*", paragraph)
sentences = [s for s in sentences if s]
print(sentences)    # ['Hello', 'How are you', "I'm fine", 'Thanks']
```

### 11.4.7 编译正则——提升性能

每次调用 `re.search()`、`re.findall()` 时，Python 会在内部把正则字符串编译为"模式对象"。如果你在循环中反复使用同一个正则表达式（如处理百万行日志），重复编译会造成不必要的开销。预编译可以避免这种浪费：

```python
import re
import time

# 预编译——模式对象可以反复使用
email_pattern = re.compile(r"[\w.-]+@[\w.-]+\.\w+")

# 使用模式对象的方法——比 re.xxx() 快
emails = email_pattern.findall("联系 developer@example.com 或 admin@site.org")
print(emails)    # ['developer@example.com', 'admin@site.org']

# 性能对比
texts = ["user_{}@example.com".format(i) for i in range(100000)]
pattern = re.compile(r"user_\d+@example\.com")

start = time.perf_counter()
for t in texts:
    pattern.match(t)                    # 预编译
print(f"预编译耗时：{time.perf_counter() - start:.4f}s")

start = time.perf_counter()
for t in texts:
    re.match(r"user_\d+@example\.com", t)  # 每次编译
print(f"动态编译耗时：{time.perf_counter() - start:.4f}s")
```

### 11.4.8 常用正则"配方"

```python
import re

# 邮箱地址
email_re = re.compile(r"[\w.-]+@[\w.-]+\.\w+")

# 手机号（中国大陆，简化版）
phone_re = re.compile(r"1[3-9]\d{9}")

# URL
url_re = re.compile(r"https?://[^\s]+")

# IPv4 地址（简单版）
ip_re = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")

# 日期（YYYY-MM-DD）
date_re = re.compile(r"\d{4}-\d{2}-\d{2}")

# 从日志中提取时间、级别和消息
log_re = re.compile(
    r"(?P<time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) "
    r"(?P<level>INFO|WARN|ERROR) "
    r"(?P<message>.+)"
)

log_line = "2024-06-29 14:30:45 ERROR 数据库连接失败"
match = log_re.match(log_line)
if match:
    print(f"时间：{match['time']}")
    print(f"级别：{match['level']}")
    print(f"消息：{match['message']}")
```

### 11.4.9 实战练习

1. **身份证提取**：给定一段文本，用正则表达式提取其中所有的18位身份证号码（假设前17位是数字，最后一位是数字或X）。测试文本：`"张三 110101199001011234，李四 32010219851215789X，不是身份证的 123456789012345678"`

2. **格式化清理**：编写一个函数 `clean_text(text)`，使用正则表达式做三件事：
   - 把所有连续空白（空格、tab、换行）替换为一个空格
   - 去掉所有的 HTML 标签（`<...>`）
   - 把中文和英文/数字之间插入一个空格（如 `"Python3.9版本"` → `"Python 3.9 版本"`）

3. **日志解析器**：以下是一条 Nginx 访问日志的格式。编写正则表达式解析出 IP、时间、请求方法、请求路径、状态码五个字段：

```text
192.168.1.100 - - [29/Jun/2024:14:30:45 +0800] "GET /api/users HTTP/1.1" 200 1234
```

测试你的正则表达式能否正确提取各字段的值。