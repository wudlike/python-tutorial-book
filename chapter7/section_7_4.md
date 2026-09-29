## 7.4 特殊方法——让对象"活起来"

你已经接触过 `__init__` 这个特殊方法——它在对象创建时自动被调用。Python 中还有一整套以双下划线开头和结尾的"特殊方法"（也叫魔术方法或 dunder methods），它们让自定义类的对象能够像内置类型一样自然地进行初始化、打印、比较、运算等操作。掌握了特殊方法，你的类就从"哑巴对象"升级成了"一等公民"。

### 7.4.1 `__init__`——对象的构造函数

`__init__` 是使用频率最高的特殊方法。它在对象被创建后立即执行，负责初始化实例的属性：

```python
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

book = Book("三体", "刘慈欣", 400)
```

需要注意一个常见的误区：`__init__` 不是真正意义上的"构造函数"——在 `__init__` 被调用之前，对象已经被 Python 的 `__new__` 方法创建好了。`__init__` 的职责是**初始化**这个已经存在的对象，给它赋予初始状态。对绝大多数日常编程任务来说，你只需要关心 `__init__`，不需要碰 `__new__`。

### 7.4.2 `__str__` 和 `__repr__`——让对象"说人话"

默认情况下，打印一个自定义对象会显示类似 `<__main__.Book object at 0x7f...>` 的信息——这串字符对调试几乎没有任何帮助。`__str__` 和 `__repr__` 就是为了让对象在打印时输出有意义的信息：

```python
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __str__(self):
        """给用户看的——用 str() 或 print() 触发"""
        return f"《{self.title}》作者：{self.author}，共 {self.pages} 页"

    def __repr__(self):
        """给开发者看的——用 repr() 或在交互式环境中直接输入变量名时触发"""
        return f"Book('{self.title}', '{self.author}', {self.pages})"

book = Book("三体", "刘慈欣", 400)
print(book)           # 《三体》作者：刘慈欣，共 400 页（调用 __str__）
print(repr(book))     # Book('三体', '刘慈欣', 400)（调用 __repr__）
```

两者的分工很明确：
- **`__str__`** 面向最终用户——输出应该清晰易读，像一句话
- **`__repr__`** 面向开发者——输出应该尽可能精确，最好能直接用 `eval()` 还原出对象（`repr(obj)` 的理想标准是 `eval(repr(obj)) == obj`）

如果只定义了 `__repr__` 而没有定义 `__str__`，Python 会用 `__repr__` 代替 `__str__`。反过来则不行——所以如果只想写一个，优先写 `__repr__`。

### 7.4.3 比较运算符——`__eq__`、`__lt__` 等

默认情况下，两个自定义对象用 `==` 比较时会比较它们的**内存地址**（即是否是同一个对象），而不是比较内容。要基于内容进行比较，需要定义比较相关的特殊方法：

```python
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __eq__(self, other):
        """定义 == 的行为：分数相同即相等"""
        if not isinstance(other, Student):
            return NotImplemented
        return self.score == other.score

    def __lt__(self, other):
        """定义 < 的行为：按分数比较"""
        if not isinstance(other, Student):
            return NotImplemented
        return self.score < other.score

    def __repr__(self):
        return f"Student('{self.name}', {self.score})"

s1 = Student("小明", 90)
s2 = Student("小红", 90)
s3 = Student("小刚", 80)

print(s1 == s2)          # True——分数相同
print(s1 == s3)          # False——分数不同
print(s3 < s1)           # True——80 < 90

students = [s1, s2, s3]
print(sorted(students))  # [Student('小刚', 80), Student('小明', 90), Student('小红', 90)]
```

定义了 `__eq__` 和 `__lt__` 之后，`sorted()` 就能直接对学生列表排序了——因为 `sorted()` 内部依赖 `<` 比较来决定元素顺序。Python 提供了 `functools.total_ordering` 装饰器，只需要定义 `__eq__` 和任意一个比较方法（如 `__lt__`），其余的比较方法（`__le__`、`__gt__`、`__ge__`）会自动推导出来，省去大量重复代码。

---

\begin{notebox}
**`NotImplemented` vs `NotImplementedError`**

在上面的代码中，`isinstance` 检查失败时返回的是 `NotImplemented`（单数，一个特殊常量），而不是抛出 `NotImplementedError`（一个异常）。`NotImplemented` 告诉 Python："这个比较我不支持，请尝试用 `other` 的反向方法"，给了 Python 一个"回退"的机会。这是一种优雅的互操作机制。
\end{notebox}

---

### 7.4.4 `__len__` 和 `__contains__`——让对象支持 `len()` 和 `in`

```python
class Playlist:
    def __init__(self, name):
        self.name = name
        self.songs = []

    def add_song(self, song):
        self.songs.append(song)

    def __len__(self):
        """支持 len() 函数"""
        return len(self.songs)

    def __contains__(self, song):
        """支持 in 运算符"""
        return song in self.songs

playlist = Playlist("我的最爱")
playlist.add_song("晴天")
playlist.add_song("七里香")
playlist.add_song("稻香")

print(len(playlist))            # 3——像内置容器一样使用
print("晴天" in playlist)       # True
print("夜曲" in playlist)       # False
```

定义了这两个方法后，`Playlist` 的表现就和 Python 内置的列表一样自然——不用记 `playlist.get_count()` 或 `playlist.has_song()` 这种定制方法名，直接用熟悉的 `len()` 和 `in`。

### 7.4.5 `__getitem__` 和 `__setitem__`——像操作列表一样操作对象

```python
class SimpleDict:
    """一个简单的字典包装器，演示 __getitem__ 和 __setitem__"""
    def __init__(self):
        self._data = {}

    def __getitem__(self, key):
        """支持 obj[key] 读取"""
        print(f"读取键 '{key}'")
        return self._data[key]

    def __setitem__(self, key, value):
        """支持 obj[key] = value 赋值"""
        print(f"设置键 '{key}' = {value}")
        self._data[key] = value

    def __delitem__(self, key):
        """支持 del obj[key] 删除"""
        print(f"删除键 '{key}'")
        del self._data[key]

d = SimpleDict()
d["name"] = "小明"         # 设置键 'name' = 小明
d["age"] = 20              # 设置键 'age' = 20
print(d["name"])           # 读取键 'name' → 小明
del d["age"]               # 删除键 'age'
```

### 7.4.6 其他常用特殊方法速查

| 特殊方法 | 触发方式 | 用途 |
|:---------|:---------|:-----|
| `__init__(self, ...)` | `obj = Class(...)` | 初始化对象 |
| `__str__(self)` | `str(obj)`、`print(obj)` | 可读的字符串表示 |
| `__repr__(self)` | `repr(obj)`、交互式环境直接输入变量 | 精确的字符串表示 |
| `__len__(self)` | `len(obj)` | 返回长度 |
| `__eq__(self, other)` | `obj == other` | 相等比较 |
| `__lt__(self, other)` | `obj < other` | 小于比较 |
| `__add__(self, other)` | `obj + other` | 加法运算 |
| `__getitem__(self, key)` | `obj[key]` | 索引访问 |
| `__setitem__(self, key, val)` | `obj[key] = val` | 索引赋值 |
| `__contains__(self, item)` | `item in obj` | 成员判断 |
| `__call__(self, ...)` | `obj(...)` | 让实例像函数一样被调用 |
| `__enter__`/`__exit__` | `with obj:` | 上下文管理器 |

### 7.4.7 实战练习

1. 定义一个 `Vector2D` 类，表示二维向量。包含 `x` 和 `y` 两个属性，实现 `__add__`（向量加法）、`__str__`（格式：`"Vector2D(x, y)"`）和 `__eq__`（两个向量的 x 和 y 都相等）。创建两个向量 `Vector2D(1, 2)` 和 `Vector2D(3, 4)`，测试加法和相等比较。

2. 定义一个 `Group` 类，内部用列表存储成员。实现 `__len__`（返回成员数量）、`__contains__`（判断某人是否在组里）和 `__getitem__`（支持用索引访问成员，如 `group[0]`）。创建一个包含三个成员的组并测试这三个特殊方法。

3. 下面的代码有什么问题？请修正：

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return self.name + " - " + self.price + "元"

p = Product("键盘", 299)
print(p)
```