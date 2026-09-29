## 7.1 类与对象——"蓝图"与"房子"

在第 6 章中我们学习了函数——它把一段段逻辑封装成可复用的模块。但函数只封装了"行为"，没有封装"数据"。现实世界中的事物既有属性（数据）也有行为（方法），比如一个学生有姓名和成绩（数据），还能考试和升级（行为）。面向对象编程（Object-Oriented Programming，简称 OOP）正是为了用代码自然地模拟这种"数据 + 行为"的组合。

### 7.1.1 从现实到代码——类的概念

想象你是一个建筑设计师。在动工之前，你先画了一张**蓝图**（Blueprint），上面规定了房子的结构：几室几厅、门朝哪开、窗户多大。但这张蓝图本身不能住人——你需要按照蓝图一砖一瓦地盖出实际的**房子**，而且同一张蓝图可以盖出很多栋房子。

在面向对象编程中：
- **类（Class）**就是蓝图——它定义了某一类事物应该有什么数据和什么行为
- **对象（Object）**就是按照蓝图盖出来的房子——类的具体实例

```python
class Student:
    """学生类——描述一个学生的基本特征和行为"""
    pass

# 根据 Student 蓝图创建两个具体的"房子"（对象）
student1 = Student()
student2 = Student()

print(type(student1))    # <class '__main__.Student'>
print(student1)          # <__main__.Student object at 0x...>
```

这个 `Student` 类暂时是一个空壳——`pass` 关键字表示"什么也不做，先占个位置"。但我们已经可以用它来创建对象了。`student1` 和 `student2` 都是 `Student` 类型的实例，但它们占据不同的内存地址，是相互独立的个体。

### 7.1.2 `__init__()` 方法——对象的"出生仪式"

光有空壳没用——我们需要在创建对象时给它赋予初始数据，比如每个学生出生时就应该有名字和年龄。这通过 `__init__()` 方法实现，它在对象创建时自动被调用：

```python
class Student:
    def __init__(self, name, age):
        """初始化方法——对象创建时自动执行"""
        self.name = name        # 把传入的 name 绑定到当前实例上
        self.age = age          # 把传入的 age 绑定到当前实例上

student1 = Student("小明", 18)
student2 = Student("小红", 20)

print(student1.name, student1.age)    # 小明 18
print(student2.name, student2.age)    # 小红 20
```

逐行解析这段代码：

- `__init__` 前后各有两个下划线，这是 Python 的命名约定——以双下划线包裹的方法是"特殊方法"（也叫魔术方法），由 Python 解释器在特定时机自动调用，你不需要手动调用它
- `self` 是第一个参数，它代表**当前这个实例本身**。当写 `student1 = Student("小明", 18)` 时，Python 会自动把 `student1` 这个新创建的对象传给 `self`，这样 `self.name = name` 就等于 `student1.name = "小明"`
- `name` 和 `age` 是 `__init__` 的普通参数，在创建对象时由调用者提供

---

\begin{definitionbox}
**`self`——面向对象的第一道坎**

初学者最容易困惑的就是 `self`。一个简单的理解方式：

```python
student1 = Student("小明", 18)
student1.name    # 等价于 Student.__init__(student1, "小明", 18) 中 self.name = "小明"
```

`self` 就像"我"这个代词——每个人说"我的名字"时，"我"指的都是说话者自己。在 `student1.name` 中，`self` 就是 `student1`；在 `student2.name` 中，`self` 就是 `student2`。`self` 不是 Python 的关键字，写成 `this` 或 `me` 语法上也行——但整个 Python 社区都用 `self`，请务必遵守这个约定。
\end{definitionbox}

---

### 7.1.3 类属性 vs 实例属性

上面的 `name` 和 `age` 是**实例属性**——每个对象自己独有的数据，互不影响。还有一种属性叫**类属性**——属于类本身，被所有实例共享：

```python
class Student:
    school = "第一中学"       # 类属性——所有学生属于同一所学校

    def __init__(self, name, age):
        self.name = name      # 实例属性——每个学生有自己的名字
        self.age = age        # 实例属性——每个学生有自己的年龄

s1 = Student("小明", 18)
s2 = Student("小红", 20)

print(s1.school)    # 第一中学（通过实例访问类属性）
print(s2.school)    # 第一中学（同上）
print(Student.school)    # 第一中学（通过类名直接访问）

Student.school = "第二中学"    # 修改类属性，所有实例都会看到变化
print(s1.school)    # 第二中学
print(s2.school)    # 第二中学
```

类属性适合存放"这个类所有实例共同拥有的数据"，比如学校的名称、游戏的最高分数上限、数据库的连接配置等。实例属性则存放"每个实例独有的数据"。

### 7.1.4 实战练习

1. 定义一个 `Book` 类，`__init__` 方法接收 `title`（书名）和 `author`（作者）两个参数，将它们绑定为实例属性。创建两本书的对象并分别打印它们的书名和作者。

2. 定义一个 `Counter` 类，包含一个类属性 `count`（初始值为 0）。`__init__` 方法中让 `count` 每次创建新实例时自动加 1。连续创建三个 `Counter` 对象后，打印 `Counter.count`，观察输出。

3. 找出下面代码中的错误（共两处），并写出正确的版本：

```python
class Dog:
    def __init__(name):
        self.name = name

d = Dog("旺财")
print(d.name)
```