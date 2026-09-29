## 8.3 第三方包的安装与管理——Python 的"应用商店"

如果说标准库是 Python 自带的"基础工具包"，那第三方包就是整个 Python 社区的"应用商店"——全球开发者贡献了超过 50 万个包，涵盖 Web 开发、数据科学、机器学习、自动化测试等几乎所有领域。这一节教你如何找到、安装和管理这些包。

### 8.3.1 PyPI——Python 包的"官方仓库"

PyPI（Python Package Index，读音"pie-pee-eye"）是 Python 官方维护的第三方包仓库，网址是 [https://pypi.org](https://pypi.org)。你可以在上面搜索需要的包，查看文档、安装命令和版本历史。几乎任何一个你能想到的需求，PyPI 上都有对应的解决方案——从发送邮件到处理 PDF，从调用 ChatGPT API 到控制无人机。

### 8.3.2 `pip`——包管理器的标准配置

`pip`（"Pip Installs Packages" 的递归缩写）是 Python 事实上的包管理器。它随 Python 3.4+ 一起安装，直接在命令行中使用：

```bash
pip install 包名           # 安装最新版本
pip install 包名==版本号   # 安装指定版本
pip install 包名>=版本号   # 安装不低于某个版本

pip uninstall 包名         # 卸载

pip list                   # 列出当前环境已安装的所有包
pip show 包名              # 查看某个包的详细信息

pip install --upgrade 包名  # 升级包到最新版本
```

常用示例：

```bash
pip install requests       # HTTP 请求库——发送网络请求
pip install numpy           # 科学计算库——高性能数组运算
pip install pandas          # 数据分析库——表格数据处理
pip install matplotlib      # 数据可视化库——绘制图表
pip install flask           # Web 框架——搭建网站和 API
```

---

\begin{tipbox}
**pip 太慢怎么办？换国内镜像源**

默认从 PyPI 官方服务器下载，在国内可能很慢。可以临时指定镜像源：

```bash
pip install 包名 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

或者一劳永逸地设置默认镜像（清华源为例）：

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

常用的国内镜像包括清华（tuna）、阿里云、中科大等。
\end{tipbox}

---

### 8.3.3 `requirements.txt`——环境的"购物清单"

当你开发了一个项目后，别人想运行你的代码，首先得安装你用的所有包。手动一个一个 `pip install` 不现实——这时用 `requirements.txt` 记录所有依赖：

```bash
pip freeze > requirements.txt    # 把当前环境所有包及版本写入文件
```

生成的 `requirements.txt` 内容示例：

```text
flask==3.1.0
numpy==2.1.3
pandas==2.2.3
requests==2.32.3
```

别人拿到项目后，只需一条命令安装全部依赖：

```bash
pip install -r requirements.txt
```

在实际团队协作中，`requirements.txt` 应该和项目代码一起提交到 Git 仓库中，这样每个协作者都能在几秒钟内搭建出相同的开发环境。

### 8.3.4 虚拟环境——项目的"独立房间"

不同的项目可能需要同一个包的不同版本。比如项目 A 需要 `Django 3.2`，项目 B 需要 `Django 5.0`。如果都装在系统 Python 里，必然会冲突。虚拟环境为每个项目创建独立的 Python 解释器和包空间：

**使用 `venv`（Python 内置）：**

```bash
python -m venv myproject_env       # 创建虚拟环境

# 激活（Windows）
myproject_env\Scripts\activate

# 激活（macOS/Linux）
source myproject_env/bin/activate

# 退出
deactivate
```

激活后，终端提示符前会出现 `(myproject_env)` 标识。此时用 `pip install` 安装的所有包都只存在于这个虚拟环境中，与系统 Python 和其他项目完全隔离。

**使用 `conda` / `miniforge`：** 如果你之前按照第 1 章的教程安装了 Anaconda 或 Miniforge，你已经拥有了 `conda` 环境管理工具。创建和管理环境的方式为：

```bash
conda create -n 环境名 python=3.12    # 创建环境并指定 Python 版本
conda activate 环境名                  # 激活
conda deactivate                       # 退出
conda env list                         # 列出所有环境
```

`conda` 不仅能管理 Python 包，还能管理非 Python 的底层依赖（如 C 库），在数据科学和机器学习领域尤其流行。

### 8.3.5 实战练习

1. 分别使用 `pip install` 和 `pip uninstall` 安装并卸载 `requests` 包。安装后用 `pip show requests` 查看包的信息。

2. 创建一个虚拟环境，激活它，在里面安装 `flask`，然后运行 `pip freeze` 查看环境中的包列表。最后退出虚拟环境。

3. 以下哪种做法是正确的？错误的做法有什么问题？

   - A：把所有项目的包都装在系统 Python 中
   - B：每个项目使用独立的虚拟环境
   - C：把 `requirements.txt` 加入 `.gitignore`，不提交到 Git
   - D：使用 `pip freeze > requirements.txt` 定期更新依赖清单