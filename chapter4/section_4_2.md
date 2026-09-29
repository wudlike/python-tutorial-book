## 4.2 循环语句——让程序不知疲倦地重复

计算机相对于人最大的优势之一，就是能不知疲倦地执行重复性工作。循环语句正是释放这一能力的工具——用几行代码驱动成千上万次运算。

Python 提供两种循环：`for`（遍历循环）和 `while`（条件循环），各有适用场景。

### 4.2.1 `for` 循环：逐个取出，依次处理

`for` 循环适合"已知要处理多少个元素"的场景——从一个序列中逐个取出元素，对每个元素执行相同的操作。

```python
fruits = ["苹果", "香蕉", "橘子"]
for fruit in fruits:
    print(f"我喜欢吃{fruit}")

# 输出：
# 我喜欢吃苹果
# 我喜欢吃香蕉
# 我喜欢吃橘子
```

---

\begin{tipbox}
**理解 `for fruit in fruits`**

这里的 `fruit` 是一个**临时变量**，每次循环时它被赋值为列表中的当前元素。你可以给它起任何名字，但建议用有意义的名字（如 `for student in students`、`for score in scores`）。
\end{tipbox}

---

#### `range()`：生成数字序列

`for` 循环最常见的搭档是 `range()`，它生成一个整数序列：

```python
range(stop)              # 从 0 到 stop-1
range(start, stop)       # 从 start 到 stop-1
range(start, stop, step) # 从 start 到 stop-1，步长为 step
```

```python
for i in range(5):
    print(i, end=" ")
# 输出：0 1 2 3 4

for i in range(2, 7):
    print(i, end=" ")
# 输出：2 3 4 5 6

for i in range(1, 10, 2):
    print(i, end=" ")
# 输出：1 3 5 7 9
```

**`for` + `range()` 的经典应用：**

```python
# 计算 1 到 100 的和
total = 0
for i in range(1, 101):
    total += i
print(total)  # 5050

# 输出九九乘法表
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}×{i}={i*j:2}", end="  ")
    print()  # 换行
```

---

\begin{definitionbox}
**嵌套循环**

一个循环内再写一个循环称为**嵌套循环**。外层循环每执行一次，内层循环要完整执行一轮。上面的九九乘法表中，`i=1` 时内层执行 1 次，`i=2` 时内层执行 2 次……共执行 `1+2+...+9=45` 次 `print`。
\end{definitionbox}

---

### 4.2.2 `while` 循环：满足条件就一直跑

`while` 循环适合"不知道要循环多少次，只知道循环停止条件"的场景——只要条件为 True，就继续循环。

```python
# 让用户输入密码，直到输入正确
password = ""
while password != "123456":
    password = input("请输入密码：")
print("密码正确，登录成功！")
```

**`while` 与 `for` 的区别：**

| 对比维度 | `for` | `while` |
|:--------:|:------|:--------|
| 适用场景 | 已知循环次数 | 未知循环次数，依赖条件 |
| 典型搭档 | `range()`、列表、字符串 | 布尔条件表达式 |
| 循环次数 | 自动确定 | 由条件控制，需手动更新 |
| 使用频率 | 更高（日常占 70%） | 较少但不可替代 |

**`while` 的另一经典用法——计数器模式：**

```python
count = 0
while count < 5:
    print(f"第 {count + 1} 次循环")
    count += 1
# 输出：
# 第 1 次循环
# 第 2 次循环
# 第 3 次循环
# 第 4 次循环
# 第 5 次循环
```

---

\begin{warningbox}
**小心"死循环"！**

如果 `while` 的条件永远为 True，程序将永远跑下去（只能按 `Ctrl+C` 强制终止）：

```python
# 死循环——条件永远为 True
while True:
    print("停不下来了……")
```

写 `while` 循环时务必确保：**循环体内有能让条件最终变为 False 的语句**（如 `count += 1`）。
\end{warningbox}

---

### 4.2.3 `for` 循环遍历字典

`for` 不仅限于列表和字符串，对字典也有专项支持：

```python
student = {"name": "小明", "age": 20, "score": 88}

for key in student:
    print(f"{key} → {student[key]}")
# name → 小明
# age → 20
# score → 88

for key, value in student.items():
    print(f"{key}: {value}")
# 效果同上，写法更优雅
```

### 4.2.4 实战练习

1. 使用 `for` 循环计算 1 到 100 之间所有偶数的和，以及所有奇数的和，分别输出。

2. 用户不断输入数字，输入 `0` 时停止。程序输出所有输入数字的总和与平均值（保留两位小数）。要求使用 `while` 循环实现。

3. 使用嵌套循环输出以下图形（行数由用户输入，示例为输入 5）：

   ```text
   1
   22
   333
   4444
   55555
   ```