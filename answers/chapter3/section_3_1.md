# 第3章 习题答案

## 3.1 注释和代码规范

### 练习1：修正代码规范

**题目：** 找出代码中的 PEP 8 规范问题并修正。

**答案（修正后）：**

```python
score_x = 10
score_y = 20

if score_x < score_y:
    print("x小于y")

result = score_x + score_y * 3 - 4 / 2
print(result)
```

**修正说明（3 处以上问题）：**

| 原代码 | 问题 | 修正 |
|:-------|:-----|:-----|
| `x=10` | `=` 前后缺少空格 | `score_x = 10` |
| `if x<y:` | `<` 前后缺少空格 | `if score_x < score_y:` |
| `  print(...)` | 缩进只有 2 个空格 | 改为 4 个空格 |
| `z=x+y*3-4/2` | 运算符前后缺少空格 | `result = score_x + score_y * 3 - 4 / 2` |
| `x` `y` `z` | 变量名无意义，不符合"见名知意" | 改为有意义的名字 |

> **额外建议：** 在 VS Code 中写完代码后按 `Shift+Alt+F`，Black 插件会自动修正以上所有格式问题。

---

### 练习2：添加注释

**题目：** 为以下代码添加合适的注释（解释"为什么"）。

**答案：**

```python
# 根据单价和数量计算商品总价
total_price = price * quantity

# 全场九折，所以总价乘以 0.9
final_price = total_price * 0.9

# input() 返回字符串，用 int() 转为整数才能参与计算
age = int(input("请输入你的年龄："))
```

**解析：**
- 注释应解释代码的**意图**和**原因**，而不是重复代码本身
- 反面例子：`total_price = price * quantity  # 把price乘以quantity赋值给total_price`——这是废话
- 第三条注释解释了为什么要用 `int()`，这是初学者容易忽略的知识点

---

### 练习3：变量命名改正

**题目：** 将变量名改为蛇形命名法。

**答案：**

| 原命名 | 问题 | 改正 |
|:-------|:-----|:-----|
| `UserName` | 不符合 Python 习惯（帕斯卡命名用于类名） | `user_name` |
| `studentage` | 单词连在一起，难以阅读 | `student_age` |
| `order date` | 包含空格，Python 不允许 | `order_date` |
| `2nd_place` | 以数字开头，Python 不允许 | `second_place` |

**解析：**
- Python 变量命名的四大规则：字母/数字/下划线、不能数字开头、不能用关键字、见名知意
- 蛇形命名法：小写字母 + 下划线分隔，如 `user_name`、`total_score`
- 当遇到"不能以数字开头"的情况时，用英文单词替代：`2nd` → `second`、`1st` → `first`