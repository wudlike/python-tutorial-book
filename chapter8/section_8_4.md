## 8.4 自定义包的创建——组织大型项目的艺术

当项目变得足够大时，单层的模块文件也会失控——几十个 `.py` 文件堆在同一个目录下，分不清哪些是核心逻辑、哪些是工具函数、哪些是配置。包（Package）就是解决这个问题的终极方案——它把相关模块组织成目录层级，为大型项目提供清晰的结构骨架。

### 8.4.1 从模块到包——加一个 `__init__.py`

在 Python 中，**包就是一个包含 `__init__.py` 文件的目录**。`__init__.py` 可以是一个空文件——它的存在本身就是在告诉 Python："这个目录是一个包，请把它当作模块的集合来处理。"

一个典型包的目录结构：

```text
mylib/
    __init__.py         # 标识 mylib 是一个包
    core.py             # 核心逻辑
    utils.py            # 工具函数
    constants.py        # 常量定义
```

在代码中可以这样导入：

```python
import mylib.core                   # 导入 core 子模块
from mylib.utils import helper_func # 从 utils 子模块导入特定函数

mylib.core.run()                    # 通过完整路径调用
helper_func()                       # 直接调用导入的函数
```

`__init__.py` 不仅仅是一个标记文件——你可以把包的初始化代码放进去，也可以在里面定义 `__all__` 列表来精确控制 `from package import *` 的行为：

```python
# mylib/__init__.py
__all__ = ["core", "utils"]    # 只有这两个子模块会通过 from mylib import * 被导出
```

### 8.4.2 相对导入——包内部的"自家引用"

在一个包内部，子模块之间经常需要互相引用。有两种方式：

```python
# mylib/core.py
from mylib.utils import helper_func      # 方式一：绝对导入——写全路径
from .utils import helper_func           # 方式二：相对导入——用 "." 表示同级目录
from ..parent_pkg import something       # ".." 表示上级目录
```

绝对导入（方式一）的优点是不怕移动文件位置（只要顶层包路径不变），适合公开接口。相对导入（方式二）更简洁，在包内部重命名模块时不容易漏改，是包内部模块间引用的推荐写法。

```python
# 相对导入示意
from .core import start           # 同目录下的 core 模块
from .subpkg import something     # 同目录下 subpkg 包中的模块
from ..sibling import func        # 上级目录的兄弟包
```

### 8.4.3 一个完整的包实例

下面用一个微型的数据处理包来展示完整的包结构：

```text
datatools/
    __init__.py
    reader.py         # 读取数据
    cleaner.py        # 清洗数据
    analyzer.py       # 分析数据
```

```python
# datatools/__init__.py
"""datatools——一个简单的数据处理工具包"""

__version__ = "1.0.0"
__all__ = ["reader", "cleaner", "analyzer"]

from .reader import read_csv, read_json
from .cleaner import remove_duplicates, fill_missing
from .analyzer import mean, median
```

```python
# datatools/reader.py
import csv
import json

def read_csv(filepath):
    """读取 CSV 文件，返回表头和数据行"""
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = [row for row in reader]
    return headers, rows

def read_json(filepath):
    """读取 JSON 文件"""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
```

```python
# datatools/cleaner.py
def remove_duplicates(data):
    """去重——保持原顺序"""
    seen = set()
    result = []
    for item in data:
        key = tuple(item) if isinstance(item, list) else item
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result

def fill_missing(data, fill_value=0):
    """填充缺失值（None 替换为 fill_value）"""
    return [fill_value if x is None else x for x in data]
```

```python
# datatools/analyzer.py
def mean(data):
    """计算平均数"""
    if not data:
        return 0
    return sum(data) / len(data)

def median(data):
    """计算中位数"""
    if not data:
        return 0
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    return sorted_data[mid]
```

因为 `__init__.py` 中导入了各子模块的关键函数，使用者可以用非常简洁的方式调用：

```python
# main.py——使用 datatools 包
from datatools import read_csv, remove_duplicates, mean

headers, rows = read_csv("sales.csv")
print(f"表头：{headers}")
print(f"行数：{len(rows)}")

clean_rows = remove_duplicates(rows)
print(f"去重后行数：{len(clean_rows)}")

sales = [float(r[2]) for r in clean_rows]    # 假设第 3 列是销售额
print(f"平均销售额：{mean(sales):.2f}")
```

`__init__.py` 在这里充当了"门面"（Facade）——把分散在多个子模块中的函数统一暴露在包名 `datatools` 之下，使用者不需要知道 `reader.py`、`cleaner.py` 的内部结构，只需要 `from datatools import 函数名` 即可。这是优秀 API 设计的标志。

### 8.4.4 把自己的包发布到 PyPI（简述）

如果你写的包足够实用，可以考虑发布到 PyPI，让全世界的 Python 开发者都能 `pip install` 你的作品。发布流程大致为：

1. 整理项目结构，添加 `setup.py`（或现代化的 `pyproject.toml`）定义包的元信息
2. 注册 PyPI 账号并获取 API Token
3. 安装构建工具：`pip install build twine`
4. 构建分发包：`python -m build`
5. 上传到 PyPI：`python -m twine upload dist/*`

发布开源包不仅是分享代码，更是参与 Python 社区的重要方式。许多流行的库（如 `requests`、`flask`）都是从一个简单的想法和几十行代码开始成长起来的。

### 8.4.5 实战练习

1. 创建一个包 `calculator`，目录结构如下：

```text
calculator/
    __init__.py
    basic.py        # 包含 add(a, b) 和 subtract(a, b)
    advanced.py     # 包含 power(base, exp) 和 factorial(n)
```

   在 `__init__.py` 中导入所有四个函数，使得使用者可以直接 `from calculator import add, power`。编写 `main.py` 测试包的导入和调用。

2. 在 `advanced.py` 中使用相对导入 `from .basic import add` 来实现 `power` 函数（用 `add` 的循环来实现乘法，暂不深究性能），验证相对导入是否正常工作。

3. 自由思考题：回想你之前写过的所有练习代码（比如第 7 章的学生管理系统），如果要把它们重构成一个包，你会怎么组织目录结构？各模块分别承担什么职责？