## 7.1 类与对象

### 练习1：Book 类

**答案：**

```python
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

book1 = Book("三体", "刘慈欣")
book2 = Book("活着", "余华")

print(f"《{book1.title}》作者：{book1.author}")
print(f"《{book2.title}》作者：{book2.author}")
```

**输出：**

```text
《三体》作者：刘慈欣
《活着》作者：余华
```

---

### 练习2：Counter 类

**答案：**

```python
class Counter:
    count = 0          # 类属性——所有实例共享

    def __init__(self):
        Counter.count += 1

c1 = Counter()
c2 = Counter()
c3 = Counter()

print(Counter.count)   # 3
```

**解析：** 每次 `__init__` 被调用时 `Counter.count += 1` 都会执行。因为 `count` 是类属性（挂在 `Counter` 类上），三个对象共享同一个计数器，累积结果为 3。

---

### 练习3：找错并修正

**错误代码：**

```python
class Dog:
    def __init__(name):       # 错误：缺少 self
        self.name = name

d = Dog("旺财")
print(d.name)
```

**错误分析：**
1. **`__init__` 没有 `self` 参数**：`def __init__(name)` 中 `name` 被当作 `self` 接收了实例对象，导致 `"旺财"` 没有被正确接收。调用时会报 `TypeError: __init__() takes 1 positional argument but 2 were given`（因为 Python 自动传 `self`，再加上 `"旺财"` 就变成了两个参数）。
2. **缺少 `self` 导致 `self.name` 赋值的是实例对象本身**：即使不报错，`self.name = name` 也会把实例对象赋给自己的 `name` 属性，完全不符合预期。

**正确代码：**

```python
class Dog:
    def __init__(self, name):    # self 必须是第一个参数
        self.name = name

d = Dog("旺财")
print(d.name)                    # 旺财
```


## 7.2 属性与方法

### 练习1：Rectangle 类

**答案：**

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

rect = Rectangle(4, 5)
print(f"面积：{rect.area()}")          # 面积：20
print(f"周长：{rect.perimeter()}")     # 周长：18
```

---

### 练习2：类属性与类方法

**答案：**

```python
class Rectangle:
    shape_name = "矩形"          # 类属性

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    @classmethod
    def describe(cls):
        print(f"这是一个形状：{cls.shape_name}")

Rectangle.describe()    # 这是一个形状：矩形
```

---

### 练习3：Temperature 类

**答案：**

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius       # 触发 setter 验证

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError(f"温度不能低于绝对零度（-273.15°C），收到 {value}")
        self._celsius = value

    @property
    def fahrenheit(self):
        """华氏度——只读属性，根据摄氏度动态计算"""
        return self._celsius * 9 / 5 + 32

t = Temperature(25)
print(f"摄氏度：{t.celsius}°C")         # 摄氏度：25°C
print(f"华氏度：{t.fahrenheit}°F")      # 华氏度：77.0°F

t.celsius = 100
print(f"摄氏度：{t.celsius}°C")         # 摄氏度：100°C
print(f"华氏度：{t.fahrenheit}°F")      # 华氏度：212.0°F

try:
    t.celsius = -300                   # 触发 ValueError
except ValueError as e:
    print(f"错误：{e}")                # 错误：温度不能低于绝对零度...
```


## 7.3 继承与多态

### 练习1：Vehicle 继承

**答案：**

```python
class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    def run(self):
        print(f"{self.brand} 正在行驶")

class Car(Vehicle):
    def run(self):
        print(f"{self.brand} 汽车正在公路上行驶")

class Bicycle(Vehicle):
    def run(self):
        print(f"{self.brand} 自行车正在小路上行驶")

car = Car("宝马")
bike = Bicycle("捷安特")

car.run()      # 宝马 汽车正在公路上行驶
bike.run()     # 捷安特 自行车正在小路上行驶
```

---

### 练习2：Employee 与 Manager

**答案：**

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def describe(self):
        print(f"姓名：{self.name}，工资：{self.salary}")

class Manager(Employee):
    def __init__(self, name, salary, department):
        super().__init__(name, salary)       # 先调用父类的初始化
        self.department = department

    def describe(self):
        super().describe()                   # 先调用父类的描述
        print(f"部门：{self.department}")    # 再追加子类独有的信息

mgr = Manager("张总", 30000, "技术部")
mgr.describe()
# 姓名：张总，工资：30000
# 部门：技术部
```

---

### 练习3：MRO 输出

**代码：**

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

**输出：**

```text
CB
(<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)
```

**逐层解析：**

1. `D` 的 MRO 顺序是 `D → B → C → A → object`（C3 线性化算法，先深度搜索 `B`，再搜 `C`，最后 `A`）
2. `d.action()` 首先在 `D` 中查找——`D` 没有定义 `action`，向上找 `B`
3. `B.action()` 中调用 `super().action()`——在 MRO 链中，`B` 的 `super()` 是 `C`（不是 `A`！因为 `D(B, C)` 的 MRO 使得 `B` 的下一个是 `C`）
4. `C.action()` 返回 `"C"`，`B.action()` 在后面加上 `"B"`，最终返回 `"CB"`
5. 因为 `C.action()` 没有调用 `super()`（它直接 `return "C"`），所以 `A.action()` 不会被执行——`"A"` 永远不会出现在结果中


## 7.4 特殊方法

### 练习1：Vector2D 类

**答案：**

```python
class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        """向量加法：(x1, y1) + (x2, y2) = (x1+x2, y1+y2)"""
        return Vector2D(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f"Vector2D({self.x}, {self.y})"

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"

    def __eq__(self, other):
        """两个向量的 x 和 y 都相等时视为相等"""
        if not isinstance(other, Vector2D):
            return NotImplemented
        return self.x == other.x and self.y == other.y

v1 = Vector2D(1, 2)
v2 = Vector2D(3, 4)
v3 = Vector2D(4, 6)

print(v1 + v2)          # Vector2D(4, 6)
print(v1 + v2 == v3)    # True
print(v1 == v2)         # False
```

---

### 练习2：Group 类

**答案：**

```python
class Group:
    def __init__(self):
        self.members = []

    def add(self, name):
        self.members.append(name)

    def __len__(self):
        return len(self.members)

    def __contains__(self, name):
        return name in self.members

    def __getitem__(self, index):
        return self.members[index]

    def __repr__(self):
        return f"Group({self.members})"

group = Group()
group.add("小明")
group.add("小红")
group.add("小刚")

print(len(group))            # 3
print("小红" in group)       # True
print("小李" in group)       # False
print(group[0])              # 小明
print(group[1])              # 小红
```

---

### 练习3：修正代码

**错误代码：**

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return self.name + " - " + self.price + "元"     # 错误：price 是数字，不能和字符串拼接

p = Product("键盘", 299)
print(p)
```

**错误分析：** `self.price` 是整数（299），不能用 `+` 直接和字符串拼接。Python 中数字和字符串之间没有隐式类型转换。

**正确代码（两种修正方式）：**

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} - {self.price}元"     # 用 f-string 自动处理类型转换

p = Product("键盘", 299)
print(p)     # 键盘 - 299元
```

或显式转换：

```python
def __str__(self):
    return self.name + " - " + str(self.price) + "元"
```


## 7.5 案例：学生管理系统

### 练习1：添加 `__lt__` 方法

**答案：**

```python
class Student:
    # ... 之前的代码保持不变 ...

    def __lt__(self, other):
        """按平均分比较——支持 sorted() 排序"""
        return self.get_average_score() < other.get_average_score()

# 测试
s1 = Student("小明", 18)
s2 = Student("小红", 17)
s3 = Student("小刚", 19)

s1.add_or_update_score("数学", 90)
s2.add_or_update_score("数学", 95)
s3.add_or_update_score("数学", 75)

students = [s1, s2, s3]
sorted_students = sorted(students)           # 默认升序（低→高）
for s in sorted_students:
    print(f"{s.name}：{s.get_average_score():.1f}")
# 小刚：75.0
# 小明：90.0
# 小红：95.0

sorted_desc = sorted(students, reverse=True)  # 降序（高→低）
for s in sorted_desc:
    print(f"{s.name}：{s.get_average_score():.1f}")
# 小红：95.0
# 小明：90.0
# 小刚：75.0
```

---

### 练习2：添加 `remove_student` 方法

**答案：**

```python
class StudentManager:
    # ... 之前的代码保持不变 ...

    def remove_student(self, name):
        """按姓名删除学生"""
        for i, s in enumerate(self.students):
            if s.name == name:
                removed = self.students.pop(i)
                print(f"学生 {name} 已删除")
                return
        print(f"未找到学生：{name}")

# 测试
manager = StudentManager()
manager.add_student("小明", 18)
manager.add_student("小红", 17)
manager.show_all()
# 共 2 人

manager.remove_student("小明")     # 学生 小明 已删除
manager.remove_student("小李")     # 未找到学生：小李
manager.show_all()                 # 共 1 人
```

---

### 练习3：添加 `statistics` 方法

**答案：**

```python
class StudentManager:
    # ... 之前的代码保持不变 ...

    def statistics(self):
        """统计信息"""
        if not self.students:
            print("暂无学生信息")
            return

        total = len(self.students)

        # 收集所有学生的平均分
        avgs = [(s.name, s.get_average_score()) for s in self.students]

        # 全局平均分
        overall_avg = sum(a[1] for a in avgs) / total

        # 最高和最低平均分
        best = max(avgs, key=lambda x: x[1])
        worst = min(avgs, key=lambda x: x[1])

        print(f"\n{'='*50}")
        print("统计信息")
        print(f"{'='*50}")
        print(f"学生总人数：{total}")
        print(f"全部学生总平均分：{overall_avg:.1f}")
        print(f"最高平均分：{best[0]}（{best[1]:.1f} 分）")
        print(f"最低平均分：{worst[0]}（{worst[1]:.1f} 分）")

# 测试
manager = StudentManager()
manager.add_student("小明", 18)
manager.add_student("小红", 17)
manager.add_student("小刚", 19)
manager.update_score("小明", "数学", 90)
manager.update_score("小红", "数学", 95)
manager.update_score("小刚", "数学", 75)

manager.statistics()
# 学生总人数：3
# 全部学生总平均分：86.7
# 最高平均分：小红（95.0 分）
# 最低平均分：小刚（75.0 分）
```

**解析：**
- 先用列表推导式 `[(s.name, s.get_average_score()) for s in self.students]` 收集所有学生的"姓名-平均分"对
- `max(avgs, key=lambda x: x[1])` 按平均分（元组的第二个元素）找最大值，`min` 同理
- `sum(a[1] for a in avgs) / total` 计算全局平均——这里用了生成器表达式而不是列表推导式，避免创建中间列表