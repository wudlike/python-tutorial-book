## 10.1 列表推导式——一行胜千言

列表推导式（List Comprehension）在前面的章节中已经多次出现——我们用它来快速生成列表、筛选元素、做数据转换。但作为一个核心 Python 特性，它值得用一整节来系统地展开，从基础用法到多条件、嵌套推导，让你彻底掌握这个"一行胜千言"的工具。

### 10.1.1 从 `for` 循环到推导式——一种思维转变

先用一个对比来感受推导式的简洁：

```python
# 传统 for 循环
squares = []
for x in range(1, 11):
    squares.append(x ** 2)

# 列表推导式——一行搞定
squares = [x ** 2 for x in range(1, 11)]

print(squares)    # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

推导式的基本语法可以概括为：`[表达式 for 变量 in 可迭代对象]`。Python 会遍历可迭代对象中的每一个元素，对每个元素计算"表达式"的值，然后把所有结果收集成一个新列表。

**推导式不仅仅是为了少写几行代码。** 它是一种声明式编程——你告诉 Python"我想要什么结果"，而不是"一步步怎么做"。在很多场景下，推导式的执行速度也比等价的 `for` 循环更快，因为它的循环逻辑是在 C 层面实现的。

### 10.1.2 带条件的推导式——筛选与映射同时进行

在推导式末尾加上 `if` 条件，就能在生成的同时完成筛选：

```python
# 只保留偶数
evens = [x for x in range(20) if x % 2 == 0]
print(evens)    # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# 映射 + 筛选——取偶数的平方
even_squares = [x ** 2 for x in range(20) if x % 2 == 0]
print(even_squares)    # [0, 4, 16, 36, 64, 100, 144, 196, 256, 324]

# 数据清洗——过滤掉空字符串并转小写
words = ["Python", "", "Java", "  ", "Go", None]
cleaned = [w.strip().lower() for w in words if w and w.strip()]
print(cleaned)    # ['python', 'java', 'go']
```

条件 `if` 可以放在推导式的两个位置，作用不同：

```python
# 位置一：末尾——用于筛选（过滤元素）
[x for x in range(20) if x % 3 == 0]          # 只保留 3 的倍数

# 位置二：表达式部分的三元运算符——用于变换值
[x if x % 2 == 0 else -x for x in range(10)]  # 偶数原样，奇数变负数
# 结果：[0, -1, 2, -3, 4, -5, 6, -7, 8, -9]
```

注意这两个 `if` 的位置和含义完全不同——在末尾的 `if` 是过滤器，在表达式里的 `if-else` 是条件表达式（三元运算符）。前者不能带 `else`，后者必须有 `else`。

### 10.1.3 嵌套推导式——处理二维数据

推导式中可以包含多层 `for`，用于处理嵌套结构：

```python
# 展开二维列表——把嵌套列表"拍平"
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
print(flattened)    # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# 等价的 for 循环写法（对比复杂度）
flattened = []
for row in matrix:
    for num in row:
        flattened.append(num)

# 生成乘法口诀表
mul_table = [[i * j for j in range(1, 10)] for i in range(1, 10)]
```

嵌套推导式最外层（最左边的 `for`）是外层循环，往右依次是内层循环——和实际 `for` 循环的书写顺序一致，这一点很自然。

---

\begin{warningbox}
**嵌套推导式的可读性边界**

推导式虽强，但过度嵌套会变成"代码谜题"。当推导式需要三行才能写完时，停下来想一想：拆成普通 `for` 循环是否更清晰？一个判断标准是：**如果你的推导式需要别人盯着看 10 秒钟才能理解它在做什么，那就拆开写。**

```python
# 糟糕——不可读
result = [y for x in lst for y in x if y > 0 and y % 2 == 0]

# 清晰——可读
result = []
for sublist in lst:
    for item in sublist:
        if item > 0 and item % 2 == 0:
            result.append(item)
```
\end{warningbox}

---

### 10.1.4 字典推导式与集合推导式

推导式语法不仅适用于列表：

```python
# 字典推导式——{键表达式: 值表达式 for ... in ...}
word_to_length = {w: len(w) for w in ["apple", "banana", "cherry"]}
print(word_to_length)    # {'apple': 5, 'banana': 6, 'cherry': 6}

# 键值互换
original = {"a": 1, "b": 2, "c": 3}
swapped = {v: k for k, v in original.items()}
print(swapped)           # {1: 'a', 2: 'b', 3: 'c'}

# 集合推导式——{表达式 for ... in ...}
unique_lengths = {len(w) for w in ["apple", "banana", "cherry", "date"]}
print(unique_lengths)    # {4, 5, 6}——自动去重
```

### 10.1.5 生成器表达式——需要时才计算的"懒推导式"

把列表推导式的方括号换成圆括号，得到的就是**生成器表达式**——它不会一次性生成整个列表，而是一个"按需生成"的迭代器（参见 10.2 节）：

```python
# 列表推导式——立即计算，占用 100 万个元素的内存
big_list = [x ** 2 for x in range(1_000_000)]

# 生成器表达式——延迟计算，几乎不占内存
big_gen = (x ** 2 for x in range(1_000_000))
print(next(big_gen))    # 1
print(next(big_gen))    # 4
print(next(big_gen))    # 9
```

当数据量巨大时（百万级、千万级），生成器表达式可以避免"撑爆内存"的情况。10.2 节将深入展开生成器的工作原理。

### 10.1.6 实战练习

1. 使用列表推导式生成 1 到 100 之间所有能被 7 整除但不能被 5 整除的数。

2. 给定字符串列表 `words = ["Python", "go", "JAVA", "rust", "C++"]`，用列表推导式完成：
   - 筛选出长度大于 3 的单词并全部转为小写
   - 生成一个字典，键为原单词，值为其长度

3. 阅读以下推导式，写出其等价的结果（或 `for` 循环版本）：

```python
result = [(x, y) for x in range(1, 4) for y in range(1, 4) if x != y]
print(result)
```