## 1.3 Anaconda 安装

在 1.2 节中，我们介绍了如何在不同操作系统上直接安装 Python。但对于初学者和数据分析从业者而言，本书更推荐使用 **Anaconda**——一个集成了 Python 解释器、包管理工具和数百个常用科学计算库的一站式解决方案。

### 1.3.1 什么是 Anaconda？

#### 定位：Python 发行版 + 环境管理器

Anaconda 本质上是一个"全家桶"式的 Python 发行版：

- **自带 Python 解释器**：无需提前安装 Python，Anaconda 内置完整的 Python 运行环境
- **预装 180+ 常用库**：NumPy、Pandas、Matplotlib、Scikit-learn 等开箱即用
- **内置 Conda**：强大的包管理和环境隔离工具，是 Anaconda 的灵魂所在

\begin{definitionbox}

**Anaconda 的核心价值——一句话概括**

装了 Anaconda，相当于同时拥有了"Python 运行环境 + 常用科学计算库 + 环境管理工具"。不再需要手动 `pip install` 逐个安装库，也不用担心不同项目之间的版本冲突。

\end{definitionbox}

#### 三大核心组件

| 组件 | 作用 | 适用场景 |
|:-----|:-----|:---------|
| **Conda** | 包与环境管理器，比 pip 更强大：不仅能装 Python 库，还能管理非 Python 依赖（如 C 编译器、R 语言包） | 命令行高效操作 |
| **Anaconda Navigator** | 图形化界面，可通过点击按钮创建环境、安装库、启动 Jupyter 等工具 | 新手友好，不熟悉命令行的读者 |
| **Jupyter Notebook** | 浏览器端交互式编程环境，支持代码与文档混排、分段运行 | 数据分析、学习笔记、实验探索 |

#### 为什么推荐新手使用？

1. **零门槛配置**：预装的 180+ 库覆盖了数据分析、可视化和机器学习的主流需求，安装后即可直接使用
2. **环境隔离**：假设项目 A 需要 Python 3.8 + TensorFlow 1.x，项目 B 需要 Python 3.10 + PyTorch 2.x，用 Conda 创建两个独立环境即可完美共存，互不干扰
3. **跨平台一致**：Windows、macOS、Ubuntu 上的 Conda 命令完全相同，无需记忆不同系统的特殊配置

\begin{tipbox}

**新手必学的 4 个 Conda 命令**

```bash
# 1. 检查安装是否成功
conda --version

# 2. 创建新环境（如 Python 3.10，命名 py310）
conda create -n py310 python=3.10

# 3. 激活环境
conda activate py310        # Windows
source activate py310       # macOS / Ubuntu

# 4. 退出环境
conda deactivate
```

掌握这四条命令，就足以开始日常使用了。

\end{tipbox}

### 1.3.2 Anaconda 安装步骤

#### Windows（以 Windows 10 / 11 为例）

**第一步：下载安装包**

- 官方渠道：[anaconda.com/download](https://www.anaconda.com/download)，选择 **64-Bit Graphical Installer**
- 国内镜像（推荐）：[清华大学 Anaconda 镜像站](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/)，下载最新的 `.exe` 文件

**第二步：运行安装程序**

1. 双击 `.exe`，安装模式选 **Just Me**（仅当前用户，无需管理员权限）
2. 安装路径建议设为 `D:\Anaconda3`（避免 C 盘空间不足，路径中不要包含中文或空格）
3. 高级选项中：**取消勾选** "Add Anaconda3 to my PATH"（可能与系统已有 Python 冲突）；**勾选** "Register Anaconda3 as my default Python"

**第三步：配置环境变量（如需要）**

若安装后命令行输入 `conda --version` 提示找不到命令，需手动添加：

```
右键"此电脑" → "属性" → "高级系统设置" → "环境变量"
在 Path 中添加以下三条路径（替换为实际安装路径）：
  D:\Anaconda3
  D:\Anaconda3\Scripts
  D:\Anaconda3\Library\bin
```

**第四步：验证安装**

```bash
conda --version    # 如 conda 24.5.0
python --version   # 如 Python 3.12.4
```

#### macOS（支持 Intel 和 Apple Silicon）

**第一步：下载安装包**

- Intel 芯片：选择 **64-Bit Graphical Installer (x86_64)**
- M1/M2/M3 芯片：选择 **64-Bit Graphical Installer (Arm64)**
- 国内镜像同样可用：[清华镜像站](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/)

**第二步：安装**

1. 双击 `.pkg` 文件，按向导点击"继续"→"同意"
2. 安装类型选"为我安装"（仅当前用户），路径默认 `/Users/你的用户名/anaconda3`
3. 输入开机密码授权，等待 3—5 分钟完成

**第三步：配置国内镜像源（推荐）**

```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --set show_channel_urls yes
```

配置后，`conda install` 下载速度将大幅提升。

**第四步：验证**

```bash
conda --version
python --version
```

#### Ubuntu（以 20.04 / 22.04 为例）

**第一步：下载安装脚本**

```bash
# 官方源
wget https://repo.anaconda.com/archive/Anaconda3-2024.06-Linux-x86_64.sh

# 或使用清华镜像（更快）
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-2024.06-Linux-x86_64.sh
```

**第二步：执行安装**

```bash
chmod +x Anaconda3-2024.06-Linux-x86_64.sh
bash Anaconda3-2024.06-Linux-x86_64.sh
```

按提示操作：按 `Enter` 阅读协议 → 输入 `yes` 同意 → 确认安装路径（默认即可）→ 输入 `yes` 让脚本自动初始化环境变量。

**第三步：验证**

```bash
source ~/.bashrc     # 刷新配置
conda --version
python --version
```

#### 常用操作速查

| 操作 | 命令 |
|:-----|:-----|
| 创建环境 | `conda create -n 环境名 python=3.10` |
| 查看所有环境 | `conda info --envs` |
| 激活环境 | `conda activate 环境名` |
| 安装包 | `conda install 包名` |
| 卸载包 | `conda remove 包名` |
| 删除环境 | `conda remove -n 环境名 --all` |
| 启动 Jupyter | `jupyter notebook` |

### 1.3.3 Anaconda 与 Miniforge

近年来，随着 Python 社区对开源合规和性能的日益重视，**Miniforge** 逐渐成为 Anaconda 的重要替代方案。

#### Anaconda 与 Miniforge 对比

| 维度 | Anaconda | Miniforge |
|:-----|:---------|:----------|
| **体积** | 约 3 GB（含预装 180+ 库） | 约 50 MB（轻量基础版） |
| **包管理工具** | conda | conda（更准确说是 mamba，conda 的加速版） |
| **默认频道** | `defaults`（Anaconda 官方源，企业大规模使用需商业许可） | `conda-forge`（社区维护，完全开源免费） |
| **适用场景** | 全套开箱即用，适合新手快速上手 | 按需安装，适合追求轻量和开源合规的用户 |
| **依赖解析速度** | 普通 | 快 5—10 倍（内置 Mamba 加速器） |

\begin{tipbox}

**一句话概括**

**Anaconda** 是"拎包入住的精装房"——家具齐全，适合不了解需要哪些工具的新手；**Miniforge** 是"毛坯房 + 建材市场"——需要什么装什么，轻量、自由、开源无限制。

\end{tipbox}

#### Miniforge 安装

Miniforge 的安装更为轻量，部分平台的安装命令甚至比 Anaconda 更简洁：

**Windows**

```powershell
# 方式一：通过 winget（Windows 11 内置）
winget install CondaForge.Miniforge3

# 方式二：通过 Scoop
scoop install miniforge3

# 方式三：手动下载 .exe
# 访问 https://github.com/conda-forge/miniforge/releases
# 下载 Miniforge3-Windows-x86_64.exe，双击安装
```

**macOS**

```bash
# 方式一：通过 Homebrew
brew install miniforge

# 方式二：下载 shell 脚本
curl -L -O https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh
# M 系列芯片用上面这行，Intel 芯片把 arm64 换成 x86_64
bash Miniforge3-MacOSX-arm64.sh
```

**Ubuntu**

```bash
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash Miniforge3-Linux-x86_64.sh
```

安装完成后，Miniforge 的使用命令与 Anaconda 完全一致——`conda create`、`conda activate`、`conda install` 照常使用。

\begin{definitionbox}

**本书的推荐**

如果你是零基础新手，推荐从 **Anaconda** 入门，它预装的完整生态能让你跳过繁琐的配置环节，直接进入学习。

如果你已有编程经验，或者对开源合规有要求，推荐 **Miniforge**——安装快、解析快、完全免费。

无论选择哪个，后续章节的环境管理命令完全通用。

\end{definitionbox}

---

至此，Python 的安装与环境管理已全部就绪。下一章我们将正式编写第一行 Python 代码——**从"Hello, World!"开始，踏上编程之旅**。