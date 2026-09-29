## 10.3 闭包与装饰器进阶——函数的"记忆"与"包装"

在第 6 章中你已经学会了装饰器的基本用法——用 `@decorator` 语法给函数增加日志、计时等功能。但这只是装饰器的"表层"。要真正理解装饰器的原理、写出带参数的装饰器、甚至用类来实现装饰器，你需要先深入理解**闭包**（Closure）。

### 10.3.1 闭包——函数"记住"了它的出生地

闭包的定义很简单：**一个内部函数引用了外部函数的变量，并且外部函数把这个内部函数返回了，这个内部函数就形成了一个闭包。** 闭包的关键在于它"记住"了外部函数的变量，即使外部函数已经执行完毕。

```python
def make_multiplier(factor):
    """返回一个"乘以 factor"的函数"""
    def multiplier(x):
        return x * factor      # multiplier 引用了外部变量 factor
    return multiplier

double = make_multiplier(2)     # factor=2——double 是"乘 2"函数
triple = make_multiplier(3)     # factor=3——triple 是"乘 3"函数

print(double(5))                # 10
print(triple(5))                # 15
```

为什么 `double(5)` 返回 10？`make_multiplier(2)` 执行完后，按理说局部变量 `factor` 应该被销毁了。但 `multiplier` 函数"记住"了它——这个变量的值被保存在了闭包对象的 `__closure__` 属性中：

```python
print(double.__closure__[0].cell_contents)    # 2——闭包确实记住了 factor 的值
```

闭包是装饰器的基石——装饰器本质上就是一个"接收函数、返回在闭包中包装过的函数"的模式。

### 10.3.2 装饰器复习与深化——让包装函数"不留痕迹"

在第 6 章中我们写过一个计时装饰器。但它有一个小瑕疵：被装饰之后，函数的 `__name__` 和 `__doc__` 变成了 `wrapper` 的，原始信息丢失了：

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} 耗时: {time.time() - start:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    """这个函数很慢"""
    total = sum(range(1_000_000))
    return total

print(slow_function.__name__)    # wrapper——而不是 slow_function！
print(slow_function.__doc__)     # None——文档字符串丢了！
```

修复这个问题，使用 `functools.wraps`：

```python
from functools import wraps

def timer(func):
    @wraps(func)                    # 把 func 的元信息"复制"到 wrapper 上
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} 耗时: {time.time() - start:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    """这个函数很慢"""
    total = sum(range(1_000_000))
    return total

print(slow_function.__name__)    # slow_function——正确！
print(slow_function.__doc__)     # 这个函数很慢——正确！
```

`@wraps(func)` 是每个装饰器都应该加上的"标准配置"——它让你的装饰器对调试工具、文档生成器和 `help()` 函数保持友好。

### 10.3.3 带参数的装饰器——"装饰器的工厂"

有时你需要装饰器本身能接受参数。比如一个 `retry` 装饰器，有时需要重试 3 次，有时需要重试 5 次。这需要在装饰器外面再包一层函数——"装饰器工厂"：

```python
from functools import wraps
import time

def retry(max_attempts=3, delay=1.0):
    """装饰器工厂——返回一个配置好的装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise       # 最后一次也失败了，抛出异常
                    print(f"第 {attempt} 次失败（{e}），{delay} 秒后重试...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def unreliable_api():
    import random
    if random.random() < 0.7:
        raise ConnectionError("网络不稳定")
    return "数据获取成功"

print(unreliable_api())
```

带参数装饰器的"三层结构"理解起来有些绕，但可以按这个思路拆解：
1. `@retry(max_attempts=3, delay=0.5)` 首先调用 `retry(max_attempts=3, delay=0.5)`，它返回一个配置好的装饰器 `decorator`
2. `decorator` 接收 `unreliable_api` 函数，返回包装后的 `wrapper`（和普通装饰器一样）
3. `wrapper` 在被调用时，按照配置的重试逻辑来执行原函数

### 10.3.4 用类实现装饰器——当装饰器需要维护状态

大多数装饰器用函数就够。但有些场景需要装饰器自身记住一些"跨调用"的状态（比如统计函数被调用了多少次），这时用类来实现更自然：

```python
from functools import wraps

class CallCounter:
    """统计函数被调用次数的装饰器"""
    def __init__(self, func):
        wraps(func)(self)           # 将 func 的元信息复制到 self 上
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"{self.func.__name__} 第 {self.count} 次被调用")
        return self.func(*args, **kwargs)

@CallCounter
def greet(name):
    print(f"Hello, {name}!")

greet("小明")    # greet 第 1 次被调用 / Hello, 小明!
greet("小红")    # greet 第 2 次被调用 / Hello, 小红!
greet("小刚")    # greet 第 3 次被调用 / Hello, 小刚!
```

用类做装饰器的关键在于 `__call__` 方法——它让实例可以像函数一样被调用。`@CallCounter` 等价于 `greet = CallCounter(greet)`，此时 `greet` 是 `CallCounter` 的一个实例，但因为它实现了 `__call__`，所以 `greet("小明")` 会触发 `__call__("小明")`。

### 10.3.5 实战练习

1. 编写一个装饰器 `repeat(n)`，让被装饰的函数重复执行 `n` 次，并将每次的返回值收集成一个列表返回。例如：

```python
@repeat(3)
def roll_dice():
    import random
    return random.randint(1, 6)

print(roll_dice())    # 例如 [4, 1, 6]
```

要求使用 `functools.wraps` 保留原函数的元信息。

2. 编写一个带缓存的装饰器 `memoize`，将函数的输入和对应的输出缓存起来。如果再次以相同的参数调用函数，直接返回缓存的结果而不重新计算。提示：用字典作为缓存存储。

```python
@memoize
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(100))    # 应该能秒出结果，比不用缓存快几个数量级
```

3. 分析以下代码的输出，解释 `@deco` 的执行时机：

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