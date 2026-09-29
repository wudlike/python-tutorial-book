## 11.1 os/sys 模块——与系统和解释器对话

在第 8 章中我们简单介绍了 `os` 和 `sys` 的基础用法——目录操作、路径拼接、命令行参数。但这两个模块的能力远不止于此。`os` 是整个操作系统接口的入口，从进程管理到环境变量，从文件遍历到权限控制；`sys` 则掌管着 Python 解释器自身的运行时状态。本节将深入它们的高级特性，让你能写出真正"接地气"的工具脚本。

### 11.1.1 `os` 模块高级特性

#### 环境变量——程序的"全局配置"

环境变量是操作系统级的键值对，常用于存储敏感配置（数据库密码、API 密钥），避免硬编码在代码中：

```python
import os

# 读取环境变量——不存在时返回默认值 None
home = os.environ.get("HOME") or os.environ.get("USERPROFILE")
print(f"用户主目录：{home}")

# 安全读取——不存在时返回自定义默认值
db_host = os.environ.get("DB_HOST", "localhost")
db_port = os.environ.get("DB_PORT", "5432")
print(f"数据库连接：{db_host}:{db_port}")

# 遍历所有环境变量
for key, value in os.environ.items():
    print(f"{key} = {value}")
```

与 `sys.path` 类似，环境变量应该被视为"输入"而非"可修改的全局状态"——读取它们没问题，但在代码中途修改环境变量可能导致难以追踪的副作用。

#### 文件和目录遍历——`os.walk()`

`os.walk()` 是批量处理文件树的核心工具。它递归地遍历一个目录及其所有子目录，每次返回 `(当前目录路径, 子目录列表, 文件列表)` 三元组：

```python
import os

target_dir = "."    # 从当前目录开始遍历

for root, dirs, files in os.walk(target_dir):
    # root: 当前正在遍历的目录路径
    # dirs: root 下的子目录名列表
    # files: root 下的文件名列表

    level = root.count(os.sep) - target_dir.count(os.sep)
    indent = "  " * level
    print(f"{indent}📁 {os.path.basename(root)}/")

    for file in files:
        print(f"{indent}  📄 {file}")
```

`os.walk()` 的一个实用技巧是**原地修改 `dirs` 列表**来排除某些目录（比如 `.git`、`node_modules`），这样 walk 就不会进入这些目录：

```python
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", "node_modules")]
    # dirs[:] = ... 修改列表本身，而非重新赋值——walk 会识别到这个变化并跳过被排除的目录
    for file in files:
        if file.endswith(".py"):
            print(os.path.join(root, file))
```

#### 进程管理——`os.system()` 与 `subprocess`

`os.system()` 可以在 Python 中执行 Shell 命令，但返回的是退出码，无法获取命令的输出。`subprocess` 模块（下节会专门介绍）是更强大的替代方案：

```python
import os

# 执行 Shell 命令——返回退出码（0 表示成功）
exit_code = os.system("echo Hello from shell")
print(f"退出码：{exit_code}")

# os.system() 的局限性：拿不到命令的输出字符串
# 需要获取输出时用 subprocess（见下文）
```

#### 文件属性与权限

```python
import os
import stat
import time

filepath = "example.txt"

# 创建测试文件
with open(filepath, "w") as f:
    f.write("test")

# 获取文件状态
info = os.stat(filepath)
print(f"文件大小：{info.st_size} 字节")
print(f"最后修改：{time.ctime(info.st_mtime)}")
print(f"最后访问：{time.ctime(info.st_atime)}")

# 检查文件类型
mode = info.st_mode
print(f"是文件：{stat.S_ISREG(mode)}")    # True
print(f"是目录：{stat.S_ISDIR(mode)}")    # False

# 批量重命名文件——实用场景
# for filename in os.listdir("photos"):
#     if filename.endswith(".jpg"):
#         new_name = f"vacation_{filename}"
#         os.rename(
#             os.path.join("photos", filename),
#             os.path.join("photos", new_name)
#         )
```

### 11.1.2 `subprocess`——现代的命令行交互

`os.system()` 是上世纪的遗留方案。`subprocess` 模块提供了全面替代——它能捕获输出、控制输入、设置超时、管理环境变量：

```python
import subprocess

# 执行命令并捕获输出（文本模式）
result = subprocess.run(
    ["echo", "Hello from subprocess"],
    capture_output=True,
    text=True,
    encoding="utf-8"
)
print(f"输出：{result.stdout.strip()}")
print(f"退出码：{result.returncode}")

# 检查命令是否成功
result = subprocess.run(["python", "--version"], capture_output=True, text=True)
if result.returncode == 0:
    print(f"Python 版本：{result.stdout.strip()}")
else:
    print(f"错误：{result.stderr}")

# 超时控制——防止命令"卡死"
try:
    result = subprocess.run(["ping", "-n", "100", "localhost"],
                            capture_output=True, text=True, timeout=5)
except subprocess.TimeoutExpired:
    print("命令执行超时，已终止")

# 管道——一个命令的输出作为另一个命令的输入
# 等价于 Shell: echo "hello world" | findstr "hello"
p1 = subprocess.Popen(["echo", "hello world"], stdout=subprocess.PIPE, text=True)
p2 = subprocess.Popen(["findstr", "hello"], stdin=p1.stdout,
                      stdout=subprocess.PIPE, text=True)
p1.stdout.close()
output = p2.communicate()[0]
print(f"管道结果：{output.strip()}")
```

---

\begin{warningbox}
**安全：永远不要用 `shell=True` 拼接用户输入**

```python
# 危险！如果 user_input = "file; rm -rf /"，后果不堪设想
subprocess.run(f"cat {user_input}", shell=True)      # 千万别这样

# 安全——使用列表形式传递参数，不经过 Shell 解释
subprocess.run(["cat", user_input])                    # 即使 user_input 含特殊字符，也只是文件名
```

`shell=True` 会启动一个系统 Shell 来执行命令，用户输入中的分号、管道符等会被 Shell 解释为命令分隔符，导致命令注入攻击。除非你明确需要 Shell 的功能（如通配符展开），否则始终使用列表形式传递命令和参数。
\end{warningbox}

---

### 11.1.3 `sys` 模块高级特性

#### 标准输入/输出/错误流——`sys.stdin`/`sys.stdout`/`sys.stderr`

这三个文件对象可以让你与标准流交互——不仅是打印输出，还可以重定向：

```python
import sys

# 标准输出——等价于 print()，但给了你更多控制
sys.stdout.write("这是标准输出\n")

# 标准错误——用于错误信息和日志，不影响正常的输出管道
sys.stderr.write("这是错误信息\n")

# 重定向标准输出到文件
original_stdout = sys.stdout                    # 保存原始的 stdout
with open("output.txt", "w", encoding="utf-8") as f:
    sys.stdout = f                              # 重定向
    print("这句话会写入文件，不会显示在屏幕上")
    print("这句话也是")
sys.stdout = original_stdout                     # 恢复
print("恢复后，这句话又显示在屏幕上了")

# 管道式程序：从 stdin 逐行读取，处理后写到 stdout
# 用法：echo "hello" | python script.py
for line in sys.stdin:
    processed = line.strip().upper()
    print(processed)
```

#### 递归深度与模块搜索路径

```python
import sys

# 递归深度限制——默认 1000，对大多数场景够用
print(f"当前递归深度限制：{sys.getrecursionlimit()}")
# 如果需要处理深度递归（如深度优先搜索极深的树），可以调大
sys.setrecursionlimit(5000)

# 模块搜索路径——Python 从这里找 import 的模块
print("模块搜索路径：")
for p in sys.path:
    print(f"  {p}")

# 动态添加搜索路径——运行时告诉 Python 去额外的地方找模块
# sys.path.insert(0, "/path/to/my/modules")
```

---

\begin{tipbox}
**`sys.exit()` —— 优雅的程序退出**

```python
import sys

def main():
    if len(sys.argv) < 2:
        print("用法：python script.py <文件名>")
        sys.exit(1)          # 退出码非 0 表示异常退出
    # 正常逻辑...
    sys.exit(0)              # 退出码 0 表示正常退出

if __name__ == "__main__":
    main()
```

退出码是程序与外界（Shell 脚本、CI/CD 系统）沟通的唯一通道——`0` 表示成功，非 `0` 表示失败。养成在脚本的关键分支使用 `sys.exit()` 的习惯，能让你的工具无缝融入自动化工作流。
\end{tipbox}

---

### 11.1.4 实战练习

1. 使用 `os.walk()` 编写一个函数 `find_python_files(directory)`，递归查找指定目录下的所有 `.py` 文件，返回它们的绝对路径列表。（要求排除 `__pycache__` 和 `.git` 目录）

2. 编写一个 Python 脚本，它接收一个文件路径作为命令行参数（通过 `sys.argv`），然后将该文件的内容全部转为大写后输出到标准输出。如果用户没有提供文件路径，打印帮助信息并以退出码 1 退出。

3. 使用 `subprocess.run()` 执行 `git status` 命令（或 `dir` 命令，如果系统没有 git），捕获输出并判断命令是否成功执行。如果失败，在标准错误流中输出错误信息。