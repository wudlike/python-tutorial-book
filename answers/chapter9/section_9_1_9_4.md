## 9.1 文件的读写操作

### 练习1：水果列表

**答案：**

```python
fruits = ["苹果", "香蕉", "橘子", "葡萄", "西瓜"]

with open("fruits.txt", "w", encoding="utf-8") as f:
    for fruit in fruits:
        f.write(fruit + "\n")

with open("fruits.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)
```

**输出：**

```text
苹果
香蕉
橘子
葡萄
西瓜
```

---

### 练习2：文件复制

**答案：**

```python
with open("source.txt", "r", encoding="utf-8") as src:
    with open("destination.txt", "w", encoding="utf-8") as dst:
        for line in src:               # 逐行迭代，不一次性加载整个文件
            dst.write(line)

print("文件复制完成")
```

**解析：** `for line in src` 每次只读取一行到内存中，处理完就丢弃。即使 `source.txt` 有 10GB，这段代码也只用了一行字符串的内存。

---

### 练习3：修正代码

**原代码问题：**

1. 意图是"追加"（append），但用了 `"w"` 模式——会清空 `data.txt` 的已有内容
2. `f.write()` 没有加 `"\n"` 换行符——三行内容会挤成一行：`"第一行第二行第三行"`

**修正：**

```python
with open("data.txt", "a", encoding="utf-8") as f:    # "a" 追加模式
    f.write("第一行\n")                                 # 加换行符
    f.write("第二行\n")
    f.write("第三行\n")
```


## 9.2 异常处理机制

### 练习1：safe_float_input

**答案：**

```python
def safe_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("输入无效，请输入一个数字（如 3.14）")

number = safe_float_input("请输入一个数字：")
print(f"你输入的是：{number}")
```

**解析：** `while True` 无限循环，只有成功执行 `return` 才会退出。`float()` 在遇到非数字输入时会抛出 `ValueError`，被 `except` 捕获后打印提示并继续循环。

---

### 练习2：read_file_safe

**答案：**

```python
def read_file_safe(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"文件不存在：{filepath}")
        return None
    except PermissionError:
        print(f"没有权限读取文件：{filepath}")
        return None
    except Exception as e:
        print(f"未知错误：{e}")
        raise          # 重新抛出，让调用方也知道出事了

content = read_file_safe("nonexistent.txt")
print(content)         # None
```

---

### 练习3：修正异常处理

**原代码的三个问题：**

1. `except:` ——光秃秃的 except 会捕获一切，包括 `KeyboardInterrupt`（Ctrl+C），导致用户无法正常终止程序
2. 错误信息太笼统——"出错了"无法帮助用户或开发者定位问题
3. 没有区分不同类型的错误——`ValueError`（输入不是数字）和 `ZeroDivisionError`（除数为零）性质完全不同，应该给出不同的提示

**修正：**

```python
try:
    num = int(input("请输入一个数字："))
    result = 100 / num
    print(f"结果：{result}")
except ValueError:
    print("输入错误：请输入一个有效的整数")
except ZeroDivisionError:
    print("数学错误：不能除以零，请重新运行")
```


## 9.3 上下文管理器

### 练习1：FileLogger

**答案：**

```python
class FileLogger:
    def __init__(self, filepath):
        self.filepath = filepath
        self.file = None

    def __enter__(self):
        self.file = open(self.filepath, "a", encoding="utf-8")
        return self.file        # as 后面的变量就是这个文件对象

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        return False             # 不压制异常

with FileLogger("app.log") as log:
    log.write("程序启动\n")
    log.write("处理数据中...\n")

# 验证写入的内容
with open("app.log", "r", encoding="utf-8") as f:
    print(f.read())
```

**输出：**

```text
程序启动
处理数据中...
```

**解析：** `__enter__` 打开文件并返回文件对象给 `as log`。`with` 块中的代码写入后，`__exit__` 自动关闭文件——无论写入过程中是否抛异常。

---

### 练习2：temp_dir 上下文管理器

**答案：**

```python
import os
import shutil
from contextlib import contextmanager

@contextmanager
def temp_dir(path):
    """创建临时目录，退出时删除"""
    os.makedirs(path, exist_ok=True)
    print(f"临时目录已创建：{path}")
    try:
        yield path
    finally:
        shutil.rmtree(path)        # 无论是否异常都删除
        print(f"临时目录已删除：{path}")

with temp_dir("tmp_data") as d:
    # 在临时目录中创建一个文件
    filepath = os.path.join(d, "test.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("临时数据")

# 此时 tmp_data 目录已被删除
print(os.path.exists("tmp_data"))    # False
```

**解析：** `yield` 之前的代码在进入 `with` 时执行（创建目录），`yield` 之后的 `finally` 代码块在退出时执行（删除目录）。用 `try...finally` 包裹确保即使 `with` 块中抛异常，删除操作也会执行。

---

### 练习3：最佳应用场景

**答案：C——管理数据库事务。** 原因如下：

- **A（温度转换）**：纯计算，不需要任何"进入/退出"清理操作
- **B（计算平均值）**：同上
- **C（数据库事务）**：完美匹配——"开始事务 → 执行操作 → 提交或回滚"是一个典型的"进入→做事→清理"模式，而且"无论成败都要提交或回滚"正是上下文管理器的核心价值
- **D（打印乘法表）**：纯输出，无资源管理需求


## 9.4 JSON/CSV 文件处理

### 练习1：读取配置文件

**答案：**

```python
import json

# 先创建 config.json
config = {
    "app_name": "我的应用",
    "version": "2.0",
    "settings": {
        "theme": "dark",
        "language": "zh-CN",
        "auto_save": True
    }
}

with open("config.json", "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

# 读取并打印
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

print(f"应用名：{config['app_name']}")
print(f"版本：{config['version']}")
print(f"主题：{config['settings']['theme']}")
print(f"语言：{config['settings']['language']}")
print(f"自动保存：{config['settings']['auto_save']}")
```

---

### 练习2：CSV 读写与平均分

**答案：**

```python
import csv

# 写入 CSV
students = [
    {"姓名": "小明", "语文": 88, "数学": 95, "英语": 73},
    {"姓名": "小红", "语文": 92, "数学": 87, "英语": 96},
    {"姓名": "小刚", "语文": 76, "数学": 82, "英语": 69},
]

fieldnames = ["姓名", "语文", "数学", "英语"]
with open("scores.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(students)

# 读回并计算平均分
with open("scores.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row["姓名"]
        chinese = int(row["语文"])
        math = int(row["数学"])
        english = int(row["英语"])
        avg = (chinese + math + english) / 3
        print(f"{name} 的平均分为 {avg:.1f}")
```

**输出：**

```text
小明 的平均分为 85.3
小红 的平均分为 91.7
小刚 的平均分为 75.7
```

**解析：** `DictReader` 返回的每一行的值都是字符串，所以需要用 `int()` 转换成数字再计算。

---

### 练习3：JSON vs CSV 选择

**参考答案：**

- **JSON 更合适的场景**：一个博客系统的把文章列表导出为 JSON 供前端读取。因为博客文章包含嵌套结构（文章标题、正文、标签列表、作者信息），JSON 能自然表示这种层级关系。
- **CSV 更合适的场景**：月度销售报表导出，包含"日期、商品名、销量、单价、总金额"五个列，需要交给财务用 Excel 打开做透视分析。CSV 的表格结构天然匹配，且双击就能在 Excel 中打开。