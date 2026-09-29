## 8.1 模块的导入与使用——代码"分而治之"

到目前为止，你写的所有代码都放在一个 `.py` 文件里。这在练习阶段没问题，但当你开始写几百行、几千行的程序时，把所有代码塞进一个文件就会变成一场灾难——滚动几百行只为找一个函数的定义、变量名满天飞容易冲突、想复用某段代码却无从下手。模块（Module）就是为解决这些问题而生的。

### 8.1.1 什么是模块？

在 Python 中，**一个 `.py` 文件就是一个模块**。模块名就是文件名去掉 `.py` 后缀。模块是一个独立的命名空间——同一个变量名在不同的模块中可以互不干扰地共存。

把代码拆分成模块有三大好处：
1. **组织清晰**：每个模块负责一个独立的功能域，比如 `database.py` 管数据库、`auth.py` 管登录验证
2. **代码复用**：一次编写，可以在项目的任何文件中导入使用，甚至可以用在其他项目中
3. **避免命名冲突**：`database.connect()` 和 `network.connect()` 虽然都叫 `connect`，但它们属于不同的模块，各走各的路

### 8.1.2 `import`——导入整个模块

最基础的导入方式：

```python
import math                     # 导入 math 模块

print(math.pi)                  # 3.141592653589793——通过"模块名.属性名"访问
print(math.sqrt(16))            # 4.0——计算平方根
print(math.sin(math.pi / 2))    # 1.0——计算正弦值
```

使用 `import math` 后，`math` 模块里所有的函数和常量都被加载了，但你必须以 `math.xxx` 的形式来访问它们。这就像一个门牌号——你告诉 Python"去 math 这个模块里找 `pi`"。

### 8.1.3 `from...import`——按需导入

如果你只需要模块中的某几个函数，可以用 `from...import` 精确导入：

```python
from math import pi, sqrt       # 只导入 pi 和 sqrt

print(pi)                       # 直接使用，不需要 math. 前缀
print(sqrt(25))                 # 5.0
# print(sin(0))                 # NameError——没有导入 sin
```

这种写法的好处是使用起来简洁，坏处是当你从多个模块导入同名函数时会产生冲突。比如 `from math import sin` 和 `from numpy import sin` 同时出现时，后导入的会覆盖先导入的。

### 8.1.4 `import...as`——给模块起别名

有些模块名比较长，每次都写全称很累赘。`as` 关键字可以起一个简短的别名：

```python
import numpy as np              # 数据分析领域的事实标准别名
import matplotlib.pyplot as plt # 数据可视化领域的事实标准别名
import pandas as pd             # 同上

array = np.array([1, 2, 3])     # 等价于 numpy.array([1, 2, 3])
```

使用业界通用别名不仅是少敲几个字的问题——它降低了代码的阅读门槛，让其他 Python 开发者一眼就能认出你用了什么库。

### 8.1.5 导入自定义模块

不仅能用 Python 自带的模块，你也可以导入自己写的 `.py` 文件。假设项目结构如下：

```text
project/
  main.py
  utils.py
```

```python
# utils.py
def greet(name):
    return f"你好，{name}！"

VERSION = "1.0"
```

```python
# main.py
import utils

print(utils.greet("小明"))     # 你好，小明！
print(utils.VERSION)          # 1.0
```

`import utils` 时，Python 会先在当前目录下找 `utils.py`，找不到再去标准库路径中找。如果你把项目文件组织得很规整——相关的函数放在一个模块里——那么 `main.py` 就可以保持极简，只负责协调调用，不包含冗长的细节逻辑。

---

\begin{tipbox}
**导入时的常见坑：循环导入**

两个模块互相导入对方时，会形成"循环导入"——Python 会因为无法决定先加载哪个而报错或产生难以追踪的 bug。例如 `a.py` 开头写 `import b`，`b.py` 开头写 `import a`。解决方法：
- 重新审视设计——两个模块是否耦合太紧？也许应该提取公共部分到第三个模块
- 把 `import` 语句移到函数内部（延迟导入），只在真正需要时才执行
\end{tipbox}

---

### 8.1.6 `__name__` 与 `"__main__"`——双面文件

同一个 `.py` 文件既可以被当作模块导入，也可以被当作脚本直接运行。`__name__` 这个内置变量就是用来区分这两种情况的：

```python
# calculator.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

if __name__ == "__main__":
    # 只有在"直接运行 calculator.py"时才执行下面这段
    print("这是计算器模块")
    print(f"3 + 5 = {add(3, 5)}")
    print(f"10 - 4 = {subtract(10, 4)}")
```

- 当执行 `python calculator.py` 时，`__name__` 的值是 `"__main__"`，`if` 条件成立，测试代码会运行
- 当另一个文件写 `import calculator` 时，`__name__` 的值是 `"calculator"`（模块名），`if` 条件不成立，测试代码不会运行——但 `add` 和 `subtract` 函数仍然可以被调用

这个机制让你可以**在一个文件中既写好可复用的函数，又能写测试代码**——测试代码不会在别人导入你的模块时意外执行。

### 8.1.7 实战练习

1. 创建两个文件：`math_ops.py`（包含 `add(a, b)` 和 `multiply(a, b)` 函数）和 `main.py`。在 `main.py` 中导入 `math_ops` 并调用两个函数，打印结果。

2. 在 `math_ops.py` 中加上 `if __name__ == "__main__"` 块，直接运行该文件时打印 `"这是一个数学运算模块"`，但作为模块被导入时不打印任何内容。验证两种运行方式的不同行为。

3. 以下是三种导入方式的对比，指出它们的区别和使用场景：

```python
# 方式 A
import math
print(math.sqrt(16))

# 方式 B
from math import sqrt
print(sqrt(16))

# 方式 C
from math import *
print(sqrt(16))
```