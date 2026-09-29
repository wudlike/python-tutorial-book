## 5.1 列表

### 练习1：成绩统计

**题目：** 创建成绩列表，完成最高/最低分、平均分、排序等操作。

**答案：**

```python
scores = [92, 78, 85, 96, 71]

# 最高分和最低分
print(f"最高分：{max(scores)}，最低分：{min(scores)}")

# 平均分
average = sum(scores) / len(scores)
print(f"平均分：{average:.1f}")

# 从高到低排序
scores.sort(reverse=True)
print(f"排序后：{scores}")

# 新增一门成绩
scores.append(86)
scores.sort(reverse=True)
print(f"新增后排序：{scores}")
```

**输出示例：**

```text
最高分：96，最低分：71
平均分：84.4
排序后：[96, 92, 85, 78, 71]
新增后排序：[96, 92, 86, 85, 78, 71]
```

**解析：**
- `max()` 和 `min()` 是 Python 内置函数，直接返回列表的最大/最小元素
- `sum()` 计算总和，除以 `len()` 得到平均数
- `sort(reverse=True)` 原地降序排列；列表持久化使用 `sort()` 配合 `append()` 维持排序状态

---

### 练习2：列表去重（不用 set）

**题目：** 通过循环和辅助列表手动去重，保持原顺序。

**答案：**

```python
data = [5, 3, 7, 3, 5, 8, 1, 7]
result = []

for num in data:
    if num not in result:      # 只在"没见过"时才加入
        result.append(num)

print(result)  # [5, 3, 7, 8, 1]
```

**解析：**
- 核心思路：维护一个"已见过"的结果列表，遍历原列表时只追加新元素
- `if num not in result` 判断元素是否已在结果中——这是去重的关键判断
- 这种方法保持了原始顺序，结果中元素出现的先后和原列表一致

---

### 练习3：列表推导式过滤

**题目：** 生成 1-50 中能被 3 整除但不能被 5 整除的数。

**答案：**

```python
result = [x for x in range(1, 51) if x % 3 == 0 and x % 5 != 0]
print(result)
# [3, 6, 9, 12, 18, 21, 24, 27, 33, 36, 39, 42, 48]
```

**解析：**
- `range(1, 51)` 生成 1 到 50 的整数
- `x % 3 == 0`：能被 3 整除
- `x % 5 != 0`：不能被 5 整除
- `and` 连接两个条件，只有同时满足才保留


## 5.2 元组

### 练习1：解包和输出

**题目：** 解包取出工作日和休息日的首尾元素。

**答案：**

```python
work_days = ("周一", "周二", "周三", "周四", "周五")
rest_days = ("周六", "周日")

first_work, *_, last_work = work_days       # *_ 收集中间的元素（不需要它们）
first_rest, last_rest = rest_days

print(f"工作日：{first_work} 到 {last_work}")
print(f"休息日：{first_rest} 到 {last_rest}")
# 工作日：周一 到 周五
# 休息日：周六 到 周日
```

**解析：**
- `*_` 是"吃下剩余元素"的惯用法——下划线 `_` 是 Python 社区约定俗成的"这个值我不需要"的变量名
- 5 个元素解包为 `first, *_, last`：first 拿第一个，last 拿最后一个，`*_` 吞掉中间的三个

---

### 练习2：函数返回元组

**答案：**

```python
def get_grades():
    scores = [88, 95, 73, 91, 82]
    return max(scores), min(scores), sum(scores) / len(scores)

highest, lowest, avg = get_grades()
print(f"最高分：{highest}，最低分：{lowest}，平均分：{avg:.1f}")
```

---

### 练习3：元组中的可变对象

**答案：**

```python
a = ([1, 2], [3, 4])
b = a
a[0].append(3)
print(b)    # ([1, 2, 3], [3, 4])
```

**解析：**
- `a[0]` 是一个列表（可变对象），`a[0].append(3)` 修改的是列表内容，不是元组结构——这是允许的
- `b = a` 让 `b` 指向和 `a` 同一个元组对象，所以 `b` 也能看到修改
- 如果写成 `a[0] = [1, 2, 3]`（试图替换元组位置 0 的引用）就会报 TypeError


## 5.3 字典

### 练习1：词频统计

**题目：** 统计文本中每个单词的出现次数。

**答案：**

```python
text = "python is great and python is easy"
words = text.split()              # ['python', 'is', 'great', 'and', 'python', 'is', 'easy']
word_count = {}

for word in words:
    word_count[word] = word_count.get(word, 0) + 1

print(word_count)
# {'python': 2, 'is': 2, 'great': 1, 'and': 1, 'easy': 1}
```

**解析：**
- `word_count.get(word, 0)` 尝试获取 `word` 的当前计数，如果键不存在则返回 0
- 加 1 后重新赋给字典中的该键，实现累加
- 这是字典统计计数的经典模板，可以用于任何"统计出现次数"的场景

---

### 练习2：通讯录查询

**答案：**

```python
contacts = {
    "小明": {"电话": "13800138000", "邮箱": "xiaoming@example.com"},
    "小红": {"电话": "13900139000", "邮箱": "xiaohong@example.com"},
    "小刚": {"电话": "13700137000", "邮箱": "xiaogang@example.com"},
}

while True:
    name = input("请输入姓名（q 退出）：")
    if name == "q":
        break
    info = contacts.get(name)             # 安全获取，不存在返回 None
    if info:
        print(f"电话：{info['电话']}，邮箱：{info['邮箱']}")
    else:
        print("未找到该联系人")
```

**解析：**
- `contacts.get(name)` 避免 `KeyError`，联系人不存在时返回 `None`
- 嵌套字典的访问使用两层键：`contacts["小明"]["电话"]`
- `while True` + `break` 模式实现持续的交互式查询

---

### 练习3：字典推导式键值互换

**答案：**

```python
original = {"a": 1, "b": 2, "c": 3}
swapped = {v: k for k, v in original.items()}
print(swapped)    # {1: 'a', 2: 'b', 3: 'c'}
```

**解析：**
- `original.items()` 返回键值对，`for k, v` 解包分别拿到键和值
- 新字典中 `v: k` 将原来的值作为键、键作为值
- 注意：如果原字典的值有重复，互换后会丢失数据（字典的键不能重复）


## 5.4 集合

### 练习1：集合运算

**答案：**

```python
list1 = [1, 2, 3, 4, 5]
list2 = [4, 5, 6, 7, 8]

s1 = set(list1)
s2 = set(list2)

print(f"共同元素：{s1 & s2}")              # {4, 5}
print(f"只在 list1 中：{s1 - s2}")         # {1, 2, 3}
print(f"合并去重：{s1 | s2}")              # {1, 2, 3, 4, 5, 6, 7, 8}
```

**解析：**
- 先转集合再做运算，是处理"两个列表之间关系"的标准套路
- 最后一步如果需要转回列表：`list(s1 | s2)`

---

### 练习2：考试统计建模

**题目：** 计算没参加期中/期末考试及两次都没参加的人数。

**答案：**

```python
total = set(range(1, 31))           # 全班 30 人（用 1-30 编号）
midterm = set(range(1, 29))        # 期中参加：第 1-28 号
final = set(range(1, 28))          # 期末参加：第 1-27 号

no_midterm = total - midterm       # 没参加期中
no_final = total - final           # 没参加期末
no_both = total - (midterm | final)  # 两次都没参加

print(f"没参加期中：{len(no_midterm)} 人")     # 2
print(f"没参加期末：{len(no_final)} 人")       # 3
print(f"两次都没参加：{len(no_both)} 人")      # 2
```

**解析：**
- 用 `set(range(...))` 建模班级全集和参与者子集
- `total - midterm` 差集 = 在全班但不在期中参与者中的人数
- `total - (midterm | final)` = 在全班但不在任何一次考试中的人数（两次都没参加）
- 可以验证：`len(midterm & final) = 26`（两次都参加的），符合题目给出的条件

---

### 练习3：输入去重并排序

**答案：**

```python
text = input("请输入一串字母：")
unique_letters = set(text)
result = sorted(unique_letters)
print(set(result))     # 或者直接 print(unique_letters)
```

**输出示例：**

```text
请输入一串字母：abracadabra
{'a', 'b', 'c', 'd', 'r'}
```

**解析：**
- `set(text)` 直接将字符串转为集合，自动去重——字符串会被拆成单个字符
- `sorted()` 返回排好序的列表（字母顺序），再用 `set()` 转回集合纯粹是为了匹配输出格式
- 一行链式写法：`print(set(sorted(set(text))))` ——不过拆开写可读性更好


## 5.5 切片

### 练习1：字符串切片

**答案：**

```python
s = "Python编程语言"

print(s[:6])          # Python（前 6 个字符）
print(s[6:])          # 编程语言（从位置 6 到末尾）
print(s[::-1])        # 言语程编nohtyP（倒序）
print(s[::2])         # Pto编语（奇数位置：0,2,4,6,...）
```

---

### 练习2：列表切片与修改

**答案：**

```python
nums = [10, 20, 30, 40, 50, 60, 70, 80]

# 替换前三个元素
nums[:3] = [99, 88]
print(nums)           # [99, 88, 40, 50, 60, 70, 80]

# 删除索引 2 到 5
del nums[2:6]         # 索引 2,3,4,5（不包含 6）
print(nums)           # [99, 88, 80]

# 反转对比
a = [1, 2, 3, 4]
b = a[::-1]           # 切片反转：a 不变
print(a)              # [1, 2, 3, 4]
print(b)              # [4, 3, 2, 1]

a.reverse()           # 原地反转：a 被修改
print(a)              # [4, 3, 2, 1]
```

---

### 练习3：回文判断

**答案：**

```python
text = input("请输入一句话：")
cleaned = text.replace(" ", "").lower()   # 去空格，转小写

if cleaned == cleaned[::-1]:
    print("是回文")
else:
    print("不是回文")
```

**解析：**
- `replace(" ", "")` 去掉所有空格
- `lower()` 忽略大小写差异
- `cleaned[::-1]` 用切片取倒序——判断回文只需要比较原字符串和倒序字符串是否相等
- 整个过程是管道式的：原始输入 → 去空格 → 转小写 → 切片比较