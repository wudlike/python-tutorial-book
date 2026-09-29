## 10.2 生成器与迭代器——"按需供货"的智慧

在 10.1 节的末尾，我们提到了生成器表达式——用 `()` 代替 `[]`，就能把一个列表推导式变成"不占内存的懒计算版本"。这个魔法背后是 Python 中最强大也最容易被忽视的两个概念：**迭代器**和**生成器**。理解它们，你就能在处理海量数据时游刃有余。

### 10.2.1 迭代器——可以"逐个取东西"的对象

迭代器（Iterator）不是一种特定的数据结构，而是一种**协议**——任何实现了 `__iter__()` 和 `__next__()` 两个方法的对象，都是一个迭代器。它的核心能力是"记住自己当前遍历到哪里了"，每次调用 `__next__()` 就返回下一个元素。

Python 中几乎所有能用在 `for...in` 循环中的东西都是可迭代对象（Iterable）——列表、元组、字典、集合、字符串、文件对象……但它们不一定是迭代器。区别在于：

- **可迭代对象**（Iterable）：实现了 `__iter__()`，可以被 `iter()` 转换成迭代器
- **迭代器**（Iterator）：同时实现了 `__iter__()` 和 `__next__()`，是一个"状态机"

```python
nums = [1, 2, 3]
it = iter(nums)             # 将列表转换成迭代器

print(next(it))             # 1——取出第一个
print(next(it))             # 2——取出第二个
print(next(it))             # 3——取出第三个
print(next(it))             # StopIteration 异常——没有更多元素了
```

`for` 循环在底层就是上面这套流程的自动化——它先调用 `iter()` 获取迭代器，然后反复调用 `next()` 直到捕获 `StopIteration`。这也解释了为什么 `for` 循环结束后迭代器就"空了"——它已经走到了尽头：

```python
it = iter([1, 2, 3])
for x in it:
    print(x)        # 1, 2, 3
for x in it:
    print(x)        # 什么都不输出——迭代器已经耗尽了
```

### 10.2.2 自定义迭代器——让你的类支持 `for` 循环

```python
class Countdown:
    """倒计时迭代器——从 n 倒数到 1"""
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self                     # 迭代器自身就是自己的迭代器

    def __next__(self):
        if self.current <= 0:
            raise StopIteration         # 终止信号
        value = self.current
        self.current -= 1
        return value

for num in Countdown(5):
    print(num, end=" ")    # 5 4 3 2 1
```

---

\begin{notebox}
**为什么迭代器要"一次性"？**

迭代器的设计哲学是"流式处理"——从头到尾消费一遍，不会回头。这有两个好处：
1. 内存效率极高——不需要把整个数据集同时加载到内存中，只需要在每次 `next()` 时计算下一个值
2. 可以表示无限序列——比如 `itertools.count()` 会无限递增，而 `for` 循环可以用 `break` 随时停止

如果你需要多次遍历同样的数据，用列表（可迭代对象）而不是迭代器——列表每次 `for` 循环都会从头开始。
\end{notebox}

---

### 10.2.3 生成器——用函数"产出"数据

迭代器功能强大但写起来麻烦——你需要实现类、维护状态、手动抛出 `StopIteration`。生成器（Generator）是 Python 提供的"语法糖"，让你用一个包含 `yield` 关键字的函数就能创建迭代器。

```python
def countdown(n):
    """生成器函数——倒计时"""
    while n > 0:
        yield n                    # "产出"当前值，然后暂停，等待下次调用
        n -= 1

gen = countdown(5)
print(type(gen))                   # <class 'generator'>
print(next(gen))                   # 5
print(next(gen))                   # 4
print(list(gen))                   # [3, 2, 1]——消耗完剩余的值
```

**`yield` 和 `return` 的关键区别：**
- `return`：函数执行结束，交出控制权，所有局部变量销毁
- `yield`：函数**暂停**（不是结束），交出控制权和当前值，等待下一次 `next()` 调用时从暂停点恢复，局部变量的状态完整保留

这种"暂停-恢复"的能力让生成器非常适合处理序列化的数据流——逐行读取大文件、逐帧处理视频、逐条消费消息队列等。

### 10.2.4 生成器表达式——列表推导式的"惰性兄弟"

```python
# 列表推导式——一次性生成 1000 万个元素 → 内存爆炸
squares_list = [x ** 2 for x in range(10_000_000)]    # 谨慎运行！

# 生成器表达式——逐个产出，内存占用几乎为零
squares_gen = (x ** 2 for x in range(10_000_000))
print(next(squares_gen))    # 0
print(next(squares_gen))    # 1
```

生成器表达式可以直接作为函数参数传入（此时可以省略外面一层的括号）：

```python
total = sum(x ** 2 for x in range(10_000_000))    # 不会创建 1000 万个元素的中间列表
print(total)
```

`sum()` 内部会迭代这个生成器，逐个取值并累加——没有任何时刻内存中同时存在全部 1000 万个数值。

### 10.2.5 实战练习

1. 编写一个生成器函数 `fibonacci(n)`，生成前 `n` 个斐波那契数（前两个是 1, 1，之后每个都是前两个之和）。用 `for` 循环遍历 `fibonacci(10)` 并打印每个数。

2. 使用生成器表达式编写一行代码，计算 1 到 1000000 中所有奇数的平方和。注意不要创建包含 100 万个元素的中间列表。

3. 阅读以下代码，逐行写出输出：

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