## 6.3 返回值和作用域——函数的"输出"与"领地"

参数决定了函数能接收什么数据，而返回值决定了函数能交出什么成果。与此同时，函数内外还存在一道隐形的"围栏"——作用域——它决定了变量在哪里可见、在哪里不可见。本节将这两个密切相关的概念一并讲透。

### 6.3.1 `return` 语句——函数的"交货单"

`return` 做了两件事：**终止函数执行**，以及**把一个值（或多个值）交还给调用者**。

```python
def add(a, b):
    return a + b        # 计算并返回结果

result = add(3, 5)       # result 接收到返回值 8
print(result)
```

一个函数可以有多个 `return` 语句——不同的条件走不同的返回路径。一旦执行到任何一个 `return`，函数立刻结束：

```python
def get_grade_level(score):
    if score >= 90:
        return "优秀"
    elif score >= 80:
        return "良好"
    elif score >= 60:
        return "及格"
    return "不及格"            # 前面的都没命中时执行，无需 else

print(get_grade_level(85))     # 良好
```

没有 `return` 语句的函数（或执行了不跟任何值的 `return`），默认返回 `None`。`None` 是 Python 中表示"什么都没有"的特殊值：

```python
def say_hello():
    print("Hello!")             # 只有 print，没有 return

result = say_hello()           # 输出：Hello!
print(result)                  # None
print(type(result))            # <class 'NoneType'>
```

---

\begin{tipbox}
**"副作用"函数 vs "纯函数"**

- **纯函数**：有 `return`，不修改外部状态，同样的输入总是得到同样的输出（如 `add(3, 5)` 永远返回 `8`）。易于测试、易于理解。
- **有副作用的函数**：没有 `return`（或返回 `None`），主要依赖 `print()`、修改全局变量、写入文件等"副作用"来完成工作。

实际项目中两者都会用到，但尽量让核心计算逻辑放在纯函数中，让副作用集中在一处管理——这个习惯会让代码的可维护性提升一个数量级。
\end{tipbox}

---

### 6.3.2 返回多个值——其实返回的是一个元组

Python 的函数可以"返回多个值"，本质上是返回一个元组，调用方用解包语法接收：

```python
def get_user_info():
    return "小明", 25, "北京"     # 等价于 return ("小明", 25, "北京")

name, age, city = get_user_info()  # 解包接收
print(name, age, city)             # 小明 25 北京
```

这一特性使得函数可以自然地返回一组相关联的数据，而不需要借助全局变量或复杂的数据结构。

### 6.3.3 作用域——变量的"可见范围"

作用域（Scope）决定了变量在哪里能够被访问。Python 使用 **LEGB 规则**，从近到远依次查找变量：

| 层级 | 名称 | 说明 |
|:----:|:-----|:-----|
| **L**ocal | 局部作用域 | 函数内部定义的变量，只在函数内可见 |
| **E**nclosing | 封闭作用域 | 外层函数的局部变量，对内层函数可见 |
| **G**lobal | 全局作用域 | 模块级别定义的变量，整个文件可见 |
| **B**uilt-in | 内置作用域 | Python 自带的函数和常量（`print`、`len`、`True` 等） |

#### 局部变量 vs 全局变量

```python
x = 100                    # 全局变量 x

def show():
    x = 200                # 局部变量 x——和全局 x 不是同一个
    print(f"函数内 x = {x}")

show()                     # 函数内 x = 200
print(f"函数外 x = {x}")   # 函数外 x = 100（全局 x 没有被修改）
```

在这个例子中，函数内赋值的 `x = 200` 创建了一个全新的局部变量，它和全局的 `x` 只是名字相同，实际上是完全独立的两块内存空间。函数内部优先使用局部变量，这就是 LEGB 规则中的 L（Local）在起作用。

#### 在函数内修改全局变量

如果确实需要在函数内部修改全局变量，使用 `global` 关键字声明：

```python
count = 0

def increment():
    global count              # 声明"我要用全局的 count，不是新建局部的"
    count += 1

increment()
increment()
print(count)                  # 2
```

---

\begin{warningbox}
**慎用 `global`！**

`global` 虽然提供了修改全局变量的能力，但过度使用会让程序的逻辑流变得难以追踪——你无法确定一个全局变量是在哪个函数的哪个角落被修改的。如果一个函数需要修改外部状态，优先考虑通过**参数传入、返回值传出**的方式，这样函数的输入输出都是显式的，可读性和可测试性都更好。
\end{warningbox}

---

#### 封闭作用域与 `nonlocal`

当函数嵌套定义时，内层函数可以访问外层函数的局部变量（这就是 E 层——Enclosing）。如果需要在内层函数中修改外层变量，使用 `nonlocal`：

```python
def outer():
    count = 0               # 外层函数的局部变量

    def inner():
        nonlocal count      # 声明"我要用的是外层的 count"
        count += 1
        return count

    return inner

counter = outer()
print(counter())             # 1
print(counter())             # 2
print(counter())             # 3
```

这个例子展示了一个重要的概念——**闭包**（Closure）。`outer()` 返回了 `inner` 函数本身，而 `inner` "记住"了 `outer` 中 `count` 的值。每次调用 `counter()` 时，`count` 在上一次的基础上递增，形成了一个简易的计数器。闭包是实现装饰器的基础，在 6.5 节中会再次遇到它。

### 6.3.4 实战练习

1. 定义函数 `safe_divide(a, b)`，如果 `b` 为 0 则返回字符串 `"除数不能为零"`，否则返回 `a / b` 的结果（保留两位小数）。测试 `safe_divide(10, 2)` 和 `safe_divide(10, 0)`。

2. 定义函数 `min_max_avg(*args)`，接收任意个数字，返回一个元组 `(最小值, 最大值, 平均值)`。如果没传参数，返回 `(None, None, None)`。

3. 阅读以下代码，逐行写出输出并解释为何是这个结果：

```python
msg = "你好"

def change_locally():
    msg = "Hello"
    print("函数内:", msg)

def change_globally():
    global msg
    msg = "Hello"
    print("函数内:", msg)

print("1:", msg)
change_locally()
print("2:", msg)
change_globally()
print("3:", msg)
```