## 9.4 JSON/CSV 文件处理——结构化数据的"通用语"

纯文本文件（如 `.txt`）适合存简单的字符串，但不适合存结构化数据——比如一份包含姓名、年龄、成绩的学生名单，存成文本后解析起来很麻烦。JSON 和 CSV 是两种通用的结构化数据格式，几乎所有编程语言和工具都支持它们。本节把它们放在一起讲，因为在实际项目中，你几乎总会在其中二选一。

### 9.4.1 JSON 深度实战——嵌套结构与文件交互

JSON（JavaScript Object Notation）是 Web 时代的"通用数据语"。它的语法和 Python 的字典/列表高度相似，但它是一种文本格式，可以被任何语言解析。

**Python ↔ JSON 的类型映射：**

| Python | JSON |
|:-------|:-----|
| `dict` | object（`{}`） |
| `list` / `tuple` | array（`[]`） |
| `str` | string（`""`） |
| `int` / `float` | number |
| `True` / `False` | `true` / `false` |
| `None` | `null` |

**读取和写入 JSON：**

```python
import json

# 写入 JSON 文件
data = {
    "title": "极简Python",
    "chapters": 10,
    "topics": ["基础语法", "函数", "面向对象", "文件操作"],
    "metadata": {
        "author": "Python学习者",
        "version": "1.0"
    }
}

with open("book.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 读取 JSON 文件
with open("book.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)

print(loaded["title"])                  # 极简Python
print(loaded["topics"][0])              # 基础语法
print(loaded["metadata"]["author"])     # Python学习者
```

几个参数的含义：
- `ensure_ascii=False`：允许直接输出中文，而不是转义成 `\uXXXX` 的形式
- `indent=2`：缩进 2 个空格，让 JSON 文件人类可读——不加这个参数的话，所有内容会挤在一行

**处理 JSON 字符串（不涉及文件）：**

```python
json_str = json.dumps(data, ensure_ascii=False, indent=2)    # Python → JSON 字符串
parsed = json.loads(json_str)                                 # JSON 字符串 → Python
```

---

\begin{tipbox}
**JSON 的局限性**

JSON 虽然通用，但只支持六种基本数据类型（对象、数组、字符串、数字、布尔值、null）。这意味着：
- `datetime` 对象需要转成字符串才能存（如 `"2026-01-15"`）
- `tuple` 会被转成 `list`——读取回来不再是元组
- `set` 不能直接存，需要先转成 `list`
- 自定义对象需要先序列化成字典

这些局限性在大多数应用场景下不是问题——你只需要在读写时做一层简单的转换即可。
\end{tipbox}

---

### 9.4.2 CSV 文件——表格数据的"通用格式"

CSV（Comma-Separated Values，逗号分隔值）是一种更"表格化"的格式——每一行是一条记录，每一列由逗号分隔。它可以在 Excel、Google Sheets 和任何文本编辑器中打开，是数据分析领域最常用的数据交换格式。

**使用 `csv` 模块读取 CSV：**

```python
import csv

with open("students.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    headers = next(reader)        # 第一行通常是表头
    print(f"表头：{headers}")

    for row in reader:
        name, age, score = row
        print(f"{name}，{age} 岁，成绩 {score}")
```

**使用 `csv` 模块写入 CSV：**

```python
import csv

headers = ["姓名", "年龄", "成绩"]
students = [
    ["小明", 18, 88],
    ["小红", 17, 92],
    ["小刚", 19, 76],
]

with open("students.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(headers)           # 写入表头
    writer.writerows(students)         # 批量写入数据行
```

注意 `newline=""` 这个参数——在 Windows 上如果不加，CSV 文件中会出现多余的空行。这是一个历史遗留问题，但养成每次都写的习惯可以省去不必要的困扰。

**使用 `DictReader` 和 `DictWriter`——按列名而非索引访问：**

当 CSV 的列很多时，用 `row[0]`、`row[1]` 这种数字索引会让人忘记每个数字代表什么。`DictReader` 用列名（表头）作为键，让代码清晰得多：

```python
import csv

# 读取——用列名访问
with open("students.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['姓名']}的成绩是{row['成绩']}分")
        # 而不是 row[0], row[2]——可读性大幅提升

# 写入——用字典表示每一行
data = [
    {"姓名": "小李", "年龄": 18, "成绩": 94},
    {"姓名": "小王", "年龄": 19, "成绩": 81},
]

with open("students.csv", "w", encoding="utf-8", newline="") as f:
    fieldnames = ["姓名", "年龄", "成绩"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()               # 自动写入表头
    writer.writerows(data)             # 批量写入
```

### 9.4.3 JSON vs CSV——如何选择？

| 维度 | JSON | CSV |
|:-----|:-----|:----|
| 数据结构 | 支持嵌套（对象里套数组） | 只有扁平表格（行×列） |
| 人类可读 | 良好——有缩进时 | 良好——表格结构直观 |
| 文件大小 | 较大——键名重复出现 | 紧凑——没有键名 |
| Excel 兼容 | 不直接兼容 | 直接双击就能打开 |
| 适用场景 | API 数据交换、配置文件、嵌套数据 | 数据分析、表格导出、数据库导入 |
| Python 模块 | `json` | `csv` |

一句话总结：
- 数据是**表格型、扁平、需要进 Excel** → CSV
- 数据是**嵌套型、层级型、API 交互** → JSON

### 9.4.4 实战练习

1. 创建一个名为 `config.json` 的配置文件，包含以下内容并用 Python 读取后打印每个值：

```json
{
    "app_name": "我的应用",
    "version": "2.0",
    "settings": {
        "theme": "dark",
        "language": "zh-CN",
        "auto_save": true
    }
}
```

2. 编写程序，将一个包含学生成绩的字典列表写入 `scores.csv` 文件（使用 `DictWriter`），表头为 `["姓名", "语文", "数学", "英语"]`。写入后，用 `DictReader` 读回数据并计算每位学生的平均分。

3. 你正在做一个数据导出功能，需要支持两种导出格式。请思考：什么情况下应该给用户 JSON 格式的导出，什么情况下应该给 CSV 格式？各举一个实际场景。