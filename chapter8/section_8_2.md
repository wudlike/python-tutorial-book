## 8.2 常用标准库介绍——Python 自带的"瑞士军刀"

Python 的哲学是"自带电池"（Batteries Included）——安装 Python 时就附带了大量实用的标准库，覆盖文件操作、系统交互、数学计算、时间处理、数据序列化等方方面面。了解这些内置工具，能让你在绝大多数场景下不需要安装第三方包就能高效完成任务。

### 8.2.1 `os`——与操作系统对话

`os` 模块提供了与操作系统交互的能力——创建和删除目录、遍历文件、获取环境变量等：

```python
import os

print(os.getcwd())                        # 获取当前工作目录
print(os.listdir("."))                    # 列出当前目录下的所有文件和文件夹

os.makedirs("test/subdir", exist_ok=True)  # 递归创建目录（exist_ok=True 表示已存在也不报错）

print(os.path.join("data", "config.json"))    # data/config.json——跨平台的路径拼接
print(os.path.dirname("/home/user/file.txt"))  # /home/user——取父目录
print(os.path.basename("/home/user/file.txt")) # file.txt——取文件名
print(os.path.splitext("data.csv"))            # ('data', '.csv')——拆分扩展名

print(os.environ.get("PATH", "未设置"))      # 获取环境变量，不存在时返回默认值
```

关于路径拼接，强烈建议使用 `os.path.join()` 而不是手动用 `"/"` 或 `"\"` 拼接。因为 Windows 用反斜杠、Linux/macOS 用正斜杠——`os.path.join()` 自动适配当前操作系统，保证路径正确。

### 8.2.2 `sys`——与 Python 解释器对话

`sys` 模块让你访问 Python 解释器自身的变量和功能：

```python
import sys

print(sys.version)             # Python 版本信息
print(sys.platform)            # 操作系统平台（'win32', 'darwin', 'linux'）

# 命令行参数——运行 python script.py hello world 时：
print(sys.argv)                # ['script.py', 'hello', 'world']

# 模块搜索路径——Python 从这些路径中查找导入的模块
print(sys.path[:3])            # 前三个搜索路径
```

`sys.argv` 特别实用——它是程序接收命令行参数的入口。假设你写了一个脚本，希望用户通过命令行指定输入文件和输出文件，就从 `sys.argv` 中拿。`sys.path` 则在调试导入问题时很有用——如果 Python 找不到你的模块，检查一下 `sys.path` 里有没有包含你的文件所在目录。

### 8.2.3 `math`——数学工具箱

```python
import math

print(math.pi)                 # 3.141592653589793——圆周率
print(math.e)                  # 2.718281828459045——自然常数
print(math.sqrt(25))           # 5.0——平方根
print(math.ceil(3.2))          # 4——向上取整
print(math.floor(3.8))         # 3——向下取整
print(math.factorial(5))       # 120——阶乘（5!）
print(math.gcd(36, 48))        # 12——最大公约数
print(math.radians(180))       # 3.14159...——角度转弧度
print(math.degrees(math.pi))   # 180.0——弧度转角度
```

### 8.2.4 `datetime`——时间的精确操控

处理日期和时间是编程中的高频需求，`datetime` 模块提供了类丰富的工具：

```python
from datetime import datetime, date, timedelta

# 当前时间
now = datetime.now()
print(f"当前时间：{now}")                        # 2026-01-15 14:30:45.123456
print(f"格式化：{now.strftime('%Y年%m月%d日 %H:%M:%S')}")  # 2026年01月15日 14:30:45

# 创建指定日期
birthday = datetime(2000, 6, 15)
print(f"生日：{birthday.strftime('%Y-%m-%d')}")  # 2000-06-15

# 时间计算——timedelta
today = date.today()
next_week = today + timedelta(weeks=1)
print(f"一周后：{next_week}")

days_passed = (today - date(2000, 1, 1)).days
print(f"从 2000 年元旦到今天，过了 {days_passed} 天")

# 解析日期字符串
d = datetime.strptime("2026-09-30", "%Y-%m-%d")
print(f"解析结果：{d}")
```

`strftime` 和 `strptime` 是两个方向相反的操作：前者把日期对象格式化成字符串，后者把字符串解析成日期对象。它们的格式代码相同——`%Y` 是四位年份，`%m` 是月份，`%d` 是日期。完整列表可查阅 Python 官方文档。

---

\begin{notebox}
**`%Y` 还是 `%y`？**

- `%Y`：四位年份，如 `2026`
- `%y`：两位年份，如 `26`

很多 bug 来源于混淆了这两个格式符——比如把 `%Y-%m-%d` 写成 `%y-%m-%d` 会导致年份只显示后两位。建议始终用 `%Y`。
\end{notebox}

---

### 8.2.5 `json`——数据的通用语言

JSON（JavaScript Object Notation）是目前最通用的数据交换格式，几乎所有编程语言都支持。Python 的 `json` 模块让序列化和反序列化变得极其简单：

```python
import json

# Python 对象 → JSON 字符串（序列化）
data = {
    "name": "小明",
    "age": 20,
    "courses": ["语文", "数学", "英语"],
    "graduated": False
}
json_str = json.dumps(data, ensure_ascii=False, indent=2)
print(json_str)

# JSON 字符串 → Python 对象（反序列化）
json_text = '{"name": "小红", "age": 19, "score": 95}'
person = json.loads(json_text)
print(person["name"])      # 小红
print(type(person))        # <class 'dict'>

# 文件读写
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)      # 写入文件

with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)                                  # 从文件读取
    print(loaded["name"])                                  # 小明
```

`ensure_ascii=False` 确保中文正常显示（否则中文会被转成 `\uXXXX` 的 Unicode 转义形式），`indent=2` 让 JSON 输出带有缩进和换行，便于人类阅读。

### 8.2.6 `random`——给程序加点"不确定性"

```python
import random

random.seed(42)                # 设置随机种子——让"随机"可复现（调试时非常有用）

print(random.random())         # 0.6394...——[0, 1) 之间的随机浮点数
print(random.randint(1, 10))   # 5——[1, 10] 之间的随机整数
print(random.choice(["苹果", "香蕉", "橘子"]))  # 香蕉——随机选一个
print(random.sample(range(1, 50), 6))   # [8, 15, 23, 34, 42, 47]——不重复地抽 6 个

items = [1, 2, 3, 4, 5]
random.shuffle(items)          # 原地打乱顺序
print(items)                   # [3, 1, 5, 2, 4]
```

`random.seed()` 是调试时的秘密武器。设置了相同的种子值，每次运行程序得到的"随机"序列完全相同——你可以在保留随机性的同时让 bug 稳定复现。

### 8.2.7 `collections`——增强版的数据结构

`collections` 模块提供了比内置数据结构更强大的变体。最常用的三个：

```python
from collections import Counter, defaultdict, namedtuple

# Counter——计数器
words = ["apple", "banana", "apple", "orange", "banana", "apple"]
word_count = Counter(words)
print(word_count)                         # Counter({'apple': 3, 'banana': 2, 'orange': 1})
print(word_count.most_common(2))          # [('apple', 3), ('banana', 2)]——出现最多的前 2 个

# defaultdict——带默认值的字典
students_by_city = defaultdict(list)       # 访问不存在的键时自动创建空列表
students_by_city["北京"].append("小明")
students_by_city["北京"].append("小红")
students_by_city["上海"].append("小刚")
print(dict(students_by_city))             # {'北京': ['小明', '小红'], '上海': ['小刚']}

# namedtuple——有名字的元组
Point = namedtuple("Point", ["x", "y"])
p = Point(10, 20)
print(p.x, p.y)               # 10 20——像对象一样用属性访问
print(p[0], p[1])              # 10 20——也保留了元组的索引访问
```

`defaultdict` 是实战中非常趁手的工具。以前你需要先检查键是否存在再操作，现在直接 `append` 就行——不存在的键会自动初始化成你指定的默认值类型。

### 8.2.8 其他值得了解的标准库

| 模块 | 一句话用途 |
|:-----|:----------|
| `re` | 正则表达式——复杂的文本模式匹配和替换 |
| `pathlib` | 面向对象的路径操作（比 `os.path` 更现代） |
| `csv` | 读写 CSV 文件 |
| `sqlite3` | 轻量级数据库——无需安装数据库软件 |
| `argparse` | 命令行参数解析——比 `sys.argv` 更强大 |
| `logging` | 专业日志记录——比 `print` 调试靠谱一百倍 |
| `itertools` | 高效迭代器工具——排列组合、无限迭代等 |
| `functools` | 高阶函数工具——缓存、偏函数、`total_ordering` 等 |

### 8.2.9 实战练习

1. 使用 `os` 模块写一段代码：列出当前目录下所有 `.py` 文件，并输出它们的文件名（不含扩展名）。

2. 使用 `datetime` 模块编写函数 `days_until_new_year()`，计算距离下一个元旦（1 月 1 日）还有多少天。如果当天恰好是元旦，输出 `"今天是元旦！"`。

3. 使用 `json` 模块：创建字典 `{"任务": ["学Python", "写代码", "做项目"]}`，写入文件 `tasks.json`，然后从文件中读回数据并打印。