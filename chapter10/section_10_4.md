## 10.4 并发编程基础——让程序"一心多用"

到目前为止，你写的所有程序都是**顺序执行**的——第一步做完才做第二步，第二步做完才做第三步。这种模式在大多数场景下够用，但当你需要同时处理多个任务时（比如下载 100 张图片、同时响应多个网络请求、在后台定期保存数据），顺序执行就会慢得让人无法忍受。

Python 提供了两套主流的并发方案：**多线程**（threading）适合 I/O 密集型任务（网络请求、文件读写），**多进程**（multiprocessing）适合 CPU 密集型任务（大量计算）。本节介绍两者的基本用法和选择策略。

### 10.4.1 并发 vs 并行——两个容易混淆的概念

在进入代码之前，先理清两个概念：

- **并发（Concurrency）**：多个任务**交替执行**。在某个微小的时间点上只有一个任务在运行，但任务之间切换得足够快，看起来像"同时"进行。就像一个人同时炒两个菜——一会儿翻这个锅，一会儿搅那个锅。
- **并行（Parallelism）**：多个任务**真正同时执行**。需要多核 CPU，每个核心运行一个任务。就像两个人各炒一个菜。

Python 的多线程因为**全局解释器锁**（GIL，Global Interpreter Lock）的存在，无法实现真正的并行——同一时刻只有一个线程在执行 Python 字节码。但这并不意味着多线程没用：对于 I/O 密集型任务（等待网络响应时线程会释放 GIL），多线程能显著提升效率。

### 10.4.2 `threading`——多线程

多线程的核心用法是创建一个 `Thread` 对象，把要执行的任务函数传给它，然后启动：

```python
import threading
import time

def download_file(filename, duration):
    """模拟下载文件——用 sleep 假装在等待网络响应"""
    print(f"开始下载 {filename}...")
    time.sleep(duration)            # 模拟 I/O 等待
    print(f"{filename} 下载完成（耗时 {duration} 秒）")

# 顺序执行——三个文件依次下载
start = time.time()
download_file("file1.zip", 2)
download_file("file2.zip", 3)
download_file("file3.zip", 1)
print(f"顺序执行总耗时：{time.time() - start:.1f} 秒")
# 总耗时约 6 秒（2+3+1）
```

```python
# 多线程——三个文件"同时"下载
start = time.time()
threads = [
    threading.Thread(target=download_file, args=("file1.zip", 2)),
    threading.Thread(target=download_file, args=("file2.zip", 3)),
    threading.Thread(target=download_file, args=("file3.zip", 1)),
]

for t in threads:
    t.start()          # 启动线程

for t in threads:
    t.join()           # 等待所有线程完成

print(f"多线程总耗时：{time.time() - start:.1f} 秒")
# 总耗时约 3 秒（取最长的那个）
```

输出对比：

```text
开始下载 file1.zip...
开始下载 file2.zip...
开始下载 file3.zip...
file3.zip 下载完成（耗时 1 秒）
file1.zip 下载完成（耗时 2 秒）
file2.zip 下载完成（耗时 3 秒）
多线程总耗时：3.0 秒
```

三个文件的下载"同时"开始了，总耗时大约等于最慢的那个文件（3 秒），而不是三者之和（6 秒）。这就是多线程在 I/O 密集型任务上的威力——当一个线程在等待网络响应时，其他线程可以趁这个空隙工作。

---

\begin{warningbox}
**线程安全——共享数据的危险**

当多个线程同时读写同一个变量时，可能出现"竞态条件"（Race Condition）：

```python
import threading

counter = 0

def increment():
    global counter
    for _ in range(100_000):
        counter += 1         # 这一步不是原子的！读-加-写 三步可能被打断

threads = [threading.Thread(target=increment) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(counter)              # 预期 1_000_000，实际可能小于这个值！
```

解决方法：使用 `threading.Lock` 锁保护共享数据，或者使用 `queue.Queue` 等线程安全的数据结构。
\end{warningbox}

---

### 10.4.3 `concurrent.futures`——更高级的线程池

手动创建和管理线程有些繁琐。`concurrent.futures` 模块提供了线程池（ThreadPoolExecutor），让你用更简洁的方式提交任务：

```python
from concurrent.futures import ThreadPoolExecutor
import time

def download_file(filename, duration):
    print(f"开始下载 {filename}...")
    time.sleep(duration)
    return f"{filename} 完成（{duration}s）"

with ThreadPoolExecutor(max_workers=3) as executor:
    # 同时提交多个任务
    futures = {
        executor.submit(download_file, f"file{i}.zip", i): f"file{i}.zip"
        for i in range(1, 6)
    }

    # 按完成顺序获取结果
    for future in futures:
        result = future.result()
        print(f"✅ {result}")
```

线程池的核心优势：
1. 自动管理线程的创建和销毁，避免频繁创建线程的开销
2. `max_workers` 限制了同时运行的线程数量，避免无限制地创建线程
3. `future.result()` 会阻塞直到任务完成，自动帮你完成"等待"的逻辑

### 10.4.4 CPU 密集型任务——为什么需要多进程

多线程在 I/O 密集场景下表现出色，但在 CPU 密集场景下几乎无效——因为 GIL 的存在，同一时刻只有一个线程能执行 Python 代码。计算 100 个斐波那契数，开 10 个线程和不开线程速度差不多。

这时需要**多进程**——每个进程有自己独立的 Python 解释器和 GIL，可以真正利用多核 CPU 并行计算：

```python
from concurrent.futures import ProcessPoolExecutor
import time

def cpu_heavy(n):
    """计算斐波那契数——CPU 密集型任务"""
    if n <= 1:
        return n
    return cpu_heavy(n - 1) + cpu_heavy(n - 2)

numbers = [35, 36, 37, 38]

# 顺序执行
start = time.time()
results = [cpu_heavy(n) for n in numbers]
print(f"顺序执行耗时：{time.time() - start:.2f} 秒")

# 多进程
start = time.time()
with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(cpu_heavy, numbers))
print(f"多进程耗时：{time.time() - start:.2f} 秒")
```

在 4 核 CPU 上，多进程版本的总耗时大约等于四个任务中最慢的那个而不是四者之和。

### 10.4.5 选择策略：多线程还是多进程？

| 场景 | 方案 | 原因 |
|:-----|:-----|:-----|
| 网络请求、文件读写、数据库查询 | 多线程 | I/O 等待时 GIL 会释放，多线程能充分并发 |
| 大量数学计算、图像处理、数据加密 | 多进程 | CPU 密集，需要多核真正并行计算 |
| 既需要 I/O 又需要计算 | 多线程 + 多进程组合 | 各取所长 |
| 任务简单、数量少 | 顺序执行 | 并发有额外开销，简单的任务不值得折腾 |

一个实用的判断方法：如果程序大部分时间在 `time.sleep()` 或 `requests.get()` 上等待，用多线程；如果大部分时间在 `for` 循环计算上，用多进程；如果只有一两个小任务，先试试顺序执行，不够快再考虑并发。

### 10.4.6 异步编程——`asyncio` 的前瞻

Python 3.4+ 引入了 `async`/`await` 语法，提供了另一种并发方案——异步编程（Asynchronous Programming）。它用单线程 + 事件循环的方式实现高并发，特别适合需要同时处理成千上万个网络连接的场景（如 Web 服务器）。这部分属于进阶内容，本书暂不展开，但知道它的存在可以为以后的学习方向提供指引。

### 10.4.7 实战练习

1. 使用 `threading.Thread` 编写一个程序，创建 5 个线程同时执行函数 `task(name, seconds)`，该函数打印 `"任务 X 开始"`，`sleep` 指定秒数，再打印 `"任务 X 完成"`。使用 `join()` 等待所有线程完成后打印 `"全部完成"`。

2. 使用 `ThreadPoolExecutor` 批量下载"模拟文件"。创建一个包含 10 个 URL 的列表，使用线程池（`max_workers=3`）同时下载，每个"下载"用 `time.sleep` 模拟。观察完成任务的数量是否始终不超过 3。

3. 判断下列场景应该用多线程还是多进程：

   - A：从 1000 个 URL 爬取网页内容
   - B：对 1000 张图片进行批量水印处理（每张图片需要大量像素计算）
   - C：同时监控 50 个日志文件的变化
   - D：在 GUI 程序中，点击按钮后执行一个耗时 5 秒的后台任务，同时界面保持响应