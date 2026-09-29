## 3.5 字符串

字符串是编程中处理"文字信息"的核心数据类型。从用户名到文章段落，从 URL 到 JSON 数据，字符串无处不在。Python 对字符串的处理能力极强，本节覆盖从基础操作到常用方法的完整知识链。

### 3.5.1 字符串的四种定义方式

Python 提供了多种字符串写法，覆盖不同的使用场景。

```python
s1 = '单引号字符串'               # 最简洁
s2 = "双引号字符串"               # 和单引号等价
s3 = '''三单引号字符串
可以跨多行'''                     # 用于多行文本
s4 = """三双引号字符串
同样可以跨多行"""                 # 和三个单引号等价
```

**如何选择引号类型？** 一个实用原则：当字符串本身包含引号时，外层换另一种引号，避免转义。

```python
text1 = "He said: 'Hello!'"     # 推荐：双引号在外，单引号在内
text2 = 'He said: "Hello!"'     # 也可以：单引号在外，双引号在内
text3 = 'It\'s a book'          # 不推荐：需要转义，可读性差
text4 = "It's a book"           # 推荐：直接套用，无需转义
```

### 3.5.2 字符串的索引与切片

字符串本质是一个**字符序列**，每个字符都有一个位置编号（从 0 开始），可以通过这个编号访问单个字符或截取子串。

```python
s = "Hello Python"
# 位置:  01234567891011

print(s[0])      # H（第 1 个字符）
print(s[6])      # P（第 7 个字符）
print(s[-1])     # n（倒数第 1 个字符）
print(s[-2])     # o（倒数第 2 个字符）
```

**切片语法：`s[start:end:step]`**

| 参数 | 含义 | 默认值 |
|:----:|:-----|:------:|
| `start` | 起始位置（包含） | 0 |
| `end` | 结束位置（**不包含**） | 字符串长度 |
| `step` | 步长 | 1 |

```python
s = "Hello Python"

print(s[0:5])      # Hello（位置 0 到 4，不包含 5）
print(s[:5])       # Hello（省略 start，默认从 0 开始）
print(s[6:])       # Python（省略 end，默认到末尾）
print(s[0:12:2])   # HloPto（每 2 个字符取一个）
print(s[::-1])     # nohtyP olleH（步长为 -1，倒序输出）
```

---

\begin{tipbox}
**关于切片的一个记忆口诀**

"**包含开头，不包含结尾**"——`s[2:5]` 取的是位置 2、3、4 的字符，位置 5 不取。这看似别扭，实则让计算长度变得简单：`s[2:5]` 的长度就是 `5 - 2 = 3`。
\end{tipbox}

---

### 3.5.3 字符串的不可变性

字符串一旦创建，其内容**不能修改**。想要"修改"字符串，必须生成一个新的字符串。

```python
s = "Hello"
# s[0] = "h"          # ❌ 会报错：TypeError，字符串不支持下标赋值

s = "h" + s[1:]       # ✅ 正确：生成新字符串再赋给 s
print(s)              # hello
```

理解这一点有助于避免常见的运行时错误，也解释了为什么字符串的各种方法总是返回新字符串而不是原地修改。

### 3.5.4 字符串常用方法

方法就是"字符串自带的功能函数"，用 `.方法名()` 调用。以下是最高频的 10 个方法。

#### 大小写转换

```python
text = "Hello Python"

print(text.upper())       # HELLO PYTHON（全大写）
print(text.lower())       # hello python（全小写）
print(text.title())       # Hello Python（每个单词首字母大写）
print(text.capitalize())  # Hello python（仅句首大写）
```

#### 去除空白字符

```python
raw = "   Hello Python   \n"

print(raw.strip())        # "Hello Python"（去掉两端空白）
print(raw.lstrip())       # "Hello Python   \n"（去掉左侧空白）
print(raw.rstrip())       # "   Hello Python"（去掉右侧空白）
```

---

\begin{tipbox}
**`strip()` 在数据处理中极为常用**：从文件或网络读取数据时，字符串两端经常携带换行符、多余空格，用 `strip()` 能快速清理。
\end{tipbox}

---

#### 查找与判断

```python
text = "Hello Python"

print(text.find("P"))         # 6（返回首次出现位置，未找到返回 -1）
print(text.index("P"))        # 6（和 find 类似，但未找到会报错）
print(text.count("l"))        # 2（统计子串出现次数）

print(text.startswith("He"))  # True（判断是否以 "He" 开头）
print(text.endswith("on"))    # True（判断是否以 "on" 结尾）

print("123".isdigit())        # True（是否全为数字）
print("abc".isalpha())        # True（是否全为字母）
print("abc123".isalnum())     # True（是否全为字母或数字）
```

#### 替换与拆分

```python
text = "apple,banana,orange"

print(text.replace("banana", "grape"))   # "apple,grape,orange"

fruits = text.split(",")                 # ['apple', 'banana', 'orange']（按逗号拆分）
print(fruits[1])                         # banana

date_str = "2026-09-29"
parts = date_str.split("-")              # ['2026', '09', '29']
print(f"{parts[0]}年{parts[1]}月{parts[2]}日")  # 2026年09月29日
```

#### 拼接

```python
words = ["Hello", "Python", "World"]
result = " ".join(words)       # "Hello Python World"（用空格连接）

path_parts = ["c:", "users", "docs"]
path = "\\".join(path_parts)   # "c:\\users\\docs"（用反斜杠连接）
```

---

\begin{definitionbox}
**`split()` 和 `join()` 是一对逆操作**

- `split(分隔符)`：把字符串**拆成**列表
- `"连接符".join(列表)`：把列表**拼回**字符串

这对方法在数据处理流程中如影随形——读入时 `split()` 拆分，处理完后 `join()` 拼合输出。
\end{definitionbox}

---

### 3.5.5 转义字符

有些特殊字符无法直接在字符串中输入（如换行符、制表符），需要用转义序列表示。

| 转义序列 | 含义 |
|:--------:|:-----|
| `\n` | 换行 |
| `\t` | 制表符（Tab） |
| `\\` | 反斜杠本身 |
| `\'` | 单引号 |
| `\"` | 双引号 |

```python
print("第一行\n第二行")            # 两行输出
print("姓名\t年龄\t城市")         # 三个字段用 Tab 对齐
print("文件路径：C:\\Users\\docs")  # 正确显示反斜杠
```

如果不希望任何转义生效（如处理 Windows 文件路径），在字符串前加 `r`：

```python
path = r"C:\Users\docs\new"     # 原始字符串，\n 不会被当成换行
print(path)                     # C:\Users\docs\new
```

### 3.5.6 字符串格式化回顾

在 3.3 节中已详细介绍 f-string，此处做简要回顾：

```python
name = "小明"
age = 20
height = 1.75

print(f"我叫{name}，今年{age}岁，身高{height:.2f}米")
# 输出：我叫小明，今年20岁，身高1.75米
```

f-string 是 Python 3.6+ 推荐的高效格式化方式，在变量名直接嵌入、表达式内嵌等场景都极为方便。

### 3.5.7 实战练习

1. 定义字符串 `s = "  Python is Amazing!  "`，通过方法链完成以下操作（一行代码实现）：去除两端空格 → 转为全小写 → 将 `"amazing"` 替换为 `"powerful"`，最后输出结果。

2. 用户按格式输入手机号 `"138-1234-5678"`（用 `input()` 接收），请编写程序：
   - 去掉中间的连字符 `-`，输出纯数字手机号
   - 将中间四位用 `****` 遮挡，输出 `138-****-5678`

3. 字符串切片练习：令 `s = "Python基础教程"`，用切片操作分别输出：
   - 前 6 个字符
   - 去掉前 6 个字符后的剩余部分
   - 整个字符串的倒序