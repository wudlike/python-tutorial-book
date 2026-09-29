## 4.1 条件语句

### 练习1：闰年判断

**题目：** 输入年份，判断是否为闰年。

**答案：**

```python
year = int(input("请输入年份："))

if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
    print(f"{year} 年是闰年")
else:
    print(f"{year} 年不是闰年")
```

**解析：**
- 能被 4 整除但不能被 100 整除：`year % 4 == 0 and year % 100 != 0`
- 能被 400 整除：`year % 400 == 0`
- 两个条件用 `or` 连接，满足其一即为闰年
- 判断顺序：先算 `%`，再算 `==` 和 `!=`，再算 `and`，最后算 `or`。加上括号后意图更清晰

---

### 练习2：BMI 计算器

**题目：** 输入身高和体重，输出 BMI 和体型评价。

**答案：**

```python
height = float(input("请输入身高（米）："))
weight = float(input("请输入体重（千克）："))

bmi = weight / (height ** 2)

if bmi < 18.5:
    level = "偏瘦"
elif bmi < 24:
    level = "正常"
elif bmi < 28:
    level = "偏胖"
else:
    level = "肥胖"

print(f"BMI = {bmi:.1f}，体型评价：{level}")
```

**解析：**
- `if-elif-else` 的多分支结构非常适合这种"按区间划分等级"的场景
- 条件顺序从上到下，越严格的条件越靠前。当 `bmi = 22` 时，先判断 `< 18.5`（False），再判断 `< 24`（True），输出"正常"
- `{bmi:.1f}` 保留 1 位小数

---

### 练习3：外卖满减

**题目：** 根据订单金额应用最大优惠。

**答案：**

```python
amount = float(input("请输入订单金额："))

if amount >= 100:
    pay = amount - 20
    discount = 20
elif amount >= 50:
    pay = amount - 8
    discount = 8
elif amount >= 30:
    pay = amount - 3
    discount = 3
else:
    pay = amount
    discount = 0

print(f"原价：{amount} 元，优惠：{discount} 元，实付：{pay:.2f} 元")
```

**关键点：为什么不需要担心"120 元该减 20 还是减 8"？**

因为条件从大到小排列（`>= 100` → `>= 50` → `>= 30`），120 元首先命中 `>= 100`，执行减 20 后就不再往下判断。这正是 `elif` 的执行机制——**只匹配第一个为 True 的分支**。


## 4.2 循环语句

### 练习1：偶数和与奇数和

**题目：** 计算 1-100 之间偶数和与奇数和。

**答案：**

```python
even_sum = 0
odd_sum = 0

for i in range(1, 101):
    if i % 2 == 0:
        even_sum += i
    else:
        odd_sum += i

print(f"偶数和：{even_sum}")    # 2550
print(f"奇数和：{odd_sum}")    # 2500
```

**解析：**
- `i % 2 == 0` 判断偶数（能被 2 整除）
- 在循环内部分类累加，每种情况各维护一个累加器
- 验证：偶数和 + 奇数和 = `5050`（1 到 100 的和）

---

### 练习2：输入求和

**题目：** 不断输入数字，输入 0 停止，输出总和与平均值。

**答案：**

```python
total = 0
count = 0

while True:
    num = int(input("请输入数字（0 结束）："))
    if num == 0:
        break
    total += num
    count += 1

if count > 0:
    avg = total / count
    print(f"总和：{total}，平均值：{avg:.2f}")
else:
    print("没有输入任何有效的数字。")
```

**解析：**
- `while True` + `break` 模式：先执行循环体，在循环中间判断退出条件
- `count` 用于记录有效输入的次数，平均数 = 总和 / 次数
- 额外处理了"一个有效数字都没输入"的边界情况

---

### 练习3：数字图形

**题目：** 根据用户输入的行数输出数字图形。

**答案：**

```python
n = int(input("请输入行数："))

for i in range(1, n + 1):
    for j in range(1, i + 1):
        print(i, end="")
    print()  # 每行结束后换行
```

**输出示例（n=5）：**

```text
1
22
333
4444
55555
```

**解析：**
- 外层循环控制行数（`i` 从 1 到 n）
- 内层循环控制每行打印几个数字（第 i 行打印 i 次）
- `print(i, end="")` 不换行打印数字，`print()` 打印空换行


## 4.3 循环控制

### 练习1：判断素数

**题目：** 使用 `for` + `else` 判断素数。

**答案：**

```python
n = int(input("请输入一个正整数："))

if n < 2:
    print(f"{n} 不是素数")
else:
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            print(f"{n} = {i} × {n//i}，不是素数")
            break
    else:
        print(f"{n} 是素数")
```

**解析：**
- 1 和小于 1 的数不是素数，单独处理
- 只需检查 2 到 √n 的因数（因为因数成对出现，√n 是分界点）
- `for-else` 结构：`break` 发生时跳过 `else`，无 `break` 则执行 `else`，恰好对应"找到了因数 → 不是素数"和"没找到因数 → 是素数"

---

### 练习2：抽奖转盘

**题目：** 遍历奖项列表，遇到"三等奖"停止，跳过"谢谢参与"。

**答案：**

```python
prizes = ["谢谢参与", "五等奖", "四等奖", "三等奖", "二等奖", "一等奖", "特等奖"]

for prize in prizes:
    if prize == "谢谢参与":
        continue          # 跳过不打印
    if prize == "三等奖":
        print(f"🎉 {prize}！恭喜获得三等奖以上的奖品！")
        break             # 停止抽奖
    print(f"当前奖项：{prize}")

# 输出：
# 当前奖项：五等奖
# 当前奖项：四等奖
# 🎉 三等奖！恭喜获得三等奖以上的奖品！
```

**解析：**
- `continue` 和 `break` 在同一循环中配合使用：前者过滤无效项，后者提前终止
- `continue` 的判断放在前面：先决定要不要跳过，再决定要不要终止
- 注意：`break` 所在的 `if` 独立于 `continue` 的 `if`，两者互不包含

---

### 练习3：按任意键继续

**题目：** 模拟交互循环，q 退出，空输入跳过，其他打印。

**答案：**

```python
while True:
    user_input = input("请输入内容（q 退出）：")

    if user_input == "q":
        print("程序结束。")
        break               # 退出循环

    if user_input == "":
        continue            # 空输入，跳过打印

    print(f"你输入了：{user_input}")
```

**解析：**
- 三个分支各有独立的作用：退出、跳过、处理
- `if user_input == ""` 中的 `continue` 会使循环跳回 `input()`，不会执行下面的 `print`
- 这种模式适合交互式命令行程序的输入校验


## 4.4 综合案例——修仙渡劫模拟器

以下是 4.4.4 节三道扩展挑战的参考答案。每道题的修改位置均以注释标注，改动前后对比即可看到差异。

### 挑战1：增加"顿悟"机制

**需求：** 修炼时 10% 概率触发顿悟，额外获得 20 点灵气。

**修改位置：** `elif choice == "1"` 分支内，在 `qi += gain` 之后追加：

```python
elif choice == "1":
    gain = random.randint(10, 30)
    qi += gain
    print(f"🧘 你闭关修炼，获得 {gain} 点灵气！")

    # ===== 新增：顿悟机制 =====
    if random.random() < 0.1:          # 10% 概率
        bonus = 20
        qi += bonus
        print(f"💡 灵感爆发！你顿悟了，额外获得 {bonus} 点灵气！")
```

**解析：**
- `random.random()` 返回 0 到 1 之间的随机浮点数，`< 0.1` 即 10% 触发概率
- 将概率判断放在常规修炼逻辑之后，自然形成"先修炼，再检查是否顿悟"的流程
- `bonus` 单独声明，便于以后调整数值

---

### 挑战2：调整难度——增加"心魔"机制

**需求：** 渡劫时 20% 概率触发心魔，本次天雷伤害翻倍。

**修改位置：** 渡劫 `for` 循环内，在天雷伤害计算之前追加心魔判断：

```python
for strike in range(1, lightning_count[realm_index] + 1):
    # ===== 新增：心魔机制 =====
    inner_demon = random.random() < 0.2  # 20% 概率触发心魔
    if inner_demon:
        print("  👹 心魔来袭！本次天雷伤害翻倍！")

    hit = random.random() < 0.4
    if hit:
        damage = random.randint(5, 15)
        if inner_demon:
            damage *= 2              # 心魔状态下伤害翻倍
        qi -= damage
        print(f"  第 {strike} 道天雷劈中！灵气 -{damage}（剩余 {qi}）")
    else:
        print(f"  第 {strike} 道天雷落空！你躲过一劫（灵气 {qi}）")

    if qi <= 0:
        print("💀 灵气耗尽，渡劫失败！")
        break
```

**完整修改逻辑：**
1. 在天雷击中判断之前，先用 `random.random() < 0.2` 判断是否触发心魔
2. 触发心魔时用 `inner_demon`（布尔值）标记状态
3. 计算伤害时：`if inner_demon: damage *= 2`
4. 心魔只在"被天雷劈中"时生效——如果天雷落空，心魔不造成影响（符合设定）

**额外调整——失败后灵气折损比例：** 将原文的 `qi = tribulation_qi // 2` 改为 `qi = tribulation_qi * 2 // 3`（折损 1/3 而非 1/2），降低惩罚力度：

```python
else:
    fail_streak += 1
    qi = tribulation_qi * 2 // 3   # 改为仅折损 1/3
    print(f"\n😞 渡劫失败……灵气折损，继续修炼吧。")
```

---

### 挑战3：记录修仙履历

**需求：** 用列表记录每次渡劫结果，游戏结束时打印历史。

**修改步骤：**

**第一步（初始化区新增）：**

```python
# ===== 新增：修仙履历列表 =====
history = []
```

**第二步（渡劫成功/失败处新增）：**

```python
# 渡劫成功时
if qi > 0:
    realm_index += 1
    fail_streak = 0
    # ===== 新增：记录成功的渡劫 =====
    history.append(f"✅ 突破至【{realms[realm_index]}】——剩余灵气 {qi}")
    print(f"\n🎉 渡劫成功！你已突破至【{realms[realm_index]}】！")
else:
    fail_streak += 1
    qi = tribulation_qi // 2
    # ===== 新增：记录失败的渡劫 =====
    history.append(f"❌ 渡劫失败——灵气折半至 {qi}")
    print(f"\n😞 渡劫失败……灵气折半，继续修炼吧。")
```

**第三步（游戏结束处新增）：**

在游戏结束的任意出口之前加入：

```python
# 打印修仙履历
print("\n" + "=" * 40)
print("📜 修仙履历")
print("-" * 40)
for i, record in enumerate(history, 1):
    print(f"  {i}. {record}")
print("=" * 40)
```

**输出示例：**

```text
📜 修仙履历
----------------------------------------
  1. ✅ 突破至【筑基】——剩余灵气 12
  2. ❌ 渡劫失败——灵气折半至 45
  3. ✅ 突破至【筑基】——剩余灵气 8
  4. ✅ 突破至【金丹】——剩余灵气 3
  5. ❌ 渡劫失败——灵气折半至 58
========================================
```

**解析：**
- `history = []` 创建一个空列表，在初始化时声明
- `history.append(...)` 在每次渡劫结束时追加一条记录
- `enumerate(history, 1)` 同时获取索引（从 1 开始）和记录内容，用于输出编号
- 列表的灵活性使得记录内容可以是任意格式的字符串