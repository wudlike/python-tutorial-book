## 11.2 datetime/time 模块——掌控时间的每一个刻度

时间处理是编程中最容易踩坑的领域之一——时区转换、夏令时、闰秒、格式不统一……Python 的 `time` 和 `datetime` 两个模块为这一切提供了坚实的底层支持。`time` 偏重底层的时间戳和性能计时，`datetime` 则提供了人类友好、可计算的时间对象。掌握它们，你就能从容应对日志解析、定时任务、时间差计算等日常需求。

### 11.2.1 `time` 模块——时间的"底层语言"

`time` 模块的核心概念是**时间戳**（timestamp）——从 1970 年 1 月 1 日 00:00:00 UTC（Unix 纪元）到某个时刻的秒数（浮点数）。这个看似"古怪"的设计让时间的存储和计算变得极其简单——两个时间差就是两个浮点数相减：

```python
import time

# 当前时间戳——Unix 时间
now_timestamp = time.time()
print(f"当前时间戳：{now_timestamp}")                 # 如 1719619200.123456

# 时间戳 ↔ 结构化时间
local_time = time.localtime(now_timestamp)            # 转为本地时间的 struct_time
utc_time = time.gmtime(now_timestamp)                  # 转为 UTC 时间的 struct_time

print(f"本地时间：{local_time.tm_year}-{local_time.tm_mon:02d}-{local_time.tm_mday:02d}")
print(f"年={local_time.tm_year}, 月={local_time.tm_mon}, 日={local_time.tm_mday}")
print(f"时={local_time.tm_hour}, 分={local_time.tm_min}, 秒={local_time.tm_sec}")
print(f"星期几={local_time.tm_wday}（0=周一）")

# 结构化时间 → 时间戳
back_to_timestamp = time.mktime(local_time)

# 格式化输出
formatted = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
print(f"格式化时间：{formatted}")                      # 2024-06-29 12:00:00

# 字符串 → 结构化时间
parsed = time.strptime("2024-06-29 12:00:00", "%Y-%m-%d %H:%M:%S")
print(f"解析结果：{parsed.tm_year}年")
```

#### `time.sleep()` 与性能计时

```python
import time

# 让程序暂停
print("开始等待...")
time.sleep(2)                              # 暂停 2 秒（阻塞当前线程）
print("等待结束")

# 高精度性能计时——比 time.time() 更精确，不受系统时间调整影响
start = time.perf_counter()
# 这里执行你想测量的代码
total = sum(range(10_000_000))
elapsed = time.perf_counter() - start
print(f"计算耗时：{elapsed:.6f} 秒")

# 进程 CPU 时间——只计算当前进程实际占用的 CPU 时间，不含 sleep
start = time.process_time()
time.sleep(1)
elapsed_cpu = time.process_time() - start
print(f"CPU 时间（不包含 sleep）：{elapsed_cpu:.6f} 秒")    # 接近 0
```

### 11.2.2 `datetime` 模块——时间的"高层接口"

`datetime` 提供了四个核心类：`date`（日期）、`time`（时间）、`datetime`（日期+时间）、`timedelta`（时间差）：

```python
from datetime import date, time, datetime, timedelta

# date —— 只含年、月、日
today = date.today()
print(f"今天：{today}")                     # 2024-06-29
print(f"年：{today.year}, 月：{today.month}, 日：{today.day}")
print(f"星期几：{today.weekday()}（0=周一）")
print(f"ISO 星期几：{today.isoweekday()}（1=周一）")

# 自定义日期
birthday = date(1990, 5, 20)
print(f"生日：{birthday}")

# time —— 只含时、分、秒、微秒
noon = time(12, 0, 0)
alarm = time(7, 30, 0)
print(f"正午：{noon}")
print(f"闹钟：{alarm}")

# datetime —— 日期 + 时间（最常用）
now = datetime.now()
print(f"现在：{now}")
print(f"日期部分：{now.date()}，时间部分：{now.time()}")

# 自定义 datetime
event = datetime(2024, 12, 31, 23, 59, 59)
print(f"跨年夜：{event}")
```

### 11.2.3 `timedelta`——时间的加减法

`timedelta` 表示两个时间点之间的差异，是天、秒、微秒的组合：

```python
from datetime import datetime, timedelta

now = datetime.now()

# 时间加减——最实用的功能
tomorrow = now + timedelta(days=1)
yesterday = now - timedelta(days=1)
next_week = now + timedelta(weeks=1)
three_hours_later = now + timedelta(hours=3)
half_hour_ago = now - timedelta(minutes=30)

print(f"明天：{tomorrow}")
print(f"昨天：{yesterday}")
print(f"下周：{next_week}")

# 计算两个日期之间的差
birthday = datetime(1990, 5, 20)
delta = now - birthday
print(f"已经过了 {delta.days} 天")
print(f"大约 {delta.days // 365} 年")

# 计算项目截止时间
deadline = datetime(2024, 12, 31, 18, 0, 0)
remaining = deadline - now
if remaining.total_seconds() > 0:
    print(f"距离截止还有 {remaining.days} 天 {remaining.seconds // 3600} 小时")
```

### 11.2.4 格式化与解析——`strftime`/`strptime`

日期和字符串之间的互转是最频繁的操作，关键在于掌握格式化代码：

| 代码 | 含义 | 示例 |
|:-----|:-----|:-----|
| `%Y` | 四位年份 | 2024 |
| `%y` | 两位年份 | 24 |
| `%m` | 月份（补零） | 06 |
| `%d` | 日期（补零） | 29 |
| `%H` | 24 小时制小时 | 14 |
| `%I` | 12 小时制小时 | 02 |
| `%M` | 分钟 | 30 |
| `%S` | 秒 | 45 |
| `%A` | 星期几（全称） | Saturday |
| `%B` | 月份（全称） | June |
| `%p` | AM/PM | PM |

```python
from datetime import datetime

now = datetime.now()

# datetime → 字符串（strftime — "format time"）
print(now.strftime("%Y-%m-%d"))                          # 2024-06-29
print(now.strftime("%Y年%m月%d日"))                        # 2024年06月29日
print(now.strftime("%A, %B %d, %Y"))                     # Saturday, June 29, 2024
print(now.strftime("%Y-%m-%d %H:%M:%S"))                 # 2024-06-29 14:30:45

# 字符串 → datetime（strptime — "parse time"）
log_time = datetime.strptime("2024-06-29 14:30:45", "%Y-%m-%d %H:%M:%S")
print(f"解析结果：{log_time}")

chinese_date = datetime.strptime("2024年06月29日", "%Y年%m月%d日")
print(f"中文日期解析：{chinese_date}")

# 实用：解析各种日志格式
apache_log_time = datetime.strptime("29/Jun/2024:14:30:45", "%d/%b/%Y:%H:%M:%S")
print(f"Apache 日志时间：{apache_log_time}")
```

### 11.2.5 时区处理——`datetime.timezone`

Python 3.9+ 内置了 `zoneinfo` 模块（之前需要安装 `pytz`），让时区处理变得简单：

```python
from datetime import datetime
from zoneinfo import ZoneInfo

# 获取当前 UTC 时间（带时区信息）
utc_now = datetime.now(ZoneInfo("UTC"))
print(f"UTC 时间：{utc_now}")

# 转换为不同时区
tokyo_time = utc_now.astimezone(ZoneInfo("Asia/Tokyo"))
ny_time = utc_now.astimezone(ZoneInfo("America/New_York"))
shanghai_time = utc_now.astimezone(ZoneInfo("Asia/Shanghai"))

print(f"东京时间：{tokyo_time}")
print(f"纽约时间：{ny_time}")
print(f"北京时间：{shanghai_time}")

# 使用时区意识创建时间——避免"naive datetime"的陷阱
meeting = datetime(2024, 6, 29, 15, 0, tzinfo=ZoneInfo("Asia/Shanghai"))
print(f"北京时间 15:00 = 纽约时间 {meeting.astimezone(ZoneInfo('America/New_York'))}")

# 列出所有可用时区
# import zoneinfo
# print(zoneinfo.available_timezones())
```

---

\begin{warningbox}
**naive datetime 陷阱**

不带时区信息的 `datetime` 对象被称为"naive datetime"。两个 naive datetime 做运算时代码能跑通，但结果是"模糊的"——你不知道它们各自代表哪个时区的时刻。在与外界系统（数据库、API）交互时，这可能导致几小时甚至一整天的偏差。如果你在一个跨时区的项目中工作，请始终使用带 `tzinfo` 的 datetime 对象。
\end{warningbox}

---

### 11.2.6 实战练习

1. 编写一个函数 `get_age(birth_date_str)`，接收一个形如 `"1990-05-20"` 的生日字符串，返回当前的周岁年龄。注意考虑生日还没到的情形。

2. 编写一个函数 `format_timestamp(timestamp, fmt="%Y-%m-%d %H:%M:%S")`，接收一个 Unix 时间戳（浮点数），返回格式化后的日期时间字符串。例如输入 `0`（Unix 纪元），返回 `"1970-01-01 08:00:00"`（东八区）。

3. 计算活了多久——写一个程序：输入出生日期和时间（例如 `"1990-05-20 08:30:00"`），输出精确到秒的"你已经活了 X 天 Y 小时 Z 分钟 W 秒"。