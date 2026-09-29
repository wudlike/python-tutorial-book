## 7.3 继承与多态——"子承父业"与"随机应变"

如果每写一个新类都要从零开始定义所有属性和方法，那代码复用就无从谈起。继承（Inheritance）正是 OOP 中解决这一问题的核心机制——子类自动获得父类的所有属性和方法，只需在此基础上添加或修改自己的特色。而多态（Polymorphism）则让不同的子类可以对同一个方法名做出不同的响应，实现了"同一个接口，多种实现"。

### 7.3.1 继承的基本语法

继承的语法非常简单——在类名后的括号中写上父类的名字：

```python
class Animal:
    """父类——动物基类"""
    def __init__(self, name):
        self.name = name

    def speak(self):
        """所有动物都会发声，但具体怎么发由于类决定"""
        print(f"{self.name} 发出了声音")

class Dog(Animal):
    """子类——狗，继承 Animal"""
    def speak(self):
        """狗的叫声——覆盖父类的 speak 方法"""
        print(f"{self.name}：汪汪！")

class Cat(Animal):
    """子类——猫，继承 Animal"""
    def speak(self):
        """猫的叫声——覆盖父类的 speak 方法"""
        print(f"{self.name}：喵喵！")

dog = Dog("旺财")
cat = Cat("咪咪")

dog.speak()    # 旺财：汪汪！
cat.speak()    # 咪咪：喵喵！
```

在这个例子中，`Dog` 和 `Cat` 都继承了 `Animal` 的 `__init__` 方法（所以创建对象时需要传 `name`），但各自**重写（Override）**了 `speak` 方法——调用同名方法时，子类的版本会覆盖父类的版本。这就是多态的基础：同样的方法名 `speak`，不同的子类执行不同的逻辑。

---

\begin{definitionbox}
**方法解析顺序（MRO）——Python 如何找到正确的方法**

当调用 `dog.speak()` 时，Python 的查找顺序是：
1. 先在 `Dog` 类自身找 `speak` 方法 → 找到了，执行
2. 如果 `Dog` 没定义 `speak`，就往上找父类 `Animal` → 找到了，执行
3. 如果 `Animal` 也没定义，继续往上找 `object`（所有类的终极父类）

这个从子类到父类的搜索链条叫作**方法解析顺序（Method Resolution Order）**。可以通过 `Dog.__mro__` 或 `Dog.mro()` 查看：
```python
print(Dog.__mro__)
# (<class '__main__.Dog'>, <class '__main__.Animal'>, <class 'object'>)
```
\end{definitionbox}

---

### 7.3.2 `super()`——在子类中调用父类的方法

有时子类并不想完全替换父类的方法，而是想在父类方法的基础上**追加**一些操作。比如动物初始化时需要名字，而狗还需要品种信息。这时用 `super()` 调用父类的同名方法：

```python
class Animal:
    def __init__(self, name):
        self.name = name
        print(f"Animal.__init__ 被调用：{name}")

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)        # 先让父类完成 name 的初始化
        self.breed = breed            # 再处理子类独有的 breed
        print(f"Dog.__init__ 被调用：{name}, {breed}")

    def info(self):
        print(f"{self.name} 是一只 {self.breed}")

dog = Dog("旺财", "金毛")
# Animal.__init__ 被调用：旺财
# Dog.__init__ 被调用：旺财, 金毛
dog.info()    # 旺财 是一只 金毛
```

`super().__init__(name)` 的作用是沿着 MRO 链往上找父类的 `__init__` 方法并调用它，传入 `name` 参数。这种模式在多层继承中尤为重要——它确保每一层父类的初始化逻辑都被执行，不会因为子类的 `__init__` 覆盖而跳过。

### 7.3.3 多态——同一个接口，不同的行为

多态的核心思想是：**你不需要知道对象具体是哪个子类，只需要知道它支持某个方法**。下面的例子展示了多态的威力：

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        pass       # 父类不实现具体逻辑，交给子类

class Dog(Animal):
    def speak(self):
        return f"{self.name}：汪汪！"

class Cat(Animal):
    def speak(self):
        return f"{self.name}：喵喵！"

class Duck(Animal):
    def speak(self):
        return f"{self.name}：嘎嘎！"

def make_animals_speak(animals):
    """让一群动物依次发声——不关心每个动物具体是哪种"""
    for animal in animals:
        print(animal.speak())

zoo = [Dog("旺财"), Cat("咪咪"), Duck("唐老鸭")]
make_animals_speak(zoo)
# 旺财：汪汪！
# 咪咪：喵喵！
# 唐老鸭：嘎嘎！
```

关键点在于 `make_animals_speak` 函数——它只关心列表里的每个元素有 `speak()` 方法，完全不在乎元素是 `Dog`、`Cat` 还是 `Duck`。这种"面向接口编程"的思想让代码的扩展性极强：以后新增一个 `Pig` 类，只要它也有 `speak()` 方法，就可以直接扔进 `zoo` 列表，`make_animals_speak` 一行都不用改。

### 7.3.4 多重继承——一个子类可以有多个父类

Python 支持一个类同时继承多个父类。这在某些场景下很有用（比如一个 `Bat` 同时是"哺乳动物"和"会飞的动物"），但也引入了"钻石继承"等复杂性，需要谨慎使用：

```python
class Flyer:
    def fly(self):
        print("飞起来了！")

class Swimmer:
    def swim(self):
        print("游起来了！")

class Duck(Flyer, Swimmer):
    def speak(self):
        print("嘎嘎！")

d = Duck()
d.fly()      # 飞起来了！（继承自 Flyer）
d.swim()     # 游起来了！（继承自 Swimmer）
d.speak()    # 嘎嘎！
```

多重继承的方法解析顺序遵循 C3 线性化算法——简单说，先深度搜索再从左到右。在绝大多数日常编程中，单继承已经足够；多重继承的建议是"能不用就不用，用了就保持简单"。

### 7.3.5 实战练习

1. 定义父类 `Vehicle`，包含 `brand` 属性和 `run()` 方法（打印 `"XX 正在行驶"`）。定义子类 `Car` 和 `Bicycle`，分别重写 `run()` 方法为 `"XX 汽车正在公路上行驶"` 和 `"XX 自行车正在小路上行驶"`。创建两个子类对象并调用 `run()`。

2. 定义父类 `Employee`，包含 `name` 和 `salary` 属性（通过 `__init__` 设置），以及 `describe()` 方法（打印姓名和工资）。定义子类 `Manager`，额外接收 `department` 参数，重写 `describe()` 方法，在父类 `describe()` 输出的基础上追加 `"部门：XX"`。要求使用 `super()` 调用父类的方法。

3. 阅读以下代码，写出输出结果：

```python
class A:
    def action(self):
        return "A"

class B(A):
    def action(self):
        return super().action() + "B"

class C(A):
    def action(self):
        return "C"

class D(B, C):
    pass

d = D()
print(d.action())
print(D.__mro__)
```