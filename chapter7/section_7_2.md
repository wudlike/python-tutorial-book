## 7.2 属性与方法——对象的"数据"与"行为"

上一节我们学会了定义类并给对象赋予初始属性。但一个完整的类不仅要有数据（属性），还要有行为（方法）。就像一个人不能只有姓名和年龄——他还需要会走路、会说话、会工作。本节将系统地讲解类中的三种方法，以及属性的访问控制。

### 7.2.1 实例方法——对象的行为

实例方法是类中最常见的方法类型。它的第一个参数必须是 `self`，通过 `self` 可以访问当前实例的属性和其他方法：

```python
class Student:
    school = "第一中学"

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def introduce(self):
        """自我介绍"""
        print(f"我叫{self.name}，来自{self.school}，成绩是{self.score}分")

    def improve(self, points):
        """成绩提升"""
        self.score += points
        print(f"{self.name}的成绩提升到{self.score}分！")

s = Student("小明", 85)
s.introduce()          # 我叫小明，来自第一中学，成绩是85分
s.improve(10)          # 小明的成绩提升到95分！
s.introduce()          # 我叫小明，来自第一中学，成绩是95分
```

注意 `improve` 方法修改了 `self.score`——因为 `self` 指向的就是 `s` 这个实例，所以 `self.score += points` 相当于 `s.score += points`。这是实例方法的典型用法：读取和修改当前实例的状态。

---

\begin{tipbox}
**方法调用时 `self` 是自动传递的**

`student.introduce()` 看起来没有传参数，但方法定义里写了 `self`。这是因为 Python 在调用实例方法时会自动把点号前面的对象（`student`）作为第一个参数传入。你只需要写方法名和括号，`self` 由解释器在幕后处理。
\end{tipbox}

---

### 7.2.2 类方法与静态方法

除了实例方法，还有两种依附于类本身的方法：类方法和静态方法。它们通过**装饰器**来声明，作用各有侧重。

```python
class Student:
    total_count = 0             # 类属性——统计学生总数

    def __init__(self, name):
        self.name = name
        Student.total_count += 1

    @classmethod
    def get_total(cls):         # cls 代表类本身（就像 self 代表实例本身）
        """类方法——访问或修改类状态"""
        return f"当前共有 {cls.total_count} 名学生"

    @staticmethod
    def is_valid_name(name):    # 没有 self 也没有 cls
        """静态方法——与类和实例都无关的工具函数"""
        return len(name) >= 2 and len(name) <= 10

s1 = Student("小明")
s2 = Student("小红")

print(Student.get_total())           # 当前共有 2 名学生
print(Student.is_valid_name("王"))   # False——名字太短了
print(Student.is_valid_name("张三"))  # True
```

三种方法的对比：

| 类型 | 装饰器 | 第一个参数 | 能访问实例属性？ | 能访问类属性？ | 典型用途 |
|:-----|:------|:----------|:-------------:|:-----------:|:-----|
| 实例方法 | 无 | `self`（实例） | ✅ | ✅ | 处理单个对象的数据和行为 |
| 类方法 | `@classmethod` | `cls`（类） | ❌ | ✅ | 工厂方法、操作类级别的数据 |
| 静态方法 | `@staticmethod` | 无 | ❌ | ❌ | 与类逻辑相关的工具函数 |

选择方法类型的简单判断：需要操作实例数据 → 实例方法；需要操作类数据 → 类方法；只是逻辑上属于这个类但不需要访问任何数据 → 静态方法。

### 7.2.3 私有属性——"请勿打扰"

Python 没有像 Java 或 C++ 那样真正的 `private` 关键字。但有一个约定：**以单下划线 `_` 开头的属性和方法被视为"内部使用，请勿直接访问"；以双下划线 `__` 开头的会触发名称改写（name mangling），从语法层面增加访问难度**。

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner              # 公开属性
        self._bank = "建设银行"           # 约定保护——"建议别碰"
        self.__balance = balance        # 名称改写——"强行碰会麻烦"

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"入账 {amount} 元，余额 {self.__balance} 元")

    def get_balance(self):
        return self.__balance

account = BankAccount("小明", 1000)
account.deposit(500)                    # 入账 500 元，余额 1500 元
print(account.get_balance())            # 1500

# print(account.__balance)              # AttributeError!
# 双下划线被 Python 改写成了 _BankAccount__balance
print(account._BankAccount__balance)    # 1500——但还是别这么干
```

名称改写的本质：`__balance` 在类内部被自动重命名为 `_BankAccount__balance`（在属性名前加上一个下划线和类名）。这并非安全机制——它只是防止子类意外覆盖父类的私有属性，以及在类外部通过普通方式误访问。Python 的设计哲学是"大家都是成年人了"（We are all consenting adults here）——约定优于强制，信任程序员的自律。

### 7.2.4 `@property`——像访问属性一样调用方法

有时你希望外部能用 `obj.attr` 的方式获取一个值，但这个值需要经过计算或验证。`@property` 装饰器让方法"伪装"成属性：

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        """获取半径"""
        return self._radius

    @radius.setter
    def radius(self, value):
        """设置半径——自动检查合法性"""
        if value <= 0:
            raise ValueError("半径必须大于 0")
        self._radius = value

    @property
    def area(self):
        """面积——只读属性，根据半径动态计算"""
        return 3.14159 * self._radius ** 2

c = Circle(5)
print(c.radius)     # 5——不用写 c.radius()
print(c.area)       # 78.53975——不用写 c.area()

c.radius = 10       # 赋值时自动调用 setter 中的校验逻辑
print(c.area)       # 314.159

# c.area = 100     # AttributeError——没有定义 setter，area 是只读的
```

`@property` 的优雅之处在于：调用方的代码不需要知道 `radius` 背后是一个普通属性还是经过层层计算的方法——接口统一、调用自然。当你以后需要在获取属性时加入数据库查询、缓存刷新、日志记录等逻辑时，只需要修改 `@property` 方法，所有调用方代码一行不改。

### 7.2.5 实战练习

1. 定义一个 `Rectangle` 类，`__init__` 接收 `width` 和 `height`，定义实例方法 `area()` 返回面积，实例方法 `perimeter()` 返回周长。创建一个 `Rectangle(4, 5)` 对象并测试这两个方法。

2. 为 `Rectangle` 类添加类属性 `shape_name = "矩形"` 和一个类方法 `describe()`，该方法输出 `"这是一个形状：矩形"`。调用该方法并确认输出。

3. 定义一个 `Temperature` 类，使用 `@property` 管理摄氏温度 `celsius` 的读写，并提供一个只读属性 `fahrenheit`（华氏度 = 摄氏度 × 9/5 + 32）。要求 setter 在设置温度时拒绝低于 -273.15（绝对零度）的值。