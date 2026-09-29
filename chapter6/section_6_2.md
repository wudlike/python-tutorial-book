## 6.2 参数传递——函数的"输入通道"

参数是函数与外界沟通的桥梁。一个设计良好的函数应该像一台自动售货机——你投币（传参数），它出货（返回值），中间的机制你不需要关心。而 Python 在参数传递方面提供了丰富的语法，从最基础的位置参数到灵活的关键字参数和可变参数，掌握它们能让你的函数既强大又好用。

### 6.2.1 位置参数与关键字参数

**位置参数**是最常见的形式——调用时按顺序传值，一一对应：

```python
def describe_pet(name, animal_type):
    """描述一个宠物"""
    print(f"我有一只{animal_type}，名叫{name}。")

describe_pet("旺财", "狗")      # 正确：按顺序，name="旺财", animal_type="狗"
describe_pet("狗", "旺财")      # 逻辑错误！参数顺序反了，变成"我有一只旺财，名叫狗。"
```

当参数较多时，纯粹依赖顺序容易出错。Python 提供了**关键字参数**——调用时明确写出参数名，顺序就无关紧要了：

```python
describe_pet(animal_type="狗", name="旺财")    # 用关键字指定，顺序任意
describe_pet(name="咪咪", animal_type="猫")
```

位置参数和关键字参数可以混用，但有一个硬性规则：**位置参数必须放在关键字参数之前**。下面的写法会报错：

```python
describe_pet(name="旺财", "狗")     # SyntaxError！位置参数不能跟在关键字参数之后
```

---

\begin{tipbox}
**什么时候用关键字参数？**

如果函数有多个参数，且有些参数的含义从名字上不容易推断顺序（比如 `create_user(name, age, city, phone, email)`），用关键字参数能让调用代码自文档化——你不需要翻到函数定义处就能看懂每个值代表什么。这在大团队协作中尤其重要。
\end{tipbox}

---

### 6.2.2 默认参数——给参数预设"后备值"

有些参数在大多数调用中都是同一个值，只有少数情况才需要改。这时可以给参数设置**默认值**，调用时如果没传这个参数就使用默认值：

```python
def greet(name, greeting="你好"):
    """打招呼，默认用"你好" """
    print(f"{greeting}，{name}！")

greet("小明")                              # 你好，小明！（使用默认 greeting）
greet("小红", greeting="早上好")           # 早上好，小红！（覆盖默认值）
greet("小刚", "晚上好")                    # 晚上好，小刚！（按位置覆盖）
```

---

\begin{warningbox}
**默认参数的"陷阱"——不要用可变对象做默认值**

这是一个几乎每个 Python 程序员都踩过的坑：

```python
def add_item(item, items=[]):          # 错误！用空列表做默认值
    items.append(item)
    return items

print(add_item("a"))    # ['a']
print(add_item("b"))    # ['a', 'b']——预期是 ['b']，但上一次的列表还在！
```

原因在于：默认参数只在函数**定义时**被求值一次，而不是每次调用都重新创建。所以 `items=[]` 中的空列表在内存中是同一个对象，每次调用都在往同一个列表里追加。

**正确的做法：**

```python
def add_item(item, items=None):
    if items is None:
        items = []                     # 每次调用都创建新列表
    items.append(item)
    return items
```
\end{warningbox}

---

### 6.2.3 `*args`——接收任意数量的位置参数

当你不确定调用者会传多少个位置参数进来时（比如求任意个数的最大值），用 `*args` 来接收。星号 `*` 的作用是把所有多余的位置参数"打包"成一个元组。

```python
def sum_all(*args):
    """求任意个数的和"""
    print(f"收到了 {len(args)} 个参数：{args}")
    return sum(args)

print(sum_all(1, 2, 3))           # 收到了 3 个参数：(1, 2, 3)  → 6
print(sum_all(10, 20, 30, 40))    # 收到了 4 个参数：(10, 20, 30, 40)  → 100
```

`*args` 可以和普通参数混合使用。普通参数按位置正常匹配，剩余的由 `*args` 接收：

```python
def print_scores(course, *scores):
    """打印某门课的所有成绩"""
    total = sum(scores)
    print(f"{course}课共 {len(scores)} 次成绩，总分 {total}，平均 {total/len(scores):.1f}")

print_scores("数学", 88, 95, 73, 91)
# 数学课共 4 次成绩，总分 347，平均 86.8
```

---

\begin{notebox}
**`args` 只是约定俗成的名字**

`*args` 中的 `args` 可以换成任何合法的变量名（如 `*numbers`、`*items`），写成 `args` 只是 Python 社区的习惯。真正起作用的是前面的星号 `*`——它告诉 Python"把多个值打包成一个元组"。类似的，`**kwargs` 中的 `kwargs` 也可以改名，起作用的是双星号 `**`。
\end{notebox}

---

### 6.2.4 `**kwargs`——接收任意数量的关键字参数

双星号 `**` 把多余的关键字参数"打包"成一个字典：

```python
def build_profile(**kwargs):
    """构建一个用户档案"""
    for key, value in kwargs.items():
        print(f"{key}: {value}")

build_profile(name="小明", age=20, city="北京", hobby="编程")
# name: 小明
# age: 20
# city: 北京
# hobby: 编程
```

`*args` 和 `**kwargs` 可以同时使用。当四类参数（普通参数、`*args`、`**kwargs`）同时出现时，顺序必须严格遵循：**普通参数 → `*args` → 关键字参数 → `**kwargs`**。

### 6.2.5 参数传递的本质——引用传递

要深入理解函数参数，需要明白一个事实：Python 中变量名是"标签"，不是"盒子"。当调用 `func(x)` 时，形参和实参指向同一个对象。这意味着：

- 传递**不可变对象**（数字、字符串、元组）时，函数内修改不会影响外部——因为不可变对象本身无法被修改，"修改"操作实际上是创建了新对象
- 传递**可变对象**（列表、字典）时，函数内修改**会**影响外部——因为修改的是同一个对象的内容

```python
def modify_num(n):
    n = n + 10             # 创建了新整数对象，外部不受影响
    print(f"函数内：{n}")

def modify_list(lst):
    lst.append(4)          # 修改的是同一个列表对象，外部会受影响
    print(f"函数内：{lst}")

x = 5
modify_num(x)              # 函数内：15
print(f"函数外：{x}")      # 函数外：5（不变）

data = [1, 2, 3]
modify_list(data)          # 函数内：[1, 2, 3, 4]
print(f"函数外：{data}")   # 函数外：[1, 2, 3, 4]（被改了！）
```

这一行为是理解函数参数的关键。当你的函数"不小心"修改了传入的列表或字典时，bug 往往就来源于忘记了这个原则。

### 6.2.6 实战练习

1. 定义函数 `describe_city(city, country="中国")`，打印 `"XXX 在 YYY"`。分别以默认国家和不默认国家的方式调用两次。

2. 定义函数 `max_of_n(*args)`，接收任意个数字，返回其中的最大值。如果没传参数，返回 `None`。

3. 阅读以下代码，预测输出并解释原因：

```python
def mystery(a, b=[]):
    b.append(a)
    return b

print(mystery(1))
print(mystery(2))
print(mystery(3, []))
print(mystery(4))
```