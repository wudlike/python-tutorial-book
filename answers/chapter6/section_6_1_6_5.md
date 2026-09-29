## 6.1 函数的定义与调用

### 练习1：判断偶数

**答案：**

```python
def is_even(n):
    """返回 n 是否为偶数"""
    return n % 2 == 0

print(is_even(7))    # False
print(is_even(12))   # True
```

**解析：**
- `n % 2` 得到 `n` 除以 2 的余数。偶数的余数为 0，所以 `n % 2 == 0` 为 `True`
- 返回值直接是布尔表达式的结果，无需写成 `if n % 2 == 0: return True else: return False`

---

### 练习2：三角形面积

**答案：**

```python
def triangle_area(base, height):
    """返回三角形面积"""
    return base * height / 2

result = triangle_area(4, 5)
print(f"三角形面积为：{result}")    # 三角形面积为：10.0
```

---

### 练习3：乘法口诀

**答案：**

```python
def print_multiplication_table(n):
    """打印 n 的乘法口诀（1×n 到 9×n）"""
    for i in range(1, 10):
        print(f"{i} × {n} = {i * n}")

print_multiplication_table(7)
```

**输出：**

```text
1 × 7 = 7
2 × 7 = 14
3 × 7 = 21
4 × 7 = 28
5 × 7 = 35
6 × 7 = 42
7 × 7 = 49
8 × 7 = 56
9 × 7 = 63
```

**解析：**
- `range(1, 10)` 生成 1 到 9 的整数（不包含 10）
- `for` 循环遍历 1 到 9，每次打印一行乘法算式
- 函数只负责打印（副作用），不返回任何值（默认返回 `None`）


## 6.2 参数传递

### 练习1：城市描述

**答案：**

```python
def describe_city(city, country="中国"):
    print(f"{city} 在 {country}")

describe_city("北京")                       # 北京 在 中国（使用默认值）
describe_city("东京", country="日本")       # 东京 在 日本（覆盖默认值）
```

---

### 练习2：求最大值

**答案：**

```python
def max_of_n(*args):
    """返回多个参数中的最大值；无参数返回 None"""
    if not args:                # 检查元组是否为空
        return None
    return max(args)

print(max_of_n(3, 7, 2, 9, 5))    # 9
print(max_of_n())                  # None
```

**解析：**
- `if not args`：空元组的布尔值为 `False`，`not ()` 为 `True`
- `max()` 是 Python 内置函数，可以直接用于元组

---

### 练习3：预测输出

**代码：**

```python
def mystery(a, b=[]):
    b.append(a)
    return b

print(mystery(1))
print(mystery(2))
print(mystery(3, []))
print(mystery(4))
```

**输出：**

```text
[1]
[1, 2]
[3]
[1, 2, 4]
```

**逐行解析：**

- **`mystery(1)`**：`b` 使用默认值 `[]`（一个空列表）。`b.append(1)` 后，`b` 变成 `[1]`。注意这个列表对象被 Python 保留在内存中，下次调用时会继续使用同一个对象。
- **`mystery(2)`**：`b` 还是用默认值——同一个列表！此时 `b` 已经是 `[1]`，`b.append(2)` 后变成 `[1, 2]`。
- **`mystery(3, [])`**：这次显式传入了 `[]`，创建了一个全新的空列表，不会影响默认参数的列表。`b.append(3)` 后返回 `[3]`。
- **`mystery(4)`**：再次使用默认值——还是那个从第一次就存在的列表。它现在是 `[1, 2]`，`b.append(4)` 后变成 `[1, 2, 4]`。

**核心教训：** 默认参数只在函数**定义时**被求值一次。可变对象（列表、字典）作为默认参数会累积状态，导致每次调用产生非预期的"记忆"效果。正确的写法是 `def mystery(a, b=None): if b is None: b = []`。


## 6.3 返回值和作用域

### 练习1：安全除法

**答案：**

```python
def safe_divide(a, b):
    if b == 0:
        return "除数不能为零"
    return round(a / b, 2)          # 或 f"{a/b:.2f}"

print(safe_divide(10, 2))    # 5.0
print(safe_divide(10, 0))    # 除数不能为零
```

---

### 练习2：min/max/avg

**答案：**

```python
def min_max_avg(*args):
    if not args:
        return (None, None, None)
    return (min(args), max(args), sum(args) / len(args))

print(min_max_avg(3, 7, 2, 9, 5))    # (2, 9, 5.2)
print(min_max_avg())                  # (None, None, None)
```

---

### 练习3：作用域输出预测

**代码：**

```python
msg = "你好"

def change_locally():
    msg = "Hello"
    print("函数内:", msg)

def change_globally():
    global msg
    msg = "Hello"
    print("函数内:", msg)

print("1:", msg)          # ①
change_locally()          # ②
print("2:", msg)          # ③
change_globally()         # ④
print("3:", msg)          # ⑤
```

**输出：**

```text
1: 你好
函数内: Hello
2: 你好
函数内: Hello
3: Hello
```

**逐行解析：**

- **①**：全局 `msg` 的初始值为 `"你好"`。
- **②**：`change_locally()` 内部创建了一个**局部**变量 `msg`，赋值为 `"Hello"`。它和全局的 `msg` 只是同名，实际是不同的变量。打印 `"函数内: Hello"`。函数结束后，局部 `msg` 被销毁。
- **③**：全局 `msg` 仍是 `"你好"`——局部变量不影响全局。
- **④**：`change_globally()` 中声明了 `global msg`，告诉 Python "我要操作的是全局的那个 `msg`"。赋值 `msg = "Hello"` 修改了全局变量。打印 `"函数内: Hello"`。
- **⑤**：全局 `msg` 已经被修改为 `"Hello"`。


## 6.4 匿名函数：`lambda`

### 练习1：按第二个元素排序

**答案：**

```python
pairs = [(1, 3), (4, 1), (2, 2), (5, 0)]
result = sorted(pairs, key=lambda p: p[1])
print(result)    # [(5, 0), (4, 1), (2, 2), (1, 3)]
```

**解析：**
- `lambda p: p[1]` 告诉 `sorted()`："对于列表中的每个元组 `p`，用 `p[1]`（第二个元素）作为排序依据"
- `sorted()` 默认升序，所以 0, 1, 2, 3 依次排列

---

### 练习2：筛选长单词

**答案：**

```python
words = ["Python", "Go", "Java", "C", "Rust"]
result = list(filter(lambda w: len(w) > 3, words))
print(result)    # ['Python', 'Java', 'Rust']
```

**解析：**
- `lambda w: len(w) > 3` 对每个单词判断其长度是否大于 3
- `filter()` 保留判断结果为 `True` 的元素（Python, Java, Rust），去掉 Go 和 C

---

### 练习3：学生成绩排名

**答案：**

```python
scores = {"小明": 85, "小红": 92, "小刚": 78, "小李": 95, "小王": 88}

# 最高分
best = max(scores, key=lambda name: scores[name])
print(f"最高分学生：{best} ({scores[best]}分)")    # 小李 (95分)

# 从高到低排序
ranking = sorted(scores, key=lambda name: scores[name], reverse=True)
print(ranking)    # ['小李', '小红', '小王', '小明', '小刚']
```

**解析：**
- `max(scores, key=...)` 对字典的键（学生姓名）应用 `key` 函数，找出对应值最大的键。`lambda name: scores[name]` 读取每个学生的成绩进行比较
- `sorted(scores, key=..., reverse=True)` 对所有键按成绩降序排列
- 注意：这里的 `lambda` 参数是字典的**键**（名字），而不是键值对。要拿到键对应的值，需要 `scores[name]`


## 6.5 装饰器

### 练习1：加粗装饰器

**答案：**

```python
def bold_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"**{result}**"
    return wrapper

@bold_decorator
def get_title():
    return "Python教程"

print(get_title())    # **Python教程**
```

**解析：**
- 装饰器接收原函数 `func`，返回一个包装后的 `wrapper`
- `wrapper` 内部调用 `func()` 拿到原始返回值，然后在其前后加上 `**`，形成加粗效果
- `*args, **kwargs` 保证装饰器能适配任意参数的函数

---

### 练习2：重试装饰器

**答案：**

```python
def retry(func):
    def wrapper(*args, **kwargs):
        max_attempts = 3
        last_exception = None
        for attempt in range(1, max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                print(f"第 {attempt} 次尝试失败：{e}")
        raise last_exception          # 3 次都失败，抛出最后一次的异常
    return wrapper

@retry
def unstable_function():
    import random
    if random.random() < 0.7:        # 70% 概率失败
        raise ValueError("随机失败！")
    return "成功！"

for i in range(3):
    print(f"\n--- 第 {i+1} 轮调用 ---")
    try:
        print(unstable_function())
    except ValueError as e:
        print(f"最终失败：{e}")
```

**输出示例：**

```text
--- 第 1 轮调用 ---
第 1 次尝试失败：随机失败！
第 2 次尝试失败：随机失败！
第 3 次尝试失败：随机失败！
最终失败：随机失败！

--- 第 2 轮调用 ---
第 1 次尝试失败：随机失败！
成功！

--- 第 3 轮调用 ---
成功！
```

**解析：**
- `for attempt in range(1, max_attempts + 1)` 最多尝试 3 次
- `try...except` 捕获异常，如果成功就 `return` 退出；如果失败就记录异常并继续下一次尝试
- 3 次全部失败后，把最后一次的异常重新 `raise` 出去
- 这个装饰器在生产环境中非常实用——调用外部 API、读写数据库时网络抖动是常有的事，自动重试可以大幅减少因瞬时故障导致的失败

---

### 练习3：阅读代码写输出

**输出：**

```text
开始
Hello, 小明!
结束
---
开始
结束
3
```

等一下，`add(3, 5)` 返回 `3 + 5 = 8`，但打印应该是 `print(add(3, 5))`，所以输出 8。让我重新写：

```text
开始
Hello, 小明!
结束
---
开始
结束
8
```

**解析：**

- `greet("小明")`：装饰器的 `wrapper` 先打印 `"开始"`，然后调用原函数 `greet("小明")` 打印 `"Hello, 小明!"`，最后打印 `"结束"`。`greet` 没有 `return`，所以 `result` 是 `None`，但也没被打印。
- `print("---")`：打印分隔线。
- `print(add(3, 5))`：装饰器的 `wrapper` 打印 `"开始"`，调用原函数 `add(3, 5)` 返回 `8`，打印 `"结束"`。`wrapper` 返回 `8`，外层的 `print()` 接着打印 `8`。

注意装饰器中 `status = func(*args)` 接收了原函数的返回值，并且 `wrapper` 也 `return status` 把它传递了出去，这样外层才能拿到 `8` 这个值。