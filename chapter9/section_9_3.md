## 9.3 上下文管理器——`with` 语句的优雅之道

在前两节中，你已经见过 `with open(...) as f:` 这种写法。它的作用是自动帮你在代码块结束时关闭文件，不需要手动调用 `f.close()`。这个语法背后的机制叫**上下文管理器**（Context Manager），它不仅仅用于文件，而是一种通用的"资源管理模式"——打开和关闭数据库连接、获取和释放锁、启动和停止计时器……凡是成对的"开始/结束"操作，都可以用它来优雅地表达。

### 9.3.1 `with` 语句的工作原理

`with` 语句的核心思想是：**进入时做准备工作，退出时做清理工作——无论中间的代码是正常结束还是抛出异常，清理工作都会被执行**。

```python
# 传统写法——容易忘记 close()
f = open("data.txt", "r", encoding="utf-8")
try:
    content = f.read()
    print(content)
finally:
    f.close()              # 必须用 finally 保证关闭，否则异常时会泄露资源

# with 写法——自动清理，简洁安全
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)
# 出了 with 块，文件自动关闭——即使中间抛了异常也一样
```

`with` 把"保证清理"的逻辑从你的代码中剥离出来，交给了 `open()` 返回的文件对象自己处理。这不仅是少写两行代码的问题——它从根本上杜绝了"忘记关闭"这个人类最容易犯的错误。

### 9.3.2 `__enter__` 与 `__exit__`——上下文管理器的灵魂

任何定义了 `__enter__` 和 `__exit__` 两个特殊方法的对象，都可以用在 `with` 语句中。`__enter__` 在进入 `with` 块时被调用，返回值赋给 `as` 后面的变量；`__exit__` 在退出时被调用（无论正常退出还是异常退出）。

下面自定义一个计时器上下文管理器，来演示这两个方法的使用：

```python
import time

class Timer:
    """一个计时的上下文管理器——测量代码块的执行时间"""

    def __enter__(self):
        self.start = time.time()
        print("计时开始...")
        return self                    # 返回给 as 后面的变量

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        elapsed = self.end - self.start
        print(f"计时结束，耗时：{elapsed:.4f} 秒")

        # 返回 False 表示不压制异常——如果有异常，让它继续向外传播
        # 返回 True 则表示"异常已处理"，不再向外抛出
        return False

with Timer():
    total = sum(range(10_000_000))     # 一千万次求和
    print(f"计算结果：{total}")
```

输出：

```text
计时开始...
计算结果：49999995000000
计时结束，耗时：0.1287 秒
```

逐行解析这段代码：

- **`__enter__(self)`**：进入 `with` 块时调用。这里记录了开始时间。`return self` 让 `with Timer() as t` 中的 `t` 指向这个 `Timer` 实例。
- **`__exit__(self, exc_type, exc_val, exc_tb)`**：退出 `with` 块时调用。三个参数分别表示异常类型、异常值和回溯对象——如果代码块正常结束，这三个参数都是 `None`。这里记录了结束时间并打印耗时。
- **返回值 `False`**：表示"我没有处理异常，如果有异常请继续向外传播"。返回 `True` 则会吞掉异常（慎用）。

---

\begin{notebox}
**`__exit__` 的三个参数什么时候有值？**

```python
class Inspector:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            print("正常退出，无事发生")
        else:
            print(f"异常退出：{exc_type.__name__}——{exc_val}")

with Inspector():
    1 / 0          # 触发 ZeroDivisionError
# 输出：异常退出：ZeroDivisionError——division by zero
# 然后异常继续向外抛出（因为 __exit__ 返回了 None，等价于 False）
```

这三个参数让你有机会在退出时知道"是怎么退出的"，以便做出不同的清理策略——比如异常退出时需要回滚事务，正常退出时提交事务。
\end{notebox}

---

### 9.3.3 `contextlib.contextmanager`——用生成器写上下文管理器

`class` 版本的上下文管理器功能最全，但有时嫌重。对于简单的"进入/退出"场景，`contextlib` 模块提供的 `@contextmanager` 装饰器可以让你用生成器函数（参见 10.2 节）来写：

```python
from contextlib import contextmanager

@contextmanager
def timer():
    """函数版的计时器上下文管理器"""
    import time
    start = time.time()
    print("开始计时...")
    yield                           # 在此交出控制权，执行 with 块中的代码
    end = time.time()
    print(f"结束计时，耗时：{end - start:.4f} 秒")

with timer():
    total = sum(range(5_000_000))
    print(f"结果：{total}")
```

`yield` 之前的代码在进入 `with` 时执行，`yield` 之后的代码在退出 `with` 时执行——无论是否有异常。这种写法比定义类更轻量，适合快速搭建简单的上下文管理器。不过对于复杂的资源管理（需要区分异常和正常退出），还是类版本更灵活。

### 9.3.4 实战练习

1. 编写一个上下文管理器 `FileLogger` 类，在进入 `with` 块时打开一个日志文件（追加模式），在退出时自动关闭。`with` 块内通过 `as` 获取文件对象并写入日志。使用方式：

```python
with FileLogger("app.log") as log:
    log.write("程序启动\n")
    log.write("处理数据中...\n")
```

2. 使用 `@contextmanager` 装饰器编写一个上下文管理器 `temp_dir`，在进入时创建一个临时目录，退出时删除该目录及其中的所有文件。提示：使用 `os.makedirs()` 创建目录，使用 `shutil.rmtree()` 删除目录。

3. 以下哪个操作最适合用上下文管理器来封装？为什么？

   - A：将摄氏温度转换为华氏温度
   - B：计算列表中所有元素的平均值
   - C：管理数据库事务（开始事务 → 执行操作 → 提交或回滚）
   - D：打印九九乘法表