## 4.3 循环控制——驾驭循环的"方向盘"

循环默认会从第一个元素跑到最后一个元素，但有些场景需要中途干预——提前结束、跳过本轮、或保持某个状态。Python 提供了三个关键字来精确控制循环的行为：`break`、`continue` 和 `pass`。

### 4.3.1 `break`：立即终止循环

`break` 的作用是**跳出当前所在的循环**，即使循环条件仍为 True 或还有未处理的元素，也不再继续。

```python
for i in range(1, 11):
    if i == 5:
        break
    print(i, end=" ")
# 输出：1 2 3 4
# i=5 时触发 break，循环终止，5 到 10 都不会执行
```

**`break` 在 `while` 中的典型用法：**

```python
while True:           # 故意设为死循环
    answer = input("退出请输入 q：")
    if answer == "q":
        break         # 用户输入 q 时跳出
    print(f"你输入了：{answer}")
```

---

\begin{tipbox}
**`break` vs 直接设条件**

上面 `while True` + `break` 的模式看起来很危险，但在需要"先执行一次再判断"的场景中非常实用——它把判断逻辑放在了循环体中间，而不是循环头上，使代码更自然。
\end{tipbox}

---

### 4.3.2 `continue`：跳过本轮，进入下一轮

`continue` 的作用是**跳过当前循环的剩余代码，直接进入下一轮循环**——它不终止循环，只跳过本轮。

```python
for i in range(1, 8):
    if i % 2 == 0:     # 偶数时跳过
        continue
    print(i, end=" ")
# 输出：1 3 5 7
# i 为偶数时，continue 跳过了 print，直接进入下一轮
```

**实用场景——过滤无效数据：**

```python
scores = [88, -1, 95, 62, -1, 77, 90]

total = 0
count = 0
for s in scores:
    if s == -1:       # -1 表示缺考，跳过不计算
        continue
    total += s
    count += 1

print(f"有效成绩合计：{total}，平均分：{total/count:.1f}")
# 输出：有效成绩合计：412，平均分：82.4
```

**`break` 与 `continue` 的区别：**

| 关键字 | 效果 | 比喻 |
|:------:|:-----|:-----|
| `break` | 终止整个循环，不再执行 | **电影散场**——直接走人 |
| `continue` | 跳过本轮，继续下一轮 | **插播广告**——跳过当前节目，下一个接着看 |

### 4.3.3 `pass`：占位符

`pass` 是一个什么都不做的语句，纯粹用于**语法占位**。当你还没想好某个代码块写什么，又需要程序先能运行时，用 `pass` 填充。

```python
if score >= 60:
    pass  # 及格的处理逻辑还没想好，先占位
else:
    print("不及格，需要补考")

# 在函数、类定义中同样适用
def future_function():
    pass
```

---

\begin{warningbox}
**`pass` vs `continue`：不要混淆**

- `pass` 是"什么都不做"，对循环流程零影响
- `continue` 是"跳过本轮"，会中断当前循环的后续代码

```python
for i in range(3):
    if i == 1:
        pass         # 什么都不做，print 仍会执行
    print(i)
# 输出：0 1 2

for i in range(3):
    if i == 1:
        continue     # 跳过 print
    print(i)
# 输出：0 2
```
\end{warningbox}

---

### 4.3.4 `else` 在循环中的特殊用法

Python 的 `for` 和 `while` 循环支持一个不太常见的 `else` 子句——它在**循环正常结束**（即没有被 `break` 中断）时执行。

```python
for i in range(5):
    print(i)
else:
    print("循环正常结束")

# 输出：
# 0 1 2 3 4
# 循环正常结束
```

**经典应用——判断素数：**

```python
n = 29
for i in range(2, int(n ** 0.5) + 1):
    if n % i == 0:
        print(f"{n} 不是素数")
        break
else:
    print(f"{n} 是素数")

# 输出：29 是素数
```

`else` 在 `for` 被 `break` 时不执行，所以只有循环完整跑完（没有找到因数）才会进入 `else`，正好符合"是素数"的逻辑。

---

\begin{notebox}
**这个 `else` 取什么名字更好？**

很多 Python 教程都承认，`for-else` 中的 `else` 命名不太直观。如果你觉得别扭，可以把它理解为 `for-nobreak`——即"没有 break 就执行"。随着使用经验的积累，它会逐渐变得自然。
\end{notebox}

---

### 4.3.5 实战练习

1. 用户输入一个正整数，判断它是否为素数（只能被 1 和自身整除的数）。要求使用 `for` 循环 + `else` 子句实现。

2. 模拟"抽奖转盘"：程序从一个列表 `["谢谢参与", "五等奖", "四等奖", "三等奖", "二等奖", "一等奖", "特等奖"]` 中依次输出奖项，但遇到"三等奖"时提前结束（使用 `break`），说明"恭喜获得三等奖以上的奖品！"；遇到"谢谢参与"时跳过不打印（使用 `continue`）。

3. 编写一个"按任意键继续"的模拟程序：`while` 循环中不断提示用户输入，如果用户输入 `"q"` 则退出循环（`break`），如果输入的是空字符串则跳过（`continue`），否则打印用户输入的内容。