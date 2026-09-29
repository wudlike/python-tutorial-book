## 11.1 os/sys 模块

### 练习1：find_python_files

**答案：**

```python
import os

def find_python_files(directory):
    py_files = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git")]
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.abspath(os.path.join(root, file)))
    return py_files

# 测试
result = find_python_files(".")
for f in result:
    print(f)
```

**解析：**
- `dirs[:] = [...]` 通过切片赋值修改 `dirs` 列表本身（而不是重新绑定变量），这样 `os.walk()` 就能识别到并跳过被排除的目录
- `os.path.abspath()` 将相对路径转为绝对路径，确保结果的一致性和可用性

---

### 练习2：命令行大写转换器

**答案：**

```python
import sys

def main():
    if len(sys.argv) < 2:
        print("用法：python upper.py <文件路径>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        sys.stdout.write(content.upper())
    except FileNotFoundError:
        print(f"错误：文件 '{filepath}' 不存在", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

**解析：**
- `sys.argv[0]` 是脚本名，`sys.argv[1]` 才是第一个命令行参数
- 错误信息应该输出到 `stderr`（用 `file=sys.stderr`），这样脚本的正常输出和错误信息就不会混在一起
- `sys.exit(1)` 表示异常退出——调用方可以通过退出码判断脚本是否成功

---

### 练习3：subprocess 执行命令

**答案：**

```python
import subprocess
import sys

# 尝试执行 git status，如果不存在则执行 dir
command = ["git", "status"]
try:
    result = subprocess.run(command, capture_output=True, text=True, timeout=10)
except FileNotFoundError:
    # git 不存在，换用 dir
    command = ["cmd", "/c", "dir"]
    result = subprocess.run(command, capture_output=True, text=True, timeout=10)

if result.returncode == 0:
    print("命令执行成功：")
    print(result.stdout)
else:
    print("命令执行失败：", file=sys.stderr)
    print(result.stderr, file=sys.stderr)
    sys.exit(result.returncode)
```

**解析：**
- `capture_output=True` 捕获标准输出和标准错误，结果在 `result.stdout` 和 `result.stderr` 中
- `timeout=10` 防止命令"卡死"——超时后会抛出 `subprocess.TimeoutExpired`
- 通过 `result.returncode` 判断命令是否成功，并将退出码传递给 `sys.exit()`


## 11.2 datetime/time 模块

### 练习1：get_age 计算周岁

**答案：**

```python
from datetime import datetime

def get_age(birth_date_str):
    birth = datetime.strptime(birth_date_str, "%Y-%m-%d")
    today = datetime.now()

    # 先按年份差算
    age = today.year - birth.year

    # 如果今年的生日还没到，减一岁
    if (today.month, today.day) < (birth.month, birth.day):
        age -= 1

    return age

print(get_age("1990-05-20"))    # 例如 34（取决于当前日期）
print(get_age("2010-12-31"))
```

**解析：**
- 直接用 `年份差` 会高估——如果今天是 6 月而生日是 12 月，还没到生日
- `(today.month, today.day) < (birth.month, birth.day)` 通过元组比较判断"今年的生日过了没有"——Python 的元组比较是按元素逐个比较的，非常方便

---

### 练习2：format_timestamp

**答案：**

```python
from datetime import datetime, timezone, timedelta

def format_timestamp(timestamp, fmt="%Y-%m-%d %H:%M:%S"):
    # 将时间戳转为 UTC 时间的 datetime，再转为东八区
    utc_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    local_time = utc_time.astimezone(timezone(timedelta(hours=8)))
    return local_time.strftime(fmt)

print(format_timestamp(0))                      # 1970-01-01 08:00:00
print(format_timestamp(1719619200))             # 如 2024-06-29 08:00:00
print(format_timestamp(0, "%Y年%m月%d日"))       # 1970年01月01日
```

**解析：**
- `datetime.fromtimestamp(0)` 在不指定时区时返回的是**本地时间**（取决于运行机器的时区设置）。为了明确表达"东八区"，我们先用 `timezone.utc` 获取 UTC 时间，再转为 `+8` 时区
- Unix 纪元（0 秒）对应的是 UTC 1970-01-01 00:00:00，东八区就是 08:00:00

---

### 练习3：活了多久

**答案：**

```python
from datetime import datetime

birth_str = input("请输入出生日期和时间（格式：1990-05-20 08:30:00）：")
birth = datetime.strptime(birth_str, "%Y-%m-%d %H:%M:%S")
now = datetime.now()

delta = now - birth

total_seconds = int(delta.total_seconds())
days = total_seconds // 86400
remaining = total_seconds % 86400
hours = remaining // 3600
remaining %= 3600
minutes = remaining // 60
seconds = remaining % 60

print(f"你已经活了 {days} 天 {hours} 小时 {minutes} 分钟 {seconds} 秒")
```

**解析：**
- `delta.total_seconds()` 返回时间差的总秒数（浮点数）
- 然后通过整除和取模逐步分解为天、小时、分钟、秒
- `86400 = 24 × 60 × 60`（一天的秒数），`3600 = 60 × 60`（一小时的秒数）


## 11.3 random/math 模块

### 练习1：抽奖程序

**答案：**

```python
import random

participants = ["张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十",
                "郑一", "冯二"]

# 总共要抽 1 + 2 + 3 = 6 个人，每人最多中一次 → 用 sample
winners = random.sample(participants, k=6)

first = winners[0:1]
second = winners[1:3]
third = winners[3:6]

print("🎉 抽奖结果：")
print(f"一等奖（1人）：{first[0]}")
print(f"二等奖（2人）：{', '.join(second)}")
print(f"三等奖（3人）：{', '.join(third)}")
```

**解析：**
- `random.sample()` 不放回抽样——确保每人最多中奖一次
- 一次抽取 6 人，然后按顺序分配奖项——简单且公平

---

### 练习2：三角形面积

**答案：**

```python
import math

def calc_triangle_area(a, b, angle_c):
    """已知两边及其夹角（度数），计算三角形面积"""
    angle_rad = math.radians(angle_c)               # 度数 → 弧度
    area = 0.5 * a * b * math.sin(angle_rad)
    return area

print(f"a=3, b=4, 夹角=90° → 面积 = {calc_triangle_area(3, 4, 90):.1f}")   # 6.0
print(f"a=5, b=5, 夹角=60° → 面积 = {calc_triangle_area(5, 5, 60):.2f}")   # 10.83
```

**验证：**
- `3-4-5` 直角三角形的面积：`0.5 × 3 × 4 = 6.0` ✓
- 边长为 5 的等边三角形面积：`0.5 × 5 × 5 × sin(60°) ≈ 10.825` ✓

---

### 练习3：硬币实验

**答案：**

```python
import random

def coin_experiment(n_flips=10000):
    """抛硬币 n 次，返回正面比例"""
    heads = sum(1 for _ in range(n_flips) if random.randint(0, 1) == 1)
    return heads / n_flips

# 重复 1000 次实验
proportions = [coin_experiment() for _ in range(1000)]

# 统计
import math
mean = sum(proportions) / len(proportions)
variance = sum((p - mean) ** 2 for p in proportions) / len(proportions)
std_dev = math.sqrt(variance)

print(f"1000 次实验（每次抛 10000 次）：")
print(f"正面比例均值：{mean:.4f}")
print(f"正面比例标准差：{std_dev:.4f}")

# 理论值
print(f"理论均值：0.5000")
print(f"理论标准差：{math.sqrt(0.5 * 0.5 / 10000):.4f}")
```

**输出示例：**

```text
1000 次实验（每次抛 10000 次）：
正面比例均值：0.5000
正面比例标准差：0.0050
理论均值：0.5000
理论标准差：0.0050
```

**解析：**
- 每次实验抛 10000 次，正面比例已经非常接近 0.5
- 标准差约 0.005，说明 95% 的实验结果在 0.490 ~ 0.510 之间（均值 ± 2 倍标准差）
- 这验证了大数定律——实验次数越多，样本比例越接近真实概率


## 11.4 re 正则表达式

### 练习1：身份证提取

**答案：**

```python
import re

text = "张三 110101199001011234，李四 32010219851215789X，不是身份证的 123456789012345678"

# 模式：前 17 位数字 + 最后一位（数字或 X）
pattern = re.compile(r"\b\d{17}[\dX]\b")
ids = pattern.findall(text)
print(ids)    # ['110101199001011234', '32010219851215789X']

# 解释为什么 123456789012345678 没有被匹配
# 123456789012345678 只匹配了前 17 位是数字，但第 18 位是 8（数字），看似应该匹配
# 实际上它有 18 位、全是数字 → 应该被匹配！
# 等等——123456789012345678 确实是 18 位数字，正则能匹配到
# 真正"不是身份证"的意思是它不是合法的身份证号，但正则只能做格式匹配，不能做校验
```

**修正分析：** 实际上 `123456789012345678` 也会被匹配（它是 18 位纯数字）。正则表达式只能做**格式层面的匹配**，无法判断身份证号码的校验位、出生日期是否合法。真正的身份证校验需要结合校验码算法：

```python
# 改进——增加一个简单的 check 过滤明显不合法的
def is_plausible_id(id_str):
    """粗略判断：出生日期在合理范围"""
    year = int(id_str[6:10])
    month = int(id_str[10:12])
    day = int(id_str[12:14])
    return 1900 <= year <= 2024 and 1 <= month <= 12 and 1 <= day <= 31

ids = pattern.findall(text)
plausible = [i for i in ids if is_plausible_id(i)]
print(plausible)    # ['110101199001011234', '32010219851215789X']
```

---

### 练习2：clean_text

**答案：**

```python
import re

def clean_text(text):
    # 1. 去掉 HTML 标签
    text = re.sub(r"<[^>]+>", "", text)

    # 2. 把所有连续空白替换为一个空格
    text = re.sub(r"\s+", " ", text).strip()

    # 3. 中文和英文/数字之间插入空格
    text = re.sub(r"([\u4e00-\u9fff])([a-zA-Z0-9])", r"\1 \2", text)
    text = re.sub(r"([a-zA-Z0-9])([\u4e00-\u9fff])", r"\1 \2", text)

    return text

# 测试
dirty = "<p>这是Python3.9版本，运行在Windows10上。</p>   多余   空格"
print(clean_text(dirty))
# → 这是 Python 3.9 版本，运行在 Windows 10 上。 多余 空格
```

**解析：**
- `r"<[^>]+>"` 匹配 `<` 开头、`>` 结尾、中间是任意非 `>` 字符的标签
- `([\u4e00-\u9fff])([a-zA-Z0-9])` 匹配"中文字符紧接着英文字符"，替换为中间加空格
- 反过来再匹配一次 `([a-zA-Z0-9])([\u4e00-\u9fff])` 处理"英文字符紧接着中文"的情况

---

### 练习3：Nginx 日志解析器

**答案：**

```python
import re

log_line = '192.168.1.100 - - [29/Jun/2024:14:30:45 +0800] "GET /api/users HTTP/1.1" 200 1234'

pattern = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+) '           # IP 地址
    r'\S+ \S+ '                                 # 跳过的两个字段（ident 和 user）
    r'\[(?P<time>[^\]]+)\] '                    # 时间（方括号内所有内容）
    r'"(?P<method>\S+) '                        # 请求方法
    r'(?P<path>\S+) '                           # 请求路径
    r'\S+" '                                    # 协议版本（跳过）
    r'(?P<status>\d{3}) '                       # 状态码
    r'(?P<size>\d+)'                            # 响应大小
)

match = pattern.match(log_line)
if match:
    print(f"IP:     {match['ip']}")
    print(f"时间:   {match['time']}")
    print(f"方法:   {match['method']}")
    print(f"路径:   {match['path']}")
    print(f"状态码: {match['status']}")
    print(f"大小:   {match['size']} 字节")

    # 判断响应是否成功
    if match['status'].startswith('2'):
        print("✅ 请求成功")
    elif match['status'].startswith('4'):
        print("⚠️ 客户端错误")
    elif match['status'].startswith('5'):
        print("❌ 服务器错误")
```

**输出：**

```text
IP:     192.168.1.100
时间:   29/Jun/2024:14:30:45 +0800
方法:   GET
路径:   /api/users
状态码: 200
大小:   1234 字节
✅ 请求成功
```

**解析：**
- `[^\]]+` 匹配方括号内的所有内容（直到 `]`），这是一个常见的"匹配定界符之间的内容"的模式
- `(?P<name>...)` 命名分组让代码更可读——`match['ip']` 比 `match.group(1)` 清晰得多
- 可以用`str.startswith()`判断状态码类别（2xx=成功, 4xx=客户端错误, 5xx=服务器错误）