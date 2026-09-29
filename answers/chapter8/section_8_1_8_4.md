## 8.1 模块的导入与使用

### 练习1：跨文件导入

**答案：**

```python
# math_ops.py
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
```

```python
# main.py
import math_ops

print(math_ops.add(3, 5))          # 8
print(math_ops.multiply(4, 7))     # 28
```

---

### 练习2：`__name__` 的两种行为

**答案：**

```python
# math_ops.py
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

if __name__ == "__main__":
    print("这是一个数学运算模块")
    print(f"测试：3 + 5 = {add(3, 5)}")
```

- 直接运行 `python math_ops.py`：输出 `"这是一个数学运算模块"` 和 `"测试：3 + 5 = 8"`
- 在 `main.py` 中 `import math_ops`：不输出任何内容，`add` 和 `multiply` 仍然可用

**解析：** `__name__` 的值取决于文件的执行方式。直接运行时为 `"__main__"`，被导入时为模块名（`"math_ops"`）。`if __name__ == "__main__"` 利用了这点来区分两种场景。

---

### 练习3：三种导入方式对比

| 方式 | 写法 | `sqrt` 调用方式 | 优缺点 |
|:----:|:-----|:---------------|:------|
| A | `import math` | `math.sqrt(16)` | 命名空间清晰，不会冲突；但写起来稍长 |
| B | `from math import sqrt` | `sqrt(16)` | 简洁；但容易和同名变量或函数冲突 |
| C | `from math import *` | `sqrt(16)` | 极简；但**极不推荐**——导入一切，可能污染命名空间，可读性差 |

**推荐：**
- 日常编程用方式 A 或 B，优先 A（清晰＞简洁）
- **永远不要**用方式 C（`from ... import *`），除非在 `__init__.py` 中配合 `__all__` 使用且你完全清楚自己在做什么


## 8.2 常用标准库介绍

### 练习1：列出 `.py` 文件

**答案：**

```python
import os

py_files = [f for f in os.listdir(".") if f.endswith(".py")]
for f in py_files:
    name = os.path.splitext(f)[0]      # 去掉 .py 后缀
    print(name)
```

**解析：**
- `os.listdir(".")` 列出当前目录下所有文件和文件夹
- `f.endswith(".py")` 筛选出 `.py` 文件
- `os.path.splitext(f)[0]` 拆分文件名和扩展名，取文件名部分

---

### 练习2：计算距元旦天数

**答案：**

```python
from datetime import date

def days_until_new_year():
    today = date.today()
    next_new_year = date(today.year + 1, 1, 1)    # 下一年元旦
    days = (next_new_year - today).days
    if days == 365:     # 如果"下一年元旦"距今 365 天，说明今天就是元旦
        print("今天是元旦！")
    else:
        print(f"距离下一个元旦还有 {days} 天")

days_until_new_year()
```

---

### 练习3：JSON 读写

**答案：**

```python
import json

data = {"任务": ["学Python", "写代码", "做项目"]}

# 写入文件
with open("tasks.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 从文件读取
with open("tasks.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)

print(loaded)                # {'任务': ['学Python', '写代码', '做项目']}
print(loaded["任务"])        # ['学Python', '写代码', '做项目']
```


## 8.3 第三方包的安装与管理

### 练习1：安装与卸载 requests

**答案（命令行操作记录）：**

```bash
# 安装
pip install requests
# 输出示例：Successfully installed certifi-... charset_normalizer-... idna-... requests-... urllib3-...

# 查看信息
pip show requests
# 输出示例：
# Name: requests
# Version: 2.32.3
# Summary: Python HTTP for Humans.
# Home-page: https://requests.readthedocs.io
# ...

# 卸载
pip uninstall requests -y
# 输出示例：Successfully uninstalled requests-...
```

**解析：** `pip show` 是查看包元信息的快捷方式，`-y` 参数跳过卸载确认提示。

---

### 练习2：虚拟环境操作

**答案（命令行操作记录）：**

```bash
# 创建虚拟环境
python -m venv test_env

# 激活（Windows）
test_env\Scripts\activate

# 安装 flask
pip install flask

# 查看已安装的包
pip freeze
# 输出会包含 flask 及其所有依赖（click, blinker, itsdangerous, jinja2, markupsafe, werkzeug）

# 退出虚拟环境
deactivate
```

**解析：** 虚拟环境激活后，`pip freeze` 列出的包远比 `flask` 多——这是因为 `flask` 自身也依赖了其他包，`pip` 会自动把依赖链上的所有包一并安装进来。这就是为什么一个看似简单的项目，`requirements.txt` 可能有几十行。

---

### 练习3：判断对错

- **A（把所有项目的包都装在系统 Python 中）——错误。** 不同项目可能依赖同一个包的不同版本，系统 Python 只能装一个版本，必然冲突。而且卸载系统 Python 时所有项目的包都会丢失。
- **B（每个项目使用独立的虚拟环境）——正确。** 这是 Python 社区的最佳实践。每个项目的依赖完全隔离，互不影响。
- **C（把 `requirements.txt` 加入 `.gitignore`）——错误。** `requirements.txt` 应该提交到 Git，这样其他协作者才能用 `pip install -r requirements.txt` 快速搭建相同环境。
- **D（使用 `pip freeze > requirements.txt` 定期更新依赖清单）——正确。** 每次新增或升级依赖后都应更新 `requirements.txt`，保持清单与实际环境同步。


## 8.4 自定义包的创建

### 练习1：创建 calculator 包

**答案：**

```text
calculator/
    __init__.py
    basic.py
    advanced.py
```

```python
# calculator/__init__.py
from .basic import add, subtract
from .advanced import power, factorial
```

```python
# calculator/basic.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
```

```python
# calculator/advanced.py
def power(base, exp):
    result = 1
    for _ in range(exp):
        result *= base
    return result

def factorial(n):
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```

```python
# main.py（放在 calculator 包的上级目录）
from calculator import add, subtract, power, factorial

print(add(3, 5))          # 8
print(subtract(10, 4))    # 6
print(power(2, 10))       # 1024
print(factorial(5))       # 120
```

---

### 练习2：相对导入实现

**答案：**

修改 `calculator/advanced.py`，用相对导入引用 `basic.py` 中的 `add`：

```python
# calculator/advanced.py
from .basic import add          # 相对导入——从同级目录的 basic 模块导入 add

def multiply(a, b):
    """用 add 的循环实现乘法"""
    result = 0
    for _ in range(b):
        result = add(result, a)    # 调用 basic.add
    return result

def power(base, exp):
    result = 1
    for _ in range(exp):
        result = multiply(result, base)
    return result

def factorial(n):
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result = multiply(result, i)
    return result
```

**验证：**

```python
# main.py
from calculator.advanced import multiply, power, factorial

print(multiply(6, 7))      # 42
print(power(3, 4))         # 81
print(factorial(6))        # 720
```

**解析：** `from .basic import add` 中的 `.` 表示"当前包（calculator）目录下"。这种写法在包内部模块间互相引用时非常方便——如果以后把 `basic.py` 重命名为 `arithmetic.py`，只需要改 `.basic` 为 `.arithmetic`，而不需要写出完整的包路径。

---

### 练习3：思考题——重构学生管理系统

**参考答案（一种合理的组织方式）：**

```text
student_system/
    __init__.py           # 统一导出接口
    models.py             # 数据模型：Student 类
    manager.py            # 业务逻辑：StudentManager 类
    utils.py              # 工具函数（成绩校验、格式化输出等）
    config.py             # 配置常量（如优秀分数线 90、成绩范围 0-100）
    cli.py                # 命令行交互界面（原来的 main 函数）
```

- **`models.py`**：只管"学生长什么样"——属性定义、`__str__`、`__lt__`、成绩计算方法。这是最纯粹的数据层。
- **`manager.py`**：只管"怎么管理学生"——增删查改、排名、统计。它依赖 `models.Student`，通过组合关系持有学生列表。
- **`utils.py`**：抽取重复的工具逻辑——比如成绩范围校验、格式化输出等。减少 `models.py` 和 `manager.py` 的代码重复。
- **`config.py`**：把魔法数字（90 分优秀线、0-100 范围等）集中管理，方便后续调参。
- **`cli.py`**：纯交互层——打印菜单、接收用户输入、调用 `manager` 的方法。不包含任何业务逻辑。
- **`__init__.py`**：对外暴露最常用的接口，让使用者 `from student_system import Student, StudentManager` 即可快速上手。

这种分层方式遵循了**关注点分离**（Separation of Concerns）原则——每个模块只做一件事。当需求变更时（比如"优秀分数线从 90 改成 85"），你只需要改 `config.py` 一个文件，不用担心连锁反应。