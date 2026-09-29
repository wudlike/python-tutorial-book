## 10.1 列表推导式

### 练习1：整除条件推导式

**答案：**

```python
result = [x for x in range(1, 101) if x % 7 == 0 and x % 5 != 0]
print(result)
# [7, 14, 21, 28, 42, 49, 56, 63, 77, 84, 91, 98]
```

**解析：** `x % 7 == 0` 筛选 7 的倍数，`x % 5 != 0` 排除 5 的倍数。`and` 确保两个条件同时满足。注意 35 和 70 因为同时是 7 和 5 的倍数（即 35 的倍数）被排除了。

---

### 练习2：字符串推导式

**答案：**

```python
words = ["Python", "go", "JAVA", "rust", "C++"]

# 筛选长度大于 3 并转小写
long_lower = [w.lower() for w in words if len(w) > 3]
print(long_lower)    # ['python', 'java', 'rust']

# 生成字典：键为原词，值为长度
word_len_dict = {w: len(w) for w in words}
print(word_len_dict)    # {'Python': 6, 'go': 2, 'JAVA': 4, 'rust': 4, 'C++': 3}
```

---

### 练习3：推导式展开

**推导式：**

```python
result = [(x, y) for x in range(1, 4) for y in range(1, 4) if x != y]
print(result)
```

**等价 for 循环：**

```python
result = []
for x in range(1, 4):      # x: 1, 2, 3
    for y in range(1, 4):  # y: 1, 2, 3
        if x != y:
            result.append((x, y))
print(result)
# [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
```

**解析：** 嵌套推导式中外层 `for x` 对应外层循环，内层 `for y` 对应内层循环。`if x != y` 排除了 `x` 和 `y` 相等的 3 种情况：`(1,1)`, `(2,2)`, `(3,3)`。所以结果是 9 - 3 = 6 个元组。


## 10.2 生成器与迭代器

### 练习1：斐波那契生成器

**答案：**

```python
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield b
        a, b = b, a + b

for num in fibonacci(10):
    print(num, end=" ")
# 1 1 2 3 5 8 13 21 34 55
```

**解析：**
- `a, b = 0, 1` 初始化前两个数（`a` 是上一个，`b` 是当前）
- 每次 `yield b` 产出当前的斐波那契数
- `a, b = b, a + b` 同时更新：`a` 变成之前的 `b`，`b` 变成 `a + b`（新的斐波那契数）
- 这种"交换+前进"的模式是生成器处理序列的经典写法

---

### 练习2：奇数平方和（生成器表达式）

**答案：**

```python
total = sum(x ** 2 for x in range(1, 1_000_001) if x % 2 != 0)
print(total)    # 166666666666500000
```

**解析：** `(x ** 2 for x in range(1, 1_000_001) if x % 2 != 0)` 是一个生成器表达式，传递给 `sum()` 时不会创建包含 50 万个奇数的中间列表。每个数的平方在需要的时候才计算一次，计算完就丢弃。

---

### 练习3：生成器执行流程

**代码：**

```python
def simple_gen():
    print("开始")
    yield 1
    print("中间")
    yield 2
    print("结束")

g = simple_gen()
print("A")
print(next(g))
print("B")
print(next(g))
print("C")
print(next(g))
```

**输出：**

```text
A
开始
1
B
中间
2
C
结束
StopIteration（异常，程序终止）
```

**逐行解析：**
1. `g = simple_gen()` ——创建生成器对象，**不执行任何代码**（函数体中的代码此时还没有运行）
2. `print("A")` ——输出 A
3. `print(next(g))` ——第一次调用 `next()`，开始执行函数体。打印"开始"，`yield 1` 暂停并返回 1。`print` 输出 1。
4. `print("B")` ——输出 B
5. `print(next(g))` ——第二次调用 `next()`，从上次暂停的 `yield 1` 之后恢复执行。打印"中间"，`yield 2` 暂停并返回 2。`print` 输出 2。
6. `print("C")` ——输出 C
7. `print(next(g))` ——第三次调用 `next()`，从 `yield 2` 之后恢复。打印"结束"，函数到达末尾，抛出 `StopIteration`。

**关键理解：** 生成器函数在被调用时不执行，只在第一次 `next()` 时才开始执行，并在每个 `yield` 处暂停。


## 10.3 闭包与装饰器进阶

### 练习1：repeat(n) 装饰器

**答案：**

```python
from functools import wraps
import random

def repeat(n):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(n):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(3)
def roll_dice():
    return random.randint(1, 6)

print(roll_dice())       # 例如 [4, 1, 6]
print(roll_dice())       # 例如 [2, 2, 5]
```

**解析：** 三层结构——`repeat(n)` 返回 `decorator`，`decorator` 返回 `wrapper`。`wrapper` 中循环 `n` 次调用原函数，把结果收集到列表里返回。`@wraps(func)` 保留原函数的 `__name__` 和 `__doc__`。

---

### 练习2：memoize 缓存装饰器

**答案：**

```python
from functools import wraps

def memoize(func):
    cache = {}       # 闭包变量——所有调用共享同一个缓存字典

    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)    # 计算并缓存
        return cache[args]               # 返回缓存结果

    return wrapper

@memoize
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(100))    # 354224848179261915075——秒出结果
```

**解析：**
- `cache` 字典是 `memoize` 的局部变量，但被 `wrapper` 引用——它形成了一个闭包
- 每次调用 `fibonacci` 时，先检查 `args`（参数元组）是否在 `cache` 中
- 如果缓存命中，直接返回；否则计算、存缓存、返回
- 这个技术将 `fibonacci` 的时间复杂度从 O(2^n) 降到了 O(n)，从"算不出来"变成"秒出"

---

### 练习3：分析执行时机

**代码：**

```python
def deco(func):
    print(f"装饰器被调用：{func.__name__}")
    def wrapper(*args):
        print(f"wrapper 被调用，参数：{args}")
        return func(*args)
    return wrapper

print("A")
@deco
def add(a, b):
    return a + b
print("B")
print(add(3, 5))
print("C")
```

**输出：**

```text
A
装饰器被调用：add
B
wrapper 被调用，参数：(3, 5)
8
C
```

**关键发现：** `@deco` 装饰器在**函数定义时**（加载模块时）就被执行，而不是在函数调用时。`print("装饰器被调用：add")` 出现在 A 和 B 之间，说明在 `@deco` 那行代码被执行时就调用了 `deco(add)`。而 `wrapper` 内部的逻辑在 `add(3, 5)` 真正被调用时才执行。

**时间线：**
1. `print("A")` → 输出 A
2. 遇到 `@deco`，Python 执行 `deco(add)` → 输出 `"装饰器被调用：add"`，把 `wrapper` 赋给 `add`
3. `print("B")` → 输出 B
4. `print(add(3, 5))` → 此时 `add` 已经是 `wrapper` → 输出 `"wrapper 被调用，参数：(3, 5)"` 和 `8`
5. `print("C")` → 输出 C


## 10.4 并发编程基础

### 练习1：多线程任务

**答案：**

```python
import threading
import time

def task(name, seconds):
    print(f"任务 {name} 开始")
    time.sleep(seconds)
    print(f"任务 {name} 完成（{seconds}秒）")

threads = []
for i in range(1, 6):
    t = threading.Thread(target=task, args=(f"T{i}", i))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("全部完成")
```

**输出示例：**

```text
任务 T1 开始
任务 T2 开始
任务 T3 开始
任务 T4 开始
任务 T5 开始
任务 T1 完成（1秒）
任务 T2 完成（2秒）
任务 T3 完成（3秒）
任务 T4 完成（4秒）
任务 T5 完成（5秒）
全部完成
```

---

### 练习2：线程池批量下载

**答案：**

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def download(url):
    print(f"开始下载 {url}")
    time.sleep(len(url) % 3 + 1)     # 用 URL 长度模拟不同的下载时间
    return f"{url} 下载完成"

urls = [f"https://example.com/file_{i}.zip" for i in range(1, 11)]

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = {executor.submit(download, url): url for url in urls}
    for future in as_completed(futures):
        print(f"✅ {future.result()}")
```

**解析：**
- `max_workers=3` 限制了同时运行的线程数量——最多 3 个下载同时进行
- `as_completed(futures)` 按**完成顺序**（不是提交顺序）逐个返回结果——哪个先下载完就先处理哪个
- 打印输出可以观察到：始终有 2-3 个"开始下载"之后才会出现"完成"——因为线程池只有 3 个槽位

---

### 练习3：场景判断

| 场景 | 方案 | 原因 |
|:-----|:----|:-----|
| A：从 1000 个 URL 爬取网页 | **多线程** | 网络爬虫的核心瓶颈是 I/O 等待（等待服务器响应），线程在等待时会释放 GIL，多线程能大幅加速 |
| B：1000 张图片批量水印 | **多进程** | 图像处理是典型的 CPU 密集型任务——像素遍历、滤镜计算等需要大量运算，GIL 会阻塞多线程的并发效果，必须用多进程 |
| C：监控 50 个日志文件 | **多线程** | 文件 I/O 监控的瓶颈是操作系统事件等待，属于 I/O 密集型。不过实际中可能用 `asyncio` 更合适（单线程事件循环） |
| D：GUI 后台任务保持界面响应 | **多线程** | GUI 程序的 UI 线程不能阻塞——把耗时操作放到子线程中执行，主线程继续响应界面操作。这是多线程最经典的应用场景之一