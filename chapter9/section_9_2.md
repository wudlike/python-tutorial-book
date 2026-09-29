## 9.2 异常处理机制——程序中的"安全气囊"

写程序不可能不出错。用户可能输入了非法数据，文件可能不存在，网络可能突然断开。初学者遇到错误时最常见的反应是"程序崩溃了"——控制台喷出一堆红色错误信息，然后退出。但一个成熟的程序不应该这样——它应该**优雅地处理错误**，给用户一个友好的提示，然后继续运行（或安全退出）。这就是异常处理（Exception Handling）要解决的问题。

### 9.2.1 为什么要处理异常？

假设你写了一个除法计算器：

```python
a = int(input("请输入被除数："))
b = int(input("请输入除数："))
print(f"结果：{a / b}")
```

程序逻辑没有问题——直到用户输入除数为 `0`，或者输入了字母而非数字。这两种情况都会导致程序直接崩溃，用户体验极差。异常处理让程序能够在"出问题的地方"截获错误，并用预设好的备用方案应对。

### 9.2.2 `try-except`——捕获异常

最基本的异常处理结构：

```python
try:
    a = int(input("请输入被除数："))
    b = int(input("请输入除数："))
    result = a / b
    print(f"结果：{result}")
except ValueError:
    print("输入错误：请输入有效的整数！")
except ZeroDivisionError:
    print("数学错误：除数不能为零！")
```

`try` 块中的代码被"监控"起来——如果执行过程中抛出了异常，Python 会跳过后面的代码，逐一匹配 `except` 子句中的异常类型。匹配到对应的类型后，执行该 `except` 块中的代码，然后程序继续运行（不崩溃）。

注意一个关键细节：**只有第一个被匹配到的 `except` 块会被执行**。即使代码抛出的异常同时符合多个 `except` 的类型，也只会执行第一个匹配的。

### 9.2.3 Python 的异常层次结构

Python 内置了大量异常类型，它们构成一个树状的继承层次。了解这个层次结构有助于你精确地捕获你关心的异常，同时不遮住其他问题：

```text
BaseException
 ├── SystemExit           # sys.exit() 触发
 ├── KeyboardInterrupt    # Ctrl+C 触发
 └── Exception            # 所有常规异常的父类
      ├── ValueError      # 值错误（如 int("abc")）
      ├── TypeError       # 类型错误（如 "a" + 1）
      ├── ZeroDivisionError    # 除以零
      ├── FileNotFoundError    # 文件不存在
      ├── IndexError           # 索引越界
      ├── KeyError             # 字典键不存在
      ├── AttributeError       # 对象没有这个属性
      └── ...                  # 还有很多
```

关键经验：**捕获异常时尽量具体，少用 `except Exception`，绝对不用光秃秃的 `except:`**。原因很简单——`except:` 会捕获一切，包括 `KeyboardInterrupt`（用户按 Ctrl+C 想终止程序），这是反直觉的。`except Exception:` 好一些，但也会掩盖你没有预料到的 bug。最佳实践是捕获你**知道如何处理**的具体异常。

### 9.2.4 `else` 和 `finally`——完整的控制流

`try-except` 可以配上 `else` 和 `finally` 形成完整的控制流：

```python
try:
    f = open("data.txt", "r", encoding="utf-8")
    content = f.read()
except FileNotFoundError:
    print("文件不存在，将使用默认数据")
    content = "默认内容"
except PermissionError:
    print("没有权限读取该文件")
    content = ""
else:
    print(f"文件读取成功，共 {len(content)} 个字符")
finally:
    try:
        f.close()
    except NameError:
        pass      # f 根本没创建成功，无需关闭
    print("文件已关闭（或无需关闭）")
```

四种代码块的执行时机：

| 代码块 | 何时执行 |
|:-------|:---------|
| `try` | 始终尝试执行 |
| `except` | `try` 中抛出匹配的异常时执行 |
| `else` | `try` 中**没有**抛出任何异常时执行 |
| `finally` | **无论如何**都执行——即使前面有 `return`、`break` 或未捕获的异常 |

`finally` 是最可靠的后勤保障——它常被用于释放资源（关闭文件、断开数据库连接、释放锁），确保即使发生意外，这些关键操作也不会被遗漏。

---

\begin{tipbox}
**捕捉异常后别忘了"打印"或"记录"它**

```python
try:
    result = risky_operation()
except ValueError as e:
    print(f"发生了错误：{e}")      # 至少让用户（或开发者）知道发生了什么
    # 生产环境应该用 logging.error(f"...", exc_info=True)
```

默默地吞掉异常（`except: pass`）是最坏的习惯——它把 bug 埋藏起来，让你在几周后面对一个"不知道为什么不对"的程序时毫无头绪。
\end{tipbox}

---

### 9.2.5 自定义异常——让错误"自解释"

当内置异常不足以描述你的业务逻辑错误时，可以定义自己的异常类型：

```python
class InsufficientFundsError(Exception):
    """余额不足异常"""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"余额不足：当前余额 {balance} 元，尝试取出 {amount} 元")

class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)
        self.balance -= amount
        return amount

account = BankAccount("小明", 1000)
try:
    account.withdraw(2000)
except InsufficientFundsError as e:
    print(e)     # 余额不足：当前余额 1000 元，尝试取出 2000 元
```

自定义异常的要点：
1. 继承自 `Exception`（不要直接继承 `BaseException`，它有特殊含义）
2. 类名以 `Error` 结尾，符合 Python 命名惯例
3. 在 `__init__` 中提供足够的上下文信息，让调用方一眼就能理解出了什么问题

### 9.2.6 实战练习

1. 编写一个 `safe_float_input(prompt)` 函数，反复提示用户输入直到得到一个合法的浮点数。如果用户输入的不是数字，捕获 `ValueError` 并提示重新输入。

2. 编写一个文件读取函数 `read_file_safe(filepath)`，尝试读取文件并返回内容。如果文件不存在，返回 `None` 并打印提示；如果权限不足，也返回 `None` 并打印提示；对于其他未知错误，打印错误信息后重新抛出异常。

3. 以下代码中的异常处理有三个问题，请指出并修正：

```python
try:
    num = int(input("请输入一个数字："))
    result = 100 / num
except:
    print("出错了")
```