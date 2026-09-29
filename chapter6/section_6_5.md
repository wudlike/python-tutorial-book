## 6.5 装饰器——给函数"穿上盔甲"

装饰器（Decorator）是 Python 中最优雅的设计模式之一。它的核心思想简洁而强大：**在不修改原函数代码的前提下，给函数增加额外的功能**。可以把装饰器理解为一件透明的盔甲——函数还是那个函数，但穿上盔甲后，它在执行之前、之后或出错时多了一套自动触发的行为。

### 6.5.1 从一个真实需求出发

假设你写了三个函数，分别处理订单、查询库存和发送通知。上线后你发现需要给每个函数加上日志——记录"谁在什么时间调用了哪个函数"。最笨的办法是修改每个函数，在开头加一行日志代码：

```python
def process_order():
    print(f"[日志] 调用了 process_order")
    # ... 业务逻辑 ...

def query_stock():
    print(f"[日志] 调用了 query_stock")
    # ... 业务逻辑 ...
```

问题是：如果有 50 个函数要加日志呢？如果以后要加权限检查、性能监控呢？每次都改 50 个函数显然不现实。装饰器的设计正是为了解决这个痛点——它把"加日志"这个横切关注点抽离出来，写一次，到处套用。

### 6.5.2 函数是一等公民——装饰器的前置知识

在理解装饰器之前，先确认一个概念：**在 Python 中，函数和整数、字符串一样，都是对象**。这意味着你可以把函数赋给变量、当作参数传递、甚至在一个函数内部定义并返回另一个函数。

```python
def say_hello():
    print("Hello!")

greet = say_hello         # 把函数赋给变量
greet()                   # Hello!——和调用 say_hello() 一样

def call_twice(func):     # 函数作为参数
    func()
    func()

call_twice(say_hello)
# Hello!
# Hello!
```

这是理解"装饰器如何工作"的基石。如果函数可以像普通变量一样被传递，那么就可以写一个函数来"包装"另一个函数，在包装过程中附加额外的行为。

### 6.5.3 手写一个最简单的装饰器

让我们一步一步构建装饰器，从最朴素的版本开始：

**第一步：定义一个"包装函数"**

```python
def log_decorator(func):
    """接收一个函数，返回一个"加过日志"的新函数"""
    def wrapper():
        print(f"[日志] 即将执行 {func.__name__}")
        result = func()
        print(f"[日志] {func.__name__} 执行完毕")
        return result
    return wrapper
```

这个 `log_decorator` 接收函数 `func` 作为参数，内部定义了 `wrapper` 函数——它在调用 `func` 前后各打印一行日志——然后返回 `wrapper`。注意 `wrapper` 是通过闭包"记住"了外层的 `func` 的。

**第二步：手动应用装饰器**

```python
def greet():
    print("Hello, World!")

greet = log_decorator(greet)     # 用装饰器"包装" greet
greet()

# 输出：
# [日志] 即将执行 greet
# Hello, World!
# [日志] greet 执行完毕
```

`log_decorator(greet)` 返回了一个新函数 `wrapper`，赋值回 `greet`。此后调用 `greet()` 实际执行的是 `wrapper()`——原函数的功能不变，但多了一层日志包裹。

**第三步：使用 `@` 语法糖**

上面的两步走可以简化为一行 `@` 符号：

```python
@log_decorator
def greet():
    print("Hello, World!")
```

`@log_decorator` 等价于 `greet = log_decorator(greet)`，但写在函数定义的正上方，意图更加明确——"这个函数被 `log_decorator` 装饰了"。当代码量变大时，这种声明式的写法比手动赋值清晰得多。

### 6.5.4 处理带参数的函数

上面的 `wrapper` 没有接收参数，这意味着它只能装饰无参数的函数。要支持任意参数的函数，使用 `*args` 和 `**kwargs`：

```python
def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"[日志] 调用 {func.__name__}, 参数: {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"[日志] {func.__name__} 返回: {result}")
        return result
    return wrapper

@log_decorator
def add(a, b):
    return a + b

result = add(3, 5)
# [日志] 调用 add, 参数: (3, 5), {}
# [日志] add 返回: 8
print(result)    # 8
```

`*args` 和 `**kwargs` 在这里扮演了"万能转发"的角色——不管原函数接收什么参数，装饰器都能原封不动地传过去。这是装饰器的标准写法，几乎每个装饰器的 `wrapper` 都会用这个模式。

### 6.5.5 一个实用的装饰器——计时器

除了日志，装饰器最常见的应用场景是**性能监控**——测量一个函数的执行时间：

```python
import time

def timer(func):
    """打印函数执行时间的装饰器"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 执行耗时: {end - start:.4f} 秒")
        return result
    return wrapper

@timer
def slow_calculation():
    total = 0
    for i in range(1, 10_000_001):
        total += i
    return total

result = slow_calculation()
# slow_calculation 执行耗时: 0.5123 秒
print(f"结果: {result}")
```

这个装饰器在后端的性能调优中极为实用——你可以快速定位哪个函数是性能瓶颈，而不需要在每个函数里手动加计时代码。

---

\begin{tipbox}
**装饰器的核心心法**

装饰器本质上就是：

```python
被装饰的函数 = 装饰器(被装饰的函数)
```

其中装饰器是一个"接收函数并返回新函数"的函数。`@` 语法只是让这个赋值过程变得隐式和美观。理解了"函数是一等公民""闭包捕获变量"和"接收函数、返回函数"这三件事，装饰器就没有任何神秘之处。
\end{tipbox}

---

### 6.5.6 实战练习

1. 编写一个装饰器 `bold_decorator`，它不修改原函数的返回值，而是在返回值的前后加上 `**`，形成"加粗"效果。例如：

```python
@bold_decorator
def get_title():
    return "Python教程"

print(get_title())    # **Python教程**
```

2. 编写一个装饰器 `retry`，它会在被装饰的函数抛出异常时自动重试最多 3 次。如果 3 次都失败，抛出最后一次的异常。提示：用 `try-except`（下一章会详细讲，这里先用 `try...except Exception: pass` 占位即可）。

3. 阅读以下代码，写出输出结果：

```python
def deco(func):
    def wrapper(*args):
        print("开始")
        result = func(*args)
        print("结束")
        return result
    return wrapper

@deco
def greet(name):
    print(f"Hello, {name}!")

@deco
def add(a, b):
    return a + b

greet("小明")
print("---")
print(add(3, 5))
```