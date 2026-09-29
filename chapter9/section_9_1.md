## 9.1 文件的读写操作——数据的"入库"与"出库"

到目前为止，你程序中的所有数据都活在内存里——程序一关，成绩列表、学生信息、计算成果，灰飞烟灭。要让数据"活"过程序的运行周期，你需要把它们存到文件中。文件操作是程序与外部世界交换数据的最基本方式，也是从"玩具程序"走向"实用工具"的第一道门槛。

### 9.1.1 从"打开"到"关闭"——文件操作的基本流程

在 Python 中操作文件遵循一个固定的四步流程：打开 → 读写 → 关闭 → 善后。其中"关闭"这一步最容易漏掉，但漏掉它的后果可轻可重——轻则浪费系统资源，重则数据写入不完整。

```python
f = open("hello.txt", "w", encoding="utf-8")    # 1. 打开文件（写入模式）
f.write("Hello, Python!\n")                      # 2. 写入内容
f.write("第二行文字\n")
f.close()                                        # 3. 关闭文件
```

`open()` 函数是最核心的入口，它接收三个关键参数：
- **文件路径**：`"hello.txt"`——相对路径，文件会创建在当前工作目录下
- **模式**：`"w"` 表示写入模式——后面 9.1.2 节会详细展开
- **编码**：`encoding="utf-8"`——强烈建议每次都显式指定，避免中文乱码

### 9.1.2 文件打开模式——不同场景用不同的"模式"

`open()` 的第二个参数决定了你打算对文件做什么。以下是全部常用模式：

| 模式 | 全称 | 含义 | 文件不存在？ | 文件已存在？ |
|:----:|:-----|:-----|:----------|:----------|
| `"r"` | read | 只读 | 报错 | 从头读 |
| `"w"` | write | 只写 | 自动创建 | **清空后写**（覆盖） |
| `"a"` | append | 追加写 | 自动创建 | 在末尾追加 |
| `"x"` | exclusive | 独占创建 | 自动创建 | 报错（防覆盖） |
| `"r+"` | read+write | 读写 | 报错 | 从头读写 |
| `"b"` | binary | 二进制模式 | 与其他组合 | 用于图片、音频等 |

模式可以组合使用，比如 `"rb"` 表示以二进制方式读取，`"ab"` 表示以二进制方式追加。

```python
# 读模式——最安全，不会改动文件内容
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)

# 写模式——会覆盖已有内容，小心！
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("这是新内容\n")

# 追加模式——在文件末尾添加，不覆盖已有内容
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("新的一行日志\n")
```

---

\begin{warningbox}
**`"w"` 模式的"杀伤力"**

`"w"` 模式会**无条件清空**已有文件的内容。如果你打开的是一个存了半年数据的文件，一个 `open("data.csv", "w")` 就能把它变成一片空白。因此：
- 写入新文件用 `"w"` 没问题
- 不确定文件是否重要时，先用 `"x"`（文件已存在会报错，给你反悔的机会）
- 想保留旧内容并在末尾添加新内容时，用 `"a"`
\end{warningbox}

---

### 9.1.3 读文件的三种方式——按需选择

Python 提供了三种读取文件内容的策略，各有适用场景：

```python
# 方式一：read()——一次性读取整个文件
with open("poem.txt", "r", encoding="utf-8") as f:
    entire = f.read()
    print(entire)

# 方式二：readline()——逐行读取，一次一行
with open("poem.txt", "r", encoding="utf-8") as f:
    line = f.readline()
    while line:
        print(line.strip())          # strip() 去掉行尾的换行符
        line = f.readline()

# 方式三：直接迭代文件对象——最 Pythonic 的逐行读取
with open("poem.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
```

三种方式的选择策略：
- 文件很小（几 KB 到几百 KB）→ `read()`，代码最简洁
- 文件很大（几 MB 到几百 MB）→ 直接迭代（方式三），只占一行内容的内存，不会把整个文件加载到内存中
- 需要更精细的行级控制（如读到特定行就停止）→ `readline()`

直接迭代文件对象（方式三）是 Python 社区的推荐做法——简洁、高效、Pythonic。

### 9.1.4 写文件的两种方式

```python
# write()——写入字符串，不会自动加换行
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("第一行")
    f.write("第二行")        # 和第一行挤在一起了——因为没有 \n

# writelines()——写入字符串列表
lines = ["第一行\n", "第二行\n", "第三行\n"]
with open("output.txt", "w", encoding="utf-8") as f:
    f.writelines(lines)
```

注意 `writelines()` 不会自动添加换行符——你需要自己在每个字符串末尾加上 `\n`。这和很多初学者的直觉相反（名字里有"line"，但行为并不"帮你分行"），是个容易中招的细节。

### 9.1.5 `tell()` 和 `seek()`——在文件中"导航"

Python 为每个打开的文件维护一个"文件指针"——它标记了当前读写位置。`tell()` 告诉你指针在哪里，`seek()` 让你移动指针到任意位置：

```python
with open("numbers.txt", "w+", encoding="utf-8") as f:
    f.write("0123456789")
    f.seek(0)                   # 指针回到文件开头

    print(f.read(3))            # "012"——从开头读 3 个字符
    print(f.tell())             # 3——指针现在在第 3 个字符后

    f.seek(5)                   # 指针跳到第 5 个字符
    print(f.read(3))            # "567"
```

`seek(n)` 接受一个整数参数，表示从文件开头跳过 `n` 个字节。在文本文件（非二进制）中使用 `seek` 需要小心——中文等多字节字符可能被从中间截断。

### 9.1.6 文件路径与编码——跨平台的注意事项

文件路径在不同操作系统上有不同的写法——Windows 用 `C:\Users\name\file.txt`，macOS/Linux 用 `/home/name/file.txt`。在代码中写死路径会导致换个系统就跑不起来。解决方案：

```python
import os

# 使用 os.path.join 构建路径——自动适配操作系统
base_dir = "data"
filename = "report.txt"
full_path = os.path.join(base_dir, filename)    # Windows: data\report.txt  Linux: data/report.txt

# 或使用 pathlib（Python 3.4+，更现代的方案）
from pathlib import Path
full_path = Path("data") / "report.txt"
```

关于编码：`utf-8` 是现今最通用的编码方式，能正确处理中文、日文、韩文、表情符号等几乎所有字符。养成每次 `open` 都写 `encoding="utf-8"` 的习惯，可以省去大量调试"乱码"问题的时间。

### 9.1.7 实战练习

1. 编写程序，将列表 `["苹果", "香蕉", "橘子", "葡萄", "西瓜"]` 的每个元素写入 `fruits.txt`，每个水果占一行。然后读取该文件，将内容打印出来。

2. 编写一个文件复制程序：将 `source.txt` 的内容逐行复制到 `destination.txt` 中。要求使用"直接迭代文件对象"的方式逐行读取，避免一次性加载整个文件。

3. 以下代码的意图是向 `data.txt` 追加三行内容，但存在一个问题。指出问题并修正：

```python
with open("data.txt", "w", encoding="utf-8") as f:
    f.write("第一行")
    f.write("第二行")
    f.write("第三行")
```