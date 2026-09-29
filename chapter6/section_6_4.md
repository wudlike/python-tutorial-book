## 6.4 匿名函数——`lambda` 的轻量之道

在 Python 中，函数是第一等公民——你可以把函数赋给变量、当参数传递、甚至作为另一个函数的返回值。但有些时候，为了定义一个只用一次、只有一行表达式的小函数而正正规规写四行 `def` 显得过于隆重。`lambda` 就是为这种场景而生的——它在**一行之内**完成"接收参数、返回结果"的全过程。

### 6.4.1 `lambda` 的基本语法

`lambda` 的语法极简：

```python
lambda 参数1, 参数2, ... : 表达式
```

它等价于一个只有 `return 表达式` 的普通函数：

```python
add = lambda a, b: a + b
print(add(3, 5))           # 8

# 等价于：
def add(a, b):
    return a + b
```

`lambda` 与 `def` 的核心区别：

| 维度 | `def` | `lambda` |
|:-----|:------|:-----|
| 函数体 | 可以有多行语句 | **只能有一个表达式**（不能有 `print`、`if` 等多行逻辑） |
| 名称 | 有显式函数名 | 匿名——通常直接在调用处写，不赋给变量 |
| 文档字符串 | 支持 `"""..."""` | 不支持 |
| 适用场景 | 复杂逻辑、需要复用多次 | 简单映射、作为参数传给其他函数时只用一次 |
| 可读性 | 良好 | 过度使用会降低可读性 |

`lambda` 的精髓在于"**用完即弃**"——你不需要给它起名字，它在你需要的地方即时生成，完成任务后悄然消失。

### 6.4.2 `lambda` 的经典搭档

`lambda` 单独使用意义不大，它的真正威力体现在配合内置高阶函数（以函数作为参数的函数）时。

#### `sorted()` 配合 `lambda`——自定义排序规则

`sorted()` 的 `key` 参数需要一个函数来指定"按什么标准排序"，这正是 `lambda` 的绝佳舞台：

```python
students = [
    {"name": "小明", "score": 85},
    {"name": "小红", "score": 92},
    {"name": "小刚", "score": 78},
]

sorted_by_score = sorted(students, key=lambda s: s["score"], reverse=True)
print(sorted_by_score)
# [{'name': '小红', 'score': 92}, {'name': '小明', 'score': 85}, {'name': '小刚', 'score': 78}]
```

这里的 `lambda s: s["score"]` 告诉 `sorted()`："对于列表中的每个字典 `s`，用 `s["score"]` 的值来决定排序顺序"。如果没有 `lambda`，你需要单独定义一个函数，传参时写函数名，两相比较，`lambda` 的简洁优势就体现出来了。

另一个常用场景——按字符串长度排序：

```python
words = ["apple", "pie", "banana", "kiwi"]
print(sorted(words, key=lambda w: len(w)))
# ['pie', 'kiwi', 'apple', 'banana']
```

#### `map()` 配合 `lambda`——对每个元素做映射

`map(func, iterable)` 把 `func` 应用到序列的每个元素上，返回一个新的迭代器：

```python
nums = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, nums))
print(squared)                # [1, 4, 9, 16, 25]

celsius = [0, 20, 37, 100]
fahrenheit = list(map(lambda c: c * 9/5 + 32, celsius))
print(fahrenheit)             # [32.0, 68.0, 98.6, 212.0]
```

不过需要指出的是，在 Python 社区中，列表推导式通常比 `map(lambda ...)` 更受欢迎，因为它的可读性更好。上面两个例子用列表推导式写更 Pythonic：

```python
squared = [x ** 2 for x in nums]
fahrenheit = [c * 9/5 + 32 for c in celsius]
```

这并不代表 `map()` 和 `lambda` 的组合没有价值——在处理复杂的多序列映射、使用已有的命名函数时，`map()` 仍旧非常实用。

#### `filter()` 配合 `lambda`——筛选元素

`filter(func, iterable)` 保留 `func` 返回 `True` 的元素：

```python
nums = [12, 35, 60, 78, 41, 55, 93]
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)                  # [12, 60, 78]

high_scores = list(filter(lambda x: x >= 60, nums))
print(high_scores)            # [60, 78, 93]
```

同样，列表推导式在这里也是可选的替代方案。

---

\begin{definitionbox}
**何时用 `lambda`、何时用列表推导式？**

一个简单判断：
- 你只是要**筛选**或**变换**一个列表 → 用列表推导式（更 Pythonic）
- 你需要一个**临时函数**传给 `sorted()` 的 `key` 参数，或传给 `min()`/`max()` → 用 `lambda`（最自然）
- 逻辑超过一行，或需要复用 → 老老实实写 `def`

`lambda` 的魅力是简洁，它的天敌是过度使用。当表达式开始变得含混不清时，别犹豫，换 `def`。
\end{definitionbox}

---

### 6.4.3 `lambda` 的更多实用场景

**作为 `max()` 和 `min()` 的 `key`：**

```python
words = ["elephant", "cat", "dolphin", "bat"]
longest = max(words, key=lambda w: len(w))
print(longest)                # elephant

students = [("小明", 85), ("小红", 92), ("小刚", 78)]
best = max(students, key=lambda s: s[1])
print(best)                   # ('小红', 92)
```

**在 GUI 编程和事件处理中：** 当按钮点击需要执行一个简单函数时，`lambda` 可以让代码更紧凑（这部分在涉及具体框架时再深入）。

### 6.4.4 实战练习

1. 给定列表 `pairs = [(1, 3), (4, 1), (2, 2), (5, 0)]`，使用 `sorted()` 和 `lambda` 按每个元组的第二个元素从小到大排序，输出结果。

2. 给定列表 `words = ["Python", "Go", "Java", "C", "Rust"]`，使用 `filter()` 和 `lambda` 筛选出长度大于 3 的单词，将结果转为列表输出。

3. 给定学生成绩字典 `scores = {"小明": 85, "小红": 92, "小刚": 78, "小李": 95, "小王": 88}`：
   - 使用 `max()` 和 `lambda` 找出最高分的学生姓名
   - 使用 `sorted()` 和 `lambda` 将学生按成绩从高到低排列，输出姓名列表